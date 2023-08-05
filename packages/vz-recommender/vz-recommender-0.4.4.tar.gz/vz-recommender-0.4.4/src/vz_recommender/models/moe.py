from typing import (TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple, Union,
                    cast)

import numpy as np
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.distributions.normal import Normal
from torch.nn import Module, ModuleList

gumbel_map: Dict[torch.device, Callable] = {}

def gumbel_rsample(shape: Tuple, device: torch.device) -> Tensor:
    gumbel = gumbel_map.get(device)
    if gumbel is None:
        one = torch.tensor(1.0, device=device)
        zero = torch.tensor(0.0, device=device)
        gumbel = torch.distributions.gumbel.Gumbel(zero, one).rsample  # type: ignore
        gumbel_map[device] = gumbel
    return gumbel(shape)


def one_hot(tensor: torch.Tensor, num_classes: int) -> Tensor:
    """Workaround for https://github.com/pytorch/pytorch/issues/55579"""
    assert num_classes > 0, "num_classes must be a positive integer"
    ret = torch.zeros(tensor.shape + (num_classes,), device=tensor.device, dtype=tensor.dtype)
    ret.scatter_(-1, tensor.unsqueeze(-1), 1)
    return ret


def top2gating(logits: torch.Tensor) -> Tuple[Tensor, Tensor, Tensor]:
    """Implements Top2Gating on logits."""
    # NOTE(msb) softmax requires FP32: https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/
    gates = F.softmax(logits, dim=1, dtype=torch.float)

    # gates has shape of SE
    num_tokens = gates.shape[0]
    num_experts = gates.shape[1]
    # capacity = 2S/E
    capacity = 2 * num_tokens
#     capacity = 2 * num_tokens // num_experts
#     assert num_tokens % num_experts == 0

    # Create a mask for 1st's expert per token
    indices1_s = torch.argmax(gates, dim=1)
    mask1 = one_hot(indices1_s, num_classes=num_experts)

    # Create a mask for 2nd's expert per token using Gumbel-max trick
    # https://timvieira.github.io/blog/post/2014/07/31/gumbel-max-trick/
    logits_w_noise = logits + gumbel_rsample(logits.shape, device=logits.device)
    # Replace top-expert with min value
    logits_except1 = logits_w_noise.masked_fill(mask1.bool(), float("-inf"))
    indices2_s = torch.argmax(logits_except1, dim=1)
    mask2 = one_hot(indices2_s, num_classes=num_experts)

    # Compute locations in capacity buffer
    locations1 = torch.cumsum(mask1, dim=0) - 1
    locations2 = torch.cumsum(mask2, dim=0) - 1
    # Update 2nd's location by accounting for locations of 1st
    locations2 += torch.sum(mask1, dim=0, keepdim=True)

    # Compute l_aux
    me = torch.mean(gates, dim=0)
    ce = torch.mean(mask1.float(), dim=0)
    l_aux = torch.mean(me * ce)

    # Remove locations outside capacity from mask
    mask1 *= torch.lt(locations1, capacity)
    mask2 *= torch.lt(locations2, capacity)

    # Store the capacity location for each token
    locations1_s = torch.sum(locations1 * mask1, dim=1)
    locations2_s = torch.sum(locations2 * mask2, dim=1)

    # Normalize gate probabilities
    gates1_s = (gates * mask1).sum(dim=1)  # einsum("se,se->s")
    gates2_s = (gates * mask2).sum(dim=1)  # einsum("se,se->s")
    denom_s = gates1_s + gates2_s
    # Avoid divide-by-zero
    denom_s = torch.clamp(denom_s, min=torch.finfo(denom_s.dtype).eps)
    gates1_s /= denom_s
    gates2_s /= denom_s

    # Calculate combine_weights and dispatch_mask
    gates1 = gates1_s.unsqueeze(-1) * mask1  # einsum("s,se->se")
    gates2 = gates2_s.unsqueeze(-1) * mask2  # einsum("s,se->se")
    locations1_sc = one_hot(locations1_s, num_classes=capacity)
    locations2_sc = one_hot(locations2_s, num_classes=capacity)
    combine1_sec = gates1.unsqueeze(2) * locations1_sc.unsqueeze(1)  # einsum("se,sc->sec")
    combine2_sec = gates2.unsqueeze(2) * locations2_sc.unsqueeze(1)  # einsum("se,sc->sec")
    combine_weights = combine1_sec + combine2_sec
    dispatch_mask = combine_weights.bool()

    return l_aux.to(logits.dtype), combine_weights.to(logits.dtype), dispatch_mask


class Top2Gate(torch.nn.Module):
    """Gate module which implements Top2Gating as described in Gshard_.
    ::
        gate = Top2Gate(model_dim, num_experts)
        l_aux, combine_weights, dispatch_mask = gate(input)
    .. Gshard_: https://arxiv.org/pdf/2006.16668.pdf
    Args:
        model_dim (int):
            size of model embedding dimension
        num_experts (ints):
            number of experts in model
    """

    wg: torch.nn.Linear
    
    def __init__(
        self,
        model_dim: int,
        num_experts: int,
    ) -> None:
        super().__init__()
        self.wg = torch.nn.Linear(model_dim, num_experts, bias=False)

    def forward(self, input: torch.Tensor) -> Tuple[Tensor, Tensor, Tensor]:  # type: ignore
        logits = self.wg(input)
        return top2gating(logits)

# Based on https://github.com/pytorch/pytorch/pull/40762
# class _AllToAll(torch.autograd.Function):
#     @staticmethod
#     def forward(ctx: Any, group: dist.ProcessGroup, input: Tensor) -> Tensor:  # type: ignore
#         ctx.group = group
#         input = input.contiguous()
#         output = torch.empty_like(input)
#         dist.all_to_all_single(output, input, group=group)
#         return output

#     @staticmethod
#     def backward(ctx: Any, *grad_output: Tensor) -> Tuple[None, Tensor]:
#         return (None, _AllToAll.apply(ctx.group, *grad_output))


class MOELayer(torch.nn.Module):
    """MOELayer module which implements MixtureOfExperts as described in Gshard_.
    ::
        gate = Top2Gate(model_dim, num_experts)
        moe = MOELayer(gate, expert)
        output = moe(input)
        l_aux = moe.l_aux
    .. _Gshard: https://arxiv.org/pdf/2006.16668.pdf
    Args:
        gate: gate network
        expert: expert network
        group: group to use for all-to-all communication
    """

    def __init__(self, gate: Module, experts: Union[Module, ModuleList], embed_dim, group: Optional[Any] = None) -> None:
        super().__init__()
        self.gate = gate
        self.embed_dim = embed_dim
        if type(experts) == ModuleList:
            self.experts = cast(ModuleList, experts)
        else:
            self.experts = ModuleList([experts])
#         self.group = group if group is not None else dist.group.WORLD
        for expert in self.experts:
            for p in experts.parameters():
                p.expert = True  # type: ignore
#         self.world_size = dist.get_world_size(self.group)
        self.num_local_experts = len(self.experts)

    def forward(self, *input: Tensor, **kwargs: Any) -> Tensor:
#         assert len(input) == 1, "only single input Tensor supported"
#         assert len(input[0].shape) == 3, "input Tensor must have dimensions: (s)equence, (t)oken, (m)odel"
#         assert input[0].shape[0] % len(self.experts) == 0, "num tokens must be order of number of local experts"

        # Implement Algorithm 2 from GShard paper.
        d_model = input[0].shape[2]

        # Reshape into S tokens by dropping sequence dimension.
        reshaped_input = input[0].reshape(-1, d_model)
        l_aux, combine_weights, dispatch_mask = self.gate(reshaped_input)
        dispatched_input = torch.einsum("sec,sm->ecm", dispatch_mask.float(), reshaped_input)
#         dispatched_input = _AllToAll.apply(self.group, dispatched_input)
        # Re-shape after all-to-all: ecm -> gecm
#         dispatched_input = dispatched_input.reshape(self.world_size, self.num_local_experts, -1, d_model)
        chunks = dispatched_input.chunk(self.num_local_experts, dim=1)
        expert_outputs = []
        for chunk, expert in zip(chunks, self.experts):
            expert_outputs += [expert(chunk)]
        expert_output = torch.cat(expert_outputs, dim=1)
#         expert_output = _AllToAll.apply(self.group, expert_output)
        # Re-shape back: gecm -> ecm
#         expert_output = expert_output.reshape(self.world_size * self.num_local_experts, -1, d_model)
        combined_output = torch.einsum("sec,ecm->sm", combine_weights, expert_output)
    
        return combined_output.reshape(input[0].shape), l_aux
#         return combined_output.reshape(torch.Size([input[0].shape[0], self.embed_dim])), l_aux


class SparseDispatcher(object):
    """Helper for implementing a mixture of experts.
    The purpose of this class is to create input minibatches for the
    experts and to combine the results of the experts to form a unified
    output tensor.
    There are two functions:
    dispatch - take an input Tensor and create input Tensors for each expert.
    combine - take output Tensors from each expert and form a combined output
      Tensor.  Outputs from different experts for the same batch element are
      summed together, weighted by the provided "gates".
    The class is initialized with a "gates" Tensor, which specifies which
    batch elements go to which experts, and the weights to use when combining
    the outputs.  Batch element b is sent to expert e iff gates[b, e] != 0.
    The inputs and outputs are all two-dimensional [batch, depth].
    Caller is responsible for collapsing additional dimensions prior to
    calling this class and reshaping the output to the original shape.
    See common_layers.reshape_like().
    Example use:
    gates: a float32 `Tensor` with shape `[batch_size, num_experts]`
    inputs: a float32 `Tensor` with shape `[batch_size, input_size]`
    experts: a list of length `num_experts` containing sub-networks.
    dispatcher = SparseDispatcher(num_experts, gates)
    expert_inputs = dispatcher.dispatch(inputs)
    expert_outputs = [experts[i](expert_inputs[i]) for i in range(num_experts)]
    outputs = dispatcher.combine(expert_outputs)
    The preceding code sets the output for a particular example b to:
    output[b] = Sum_i(gates[b, i] * experts[i](inputs[b]))
    This class takes advantage of sparsity in the gate matrix by including in the
    `Tensor`s for expert i only the batch elements for which `gates[b, i] > 0`.
    """

    def __init__(self, num_experts, gates):
        """Create a SparseDispatcher."""

        self._gates = gates
        self._num_experts = num_experts
        # sort experts
        sorted_experts, index_sorted_experts = torch.nonzero(gates).sort(0)
        # drop indices
        _, self._expert_index = sorted_experts.split(1, dim=1)
        # get according batch index for each expert
        self._batch_index = torch.nonzero(gates)[index_sorted_experts[:, 1], 0]
        # calculate num samples that each expert gets
        self._part_sizes = (gates > 0).sum(0).tolist()
        # expand gates to match with self._batch_index
        gates_exp = gates[self._batch_index.flatten()]
        self._nonzero_gates = torch.gather(gates_exp, 1, self._expert_index)

    def dispatch(self, inp):
        """Create one input Tensor for each expert.
        The `Tensor` for a expert `i` contains the slices of `inp` corresponding
        to the batch elements `b` where `gates[b, i] > 0`.
        Args:
          inp: a `Tensor` of shape "[batch_size, <extra_input_dims>]`
        Returns:
          a list of `num_experts` `Tensor`s with shapes
            `[expert_batch_size_i, <extra_input_dims>]`.
        """

        # assigns samples to experts whose gate is nonzero

        # expand according to batch index so we can just split by _part_sizes
        inp_exp = inp[self._batch_index].squeeze(1)
        return torch.split(inp_exp, self._part_sizes, dim=0)

    def combine(self, expert_out, multiply_by_gates=True):
        """Sum together the expert output, weighted by the gates.
        The slice corresponding to a particular batch element `b` is computed
        as the sum over all experts `i` of the expert output, weighted by the
        corresponding gate values.  If `multiply_by_gates` is set to False, the
        gate values are ignored.
        Args:
          expert_out: a list of `num_experts` `Tensor`s, each with shape
            `[expert_batch_size_i, <extra_output_dims>]`.
          multiply_by_gates: a boolean
        Returns:
          a `Tensor` with shape `[batch_size, <extra_output_dims>]`.
        """
        # apply exp to expert outputs, so we are not longer in log space
        stitched = torch.cat(expert_out, 0).exp()

        if multiply_by_gates:
            stitched = stitched.mul(self._nonzero_gates)
        zeros = torch.zeros(self._gates.size(0), expert_out[-1].size(1), requires_grad=True, device=stitched.device)
        # combine samples that have been processed by the same k experts
        combined = zeros.index_add(0, self._batch_index, stitched.float())
        # add eps to all zero values in order to avoid nans when going back to log space
        combined[combined == 0] = np.finfo(float).eps
        # back to log space
        return combined.log()

    def expert_to_gates(self):
        """Gate values corresponding to the examples in the per-expert `Tensor`s.
        Returns:
          a list of `num_experts` one-dimensional `Tensor`s with type `tf.float32`
              and shapes `[expert_batch_size_i]`
        """
        # split nonzero gates for each expert
        return torch.split(self._nonzero_gates, self._part_sizes, dim=0)

class MLP(nn.Module):
    def __init__(self, input_size, output_size, hidden_size):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.soft = nn.Softmax(1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.soft(out)
        return out


class MoE(nn.Module):

    """Call a Sparsely gated mixture of experts layer with 1-layer Feed-Forward networks as experts.
    Args:
    input_size: integer - size of the input
    output_size: integer - size of the input
    num_experts: an integer - number of experts
    hidden_size: an integer - hidden size of the experts
    noisy_gating: a boolean
    k: an integer - how many experts to use for each batch element
    """

    def __init__(self, input_size, output_size, num_experts, hidden_size, noisy_gating=True, k=4):
        super(MoE, self).__init__()
        self.noisy_gating = noisy_gating
        self.num_experts = num_experts
        self.output_size = output_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.k = k
        # instantiate experts
        self.experts = nn.ModuleList([MLP(self.input_size, self.output_size, self.hidden_size) for i in range(self.num_experts)])
        self.w_gate = nn.Parameter(torch.zeros(input_size, num_experts), requires_grad=True)
        self.w_noise = nn.Parameter(torch.zeros(input_size, num_experts), requires_grad=True)

        self.softplus = nn.Softplus()
        self.softmax = nn.Softmax(1)
        self.register_buffer("mean", torch.tensor([0.0]))
        self.register_buffer("std", torch.tensor([1.0]))
        assert(self.k <= self.num_experts)

    def cv_squared(self, x):
        """The squared coefficient of variation of a sample.
        Useful as a loss to encourage a positive distribution to be more uniform.
        Epsilons added for numerical stability.
        Returns 0 for an empty Tensor.
        Args:
        x: a `Tensor`.
        Returns:
        a `Scalar`.
        """
        eps = 1e-10
        # if only num_experts = 1

        if x.shape[0] == 1:
            return torch.tensor([0], device=x.device, dtype=x.dtype)
        return x.float().var() / (x.float().mean()**2 + eps)

    def _gates_to_load(self, gates):
        """Compute the true load per expert, given the gates.
        The load is the number of examples for which the corresponding gate is >0.
        Args:
        gates: a `Tensor` of shape [batch_size, n]
        Returns:
        a float32 `Tensor` of shape [n]
        """
        return (gates > 0).sum(0)

    def _prob_in_top_k(self, clean_values, noisy_values, noise_stddev, noisy_top_values):
        """Helper function to NoisyTopKGating.
        Computes the probability that value is in top k, given different random noise.
        This gives us a way of backpropagating from a loss that balances the number
        of times each expert is in the top k experts per example.
        In the case of no noise, pass in None for noise_stddev, and the result will
        not be differentiable.
        Args:
        clean_values: a `Tensor` of shape [batch, n].
        noisy_values: a `Tensor` of shape [batch, n].  Equal to clean values plus
          normally distributed noise with standard deviation noise_stddev.
        noise_stddev: a `Tensor` of shape [batch, n], or None
        noisy_top_values: a `Tensor` of shape [batch, m].
           "values" Output of tf.top_k(noisy_top_values, m).  m >= k+1
        Returns:
        a `Tensor` of shape [batch, n].
        """
        batch = clean_values.size(0)
        m = noisy_top_values.size(1)
        top_values_flat = noisy_top_values.flatten()

        threshold_positions_if_in = torch.arange(batch, device=clean_values.device) * m + self.k
        threshold_if_in = torch.unsqueeze(torch.gather(top_values_flat, 0, threshold_positions_if_in), 1)
        is_in = torch.gt(noisy_values, threshold_if_in)
        threshold_positions_if_out = threshold_positions_if_in - 1
        threshold_if_out = torch.unsqueeze(torch.gather(top_values_flat, 0, threshold_positions_if_out), 1)
        # is each value currently in the top k.
        normal = Normal(self.mean, self.std)
        prob_if_in = normal.cdf((clean_values - threshold_if_in)/noise_stddev)
        prob_if_out = normal.cdf((clean_values - threshold_if_out)/noise_stddev)
        prob = torch.where(is_in, prob_if_in, prob_if_out)
        return prob

    def noisy_top_k_gating(self, x, train, noise_epsilon=1e-2):
        """Noisy top-k gating.
          See paper: https://arxiv.org/abs/1701.06538.
          Args:
            x: input Tensor with shape [batch_size, input_size]
            train: a boolean - we only add noise at training time.
            noise_epsilon: a float
          Returns:
            gates: a Tensor with shape [batch_size, num_experts]
            load: a Tensor with shape [num_experts]
        """
        clean_logits = x @ self.w_gate
        if self.noisy_gating and train:
            raw_noise_stddev = x @ self.w_noise
            noise_stddev = ((self.softplus(raw_noise_stddev) + noise_epsilon))
            noisy_logits = clean_logits + (torch.randn_like(clean_logits) * noise_stddev)
            logits = noisy_logits
        else:
            logits = clean_logits

        # calculate topk + 1 that will be needed for the noisy gates
        top_logits, top_indices = logits.topk(min(self.k + 1, self.num_experts), dim=1)
        top_k_logits = top_logits[:, :self.k]
        top_k_indices = top_indices[:, :self.k]
        top_k_gates = self.softmax(top_k_logits)

        zeros = torch.zeros_like(logits, requires_grad=True)
        gates = zeros.scatter(1, top_k_indices, top_k_gates)

        if self.noisy_gating and self.k < self.num_experts and train:
            load = (self._prob_in_top_k(clean_logits, noisy_logits, noise_stddev, top_logits)).sum(0)
        else:
            load = self._gates_to_load(gates)
        return gates, load

    def forward(self, x, loss_coef=1e-4):
        """Args:
        x: tensor shape [batch_size, input_size]
        train: a boolean scalar.
        loss_coef: a scalar - multiplier on load-balancing losses
        Returns:
        y: a tensor with shape [batch_size, output_size].
        extra_training_loss: a scalar.  This should be added into the overall
        training loss of the model.  The backpropagation of this loss
        encourages all experts to be approximately equally used across a batch.
        """
#         d_batch = x.shape[0]
#         d_len = x.shape[1]
#         x = x.reshape(-1, x.shape[2])
        gates, load = self.noisy_top_k_gating(x, self.training)

        # calculate importance loss
        importance = gates.sum(0)
        #
        loss = self.cv_squared(importance) + self.cv_squared(load)
        loss *= loss_coef

        dispatcher = SparseDispatcher(self.num_experts, gates)
        expert_inputs = dispatcher.dispatch(x)
        gates = dispatcher.expert_to_gates()
        expert_outputs = [self.experts[i](expert_inputs[i]) for i in range(self.num_experts)]
        y = dispatcher.combine(expert_outputs)
        return y, loss
#         return y.reshape(torch.Size([d_batch, d_len, self.output_size])), loss


class TopKRouter(nn.Module):
    """
    Router using tokens choose top-1 experts assignment.
    This router uses the same mechanism as in Switch Transformer (https://arxiv.org/abs/2101.03961) and V-MoE
    (https://arxiv.org/abs/2106.05974): tokens choose their top experts. Items are sorted by router_probs and then
    routed to their choice of expert until the expert's expert_capacity is reached.
    **There is no guarantee that each token is processed by an expert**,
    or that each expert receives at least one token.
    """

    def __init__(self, num_experts, expert_capacity, hidden_size, router_bias,
                 router_jitter_noise, router_ignore_padding_tokens, router_dtype,
                 num_K=1):
        super().__init__()
        self.num_experts = num_experts
        self.expert_capacity = expert_capacity
        self.classifier = nn.Linear(hidden_size, num_experts, bias=router_bias)
        self.jitter_noise = router_jitter_noise
        self.ignore_padding_tokens = router_ignore_padding_tokens
        self.dtype = getattr(torch, router_dtype)
        self.num_K = num_K  # if num_K = 1, -> Top1Router

    def _compute_router_probabilities(self, hidden_states: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Computes router probabilities from input hidden states.
        Args:
            hidden_states (`torch.Tensor`):
                (batch_size, sequence_length, hidden_dim) from which router probabilities are computed.
        Returns:
            router_probabilities (`torch.Tensor`):
                Tensor of shape (batch_size, sequence_length, num_experts) corresponding to the probabilities for each
                token and expert. Used for routing tokens to experts.
            router_logits (`torch.Tensor`):
                Logits tensor of shape (batch_size, sequence_length, num_experts) corresponding to raw router logits.
                This is used later for computing router z-loss.
        """
        # float32 is used to ensure stability. See the discussion of "selective precision" in
        # https://arxiv.org/abs/2101.03961.
        # We also store the previous dtype to cast back the output to the previous dtype

        self.input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(self.dtype)

        if self.jitter_noise > 0:
            # Get the lower and upper bound of the uniform distribution
            # Adapted from: https://stackoverflow.com/questions/44328530/how-to-get-a-uniform-distribution-in-a-range-r1-r2-in-pytorch
            distrib_lower_bound = 1.0 - self.jitter_noise
            distrib_upper_bound = 1.0 + self.jitter_noise

            uniform_distrib = torch.rand(hidden_states.shape, device=hidden_states.device, dtype=self.dtype)
            uniform_distrib = uniform_distrib * (distrib_lower_bound - distrib_upper_bound)

            uniform_distrib = uniform_distrib + distrib_upper_bound
            # Multiply the token inputs by the uniform distribution - adding some noise
            hidden_states *= uniform_distrib

        # Shape: [num_groups, tokens_per_group, num_experts]
        self._cast_classifier()
        router_logits = self.classifier(hidden_states)

        # Apply Softmax and cast back to the original `dtype`
        router_probabilities = nn.functional.softmax(router_logits, dim=-1, dtype=self.dtype).to(self.input_dtype)
        return router_probabilities, router_logits

    def _cast_classifier(self):
        r"""
        `bitsandbytes` `Linear8bitLt` layers does not support manual casting Therefore we need to check if they are an
        instance of the `Linear8bitLt` class by checking special attributes.
        """
        if not (hasattr(self.classifier, "SCB") or hasattr(self.classifier, "CB")):
            self.classifier = self.classifier.to(self.dtype)

    def forward(self, hidden_states: torch.Tensor) -> Tuple:
        r"""
        Generic forward function for every Router class. Each Router expects to have the same input hidden states
        (`hidden_states`) corresponding to the hidden states for each token, the `expert_capacity` corresponding to the
        number of tokens the Router will send to each expert, some Routers can send up to few tokens to each expert.
        Each Router works as the following: it expects the hidden states for each token, gets the `router_probs` and
        `router_logits` from the `router_weights`. This will assign for each token, the raw probability to be assigned
        to an expert. Then each Router class will have to define its own `_compute_routing_instructions`.
        Args:
            hidden_states (`torch.Tensor`) :
                [num_groups, tokens_per_group, hidden_dim] inputs to send to experts.
            k (`int`):
                choose top-[k] experts.
        Returns:
            Tuple[`torch.Tensor`, `torch.Tensor`, `torch.Tensor`] Tuple containing the expert index, the router probs
            and the router logits. The router probabilities and logits are required to compute the loss.
        """

        assert self.num_K <= self.num_experts, "Num of experts should greater than or equal to k!"
        router_probs, router_logits = self._compute_router_probabilities(hidden_states)

        router_probs_top_k, expert_index_list = torch.topk(router_probs, k=self.num_K, dim=-1)
        expert_index = sum([torch.nn.functional.one_hot(expert_index_list[:, :, i], num_classes=self.num_experts)
                            for i in range(self.num_K)])

        # Mask tokens outside expert capacity. Sum over each sequence
        token_priority = torch.cumsum(expert_index, dim=-2)

        # mask if the token routed to to the expert will overflow
        expert_capacity_mask = token_priority <= self.expert_capacity * self.num_K
        expert_index = expert_index * expert_capacity_mask
        router_probs_top_k = router_probs_top_k.unsqueeze(-1)
        return expert_index, router_probs_top_k, router_logits


class Top1Router(nn.Module):
    """
    Router using tokens choose top-1 experts assignment.
    This router uses the same mechanism as in Switch Transformer (https://arxiv.org/abs/2101.03961) and V-MoE
    (https://arxiv.org/abs/2106.05974): tokens choose their top experts. Items are sorted by router_probs and then
    routed to their choice of expert until the expert's expert_capacity is reached. **There is no guarantee that each
    token is processed by an expert**, or that each expert receives at least one token.
    """

    def __init__(self, num_experts, expert_capacity, hidden_size, router_bias, router_jitter_noise, router_ignore_padding_tokens, router_dtype):
        super().__init__()
        self.num_experts = num_experts
        self.expert_capacity = expert_capacity
        self.classifier = nn.Linear(hidden_size, num_experts, bias=router_bias)
        self.jitter_noise = router_jitter_noise
        self.ignore_padding_tokens = router_ignore_padding_tokens
        self.dtype = getattr(torch, router_dtype)

    def _compute_router_probabilities(self, hidden_states: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        r"""
        Computes router probabilities from input hidden states.
        Args:
            hidden_states (`torch.Tensor`):
                (batch_size, sequence_length, hidden_dim) from which router probabilities are computed.
        Returns:
            router_probabilities (`torch.Tensor`):
                Tensor of shape (batch_size, sequence_length, num_experts) corresponding to the probabilities for each
                token and expert. Used for routing tokens to experts.
            router_logits (`torch.Tensor`):
                Logits tensor of shape (batch_size, sequence_length, num_experts) corresponding to raw router logits.
                This is used later for computing router z-loss.
        """
        # float32 is used to ensure stability. See the discussion of "selective precision" in
        # https://arxiv.org/abs/2101.03961.
        # We also store the previous dtype to cast back the output to the previous dtype
        self.input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(self.dtype)

        if self.jitter_noise > 0:
            # Get the lower and upper bound of the uniform distribution
            # Adapted from: https://stackoverflow.com/questions/44328530/how-to-get-a-uniform-distribution-in-a-range-r1-r2-in-pytorch
            distrib_lower_bound = 1.0 - self.jitter_noise
            distrib_upper_bound = 1.0 + self.jitter_noise

            uniform_distrib = torch.rand(hidden_states.shape, device=hidden_states.device, dtype=self.dtype)
            uniform_distrib = uniform_distrib * (distrib_lower_bound - distrib_upper_bound)

            uniform_distrib = uniform_distrib + distrib_upper_bound
            # Multiply the token inputs by the uniform distribution - adding some noise
            hidden_states *= uniform_distrib

        # Shape: [num_groups, tokens_per_group, num_experts]
        self._cast_classifier()
        router_logits = self.classifier(hidden_states)

        # Apply Softmax and cast back to the original `dtype`
        router_probabilities = nn.functional.softmax(router_logits, dim=-1, dtype=self.dtype).to(self.input_dtype)
        return router_probabilities, router_logits

    def _cast_classifier(self):
        r"""
        `bitsandbytes` `Linear8bitLt` layers does not support manual casting Therefore we need to check if they are an
        instance of the `Linear8bitLt` class by checking special attributes.
        """
        if not (hasattr(self.classifier, "SCB") or hasattr(self.classifier, "CB")):
            self.classifier = self.classifier.to(self.dtype)

    def forward(self, hidden_states: torch.Tensor) -> Tuple:
        r"""
        Generic forward function for every Router class. Each Router expects to have the same input hidden states
        (`hidden_states`) corresponding to the hidden states for each token, the `expert_capacity` corresponding to the
        number of tokens the Router will send to each expert, some Routers can send up to few tokens to each expert.
        Each Router works as the following: it expects the hidden states for each token, gets the `router_probs` and
        `router_logits` from the `router_weights`. This will assign for each token, the raw probability to be assigned
        to an expert. Then each Router class will have to define its own `_compute_routing_instructions`.
        Args:
            hidden_states (`torch.Tensor`) :
                [num_groups, tokens_per_group, hidden_dim] inputs to send to experts.
        Returns:
            Tuple[`torch.Tensor`, `torch.Tensor`, `torch.Tensor`] Tuple containing the expert index, the router probs
            and the router logits. The router probabilities and logits are required to compute the loss.
        """
        router_probs, router_logits = self._compute_router_probabilities(hidden_states)

        expert_index = torch.argmax(router_probs, dim=-1)
        expert_index = torch.nn.functional.one_hot(expert_index, num_classes=self.num_experts)

        # Mask tokens outside expert capacity. Sum over each sequence
        token_priority = torch.cumsum(expert_index, dim=-2)
        # mask if the token routed to to the expert will overflow
        expert_capacity_mask = token_priority <= self.expert_capacity
        expert_index = expert_index * expert_capacity_mask

        router_probs = torch.max(router_probs, dim=-1).values.unsqueeze(-1)
        return expert_index, router_probs, router_logits


class MoELayerNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        """
        Construct a layernorm module in the SwitchTransformers style. No bias and no subtraction of mean.
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):

        # SwitchTransformers uses a layer_norm which only scales and doesn't shift, which is also known as Root Mean
        # Square Layer Normalization https://arxiv.org/abs/1910.07467 thus varience is calculated
        # w/o mean and there is no bias. Additionally we want to make sure that the accumulation for
        # half-precision inputs is done in fp32

        variance = hidden_states.to(torch.float32).pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)

        # convert into half-precision if necessary
        if self.weight.dtype in [torch.float16, torch.bfloat16]:
            hidden_states = hidden_states.to(self.weight.dtype)

        return self.weight * hidden_states

    
class ExpertLayer(nn.Module):
    def __init__(self, d_model, d_ff, dropout_rate=0):
        super().__init__()
        self.wi = nn.Linear(d_model, d_ff, bias=False)
        self.wo = nn.Linear(d_ff, d_model, bias=False)
        self.dropout = nn.Dropout(dropout_rate)
        self.act = nn.LeakyReLU(0.2)
#         self.act = ACT2FN[config.dense_act_fn]
        
    def forward(self, hidden_states):
        hidden_states = self.wi(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.wo(hidden_states)
        return hidden_states


class SparseMoELayerTopK(nn.Module):
    r"""
    Implementation of the Switch Transformers Sparse MLP module.
    """

    def __init__(self, dim, num_experts, expert_capacity, hidden_size, expert_class, router_bias=True,
                 router_jitter_noise=0.1,
                 router_ignore_padding_tokens=False, router_dtype="float32", num_K=1):
        super().__init__()
        # Step 1: Get the correct router according to its class
        self.num_K = num_K
        self.router = TopKRouter(num_experts, expert_capacity, hidden_size, router_bias, router_jitter_noise,
                                 router_ignore_padding_tokens, router_dtype, num_K)
        # Step 2: Get the top K experts
        self.experts = nn.ModuleDict()
        for idx in range(num_experts):
            self.experts[f"expert_{idx}"] = expert_class(dim, hidden_size)

    def forward(self, hidden_states, task_state=None):
        r"""
        Hold on, this will be slightly tricky to understand In the correct order, a MoE layer does the following:
        1- Gets the `router_mask` from the router. The shape of the mask is `(batch_size, sequence_length, num_expert)`. 
        The probabilities are needed in the computation of the hidden states : they are broadcasted to the hidden states 
        values (can be interpreted as a scaling factor). 2- Dispatch the tokens to its associated experts. 
        We do a classic for loop over the experts and assign for each expert the corresponding hidden states.
        """
        # Step 1: Get the k router_masks from the router as wel as the probabilities
        router_state = hidden_states if task_state is None else task_state
        router_mask, router_probs_top_k, router_logits = self.router(router_state)
        _, expert_index = torch.topk(router_mask, dim=-1, k=self.num_K)

        # The routers introduced might not always map all the tokens, to a router, which means that some hidden states
        # can be unchanged from one layer to another. That is why the hidden states are cloned before updating only the seleced ones.

        next_states = [hidden_states.clone() for _ in range(self.num_K)]

        for k in range(self.num_K):
            for idx, expert in enumerate(self.experts.values()):
                token_indices = router_mask[:, :, idx].bool()
                next_states[k][token_indices] = expert(hidden_states[token_indices])
            next_states[k] *= router_probs_top_k[:, :, k]

        hidden_states = torch.stack(next_states, dim=0).sum(dim=0)

        return hidden_states, (router_logits, expert_index)


class SparseMoELayer(nn.Module):
    r"""
    Implementation of the Switch Transformers Sparse MLP module.
    """

    def __init__(self, dim, num_experts, expert_capacity, hidden_size, expert_class, router_bias=True, router_jitter_noise=0.1, router_ignore_padding_tokens=False, router_dtype="float32"):
        super().__init__()
        # Step 1: Get the correct router according to its class
        self.router = Top1Router(num_experts, expert_capacity, hidden_size, router_bias, router_jitter_noise, router_ignore_padding_tokens, router_dtype)
        # Step 2: Get the experts
        self.experts = nn.ModuleDict()
        for idx in range(num_experts):
            self.experts[f"expert_{idx}"] = expert_class(dim, hidden_size)

    def forward(self, hidden_states, task_state=None):
        r"""
        Hold on, this will be slightly tricky to understand In the correct order, a MoE layer does the following:
        1- Gets the `router_mask` from the router. The shape of the mask is `(batch_size, sequence_length, num_expert)`
        and corresponds to the argmax of the `router_probs`. The probabilities are needed in the computation of the
        hidden states : they are broadcasted to the hidden states values (can be interpreted as a scaling factor).
        2- Dispatch the tokens to its associated experts. We do a classic for loop over the experts and assign for each
        expert the corresponding hidden states.
        """
        # Step 1: Get the router_mask from the router as wel as the probabilities
        router_state = hidden_states if task_state is None else task_state
        router_mask, router_probs, router_logits = self.router(router_state)
        expert_index = torch.argmax(router_mask, dim=-1)

        # The routers introduced might not always map all the tokens, to a router, which means that some hidden states
        # can be unchanged from one layer to another. That is why the hidden states are cloned before updating only the seleced ones.

        next_states = hidden_states.clone()
        for idx, expert in enumerate(self.experts.values()):
#             token_indices = router_mask[:, idx].bool()
            token_indices = router_mask[:, :, idx].bool()
            next_states[token_indices] = expert(hidden_states[token_indices])

        hidden_states = router_probs * next_states
        return hidden_states, (router_logits, expert_index)


class MoEFFLayerTopK(nn.Module):
    r"""
    Switch Transformers Feed Forward layer module. This is a wrapper around the Mixture of Experts module.
    Parameters:
        config : ([`SwitchTransformersConfig`]): Model configuration class with all the parameters of the model.
            Initializing with a config file does not load the weights associated with the model, only the
            configuration. Check out the [`~PreTrainedModel.from_pretrained`] method to load the model weights.
        is_sparse (`bool`):
            Whether the MLP layer is a `Sparse` layer (contains a Mixture of Experts) or not
    """

    def __init__(self, dim, num_experts, expert_capacity, hidden_size, expert_class, dropout_rate=0, 
                 router_bias=True, router_jitter_noise=0.1, router_ignore_padding_tokens=False, 
                 router_z_loss_coef=0.001, router_aux_loss_coef=0.001, router_dtype="float32", num_K=1):
        super().__init__()
        self.mlp = SparseMoELayerTopK(dim, num_experts, expert_capacity, hidden_size, expert_class,
                                  router_bias=True, router_jitter_noise=0.1, 
                                  router_ignore_padding_tokens=False, router_dtype="float32", num_K=num_K)
        self.layer_norm = MoELayerNorm(hidden_size)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, hidden_states, task_state=None, output_router_logits=True):
        forwarded_states = self.layer_norm(hidden_states)
        forwarded_states = self.mlp(forwarded_states, task_state)

        if isinstance(forwarded_states, tuple):
            forwarded_states, router_tuple = forwarded_states
        else:
            router_tuple = None

        output = hidden_states + self.dropout(forwarded_states)

        if output_router_logits and router_tuple is not None:
            output = (output, router_tuple)

        return output


class MoEFFLayer(nn.Module):
    r"""
    Switch Transformers Feed Forward layer module. This is a wrapper around the Mixture of Experts module.
    Parameters:
        config : ([`SwitchTransformersConfig`]): Model configuration class with all the parameters of the model.
            Initializing with a config file does not load the weights associated with the model, only the
            configuration. Check out the [`~PreTrainedModel.from_pretrained`] method to load the model weights.
        is_sparse (`bool`):
            Whether the MLP layer is a `Sparse` layer (contains a Mixture of Experts) or not
    """

    def __init__(self, dim, num_experts, expert_capacity, hidden_size, expert_class, dropout_rate=0, router_bias=True, router_jitter_noise=0.1, router_ignore_padding_tokens=False, router_z_loss_coef=0.001, router_aux_loss_coef=0.001, router_dtype="float32"):
        super().__init__()
        self.mlp = SparseMoELayer(dim, num_experts, expert_capacity, hidden_size, expert_class, router_bias=True, router_jitter_noise=0.1, router_ignore_padding_tokens=False, router_dtype="float32")
        self.layer_norm = MoELayerNorm(hidden_size)
        self.dropout = nn.Dropout(dropout_rate)

    def forward(self, hidden_states, task_state=None, output_router_logits=True):
        forwarded_states = self.layer_norm(hidden_states)
        forwarded_states = self.mlp(forwarded_states, task_state)

        if isinstance(forwarded_states, tuple):
            forwarded_states, router_tuple = forwarded_states
        else:
            router_tuple = None

        output = hidden_states + self.dropout(forwarded_states)

        if output_router_logits and router_tuple is not None:
            output = (output, router_tuple)

        return output

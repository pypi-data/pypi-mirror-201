import torch
import torch.nn as nn

from .context import ContextTransformer
from .transformer import TransformerHistory


class TxTBottom(nn.Module):
    def __init__(self, ctx_nums, seq_num, cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.is_candidate_mode = is_candidate_mode
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = TransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        if is_candidate_mode:
            # self.candidate_dense = nn.Linear(
            #     in_features=self.sequence_transformer.seq_embed_size,
            #     out_features=cross_size
            # )
            pass

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """

        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)
        if self.is_candidate_mode:
            candidate_embed = self.sequence_transformer.seq_embedding(candidate_in)
            outs = torch.concat([outs, candidate_embed], dim=1)
        return outs


class TxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, act_type="gelu", cross_size=200,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        self.dense1 = nn.Linear(cross_size, seq_num // 2)
        if act_type == "relu":
            self.act = nn.ReLU()
        elif act_type == "gelu":
            self.act = nn.GELU()
        elif act_type == "leakyRelu":
            self.act = nn.LeakyReLU(0.2)
        else:
            raise NotImplementedError
        self.dense2 = nn.Linear(seq_num // 2, seq_num)

    def forward(self, ctx_in, seq_in, vl_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, ] * C] and [B, 5]
        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)  # -> [B, cross_size]
        outs = self.dense1(outs)  # -> [B, seq_num//2]
        outs = self.act(outs)
        outs = self.dense2(outs)  # -> [B, seq_num]
        return outs

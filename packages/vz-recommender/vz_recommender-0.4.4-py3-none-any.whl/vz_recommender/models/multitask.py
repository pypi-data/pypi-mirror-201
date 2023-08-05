import torch
from torch import nn
from .mmoe import MMoE
from .bst import BST
from .txt import TxTBottom
from .sequence import SequenceTransformerAEP
from .context import ContextHead, ContextTransformerAndWide
from transformers import DistilBertModel
from .utils import MeanMaxPooling


class BSTBayouTaWMultitask(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_wad_embed_dim,
                 svc_dim, svc_embed_dim, new_svc_dim, new_svc_embed_dim, page_dim, page_embed_dim, item_dim,
                 item_embed_dim, seq_embed_dim, seq_hidden_size, nlp_encoder_path, nlp_dim,
                 expert_num, expert_hidden_sizes, task_num, task_hidden_sizes, task_last_activations,
                 sequence_transformer_kwargs=None):
        super().__init__()
        self.user_context_head = ContextTransformerAndWide(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
        )

        self.svc_embedding = nn.Embedding(svc_dim, svc_embed_dim)
        self.new_svc_embedding = nn.Embedding(new_svc_dim, new_svc_embed_dim)
        self.mm_pooling = MeanMaxPooling()

        self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, item_embed_dim)
        self.sequence_transformer = SequenceTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )

        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense_0 = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.search_nlp_dense_1 = torch.nn.Linear(
            in_features=seq_embed_dim * 2,
            out_features=seq_embed_dim // 2
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        if user_num_wide:
            user_ctx_out_dims = user_wad_embed_dim
        else:
            user_ctx_out_dims = user_wad_embed_dim // 2
        self.user_dense_0 = torch.nn.Linear(
            # nlp_out + aep_seq_out + svc_out + user_ctx_out
            in_features=seq_embed_dim // 2 + seq_embed_dim + svc_embed_dim * 2 + new_svc_embed_dim * 2 + user_ctx_out_dims,
            out_features=seq_embed_dim * 2
        )
        # self.user_dense_1 = torch.nn.Linear(
        #     in_features=seq_embed_dim * 2,
        #     out_features=seq_embed_dim
        # )
        self.user_act = nn.LeakyReLU(0.2)
        # self.user_dropout = nn.Dropout(p=0.1)

        self.mmoe = MMoE(
            input_size=seq_embed_dim * 2,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, user_deep_in, svc_in, new_svc_in, page_in, item_in, vl_in, user_wide_in=None, search_in=None):
        svc_out = self.svc_embedding(svc_in.long())
        svc_out = self.mm_pooling(svc_out)
        new_svc_out = self.new_svc_embedding(new_svc_in.long())
        new_svc_out = self.mm_pooling(new_svc_out)

        aep_seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.search_nlp_dense_0(search_out)
        search_out = self.nlp_act(search_out)
        search_out = self.search_nlp_dense_1(search_out)
        search_out = self.nlp_act(search_out)

        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.cat([search_out, aep_seq_out, svc_out, new_svc_out, user_ctx_out], dim=1)
        user_out = self.user_dense_0(user_out)
        user_out = self.user_act(user_out)

        outs = user_out
        # outs = self.mmoe(outs)
        perk_outs = self.perk_out_dense(outs)
        mrc_outs = self.mrc_out_dense(outs)
        return (perk_outs, mrc_outs), user_out


class BSTAudienceMultitask(nn.Module):
    def __init__(self, user_deep_dims, user_deep_embed_dims, user_num_wide, user_num_shared, user_wad_embed_dim,
                 offer_deep_dims, offer_deep_embed_dims, offer_num_wide, offer_num_shared, offer_wad_embed_dim,
                 item_dim, item_embed_dim, page_dim, page_embed_dim, seq_embed_dim, seq_hidden_size, nlp_encoder_path,
                 expert_num, expert_hidden_sizes, task_num, task_hidden_sizes, task_last_activations, nlp_dim=0,
                 sequence_transformer_kwargs=None):
        super().__init__()
        self.user_context_head = ContextHead(
            deep_dims=user_deep_dims,
            num_wide=user_num_wide,
            deep_embed_dims=user_deep_embed_dims,
            wad_embed_dim=user_wad_embed_dim,
            num_shared=user_num_shared,
        )
        self.offer_context_head = ContextHead(
            deep_dims=offer_deep_dims,
            num_wide=offer_num_wide,
            deep_embed_dims=offer_deep_embed_dims,
            wad_embed_dim=offer_wad_embed_dim,
            num_shared=offer_num_shared,
        )

        self.page_embedding = nn.Embedding(page_dim, page_embed_dim)
        self.item_embedding = nn.Embedding(item_dim, item_embed_dim)
        self.sequence_transformer = SequenceTransformerAEP(
            page_embedding=self.page_embedding,
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )

        self.nlp_encoder = DistilBertModel.from_pretrained(nlp_encoder_path)
        self.search_nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.offer_desc_nlp_dense = torch.nn.Linear(
            in_features=nlp_dim,
            out_features=seq_embed_dim * 2
        )
        self.nlp_act = nn.LeakyReLU(0.2)

        if user_num_wide:
            user_ctx_out_dims = user_wad_embed_dim * 2
        else:
            user_ctx_out_dims = user_wad_embed_dim
        self.user_dense = torch.nn.Linear(
            in_features=seq_embed_dim * 2 + seq_embed_dim + user_ctx_out_dims,
            out_features=seq_embed_dim * 2
        )
        self.user_act = nn.LeakyReLU(0.2)
        if offer_num_wide:
            offer_ctx_out_dims = offer_wad_embed_dim * 2
        else:
            offer_ctx_out_dims = offer_wad_embed_dim
        self.offer_dense = torch.nn.Linear(
            in_features=seq_embed_dim * 2 + offer_ctx_out_dims,
            out_features=seq_embed_dim * 2
        )
        self.offer_act = nn.LeakyReLU(0.2)

        self.mmoe = MMoE(
            input_size=seq_embed_dim * 4,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, user_deep_in, offer_deep_in, page_in, item_in, vl_in,
                user_wide_in=None, offer_wide_in=None, offer_desc_in=None, search_in=None):
        """
        Args:
            deep_in: list, a list of Tensor of shape [batch_size, deep_dims].
            seq_in: Tensor, shape [batch_size, seq_len].
            vl_in: Tensor, shape [batch_size].
            wide_in: list, a list of Tensor of shape [batch_size, num_wide].
            shared_in: list, a list of Tensor of shape [batch_size, num_shared] (default=None).
            search_ids: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
            att_mask: tensor, Tensor of shape [batch_size, sentence_length] (default=None).
        Return:
            out: Tensor, shape [batch_size, seq_dim].
            user_out: Tensor, shape [batch_size, seq_embed_dim].
        """
        seq_out = self.sequence_transformer(page_in=page_in, item_in=item_in, vl_in=vl_in)

        offer_desc_out = self.nlp_encoder(**offer_desc_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        offer_desc_out = self.search_nlp_dense(offer_desc_out)
        offer_desc_out = self.nlp_act(offer_desc_out)
        search_out = self.nlp_encoder(**search_in).last_hidden_state[:, 0, :].to(dtype=torch.float32)
        search_out = self.search_nlp_dense(search_out)
        search_out = self.nlp_act(search_out)

        offer_ctx_out = self.offer_context_head(deep_in=offer_deep_in, wide_in=offer_wide_in)
        offer_out = torch.cat([offer_desc_out, offer_ctx_out], dim=1)
        offer_out = self.offer_dense(offer_out)
        offer_out = self.offer_act(offer_out)
        user_ctx_out = self.user_context_head(deep_in=user_deep_in, wide_in=user_wide_in)
        user_out = torch.cat([search_out, seq_out, user_ctx_out], dim=1)
        user_out = self.user_dense(user_out)
        user_out = self.user_act(user_out)

        outs = torch.cat([offer_out, user_out], dim=1)
        outs = self.mmoe(outs)
        return outs, user_out


class MultiTaskBST(nn.Module):
    """
    Args:
        deep_dims: size of the dictionary of embeddings.
        seq_dim: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int.
        seq_hidden_size: the dimension of the feedforward network model.
        expert_num: the number of expert layer.
        expert_hidden_sizes: the dimension of the feedforward network model.
        task_num: the number of task output.
        task_hidden_sizes: the dimension of the feedforward network model.
        task_last_activations: list of activations for each task.
        num_wide: the number of wide input features (default=0).
        num_shared: the number of embedding shared with sequence transformer (default=1).
    """
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations, num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None, 
                 item_embedding_weight=None, shared_embeddings_weight=None):
        super(MultiTaskBST, self).__init__()
        self.shared_bottom = BSTBottom(
            deep_dims=deep_dims,
            seq_dim=seq_dim,
            seq_embed_dim=seq_embed_dim,
            deep_embed_dims=deep_embed_dims,
            seq_hidden_size=seq_hidden_size,
            num_wide=num_wide,
            num_shared=num_shared,
            item_embedding_weight=item_embedding_weight,
            shared_embeddings_weight=shared_embeddings_weight,
            context_head_kwargs=context_head_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        self.mmoe = MMoE(
            input_size=seq_embed_dim,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, deep_in, seq_in, vl_in, wide_in, shared_in):
        bottom_features = self.shared_bottom(deep_in=deep_in, seq_in=seq_in, vl_in=vl_in, wide_in=wide_in, shared_in=shared_in)
        outs = self.mmoe(bottom_features)
        return outs


class MultiTaskTxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.is_candidate_mode = is_candidate_mode
        self.shared_bottom = TxTBottom(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = cross_size + self.shared_bottom.sequence_transformer.seq_embed_dim
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        bottom_features = self.shared_bottom(ctx_in, seq_in, vl_in, candidate_in, seq_history)
        outs = self.mmoe(bottom_features)
        return outs

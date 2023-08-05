import math
from typing import *

import torch
from torch import Tensor, nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .utils import MeanMaxPooling, PositionalEncoding


class ContextTransformerAndWide(nn.Module):
    """
    Transformer using deep and wide context features
    
    Args:
        deep_dims: size of dictionary of deep embeddings
        deep_embed_dims: the number of expected features in the encoder/decoder inputs (default=200)
        deep_num_heads: the number of heads in the multiheadattention models (default=4)
        deep_hidden_size: the dimension of the feedforward network model (default=512)
        deep_transformer_dropout: the dropout value (default=0.0)
        deep_num_layers: the number of sub-encoder-layers in the encoder (default=2)
        deep_pooling_dropout: the dropout value (default=0.0)
        deep_pe: If "True" then positional encoding is applied
        num_wide: No. of wide features (default=0.0)
        wad_embed_dim: no. of output features (default=64)
    """
    def __init__(self, deep_dims, deep_embed_dims=128, deep_num_heads=2,
                 deep_hidden_size=512, deep_num_layers=2, deep_transformer_dropout=0.0,
                 deep_pooling_dropout=0.0, deep_pe=False, num_wide=0, wad_embed_dim=64):
        super().__init__()
        self.deep_embedding = nn.ModuleList([
            nn.Embedding(deep_dim, deep_embed_dims)
            for deep_dim in deep_dims
        ])
        self.deep_pe = deep_pe
        self.deep_embed_dims = deep_embed_dims
        if deep_pe:
            self.pos_encoder = PositionalEncoding(d_model=deep_embed_dims,
                                                  dropout=deep_transformer_dropout,
                                                  max_len=len(deep_dims))
        encoder_layers = TransformerEncoderLayer(d_model=deep_embed_dims,
                                                 nhead=deep_num_heads,
                                                 dropout=deep_transformer_dropout,
                                                 dim_feedforward=deep_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.deep_encoder = TransformerEncoder(encoder_layers, num_layers=deep_num_layers)
        self.deep_pooling_dp = MeanMaxPooling(dropout=deep_pooling_dropout)
        self.deep_dense = torch.nn.Linear(in_features=2 * deep_embed_dims, out_features=wad_embed_dim//2)
        self.num_wide = num_wide
        if self.num_wide:
            self.wide_batch_norm = nn.BatchNorm1d(num_wide)
            self.wide_dense = nn.Linear(num_wide, wad_embed_dim//2)
            self.wide_act = nn.LeakyReLU(0.2)

    def forward(self, deep_in, wide_in):
        """
         Input data is deep_in & wide_in embedding
         
         Args:
             deep_in: list
             wide_in: list
             
         Return:
            ctx_out: Tensor

        Shape:
            deep_in: [batch_size, deep_dims]
            wide_in: [batch_size, num_wide]
            shared_in: [batch_size, num_shared]
            ctx_out: [batch_size, len(deep_dims)*deep_embed_dims+(num_shared*seq_embed_dim)+num_wide]
        """
        deep_embedding_list = [self.deep_embedding[i](input_deep).unsqueeze(1)
                                  for i, input_deep in enumerate(deep_in)]
        deep_out = torch.cat(deep_embedding_list, dim=1)
        if self.deep_pe:
            deep_out = deep_out * math.sqrt(self.deep_embed_dims)
            deep_out = self.pos_encoder(deep_out)
        deep_out = self.deep_encoder(deep_out)
        deep_out = self.deep_pooling_dp(deep_out)
        deep_out = self.deep_dense(deep_out)
        if self.num_wide:
            wide_in_list = [wide_i.float() for wide_i in wide_in]
            wide_cat = torch.stack(wide_in_list, dim=0)
            wide_out = torch.transpose(wide_cat, dim1=1, dim0=0)
            if self.num_wide != 1:
                wide_out_norm = self.wide_batch_norm(wide_out)
            else:
                wide_out_norm = wide_out
            wide_out_norm = self.wide_dense(wide_out_norm)
            wide_out_norm = self.wide_act(wide_out_norm)
            ctx_out = torch.cat((deep_out, wide_out_norm), dim=1)
        else:
            ctx_out = deep_out
        return ctx_out


class ContextHead(nn.Module):
    """
    Transformer using deep and wide context features along with embeddings shared with sequence transformer
  
    Args:
        deep_dims: size of the dictionary of embeddings
        item_embedding: item embedding shared with sequence transformer.
        deep_embed_dims: the size of each embedding vector, can be either int or list of int
        num_wide: the number of wide input features (default=0)
        wad_embed_dim: no. of output features (default=64)
        num_shared: the number of embedding shared with sequence transformer (default=1)
        shared_embeddings_weight: list of embedding shared with candidate generation model
    """
    def __init__(self, deep_dims, item_embedding=None, deep_embed_dims=100, num_wide=0, wad_embed_dim=64,
                 num_shared=0, shared_embeddings_weight=None):
        super().__init__()
        self.num_wide = num_wide
        if isinstance(deep_embed_dims, int):
            if shared_embeddings_weight is None:
                self.deep_embedding = nn.ModuleList([
                    nn.Embedding(deep_dim, deep_embed_dims)
                    for deep_dim in deep_dims
                ])
            else:
                self.deep_embedding = nn.ModuleList([
                    nn.Embedding(deep_dim, deep_embed_dims)
                    for deep_dim in deep_dims[:-len(shared_embeddings_weight)]
                ])
                from_pretrained = nn.ModuleList([
                    nn.Embedding.from_pretrained(shared_embedding_weight, freeze=True)
                    for shared_embedding_weight in shared_embeddings_weight
                ])
                self.deep_embedding.extend(from_pretrained)
        elif isinstance(deep_embed_dims, list) or isinstance(deep_embed_dims, tuple):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dim)
                for deep_dim, deep_embed_dim in zip(deep_dims, deep_embed_dims)
            ])
        else:
            raise NotImplementedError()

        self.ctx_pe = False

        if self.num_wide:
            self.wide_batch_norm = nn.BatchNorm1d(num_wide)
        self.deep_embed_dims = deep_embed_dims
        if item_embedding and num_shared:
            self.shared_embed = nn.ModuleList([
                item_embedding
                for _ in range(num_shared)
            ])
        else:
            self.shared_embed = None
        self.deep_dense = nn.Linear((len(deep_dims) + num_shared) * deep_embed_dims, wad_embed_dim//2)
        self.deep_act = nn.LeakyReLU(0.2)
        if self.num_wide:
            self.wide_dense = nn.Linear(num_wide, wad_embed_dim//2)
            self.wide_act = nn.LeakyReLU(0.2)

    def forward(self, deep_in: List[Tensor], wide_in: List[Tensor] = None, shared_in: List[Tensor] = None):
        """
        Input is deep, wide & shared embedding
        
        Args:
            deep_in: list
            wide_in: list
            shared_in: list (default=None).

        Return:
            ctx_out: Tensor
        
        Shape:
            deep_in: [batch_size, deep_dims]
            wide_in: [batch_size, num_wide]
            shared_in: [batch_size, num_shared]
            ctx_out: [batch_size, len(deep_dims)*deep_embed_dims+(num_shared*seq_embed_dim)+num_wide]
        """
        deep_embedding_list = [self.deep_embedding[i](input_deep).unsqueeze(1)
                               for i, input_deep in enumerate(deep_in)]
        if shared_in is not None and self.shared_embed is not None:
            shared_in_list = [self.shared_embed[i](input_shared).unsqueeze(1)
                              for i, input_shared in enumerate(shared_in)]
            deep_embedding_list.extend(shared_in_list)

        deep_out = torch.cat(deep_embedding_list, dim=2).squeeze(1)
        deep_out = self.deep_dense(deep_out)
        deep_out = self.deep_act(deep_out)
        if self.num_wide:
            wide_in_list = [wide_i.float() for wide_i in wide_in]
            wide_cat = torch.stack(wide_in_list, dim=0)
            wide_out = torch.transpose(wide_cat, dim1=1, dim0=0)
            if self.num_wide != 1:
                wide_out_norm = self.wide_batch_norm(wide_out)
            else:
                wide_out_norm = wide_out
            wide_out_norm = self.wide_dense(wide_out_norm)
            wide_out_norm = self.wide_act(wide_out_norm)
            ctx_out = torch.cat((deep_out, wide_out_norm), dim=1)
            return ctx_out
        else:
            return deep_out


class ContextTransformer(nn.Module):
    """
    Run transformer over contextual features
    
    Args:
        ctx_nums: the number of context input features
        cross_size: the dimension of output features
        ctx_embed_size: the number of expected features in the encoder/decoder inputs (default=100)
        ctx_num_heads: the number of heads in the multiheadattention models (default=2)
        ctx_hidden_size: the dimension of the feedforward network model (default=512)
        ctx_num_layers: the number of sub-encoder-layers in the encoder (default=1).
        ctx_transformer_dropout:
        ctx_pooling_dropout: the dropout value (default=0.0)
        ctx_pe: If "True" then positional encoding is applied       
    """
    def __init__(self, ctx_nums, cross_size, ctx_embed_size=100, ctx_num_heads=2,
                 ctx_hidden_size=512, ctx_num_layers=1, ctx_transformer_dropout=0.0,
                 ctx_pooling_dropout=0.0, ctx_pe=False):
        super().__init__()
        self.ctx_embedding = nn.ModuleList([
            nn.Embedding(ctx_num, ctx_embed_size)
            for ctx_num in ctx_nums
        ])
        self.ctx_pe = ctx_pe
        self.ctx_embed_size = ctx_embed_size
        if ctx_pe:
            self.pos_encoder = PositionalEncoding(d_model=ctx_embed_size,
                                                  dropout=ctx_transformer_dropout,
                                                  max_len=len(ctx_nums))
        encoder_layers = TransformerEncoderLayer(d_model=ctx_embed_size,
                                                 nhead=ctx_num_heads,
                                                 dropout=ctx_transformer_dropout,
                                                 dim_feedforward=ctx_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.ctx_encoder = TransformerEncoder(encoder_layers, num_layers=ctx_num_layers)
        self.ctx_pooling_dp = MeanMaxPooling(dropout=ctx_pooling_dropout)
        self.ctx_dense = torch.nn.Linear(in_features=2 * ctx_embed_size, out_features=cross_size)

    def forward(self, ctx_in):
        """
        Input is context features
        
        Args:
            ctx_in: list of Tensor
        
         Return:
            ctx_out: Tensor
            
        Shape:
            ctx_in: [batch_size, 1]
            ctx_out: [batch_size, cross_size] 
        """
        ctx_embedding_list = [self.ctx_embedding[i](input_ctx).unsqueeze(1) for i, input_ctx in enumerate(ctx_in)]
        ctx_out = torch.cat(ctx_embedding_list, dim=1)
        if self.ctx_pe:
            ctx_out = ctx_out * math.sqrt(self.ctx_embed_size)
            ctx_out = self.pos_encoder(ctx_out)
        ctx_out = self.ctx_encoder(ctx_out)
        ctx_out = self.ctx_pooling_dp(ctx_out)
        ctx_out = self.ctx_dense(ctx_out)
        return ctx_out

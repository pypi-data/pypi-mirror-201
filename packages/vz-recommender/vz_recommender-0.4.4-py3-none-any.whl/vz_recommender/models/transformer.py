import math
from typing import *

import torch
import torch.nn.functional as F
from einops import rearrange
from torch import einsum, nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .utils import *


def rotate_half(x):
    """
    Rotate the input data

    Args :
        x : input data

    Return : 
        rotated output by half
    """
    x = rearrange(x, "... (j d) -> ... j d", j=2)
    x1, x2 = x.unbind(dim=-2)
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(pos, t):
    """
    to apply rotatory for positional embeddings

    Args :
        pos : positional embeddings value
        t : t degress to rotate

    Return : 
        rotate t degrees
    """
    return (t * pos.cos()) + (rotate_half(t) * pos.sin())


class TransformerHistory(nn.Module):
    """
    TransformerHistory

    Args:
        seq_num: size of the dictionary of embeddings.
        seq_embed_dim: the number of expected features in the encoder/decoder inputs (default=200).
        seq_max_length: the max sequence input length (default=8).
        seq_num_heads: the number of heads in the multiheadattention models (default=4).
        seq_hidden_size: the dimension of the feedforward network model (default=512).
        seq_transformer_dropout: the dropout value (default=0.0).
        seq_num_layers: the number of sub-encoder-layers in the encoder (default=2).
        seq_pooling_dropout: the dropout value (default=0.0).
        seq_pe: If "True" then positional encoding is applied
    """
    def __init__(self, seq_num, seq_embed_dim=100, seq_max_length=8, seq_num_heads=4, seq_hidden_size=512, seq_transformer_dropout=0.0, 
                 seq_num_layers=2, seq_pooling_dropout=0.0, seq_pe=True):
        super().__init__()
        self.seq_embedding = nn.Embedding(seq_num, seq_embed_dim)
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    @staticmethod
    def create_key_padding_mask(seq_in, valid_length=None):
        """
        To create key padding mask

        Args :
            seq_in: input sequence to be used
            valid_length: valid length to be used
        
        Return :
            mask padded value
        """
        device = seq_in.device
        vl_len = torch.cat((seq_in.size(0)*[torch.tensor([seq_in.size(1)])]), dim=0).to(device) if valid_length is None else valid_length
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(vl_len.unsqueeze(1))
        return mask

    def forward(self, seq_in, vl_in, seq_history=None):
        """
        Takes in seq_in and vl_in, seq_history values as input parameters

        Args :
            seq_in: input sequence to be used
            vl_in: valid length to be used
            seq_history: squence history data

        Return :
            sequence output data

        Shape :
            seq_in: [batch_size, seq_len]
            vl_in: [batch_size]
            seq_history: [batch_size, history_len]

            out : [batch_size, 2*seq_embed_dim]
        """
        seq_embed_out = self.seq_embedding(seq_in.long())
        # history_embed_out = self.seq_embedding(input_history_seq.long())
        # history_embed_out = history_embed_out.transpose(0, 1).mean(dim=0, keepdim=True)
        # combined_embed_out = torch.cat([history_embed_out, seq_embed_out], dim=0)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)
        seq_out = self.seq_dense(seq_out)

        return seq_out


class TransformerAEP(TransformerHistory):
    """
    Transformer Adobe Experience Platform (AEP)

    Args :
        page_embedding : the page field embeddings
        item_embedding : the item embeddings
        seq_embed_dim : the number of expected features in the encoder/decoder inputs (default=200)
        seq_max_length : the max sequence length, (default=8)
        seq_num_heads : the number of heads in the multiheadattention models (default=4)
        seq_hidden_size : the hidden layer size of the feedforward network model (default=512).
        seq_transformer_dropout : the dropout value (default=0.0)
        seq_num_layers : the number of sub-encoder-layers in the encoder (default=2).
        seq_pooling_dropout : the pooling dropout value (default=0.0).
        seq_pe : If "True" then positional encoding is applied (default=True)
    """
    def __init__(self, page_embedding, item_embedding, seq_embed_dim, seq_max_length=8,
                 seq_num_heads=4, seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2,
                 seq_pooling_dropout=0.0, seq_pe=True):
        super().__init__(seq_embed_dim, seq_max_length=8, seq_num_heads=4, seq_hidden_size=512,
                         seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                         seq_pe=True)
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    def forward(self, page_in, item_in, vl_in, seq_history=None):
        """
        take input and output

        Args :
            page_in: page input values
            item_in : item input values
            vl_in: valid length to be used
            seq_history: Tensor

        Return :
            Sequential output after applying transformer 

        Shape :
            page_in: [batch_size, seq_len]
            item_in: [batch_size, seq_len]b
            vl_in: [batch_size]
            seq_history: [batch_size, history_len]

            out : [batch_size, 2*seq_embed_dim]
        """
        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
#         seq_embed_out = torch.cat((page_embed_out, item_embed_out), 2)
        seq_embed_out = torch.mul(page_embed_out, item_embed_out)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=page_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)
        seq_out = self.seq_dense(seq_out)
        return seq_out


class ParallelTransformerBlock(nn.Module):
    """
    Parallel Transformer Block

    Args :
        dim : the dimension size
        dim_head : dimensions of multihead attention network
        heads : no of multi-head attention required
        ff_mult : feedforward multiple layers (default=4),
        moe_kwargs : args for moe params
    """
    def __init__(self, dim, dim_head, heads, ff_mult=4, moe_kwargs=None):
        super().__init__()
        self.norm = LayerNorm(dim)

        attn_inner_dim = dim_head * heads
        ff_inner_dim = dim * ff_mult
        self.fused_dims = (attn_inner_dim, dim_head, dim_head, (ff_inner_dim * 2))

        self.heads = heads
        self.scale = dim_head**-0.5
        self.rotary_emb = RotaryEmbedding(dim_head)

        self.fused_attn_ff_proj = nn.Linear(dim, sum(self.fused_dims), bias=False)
        self.attn_out = nn.Linear(attn_inner_dim, dim, bias=False)
        
        self.ff_out = nn.Sequential(
            SwiGLU(),
            nn.Linear(ff_inner_dim, dim, bias=False)
        )       
#         self.gate = Top2Gate(dim, moe_kwargs.get("num_experts"))
#         self.fused_attn_moe_proj = MOELayer(self.gate, self.fused_attn_ff_proj, sum(self.fused_dims))

        self.register_buffer("mask", None, persistent=False)
        self.register_buffer("pos_emb", None, persistent=False)
        
    @staticmethod
    def create_key_padding_mask(seq_in, valid_length=None):
        """
        To create key padding mask

        Args :
            seq_in: input sequence to be used
            valid_length: valid length to be used
        
        Return :
            mask padded value
        """
        device = seq_in.device
        vl_len = torch.cat((seq_in.size(0)*[torch.tensor([seq_in.size(1)])]), dim=0).to(device) if valid_length is None else valid_length
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(vl_len.unsqueeze(1))
        return mask

    def get_mask(self, n, device):
        """
        take input and output

        Args :
            n: size of tensor
            device: the device to be used, cpu or gpu

        Return :
            mask value
        """
        if self.mask is not None and self.mask.shape[-1] >= n:
            return self.mask[:n, :n]

        mask = torch.ones((n, n), device=device, dtype=torch.bool).triu(1)
        self.register_buffer("mask", mask, persistent=False)
        return mask

    def get_rotary_embedding(self, n, device):
        """
        take input and output

        Args :
            n: size of tensor
            device: the device to be used, cpu or gpu

        Return :
            Rotated embeddings
        """
        if self.pos_emb is not None and self.pos_emb.shape[-2] >= n:
            return self.pos_emb[:n]

        pos_emb = self.rotary_emb(n, device=device)
        self.register_buffer("pos_emb", pos_emb, persistent=False)
        return pos_emb

    def forward(self, x, vl=None):
        """
        take input and returns output

        Args :
            x: the input to be used
            vl: valid length to be used

        Return :
            Rotatory embeddings output
        """
        n, device, h = x.shape[1], x.device, self.heads
        x = self.norm(x)
        # attention queries, keys, values, and feedforward inner
        
#         x, aux_loss = self.fused_attn_moe_proj(x)
        x = self.fused_attn_ff_proj(x)
        q, k, v, ff = x.split(self.fused_dims, dim=-1)
        q = rearrange(q, "b n (h d) -> b h n d", h=h)

        positions = self.get_rotary_embedding(n, device)
        q, k = map(lambda t: apply_rotary_pos_emb(positions, t), (q, k))
        q = q * self.scale
        sim = einsum("b h i d, b j d -> b h i j", q, k)

#         causal_mask = self.get_mask(n, device)
        mask = self.create_key_padding_mask(seq_in=x, valid_length=vl)
        sim = sim.masked_fill(mask.unsqueeze(1).unsqueeze(2), float('-inf'))

        attn = sim.softmax(dim=-1)

        out = einsum("b h i j, b j d -> b h i d", attn, v)

        out = rearrange(out, "b h n d -> b n (h d)")
#         out, aux_loss = self.fused_attn_moe_proj(out)

        out = self.attn_out(out) + self.ff_out(ff)
        return out
    
    
class TransformerAEPCat(TransformerHistory):
    """
    Transformer Adobe Experience Platform (AEP)

    Args :
        page_embedding : the page field embeddings
        item_embedding : the item embeddings
        seq_embed_dim : the number of expected features in the encoder/decoder inputs (default=200)
        seq_max_length : the max sequence length, (default=8)
        seq_num_heads : the number of heads in the multiheadattention models (default=4)
        seq_hidden_size : the hidden layer size of the feedforward network model (default=512).
        seq_transformer_dropout : the dropout value (default=0.0)
        seq_num_layers : the number of sub-encoder-layers in the encoder (default=2).
        seq_pooling_dropout : the pooling dropout value (default=0.0).
        seq_pe : If "True" then positional encoding is applied (default=True)
    """
    def __init__(self, page_embedding, item_embedding, seq_embed_dim, seq_max_length=8,
                 seq_num_heads=4, seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2,
                 seq_pooling_dropout=0.0, seq_pe=True):
        super().__init__(seq_embed_dim, seq_max_length=8, seq_num_heads=4, seq_hidden_size=512,
                         seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                         seq_pe=True)
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)

    def forward(self, page_in, item_in, vl_in, seq_history=None):
        """
        take input and output

        Args :
            page_in: page input values
            item_in : item input values
            vl_in: valid length to be used
            seq_history: Tensor

        Return :
            Sequential output after applying transformer 

        Shape :
            page_in: [batch_size, seq_len]
            item_in: [batch_size, seq_len]b
            vl_in: [batch_size]
            seq_history: [batch_size, history_len]

            out : [batch_size, 2*seq_embed_dim]
        """
        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
        seq_embed_out = torch.cat((page_embed_out, item_embed_out), 2)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=page_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)
        seq_out = self.seq_dense(seq_out)
        return seq_out


class ParallelTransformerAEP(nn.Module):
    """
    Parallel Transformer Adobe Enterprise Product

    Args :
        page_embedding : the page field embeddings 
        item_embedding : the item embeddings
        dim : the dimension size
        dim_head : dimensions of multihead attention network
        heads : no of multi-head attention required
        num_layers : number of hidden layers needed
        ff_mult : feedforward multi
        seq_pooling_dropout :  the pooling dropout value (default=0.0).
    """
    def __init__(self, page_embedding, item_embedding, dim, dim_head, heads, num_layers, ff_mult=4, seq_pooling_dropout=0.0, moe_kwargs=None):
        super().__init__()
        self.page_embedding = page_embedding
        self.item_embedding = item_embedding
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(2 * dim, dim)  
        self.num_layers = num_layers
#         self.ptransformer = nn.ModuleList([
#             ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult, moe_kwargs=moe_kwargs)
#             for _ in range(self.num_layers)
#         ])
        
        self.ptransformer = nn.ModuleList([
            Residual(ParallelTransformerBlock(dim=dim, dim_head=dim_head, heads=heads, ff_mult=ff_mult, moe_kwargs=moe_kwargs))
            for _ in range(self.num_layers)
        ])
        
    def forward(self, page_in, item_in, vl_in):
        """
        take input and output

        Args :
            page_in: input sequence
            item_in: input sequence
            vl_in: valid length of input data

        Return :
            Parallel transformer output
        """
        page_embed_out = self.page_embedding(page_in.long())
        item_embed_out = self.item_embedding(item_in.long())
#         aux_loss = 0
        x = torch.mul(page_embed_out, item_embed_out)
#         x = torch.cat((page_embed_out, item_embed_out), 2)
        for i in range(self.num_layers):
            x = self.ptransformer[i](x, vl_in)
#             x, aux_loss = self.ptransformer[i](x, vl_in)
#             aux_loss += aux_loss

        out = self.seq_pooling_dp(x)
        out = self.seq_dense(out)        
        return out

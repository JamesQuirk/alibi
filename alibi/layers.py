import torch
from torch import nn
from torch.nn import functional as F

from alibi.attention import ALiBiMultiHeadAttention
from alibi.config import ALiBiConfig


class FeedForward(nn.Module):
    def __init__(self, config: ALiBiConfig) -> None:
        super().__init__()
        d_hidden = config.d_model * config.expansion_factor
        self.fc1 = nn.Linear(config.d_model, d_hidden)
        self.fc2 = nn.Linear(d_hidden, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.gelu(self.fc1(x))
        out = self.dropout(self.fc2(x))
        return out


class ALiBiTransformerLayer(nn.Module):
    def __init__(self, config: ALiBiConfig) -> None:
        super().__init__()
        self.ffn_norm = nn.LayerNorm(config.d_model, eps=config.lnorm_eps)
        self.attn_norm = nn.LayerNorm(config.d_model, eps=config.lnorm_eps)
        self.ffn = FeedForward(config)
        self.attn = ALiBiMultiHeadAttention(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.attn_norm(x))
        x = x + self.ffn(self.ffn_norm(x))
        return x

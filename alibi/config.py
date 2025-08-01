from dataclasses import dataclass


@dataclass
class ALiBiConfig:
    num_layers: int = 6
    d_model: int = 256
    num_heads: int = 8
    max_len: int = 256
    dropout: float = 0.1
    causal: bool = True
    expansion_factor: int = 1
    lnorm_eps: float = 1e-6
    # `window` is the number of tokens to look back in the past
    window: int | None = None

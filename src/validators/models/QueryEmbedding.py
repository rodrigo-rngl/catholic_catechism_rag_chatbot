from typing import Mapping, Sequence, Optional
from pydantic import BaseModel, ConfigDict

float_vec = Sequence[float]
float_mat = Sequence[Sequence[float]]

# Base imutável para qualquer tipo de embedding
class QueryEmbeddingBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    dense: Optional[float_vec]
    sparse: Optional[Mapping[int, float]]
    late: Optional[float_mat]

# Tipos concretos
class QueryHybridEmbedding(QueryEmbeddingBase):
    dense: float_vec
    sparse: Mapping[int, float]
    late: float_mat
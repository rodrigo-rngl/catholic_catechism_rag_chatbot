from typing import Generic, Any, List, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

float_vec = List[float]
float_mat = List[List[float]]


class SparseDict(BaseModel):
    indices: List[int]
    values: List[float]


Dense = TypeVar("Dense")
Sparse = TypeVar("Sparse")
Late = TypeVar("Late")


# Base imutável (Interface)
class QueryEmbeddingBase(BaseModel, Generic[Dense, Sparse, Late]):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dense: Dense
    sparse: Sparse
    late: Late


QueryEmbeddingType = TypeVar(
    "QueryEmbeddingType", bound=QueryEmbeddingBase[Any, Any, Any])


# Tipos concretos
class QueryHybridEmbedding(QueryEmbeddingBase[float_vec, SparseDict, float_mat]):
    dense: float_vec
    sparse: SparseDict
    late: float_mat


class QueryDenseEmbedding(QueryEmbeddingBase[float_vec, SparseDict | None, float_mat | None]):
    dense: float_vec
    sparse: SparseDict | None = None
    late: float_mat | None = None

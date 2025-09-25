from typing import Generic, Dict, List, TypeVar
from pydantic import BaseModel, ConfigDict

float_vec = List[float]
float_mat = List[List[float]]


class SparseDict(BaseModel):
    indices: List[int]
    values: List[float]


Dense = TypeVar("Dense", bound=float_vec)
Sparse = TypeVar("Sparse", bound=SparseDict)
Late = TypeVar("Late", bound=float_mat)


# Base imutável (Interface)
class QueryEmbeddingBase(BaseModel, Generic[Dense, Sparse, Late]):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dense: Dense
    sparse: Sparse
    late: Late


# Tipos concretos
class QueryHybridEmbedding(QueryEmbeddingBase[float_vec, SparseDict, float_mat]):
    dense: float_vec
    sparse: SparseDict
    late: float_mat

from typing import Generic, Dict, List, TypeVar
from pydantic import BaseModel, ConfigDict
import numpy as np

float_vec = List[float]
float_mat = List[List[float]]

Dense = TypeVar("Dense", bound=float_vec)
Sparse = TypeVar("Sparse", bound=Dict[str, List[int | float]])
Late = TypeVar("Late", bound=float_mat)


# Base imutável (Interface)
class QueryEmbeddingBase(BaseModel, Generic[Dense, Sparse, Late]):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dense: Dense
    sparse: Sparse
    late: Late


# Tipos concretos
class QueryHybridEmbedding(QueryEmbeddingBase[float_vec, Dict[str, List[int | float]], float_mat]):
    dense: float_vec
    sparse: Dict[str, List[int | float]]
    late: float_mat

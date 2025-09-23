from typing import Tuple, List, Dict, Optional, Iterator, Any, TypeVar, Generic
from pydantic import BaseModel, ConfigDict
import numpy as np

float_vec = List[float]
float_mat = List[List[float]]

Dense = TypeVar("Dense", bound=List[float_vec])
Sparse = TypeVar("Sparse", bound=List[Dict[str, List[int | float]]])
Late = TypeVar("Late", bound=List[float_mat])


# Base imutável (Interface)
class IngestionEmbeddingsBase(BaseModel, Generic[Dense, Sparse, Late]):
    model_config = ConfigDict(frozen=True, extra="forbid")

    dense: Dense
    sparse: Sparse
    late: Late

    def __length(self) -> int:
        for seq in (self.dense, self.sparse, self.late):
            if seq is not None:
                return len(seq)
        return 0

    def __validate_lengths(self) -> None:
        n1, n2, n3 = len(self.dense), len(self.sparse), len(self.late)
        if not (n1 == n2 == n3):
            raise ValueError(
                "Os tamanhos dos componentes não coincidem; devem ser iguais."
            )

    def iter_components(self) -> Iterator[
            Tuple[
                Optional[float_vec],
                Optional[Dict[str, List[int | float]]],
                Optional[float_mat]
            ]]:

        self.__validate_lengths()
        n = self.__length()

        def get(seq, i: int) -> None | Any:
            return None if seq is None else seq[i]

        for i in range(n):
            yield (
                get(self.dense, i),
                get(self.sparse, i),
                get(self.late, i),
            )


# Tipos concretos
class IngestionHybridEmbeddings(IngestionEmbeddingsBase[List[float_vec], List[Dict[str, List[int | float]]], List[float_mat]]):
    dense: List[float_vec]
    sparse: List[Dict[str, List[int | float]]]
    late: List[float_mat]

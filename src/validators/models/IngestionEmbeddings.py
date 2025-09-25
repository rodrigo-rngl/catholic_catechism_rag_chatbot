from typing import Tuple, List, Optional, Iterator, Any, TypeVar, Generic, List
from pydantic import BaseModel, ConfigDict

float_vec = List[float]
float_mat = List[List[float]]


class SparseDict(BaseModel):
    indices: List[int]
    values: List[float]


Dense = TypeVar("Dense", bound=List[float_vec])
Sparse = TypeVar("Sparse", bound=List[SparseDict])
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
                Optional[SparseDict],
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
class IngestionHybridEmbeddings(IngestionEmbeddingsBase[List[float_vec], List[SparseDict], List[float_mat]]):
    dense: List[float_vec]
    sparse: List[SparseDict]
    late: List[float_mat]

from typing import Tuple, List, Dict, Optional, Iterator, Any
from pydantic import BaseModel, ConfigDict

float_vec = List[float]
float_mat = List[List[float]]


# Base imutável para qualquer tipo de embedding
class IngestionEmbeddingsBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    dense: Optional[List[float_vec]]
    sparse: Optional[List[Dict[str, List[int | float]]]]
    late: Optional[List[float_mat]]

    def __length(self) -> int:
        for seq in (self.dense, self.sparse, self.late):
            if seq is not None:
                return len(seq)
        return 0

    def __validate_lengths(self) -> None:
        lengths: List[int] = [len(seq) for seq in (
            self.dense, self.sparse, self.late) if seq is not None]

        if lengths and any(length != lengths[0] for length in lengths):
            raise ValueError(
                f"O tamanho dos componentes não coincidem. Todos os componentes devem estar alinhados, possuim o mesmo tamanho.")

    def iter_components(self) -> Iterator[
            Tuple[
                Optional[float_vec],
                Optional[Dict[str, List[int | float]]],
                Optional[float_mat]
            ]]:

        self.__validate_lengths()
        n = self.__length()

        def get(seq, i) -> None | Any:
            return None if seq is None else seq[i]

        for i in range(n):
            yield (
                get(self.dense, i),
                get(self.sparse, i),
                get(self.late, i),
            )


# Tipos concretos
class IngestionHybridEmbeddings(IngestionEmbeddingsBase):
    dense: List[float_vec]  # type: ignore
    sparse: List[Dict[str, List[int | float]]]  # type: ignore
    late: List[float_mat]  # type: ignore


class IngestionDenseEmbeddings(IngestionEmbeddingsBase):
    dense: List[float_vec]  # type: ignore

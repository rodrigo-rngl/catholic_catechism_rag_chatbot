from typing import Literal
from src.errors.types.class_not_implemented_error import ClassNotImplementedError
from src.infra.interfaces.qdrant_points_searcher_interface import QdrantPointsSearcherInterface
from src.infra.vector_db.qdrant.points_searchers.qdrant_hybrid_points_searcher import QdrantHybridPointsSearcher

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantPointsSearcherFactory")


class QdrantPointsSearcherFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']) -> None:
        self.search_type = search_type

    def produce(self) -> QdrantPointsSearcherInterface:
        if self.search_type == 'Híbrida':
            return QdrantHybridPointsSearcher()
        else:
            raise ClassNotImplementedError(
                f"Não há implementação de Buscador de Pontos Vetoriais para o tipo de busca '{self.search_type}'.")

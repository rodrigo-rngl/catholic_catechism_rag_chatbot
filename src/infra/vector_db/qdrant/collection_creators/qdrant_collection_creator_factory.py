from typing import Literal
from src.errors.types.class_not_implemented_error import ClassNotImplementedError
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.collection_creators.qdrant_hybrid_collection_creator import QdrantHybridCollectionCreator

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantCollectionCreatorFactory")


class QdrantCollectionCreatorFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']) -> None:
        self.search_type = search_type

    def produce(self) -> QdrantCollectionCreatorInterface:
        if self.search_type == 'Híbrida':
            return QdrantHybridCollectionCreator()
        else:
            raise ClassNotImplementedError(
                f"Não há implementação de Criador de Coleção para o tipo de busca '{self.search_type}'.")

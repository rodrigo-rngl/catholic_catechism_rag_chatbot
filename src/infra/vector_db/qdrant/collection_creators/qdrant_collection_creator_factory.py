from typing import Literal
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.collection_creators.qdrant_hybrid_collection_creator import QdrantHybridCollectionCreator

class QdrantCollectionCreatorFactory:
    def __init__(self, search_type: Literal['Semântica', 'Esparsa', 'Híbrida']):
        self.search_type = search_type
        
    def produce(self) -> QdrantCollectionCreatorInterface:
        if self.search_type == 'Híbrida':
            return QdrantHybridCollectionCreator()
        else:
            raise TypeError(f"Não há implementação para Criador de Coleção para o tipo de busca '{self.search_type}'.")
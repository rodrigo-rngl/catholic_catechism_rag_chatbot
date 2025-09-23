from typing import List, Any
from abc import ABC, abstractmethod
from src.validators.models.QueryEmbedding import QueryEmbeddingBase
from src.validators.models.SearchOutput import SearchOutput


class QdrantPointsSearcherInterface(ABC):
    @abstractmethod
    def search(self, collection_name: str, embedding: QueryEmbeddingBase) -> List[SearchOutput]:
        pass

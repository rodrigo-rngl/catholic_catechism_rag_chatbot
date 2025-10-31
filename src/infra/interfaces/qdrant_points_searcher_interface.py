from typing import List, Generic
from abc import ABC, abstractmethod
from src.validators.models.QueryEmbedding import QueryEmbeddingType
from src.validators.models.SearchOutput import SearchOutput


class QdrantPointsSearcherInterface(ABC, Generic[QueryEmbeddingType]):
    @abstractmethod
    async def search(self, collection_name: str, embedding: QueryEmbeddingType, top_k: int) -> List[SearchOutput]:
        pass

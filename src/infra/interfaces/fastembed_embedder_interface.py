from abc import ABC, abstractmethod
from typing import List, Generic

from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsType
from src.validators.models.QueryEmbedding import QueryEmbeddingType


class FastembedEmbedderInterface(ABC, Generic[IngestionEmbeddingsType, QueryEmbeddingType]):
    @abstractmethod
    async def embed_ingestion(self, texts: List[str]) -> IngestionEmbeddingsType:
        pass

    @abstractmethod
    async def embed_query(self, query: str) -> QueryEmbeddingType:
        pass

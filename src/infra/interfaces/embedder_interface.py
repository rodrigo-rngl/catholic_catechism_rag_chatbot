from abc import ABC, abstractmethod
from typing import Dict, List

from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase
from src.validators.models.QueryEmbedding import QueryEmbeddingBase


class EmbedderInterface(ABC):
    @abstractmethod
    async def embed_ingestion(self, texts: List[str]) -> IngestionEmbeddingsBase:
        pass

    @abstractmethod
    async def embed_query(self, query: str) -> QueryEmbeddingBase:
        pass

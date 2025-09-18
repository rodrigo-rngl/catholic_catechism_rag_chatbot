from abc import ABC, abstractmethod
from typing import Dict, List

from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase


class EmbedderInterface(ABC):
    @abstractmethod
    def embed_ingestion(self, texts: List[str]) -> IngestionEmbeddingsBase:
        pass

    @abstractmethod
    def embed_query(self, query: str) -> Dict:
        pass

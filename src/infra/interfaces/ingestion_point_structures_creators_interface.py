from typing import List
from abc import ABC, abstractmethod
from src.validators.models.Payload import Payload
from qdrant_client.http.models import PointStruct


class IngestionPointStructuresCreatorsInterface(ABC):
    @abstractmethod
    def create(self, payloads: List[Payload]) -> List[PointStruct]:
        pass

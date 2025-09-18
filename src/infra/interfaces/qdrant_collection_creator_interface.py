from abc import ABC, abstractmethod

class QdrantCollectionCreatorInterface(ABC):
    @abstractmethod
    def create(self, collection_name: str) -> None:
        pass
        
from abc import ABC, abstractmethod


class QdrantCollectionCreatorInterface(ABC):
    @abstractmethod
    async def create(self, collection_name: str) -> None:
        pass

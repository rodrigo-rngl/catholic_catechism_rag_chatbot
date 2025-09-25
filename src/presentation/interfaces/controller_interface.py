from abc import ABC, abstractmethod
from src.validators.models.HttpResponse import HttpResponse
from src.validators.models.Query import QueryOut


class ControllerInterface(ABC):
    @abstractmethod
    async def handle(self, query: QueryOut) -> HttpResponse:
        pass

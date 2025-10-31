from abc import ABC, abstractmethod
from src.validators.models.HttpResponse import HttpResponse
from src.validators.models.HttpRequest import HttpRequestOut


class ControllerInterface(ABC):
    @abstractmethod
    async def handle(self, http_request: HttpRequestOut) -> HttpResponse:
        pass

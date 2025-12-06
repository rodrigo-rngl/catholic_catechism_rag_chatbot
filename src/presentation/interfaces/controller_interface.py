from abc import ABC, abstractmethod
from typing import Generic
from src.validators.models.HttpResponse import HttpResponseType
from src.validators.models.HttpRequest import HttpRequestType


class ControllerInterface(ABC, Generic[HttpRequestType, HttpResponseType]):
    @abstractmethod
    async def handle(self, http_request: HttpRequestType) -> HttpResponseType:
        pass

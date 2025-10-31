from typing import Any, Dict
from src.errors.types.domain_error import DomainError


class ValidationDomainError(DomainError):
    def __init__(self, message: str, body: Dict[str, Any]) -> None:
        super().__init__(message=message, body=body)
        self.name = "Validation Error"
        self.status_code = 400

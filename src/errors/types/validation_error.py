from typing import Sequence


class ValidationError(Exception):
    def __init__(self, message: str, body: Sequence) -> None:
        self.message = message
        self.name = 'Validation Error'
        self.status_code = 422
        self.body = body

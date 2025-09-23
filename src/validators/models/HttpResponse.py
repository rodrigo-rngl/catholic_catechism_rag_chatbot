from typing import Any, Mapping, Sequence
from pydantic import BaseModel


class HttpResponse(BaseModel):
    status_code: int
    body: Mapping[str, Sequence[Mapping[str, Any]]]

from typing import Dict
from pydantic import BaseModel


class Payload(BaseModel):
    id: int
    text: str
    localization: Dict[str, str] | None = None

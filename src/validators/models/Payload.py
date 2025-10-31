from typing import Dict, Any
from pydantic import BaseModel


class Payload(BaseModel):
    text: str
    localization: Dict[str, str] | None = None

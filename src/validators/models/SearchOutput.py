from typing import Mapping, Optional
from pydantic import BaseModel


class SearchOutput(BaseModel):
    text: str
    localization: Optional[Mapping[str, str]] = None
    similarity_score: float

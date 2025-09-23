from typing import Mapping
from pydantic import BaseModel


class SearchOutput(BaseModel):
    text: str
    metadata: Mapping[str, str]

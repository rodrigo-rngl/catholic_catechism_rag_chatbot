from typing import Literal
from pydantic import BaseModel


class HistoryInput(BaseModel):
    role: Literal['assistant', 'user']
    content: str

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
import pendulum


class QueryIn(BaseModel):
    query: str


class QueryOut(QueryIn):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: pendulum.now('America/Sao_Paulo'))

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
import pendulum


class QueryIn(BaseModel):
    query: str = Field(..., min_length=30, max_length=100, description="Questionamento sobre a doutrina da igreja.", examples=[
                       'Quais são os frutos do Espírito Santo?'])


class QueryOut(QueryIn):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: pendulum.now('America/Sao_Paulo'))

from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, ConfigDict, Field


class HttpRequestIn(BaseModel):
    model_config = ConfigDict(
        title="HttpRequest",
        json_schema_extra={
            "example": {
                "query": "Jesus Cristo é verdadeiro Deus e verdadeiro homem?",
                "top_k": 1
            }
        },)
    query: str = Field(title="Texto Consulta",
                       description="Questionamento sobre a doutrina da igreja. Qualquer questionamento requsitado que não corresponde ao contexto da doutrina da Igreja Católica, um erro será retornado.",
                       min_length=8,
                       max_length=880)

    top_k: int = Field(title="Top Parágrafos Retornados",
                       description="Quantidade de parágrafos do catecismo mais similares à Query retornado pela aplicação. Quanto mais parágrafos solicitados, maior a chance de haver parágrafos compatíveis com o questionamento requisitado.",
                       ge=1,
                       le=10)


UTC_MINUS_3 = timezone(timedelta(hours=-3))


class HttpRequestOut(HttpRequestIn):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: datetime.now(tz=UTC_MINUS_3))

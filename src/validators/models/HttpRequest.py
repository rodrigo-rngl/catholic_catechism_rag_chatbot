from typing import Annotated, List, TypeVar, Union
from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, ConfigDict, Field


class HttpRequestInSearch(BaseModel):
    model_config = ConfigDict(
        title="HttpRequestSearch",
        json_schema_extra={
            "example": {
                "query": "Jesus Cristo é verdadeiro Deus e verdadeiro homem?",
                "top_k": 1
            }
        })
    query: str = Field(title="Texto Consulta",
                       description="Questionamento sobre a doutrina da igreja. Qualquer questionamento requsitado que não corresponde ao contexto da doutrina da Igreja Católica, um erro será retornado.",
                       min_length=8,
                       max_length=880)

    top_k: int = Field(title="Top Parágrafos Retornados",
                       description="Quantidade de parágrafos do catecismo mais similares à Query retornado pela aplicação. Quanto mais parágrafos solicitados, maior a chance de haver parágrafos compatíveis com o questionamento requisitado.",
                       ge=1,
                       le=10)


class HttpRequestInRetrieve(BaseModel):
    model_config = ConfigDict(
        title="HttpRequestRetrieve",
        json_schema_extra={
            "example": {
                "paragraph_numbers": [33, 777, 490]
            }
        })

    paragraph_numbers: Annotated[List[Annotated[int, Field(ge=1, le=2865)]], Field(min_length=1, max_length=10)] = Field(
        title="Lista do Número dos Parágrafos",
        description="Lista dos números dos parágrafos do Catecismo a serem retornados pela aplicação. Cada item deve ser inteiro maior igual a 1 e menor ou igual a 2865."
    )


class HttpRequestSearch(HttpRequestInSearch):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone(timedelta(hours=-3))))


class HttpRequestRetrieve(HttpRequestInRetrieve):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone(timedelta(hours=-3))))


class HttpRequestValidationError(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_in: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone(timedelta(hours=-3))))


HttpRequest = Union[HttpRequestSearch,
                    HttpRequestRetrieve,
                    HttpRequestValidationError]

HttpRequestType = TypeVar(
    "HttpRequestType", HttpRequestSearch, HttpRequestRetrieve)

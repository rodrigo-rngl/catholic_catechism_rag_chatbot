from uuid import UUID
from datetime import datetime
from typing import Any, Dict, List, TypeVar, Union
from pydantic import BaseModel, ConfigDict, Field


class HttpResponseBase(BaseModel):
    id: UUID = Field(title="ID", description="ID único da Requisição")
    status_code: int = Field(title="Código do Status da Resposta")
    created_in: datetime = Field(
        title="Criado em", description="Horário em que a requisição foi recebida.")
    took_ms: int = Field(title="Tempo de Resposta", ge=0,
                         description="Tempo de execução em milissegundos.")
    body: Dict[str, List[Dict[str, Any]] | Dict[str, Any]] = Field(
        title="Corpo da Resposta", description="Corpo da Resposta")


class HttpResponseSearch(HttpResponseBase):
    model_config = ConfigDict(title="HttpResponseSearch")

    query: str = Field(title="Texto Consulta",
                       description="Questionamento sobre a doutrina da igreja enviado pela requisição.")
    top_k: int = Field(title="Top Parágrafos Retornados",
                       description="Quantidade de parágrafos do catecismo mais similares à Query retornado pela aplicação.")


HttpResponse = Union[HttpResponseBase,
                     HttpResponseSearch]

HttpResponseType = TypeVar(
    "HttpResponseType", HttpResponseSearch, HttpResponseBase)

from uuid import UUID
from datetime import datetime
from typing import Any, Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class HttpResponse(BaseModel):
    model_config = ConfigDict(title="HttpResponse")
    id: UUID = Field(title="ID", description="ID único da Requisição")
    status_code: int = Field(title="Código do Status da Resposta")
    created_in: datetime = Field(
        title="Criado em", description="Horário em que a requisição foi recebida.")
    took_ms: int = Field(title="Tempo de Resposta", ge=0,
                         description="Tempo de execução em milissegundos.")
    query: str = Field(title="Texto Consulta",
                       description="Questionamento sobre a doutrina da igreja enviado pela requisição.")
    top_k: int = Field(title="Top Parágrafos Retornados",
                       description="Quantidade de parágrafos do catecismo mais similares à Query retornado pela aplicação.")
    body: Mapping[str, Sequence[Mapping[str, Any]] | Mapping[str, Any]] = Field(
        title="Corpo da Resposta", description="Corpo da Resposta")

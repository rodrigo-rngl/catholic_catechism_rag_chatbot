import json
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta
from src.errors.handle_errors import handle_errors
from fastapi.exceptions import RequestValidationError
from src.validators.models.HttpRequest import HttpRequestOut
from src.main.routes.hybrid_search_route import hybrid_search_route
from src.errors.types.validation_domain_error import ValidationDomainError
from src.infra.fastembed_embedder.fastembed_embedder_factory import get_fastembed_hybrid_embedder

load_dotenv()


@asynccontextmanager
async def embedders_inicialization_lifespan(app: FastAPI):
    get_fastembed_hybrid_embedder()
    yield

app = FastAPI(
    title="API RAG do Catecismo da Igreja Católica",
    description="Esta API tem como objetivo recuperar parágrafos do catecismo da Igreja Católica, similares a query enviada. Esta API é essencial para construir aplicações que buscam levar luz ao mundo, ao propagar a doutrina da Santa Igreja.",
    version="1.0.0",
    contact={"name": "Rodrigo Rangel", "email": "rodrigo.rngl@hotmail.com"},
    lifespan=embedders_inicialization_lifespan
)
app.include_router(hybrid_search_route)


@app.exception_handler(RequestValidationError)
async def hybrid_search_request_validation_error_handler(request: Request,
                                                         exc: RequestValidationError) -> JSONResponse:
    raw_body = await request.body()

    payload = {}
    if raw_body:
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {}

    UTC_MINUS_3 = timezone(timedelta(hours=-3))

    http_request = HttpRequestOut.model_construct(id=uuid4(),
                                                  created_in=datetime.now(
                                                      tz=UTC_MINUS_3),
                                                  query=payload.get("query"),
                                                  top_k=payload.get("top_k"))

    validation_error = ValidationDomainError(message="Erro de validação no corpo da requisição.",
                                             body={"error": exc.errors()})

    http_response = handle_errors(
        http_request=http_request,
        error=validation_error
    )

    return JSONResponse(status_code=http_response.status_code,
                        content=http_response.model_dump(mode="json"))

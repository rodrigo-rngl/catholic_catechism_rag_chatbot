from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from src.main.routes.hybrid_search_route import hybrid_search_route
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

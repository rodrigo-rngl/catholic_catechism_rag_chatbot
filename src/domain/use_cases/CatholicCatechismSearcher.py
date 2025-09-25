from typing import Any, List, Dict
from src.errors.types.bad_query_error import BadQueryError
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.validators.models.QueryEmbedding import QueryEmbeddingBase
from src.validators.models.SearchOutput import SearchOutput


class CatholicCatechismSearcher:
    def __init__(self, embedder: EmbedderInterface,
                 repository: QdrantVectorDBRepository) -> None:
        self.repository = repository
        self.embedder = embedder

    async def search(self, query: str) -> List[Dict[str, Any]]:
        if query is None:
            raise BadQueryError(f'A query não pode estar vazia.')
        if not isinstance(query, str):
            raise BadQueryError(f'A query deve ser do tipo string.')

        query_embedding: QueryEmbeddingBase = await self.embedder.embed_query(
            query=query)

        search_outputs: List[SearchOutput] = await self.repository.search_points(
            embedding=query_embedding)

        return [output.model_dump() for output in search_outputs]

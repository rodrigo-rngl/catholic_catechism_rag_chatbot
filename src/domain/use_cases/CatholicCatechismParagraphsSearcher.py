from typing import List
from src.validators.models.SearchOutput import SearchOutput
from src.domain.services.query_validator import QueryValidator
from src.validators.models.QueryEmbedding import QueryEmbeddingBase
from src.infra.interfaces.fastembed_embedder_interface import FastembedEmbedderInterface
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.validators.models.SearchPipelineResult import SearchClarification
from src.validators.models.SearchPipelineResult import SearchSuccess
from src.validators.models.SearchPipelineResult import SearchPipelineResult

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatholicCatechismParagraphsSearcher")


class CatholicCatechismParagraphsSearcher:
    def __init__(self,
                 embedder: FastembedEmbedderInterface,
                 repository: QdrantVectorDBRepository) -> None:
        self.repository = repository
        self.embedder = embedder

    async def search(self, query: str, top_k: int) -> SearchPipelineResult:
        logger.info(
            "Iniciando busca de parágrafos do catecismo da Igreja Católica...")
        query_validation = await QueryValidator().validate(query=query)

        if query_validation.action == "ask_clarifying":
            return SearchClarification(query_validation=query_validation)

        query_embedding: QueryEmbeddingBase = await self.embedder.embed_query(
            query=query)

        search_outputs: List[SearchOutput] = await self.repository.search_points(
            embedding=query_embedding, top_k=top_k)

        return SearchSuccess(search_outputs=search_outputs, query_validation=query_validation)

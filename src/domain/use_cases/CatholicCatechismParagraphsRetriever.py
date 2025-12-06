from typing import List
from src.validators.models.RetrieveSucess import RetrieveSuccess
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatholicCatechismParagraphsRetriever")


class CatholicCatechismParagraphsRetriever:
    def __init__(self, repository: QdrantVectorDBRepository) -> None:
        self.repository = repository

    async def retrieve(self, paragraph_numbers: List[int]) -> RetrieveSuccess:
        logger.info(
            "Iniciando recuperação de parágrafos do catecismo da Igreja Católica...")

        retrieve_output = await self.repository.retrieve_points(paragraph_numbers=paragraph_numbers)

        return RetrieveSuccess(retrieve_output=retrieve_output)

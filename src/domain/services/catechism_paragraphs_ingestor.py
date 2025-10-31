import asyncio
from typing import List
from src.validators.models.Payload import Payload
from qdrant_client.http.models import PointStruct
from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase
from src.infra.interfaces.fastembed_embedder_interface import FastembedEmbedderInterface
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.infra.vector_db.qdrant.ingestion_point_structures_creators.ingestion_point_structures_creators_factory import IngestionPointStructuresCreatorsFactory

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatechismIngestor")


class CatechismParagraphsIngestor:
    def __init__(self,
                 embedder: FastembedEmbedderInterface,
                 repository: QdrantVectorDBRepository) -> None:
        self.embedder = embedder
        self.repository = repository
        self.__batch_semaphore = asyncio.Semaphore(2)
        self.__batch_position = 0

    async def ingest(self, payloads: List[Payload], batch_size: int) -> None:
        n_batches = (len(payloads) + batch_size - 1) // batch_size
        logger.info(
            f"Iniciando a ingestão de {len(payloads)} payloads em {n_batches} batches...")

        tasks = [
            self.__process_batch(payloads[i:i+batch_size])
            for i in range(0, len(payloads), batch_size)
        ]

        await asyncio.gather(*tasks, return_exceptions=False)

        await self.repository.get_collection_points_count()

    async def __process_batch(self, payloads: List[Payload]) -> None:
        async with self.__batch_semaphore:
            self.__batch_position += 1
            batch_position = self.__batch_position
            logger.info(
                f"Enviando {len(payloads)} parágrafos no {batch_position}º batch...")

            texts = [payload.text for payload in payloads]

            embeddings: IngestionEmbeddingsBase = await self.embedder.embed_ingestion(
                texts=texts)

            ingestion_point_structures_creator = IngestionPointStructuresCreatorsFactory(
                embeddings=embeddings).produce()
            ingestion_points: List[PointStruct] = ingestion_point_structures_creator.create(
                payloads=payloads)

            await self.repository.upsert_points(ingestion_points=ingestion_points)

            logger.info(
                f"{len(payloads)} parágrafos do {batch_position}º foram transformados com sucesso!")

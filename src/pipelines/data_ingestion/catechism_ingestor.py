from typing import List, Dict, Any
from qdrant_client.http.models import PointStruct
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.pipelines.data_ingestion.ingestion_point_structures_creators import IngestionPointStructuresCreatorsFactory

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatechismIngestor")


class CatechismIngestor:
    def __init__(self,
                 embedder: EmbedderInterface,
                 repository: QdrantVectorDBRepository) -> None:
        self.embedder = embedder
        self.repository = repository

        self.batch_position = 0
        self.n_paragraphs_sent = 0

    def ingest(self, payloads: List[Dict[str, Any]], batch_size: int) -> None:
        n_batches = (len(payloads) + batch_size - 1) // batch_size
        logger.info(
            f"Iniciando a ingestão de {len(payloads)} payloads em {n_batches} batches...")

        for i in range(0, len(payloads), batch_size):
            batch_payloads = payloads[i:i + batch_size]

            self.batch_position += 1
            logger.info(
                f"Enviando {len(batch_payloads)} parágrafos no {self.batch_position}º batch...")

            texts = [payload['text'] for payload in batch_payloads]

            embeddings: IngestionEmbeddingsBase = self.embedder.embed_ingestion(
                texts=texts)

            ingestion_point_structures_creator = IngestionPointStructuresCreatorsFactory(
                embeddings=embeddings).produce()
            ingestion_points: List[PointStruct] = ingestion_point_structures_creator.create(
                payloads=batch_payloads)

            self.repository.upsert_points(ingestion_points=ingestion_points)

            self.n_paragraphs_sent += batch_size
            logger.info(
                f"{self.n_paragraphs_sent}/{len(payloads)} parágrafos transformados com sucesso!")

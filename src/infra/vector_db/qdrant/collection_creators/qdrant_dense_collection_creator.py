from qdrant_client.http.models import VectorParams, Distance
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantDenseCollectionCreator")


class QdrantDenseCollectionCreator(QdrantCollectionCreatorInterface):
    async def create(self, collection_name: str) -> None:
        async with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                logger.info(f"Criando a coleção '{collection_name}'...")
                await qdrant.client.create_collection(
                    collection_name=collection_name,
                    vectors_config={
                        "dense": VectorParams(size=768, distance=Distance.COSINE)}
                )

                logger.info(
                    f"A coleção '{collection_name}' foi criada com sucesso.")

            except Exception as exception:
                logger.exception(f"Exceção ao criar a coleção híbrida no Qdrant."
                                 f"Exception: {exception}.")
                raise

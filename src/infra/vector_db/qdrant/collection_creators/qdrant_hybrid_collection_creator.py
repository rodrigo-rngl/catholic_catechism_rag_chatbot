from qdrant_client import models
from qdrant_client.http.models import VectorParams, Distance
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name= "CollectionCreator")

class QdrantHybridCollectionCreator(QdrantCollectionCreatorInterface):
    def create(self, collection_name: str) -> None:
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                logger.info(f"Criando a coleção '{collection_name}'...")
                qdrant.client.create_collection(
                    collection_name= collection_name,
                    vectors_config={
                        "dense": VectorParams(size= 768, distance= Distance.COSINE),
                        "colbertv2.0": VectorParams(
                            size=128,
                            distance= Distance.COSINE,
                            multivector_config= models.MultiVectorConfig(
                                comparator= models.MultiVectorComparator.MAX_SIM,
                            ),
                        ),
                    },
                    sparse_vectors_config={
                        "sparse": models.SparseVectorParams(modifier= models.Modifier.IDF),
                    },
                )
                logger.info(f"A coleção '{collection_name}' foi criada com sucesso.")
            except Exception as error:
                logger.error(f"Ocorreu uma falha ao criar a coleção híbrida no Qdrant."
                            f"Error Message: {error}.")
                raise
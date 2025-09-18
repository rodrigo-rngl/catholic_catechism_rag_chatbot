from typing import List, Dict
from qdrant_client.http.models import PointStruct, Prefetch
from src.validators.models.SearchOutput import SearchOutput
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantVectorDBRepository")


class QdrantVectorDBRepository:
    def __init__(self, collection_name: str, collection_creator: QdrantCollectionCreatorInterface):
        self.collection_name = collection_name
        self.collection_creator = collection_creator

    def create_collection(self) -> None:
        if self.__collection_already_exist() and self.__collection_already_populated():
            logger.info(
                f"A coleção '{self.collection_name}' já existe existe e já possui dados. "
                f"Ela será excluída e criada novamente.")
            self.__delete_collection()
            self.collection_creator.create(
                collection_name=self.collection_name)
        elif not self.__collection_already_exist():
            self.collection_creator.create(
                collection_name=self.collection_name)

    def upsert_data(self, ingestion_points: List[PointStruct]):
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                logger.info(
                    f"  Enviando {len(ingestion_points)} estruturas de pontos de ingestão para '{self.collection_name}'...")

                qdrant.client.upsert(
                    collection_name=self.collection_name, points=ingestion_points)

                logger.info(
                    "  As estruturas de pontos de ingestão foram enviados com sucesso!")

                collection_info = qdrant.client.get_collection(
                    self.collection_name)
                logger.info(
                    f"A coleção '{self.collection_name}' agora possui {collection_info.points_count} parágrafos.")

            except Exception as error:
                logger.error(f"Erro ao inserir as estruturas de pontos de ingestão na coleção '{self.collection_name}'.\n"
                             f"Error Message: {error}")
                raise

    def hybrid_data_search(self, collection_name: str, prefetch_limit: int, embeddings: Dict, top_k: int = 5):
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                search_result = qdrant.client.query_points(
                    collection_name=collection_name,
                    prefetch=[
                        Prefetch(
                            query=embeddings['dense'],
                            using="dense",
                            limit=prefetch_limit,
                        ),
                        Prefetch(
                            query=embeddings['sparse'].model_dump(),
                            using="sparse",
                            limit=prefetch_limit,
                        ),
                    ],
                    query=embeddings['late'],
                    using="colbertv2.0",
                    with_payload=True,
                    limit=top_k,
                )

                search_outputs_list = [SearchOutput(
                    text=point.payload['text'],
                    metadata=point.payload['metadata']
                ) for point in search_result.points if point.payload != None]

                return [output.model_dump() for output in search_outputs_list]

            except Exception as error:
                logger.error(f"Erro ao realizar busca híbrida na coleção {collection_name}.\n"
                             f"Error Message: {error}")
                raise

    def __collection_already_exist(self) -> bool:
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                return qdrant.client.collection_exists(collection_name=self.collection_name)
            except Exception as error:
                logger.info(f"Ocorreu uma falha ao verificar se a coleção '{self.collection_name}' no Qdrant existe.\n"
                            f"Error Message: {error}.")
                raise

    def __collection_already_populated(self) -> bool:
        if self.__collection_already_exist():
            with QdrantVectorDBConnectionHandler() as qdrant:
                try:
                    return int(qdrant.client.count(collection_name=self.collection_name).count) > 0
                except Exception as error:
                    logger.info(f"Ocorreu uma falha ao verificar se a coleção '{self.collection_name}' no Qdrant já está populada.\n"
                                f"Error Message: {error}.")
                    raise
        return False

    def __delete_collection(self) -> None:
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                qdrant.client.delete_collection(
                    collection_name=self.collection_name)
                logger.info(
                    f"A coleção '{self.collection_name}' foi excluída com sucesso.")
            except Exception as error:
                logger.error(f"Ocorreu uma falha ao excluir a coleção '{self.collection_name}' do Qdrant.\n"
                             f"Error Message: {error}.")
                raise

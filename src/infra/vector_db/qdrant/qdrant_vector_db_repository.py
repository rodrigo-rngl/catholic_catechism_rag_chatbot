from typing import List
from qdrant_client.http.models import PointStruct
from src.validators.models.SearchOutput import SearchOutput
from src.validators.models.QueryEmbedding import QueryEmbeddingBase
from src.errors.types.collection_not_found_error import CollectionNotFoundError
from src.errors.types.points_searcher_not_found_error import PointsSearcherNotFoundError
from src.errors.types.collection_creator_not_found_error import CollectionCreatorNotFoundError
from src.infra.interfaces.qdrant_points_searcher_interface import QdrantPointsSearcherInterface
from src.infra.interfaces.qdrant_collection_creator_interface import QdrantCollectionCreatorInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantVectorDBRepository")


class QdrantVectorDBRepository:
    def __init__(self, collection_name: str, collection_creator: QdrantCollectionCreatorInterface | None = None,
                 points_searcher: QdrantPointsSearcherInterface | None = None) -> None:
        self.collection_name = collection_name
        self.collection_creator = collection_creator
        self.points_searcher = points_searcher

    def create_collection(self) -> None:
        if self.collection_creator is None:
            raise CollectionCreatorNotFoundError(
                f"O criador de coleção não foi passado. O criador de coleção não pode ser None.")

        if self.__collection_already_exist() and self.__collection_already_populated():
            logger.info(
                f"A coleção '{self.collection_name}' já existe existe e já possui dados."
                f"Ela será excluída e criada novamente.")
            self.__delete_collection()
            self.collection_creator.create(
                collection_name=self.collection_name)
        elif not self.__collection_already_exist():
            self.collection_creator.create(
                collection_name=self.collection_name)

    def upsert_points(self, ingestion_points: List[PointStruct]) -> None:
        if not self.__collection_already_exist():
            raise CollectionNotFoundError(
                f"A coleção '{self.collection_name}' não existe para que estruras de pontos possam ser armazenadas.")

        with QdrantVectorDBConnectionHandler() as qdrant:
            logger.info(
                f"  Enviando {len(ingestion_points)} estruturas de pontos de ingestão para '{self.collection_name}'...")
            try:
                qdrant.client.upsert(
                    collection_name=self.collection_name, points=ingestion_points)

                logger.info(
                    "  As estruturas de pontos de ingestão foram enviados com sucesso!")
            except Exception as exception:
                logger.exception(f"Exceção ao inserir as estruturas de pontos de ingestão na coleção '{self.collection_name}'.\n"
                                 f"Exception: {exception}")
                raise

            try:
                collection_info = qdrant.client.get_collection(
                    self.collection_name)
                logger.info(
                    f"A coleção '{self.collection_name}' agora possui {collection_info.points_count} parágrafos.")
            except Exception as exception:
                logger.exception(f"Exceção ao obter informações sobre a coleção '{self.collection_name}'.\n"
                                 f"Exception: {exception}")
                raise

    def search_points(self, embedding: QueryEmbeddingBase) -> List[SearchOutput]:
        if self.points_searcher is None:
            raise PointsSearcherNotFoundError(
                f"O buscador de pontos de vetoriais não foi passado. O buscador não pode ser None.")

        if not self.__collection_already_populated():
            raise CollectionNotFoundError(
                f"A coleção '{self.collection_name}' não existe! Assim, não há com realizar a busca de pontos vetoriais.")

        search_outputs: List[SearchOutput] = self.points_searcher.search(
            collection_name=self.collection_name,
            embedding=embedding)

        return search_outputs

    def __collection_already_exist(self) -> bool:
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                return qdrant.client.collection_exists(collection_name=self.collection_name)
            except Exception as exception:
                logger.exception(f"Ocorreu uma falha ao verificar se a coleção '{self.collection_name}' no Qdrant existe.\n"
                                 f"Exception: {exception}.")
                raise

    def __collection_already_populated(self) -> bool:
        if not self.__collection_already_exist():
            raise CollectionNotFoundError(
                f"A coleção '{self.collection_name}' não existe! Com isso, não dá para checar se a mesma está populada.")

        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                return int(qdrant.client.count(collection_name=self.collection_name).count) > 0
            except Exception as exception:
                logger.exception(f"Ocorreu uma falha ao verificar se a coleção '{self.collection_name}' no Qdrant já está populada.\n"
                                 f"Exception: {exception}.")
                raise

    def __delete_collection(self) -> None:
        with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                qdrant.client.delete_collection(
                    collection_name=self.collection_name)
                logger.info(
                    f"A coleção '{self.collection_name}' foi excluída com sucesso.")
            except Exception as exception:
                logger.exception(f"Ocorreu uma falha ao excluir a coleção '{self.collection_name}' do Qdrant.\n"
                                 f"Exception: {exception}.")
                raise

from typing import List
from qdrant_client.http.models import QueryResponse
from src.validators.models.SearchOutput import SearchOutput
from src.validators.models.QueryEmbedding import QueryDenseEmbedding
from src.infra.interfaces.qdrant_points_searcher_interface import QdrantPointsSearcherInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantDensePointsSearcher")


class QdrantDensePointsSearcher(QdrantPointsSearcherInterface[QueryDenseEmbedding]):
    async def search(self, collection_name: str, embedding: QueryDenseEmbedding, top_k: int) -> List[SearchOutput]:
        async with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                search_result = await qdrant.client.query_points(
                    collection_name=collection_name,
                    query=embedding.dense,
                    using="dense",
                    limit=top_k
                )

            except Exception as exception:
                logger.exception(f"Exceção ao realizar busca semântica na coleção {collection_name}.\n"
                                 f"Exception: {exception}")
                raise

            return self.__create_search_outputs(search_result)

    @classmethod
    def __create_search_outputs(cls, search_result: QueryResponse) -> List[SearchOutput]:
        search_outputs_list = [SearchOutput(
            text=point.payload['text'],
            similarity_score=point.score
        ) for point in search_result.points if point.payload != None]

        return search_outputs_list

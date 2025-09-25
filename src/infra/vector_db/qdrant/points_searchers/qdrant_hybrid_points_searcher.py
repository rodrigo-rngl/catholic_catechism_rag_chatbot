from typing import List
from qdrant_client.http.models import Prefetch
from src.validators.models.SearchOutput import SearchOutput
from src.validators.models.QueryEmbedding import QueryEmbeddingBase, SparseDict
from src.infra.interfaces.qdrant_points_searcher_interface import QdrantPointsSearcherInterface
from src.infra.vector_db.qdrant.settings.qdrant_vector_db_connection_handler import QdrantVectorDBConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantHybridPointsSearcher")


class QdrantHybridPointsSearcher(QdrantPointsSearcherInterface):
    async def search(self, collection_name: str, embedding: QueryEmbeddingBase) -> List[SearchOutput]:
        async with QdrantVectorDBConnectionHandler() as qdrant:
            try:
                search_result = await qdrant.client.query_points(
                    collection_name=collection_name,
                    prefetch=[
                        Prefetch(
                            query=embedding.dense,
                            using="dense",
                            limit=20,
                        ),
                        Prefetch(
                            query=embedding.sparse.model_dump(),
                            using="sparse",
                            limit=20,
                        ),
                    ],
                    query=embedding.late,
                    using="colbertv2.0",
                    with_payload=True,
                    limit=5,
                )

                search_outputs_list = [SearchOutput(
                    text=point.payload['text'],
                    metadata=point.payload['metadata']
                ) for point in search_result.points if point.payload != None]

                return search_outputs_list

            except Exception as exception:
                logger.exception(f"Exceção ao realizar busca híbrida na coleção {collection_name}.\n"
                                 f"Exception: {exception}")
                raise

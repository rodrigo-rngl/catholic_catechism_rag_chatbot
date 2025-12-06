import os
from qdrant_client import AsyncQdrantClient

from src.config.logger_config import setup_logger
logger = setup_logger(name="QdrantVectorDBConnectionHandler")


class QdrantVectorDBConnectionHandler:
    def __init__(self) -> None:
        self.__url = os.getenv("QDRANT_URL")
        self.__api_key = os.getenv("QDRANT_API_KEY")

        self.client = self.__create_db_client()

    def __create_db_client(self) -> AsyncQdrantClient:
        try:
            return AsyncQdrantClient(
                url=self.__url,
                api_key=self.__api_key,
                prefer_grpc=True,
                timeout=60
            )
        except Exception as exception:
            logger.error(f'Exceção ao gerar conexão com banco de dados vetorial Qdrant.\n'
                         f'Exception: {exception}')
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

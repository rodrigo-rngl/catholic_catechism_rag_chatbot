from typing import List, Any
from fastembed import TextEmbedding
from src.validators.models.QueryEmbedding import QueryDenseEmbedding
from src.validators.models.IngestionEmbeddings import IngestionDenseEmbeddings
from src.infra.interfaces.fastembed_embedder_interface import FastembedEmbedderInterface


import asyncio

from src.config.logger_config import setup_logger
logger = setup_logger(name="FastembedDenseEmbedder")


class FastembedDenseEmbedder(FastembedEmbedderInterface[IngestionDenseEmbeddings, QueryDenseEmbedding]):
    def __init__(self) -> None:
        self.embedding_models = self.__initialize_embedding_models()

    async def embed_ingestion(self, texts: List[str]) -> IngestionDenseEmbeddings:
        logger.info(
            f"       Transformando {len(texts)} parágrafos em embeddings...")

        dense_vecs = await asyncio.to_thread(self.generate_dense_embedding, texts)

        logger.info(f'       Embeddings criados com sucesso!')
        return IngestionDenseEmbeddings(
            dense=dense_vecs
        )

    async def embed_query(self, query: str) -> QueryDenseEmbedding:
        logger.info(
            f"    Transformando query em embeddings...")

        dense_vec = await asyncio.to_thread(self.generate_dense_embedding, query)

        logger.info(f'    Embeddings criados com sucesso!')
        return QueryDenseEmbedding(
            dense=dense_vec)

    @classmethod
    def __initialize_embedding_models(cls) -> TextEmbedding:
        logger.info(
            f'Inicializando modelos de Embeddings para Busca Híbrida...')

        logger.info(f'Inicializando o Dense Embedding...')
        dense_embedding_model = TextEmbedding(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        logger.info(f'O Dense Embedding foi inicializado com sucesso!')

        return dense_embedding_model

    def generate_dense_embedding(self, texts: str | List[str]) -> List[Any]:
        dense_model = self.embedding_models

        try:
            dense_embedding = dense_model.embed(texts)
        except Exception as exception:
            exception_message = 'Exceção ao gerar Dense Embedding'
            if isinstance(texts, list):
                exception_message = 'Exceção ao gerar Dense Embeddings'

            logger.exception(f'{exception_message}.\n'
                             f'Exception: {exception}')
            raise

        if isinstance(texts, str):
            return next(iter(dense_embedding)).tolist()
        if isinstance(texts, list):
            return [vector.tolist() for vector in dense_embedding]

        raise TypeError(
            "O tipo de 'texts' não é válido.")

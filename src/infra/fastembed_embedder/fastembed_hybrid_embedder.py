from fastembed import TextEmbedding
from typing import Tuple, List, Any
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.validators.models.QueryEmbedding import QueryHybridEmbedding
from src.validators.models.QueryEmbedding import SparseDict as QuerySparseDict
from src.validators.models.IngestionEmbeddings import IngestionHybridEmbeddings
from src.validators.models.IngestionEmbeddings import SparseDict as IngestionSparseDict
import numpy as np

import asyncio

from src.config.logger_config import setup_logger
logger = setup_logger(name="FastembedHybridEmbedder")


class FastembedHybridEmbedder(EmbedderInterface):
    def __init__(self) -> None:
        self.embedding_models = self.__initialize_embedding_models()

    async def embed_ingestion(self, texts: List[str]) -> IngestionHybridEmbeddings:
        logger.info(
            f"  Transformando {len(texts)} parágrafos em embeddings...")

        dense_task = asyncio.to_thread(self.generate_dense_embedding, texts)
        sparse_task = asyncio.to_thread(self.generate_sparse_embedding, texts)
        late_task = asyncio.to_thread(self.generate_late_embedding, texts)

        dense_vecs, sparse_dicts, late_mats = await asyncio.gather(
            dense_task, sparse_task, late_task
        )

        logger.info(f'  Embeddings criados com sucesso!')
        return IngestionHybridEmbeddings(
            dense=dense_vecs,
            sparse=sparse_dicts,
            late=late_mats
        )

    async def embed_query(self, query: str) -> QueryHybridEmbedding:
        logger.info(
            f"  Transformando query em embeddings...")

        dense_task = asyncio.to_thread(self.generate_dense_embedding, query)
        sparse_task = asyncio.to_thread(self.generate_sparse_embedding, query)
        late_task = asyncio.to_thread(self.generate_late_embedding, query)

        dense_vec, sparse_dict, late_mat = await asyncio.gather(
            dense_task, sparse_task, late_task
        )

        logger.info(f'  Embeddings criados com sucesso!')
        return QueryHybridEmbedding(
            dense=dense_vec,
            sparse=sparse_dict,
            late=late_mat
        )

    @classmethod
    def __initialize_embedding_models(cls) -> Tuple[TextEmbedding, Bm25, LateInteractionTextEmbedding]:
        logger.info(
            f'Inicializando modelos de Embeddings para Busca Híbrida...')

        logger.info(f'Inicializando o Dense Embedding...')
        dense_embedding_model = TextEmbedding(
            "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        logger.info(f'O Dense Embedding foi inicializado com sucesso!')

        logger.info(f'Inicializando o Sparse Embedding...')
        sparse_embedding_model = Bm25("Qdrant/bm25")
        logger.info(f'O Sparse Embedding foi inicializado com sucesso!')

        logger.info(f'Inicializando o Late Interaction Embedding...')
        late_embedding_model = LateInteractionTextEmbedding(
            "colbert-ir/colbertv2.0")
        logger.info(
            f'O Late Interaction Embedding foi inicializado com sucesso!')

        return dense_embedding_model, sparse_embedding_model, late_embedding_model

    def generate_dense_embedding(self, texts: str | List[str]) -> List[Any]:
        dense_model, _, _ = self.embedding_models

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

    def generate_sparse_embedding(self, texts: str | List[str]) -> Any:
        _, sparse_model, _ = self.embedding_models

        try:
            sparse_embedding = sparse_model.embed(texts)
        except Exception as exception:
            exception_message = 'Exceção ao gerar Sparse Embedding'
            if isinstance(texts, list):
                exception_message = 'Exceção ao gerar Sparse Embeddings'

            logger.exception(f'{exception_message}.\n'
                             f'Exception: {exception}')
            raise

        if isinstance(texts, str):
            sparse_dict_raw: dict[str, np.ndarray] = next(
                iter(sparse_embedding)).as_object()
            sparse_dict = {k: v.tolist() for k, v in sparse_dict_raw.items()}
            return QuerySparseDict(indices=sparse_dict['indices'], values=sparse_dict["values"])

        if isinstance(texts, list):
            sparse_dicts_raw = [dictionary.as_object()
                                for dictionary in sparse_embedding]
            sparse_dicts = []
            for dictionary in sparse_dicts_raw:
                sparse_dict = {k: v.tolist() for k, v in dictionary.items()}
                sparse_dicts.append(IngestionSparseDict(
                    indices=sparse_dict['indices'], values=sparse_dict["values"]))
            return sparse_dicts

        raise TypeError(
            "O tipo de 'texts' não é válido.")

    def generate_late_embedding(self, texts: str | List[str]) -> List[List[Any]]:
        _, _, late_model = self.embedding_models

        try:
            late_embedding = late_model.embed(texts)
        except Exception as exception:
            exception_message = 'Exceção ao gerar Late Embedding'
            if isinstance(texts, list):
                exception_message = 'Exceção ao gerar Late Embeddings'

            logger.exception(f'{exception_message}.\n'
                             f'Exception: {exception}')
            raise

        if isinstance(texts, str):
            return next(iter(late_embedding)).tolist()
        if isinstance(texts, list):
            return [matrix.tolist() for matrix in late_embedding]

        raise TypeError(
            "O tipo de 'texts' não é válido.")

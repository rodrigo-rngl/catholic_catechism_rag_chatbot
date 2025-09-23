from fastembed import TextEmbedding
from typing import Tuple, List, Dict
from fastembed.sparse.bm25 import Bm25
from fastembed.late_interaction import LateInteractionTextEmbedding
from src.infra.interfaces.embedder_interface import EmbedderInterface
from src.validators.models.QueryEmbedding import QueryHybridEmbedding
from src.validators.models.IngestionEmbeddings import IngestionHybridEmbeddings
import numpy as np

from src.config.logger_config import setup_logger
logger = setup_logger(name="FastembedHybridEmbedder")


class FastembedHybridEmbedder(EmbedderInterface):
    def __init__(self) -> None:
        self.embedding_models = self.__initialize_embedding_models()

    def embed_ingestion(self, texts: List[str]) -> IngestionHybridEmbeddings:
        logger.info(
            f"  Transformando {len(texts)} parágrafos em embeddings...")

        dense_model, sparse_model, late_model = self.embedding_models

        try:
            dense_embedding = dense_model.embed(texts)
            sparse_embedding = sparse_model.embed(texts)
            late_embedding = late_model.embed(texts)

            dense_vecs = [vector.tolist() for vector in dense_embedding]
            late_mats = [matrix.tolist() for matrix in late_embedding]
            sparse_dicts_raw = [dictionary.as_object()
                                for dictionary in sparse_embedding]
            sparse_dicts = []
            for dictionary in sparse_dicts_raw:
                sparse_dicts.append({k: v.tolist()}
                                    for k, v in dictionary.items())

            logger.info(f'  Embeddings criados com sucesso!')
            return IngestionHybridEmbeddings(
                dense=dense_vecs,
                sparse=sparse_dicts,
                late=late_mats
            )
        except Exception as exception:
            logger.exception(f'Exceção ao gerar embeddings dos dados para ingestão.\n'
                             f'Exception: {exception}')
            raise

    def embed_query(self, query: str) -> QueryHybridEmbedding:
        dense_model, sparse_model, late_model = self.embedding_models

        try:
            dense_embedding = dense_model.embed(query)
            sparse_embedding = sparse_model.embed(query)
            late_embedding = late_model.embed(query)

            dense_vec = next(iter(dense_embedding)).tolist()
            late_mat = next(iter(late_embedding)).tolist()

            sparse_dict_raw: dict[str, np.ndarray] = next(
                iter(sparse_embedding)).as_object()
            sparse_dict: dict[str, list[float]] = {
                k: v.tolist() for k, v in sparse_dict_raw.items()}

            return QueryHybridEmbedding(
                dense=dense_vec,
                sparse=sparse_dict,
                late=late_mat
            )
        except Exception as exception:
            logger.exception(f'Exceção ao gerar embedding da query para busca híbrida.\n'
                             f'Exception: {exception}')
            raise

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

import uuid
from typing import List, Dict
from abc import ABC, abstractmethod
from qdrant_client.http.models import PointStruct, SparseVector
from src.errors.types.class_not_implemented_error import ClassNotImplementedError
from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase
from src.validators.models.IngestionEmbeddings import IngestionHybridEmbeddings

from src.config.logger_config import setup_logger
logger = setup_logger(name="IngestionPointStructuresCreators")


class IngestionPointStructuresCreatorsInterface(ABC):
    @abstractmethod
    def create(self, payloads: List[Dict]) -> List[PointStruct]:
        pass


class HybridIngestionPointStructuresCreator(IngestionPointStructuresCreatorsInterface):
    def __init__(self, embeddings: IngestionEmbeddingsBase) -> None:
        self.embeddings = embeddings

    def create(self, payloads: List[Dict[str, str | Dict]]) -> List[PointStruct]:
        logger.info(
            f'  Transformando {len(payloads)} payloads e embeddings em estruturas de pontos para ingestão...')

        texts = [payload['text'] for payload in payloads]
        metadatas = [payload['metadata'] for payload in payloads]

        ingestion_points_list = []

        for (dense, sparse, late), text, meta in zip(self.embeddings.iter_components(), texts, metadatas):
            if sparse and dense and late:
                try:
                    point = PointStruct(
                        id=str(uuid.uuid4()),
                        vector={
                            "dense": dense,
                            "colbertv2.0": late,
                            "sparse": SparseVector(indices=sparse.indices,
                                                   values=sparse.values)
                        },
                        payload={"text": text, "metadata": meta}
                    )

                    ingestion_points_list.append(point)

                except Exception as exception:
                    logger.exception(f'Exceção ao criar um estrutura de ponto de ingestão.\n'
                                     f'Exception: {exception}')
                    raise

        logger.info(
            '  Estruturas de pontos para ingestão criadas com sucesso!')

        return ingestion_points_list


class IngestionPointStructuresCreatorsFactory:
    def __init__(self, embeddings: IngestionEmbeddingsBase) -> None:
        self.embeddings = embeddings

    def produce(self) -> IngestionPointStructuresCreatorsInterface:
        if isinstance(self.embeddings, IngestionHybridEmbeddings):
            return HybridIngestionPointStructuresCreator(embeddings=self.embeddings)
        else:
            raise ClassNotImplementedError(
                'Não há implementação para o tipo de IngestorEmbeddigs fornecido.')

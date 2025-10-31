import uuid
from typing import List
from src.validators.models.Payload import Payload
from qdrant_client.http.models import PointStruct, SparseVector
from src.validators.models.IngestionEmbeddings import IngestionHybridEmbeddings
from src.infra.interfaces.ingestion_point_structures_creators_interface import IngestionPointStructuresCreatorsInterface

from src.config.logger_config import setup_logger

logger = setup_logger(name="HybridIngestionPointStructuresCreators")


class HybridIngestionPointStructuresCreator(IngestionPointStructuresCreatorsInterface):
    def __init__(self, embeddings: IngestionHybridEmbeddings) -> None:
        self.embeddings = embeddings

    def create(self, payloads: List[Payload]) -> List[PointStruct]:
        logger.info(
            f'  Transformando {len(payloads)} payloads e embeddings em estruturas de pontos para ingestão...')

        texts = [payload.text for payload in payloads]
        localizations = [payload.localization for payload in payloads]

        ingestion_points_list = []

        for (dense, sparse, late), text, localization in zip(self.embeddings.iter_components(), texts, localizations):
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
                        payload={"text": text, "localization": localization}
                    )

                    ingestion_points_list.append(point)

                except Exception as exception:
                    logger.exception(f'Exceção ao criar um estrutura de ponto de ingestão.\n'
                                     f'Exception: {exception}')
                    raise

        logger.info(
            '  Estruturas de pontos para ingestão criadas com sucesso!')

        return ingestion_points_list

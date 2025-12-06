import uuid
from typing import List
from qdrant_client.http.models import PointStruct
from src.validators.models.Payload import Payload
from src.validators.models.IngestionEmbeddings import IngestionDenseEmbeddings
from src.infra.interfaces.ingestion_point_structures_creators_interface import IngestionPointStructuresCreatorsInterface

from src.config.logger_config import setup_logger
logger = setup_logger(name="DenseIngestionPointStructuresCreators")


class DenseIngestionPointStructuresCreator(IngestionPointStructuresCreatorsInterface):
    def __init__(self, embeddings: IngestionDenseEmbeddings) -> None:
        self.embeddings = embeddings

    def create(self, payloads: List[Payload]) -> List[PointStruct]:
        logger.info(
            f'  Transformando {len(payloads)} payloads e embeddings em estruturas de pontos para ingestão...')

        ingestion_points_list = []

        for (dense, sparse, late), payload in zip(self.embeddings.iter_components(), payloads):
            if dense:
                try:
                    point = PointStruct(
                        id=payload.id,
                        vector={
                            "dense": dense
                        },
                        payload={"text": payload.text,
                                 "localization": payload.localization}
                    )

                    ingestion_points_list.append(point)

                except Exception as exception:
                    logger.exception(f'Exceção ao criar um estrutura de ponto de ingestão.\n'
                                     f'Exception: {exception}')
                    raise

        logger.info(
            '  Estruturas de pontos para ingestão criadas com sucesso!')

        return ingestion_points_list

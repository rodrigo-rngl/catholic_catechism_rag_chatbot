from src.validators.models.IngestionEmbeddings import IngestionEmbeddingsBase
from src.validators.models.IngestionEmbeddings import IngestionHybridEmbeddings, IngestionDenseEmbeddings
from src.infra.interfaces.ingestion_point_structures_creators_interface import IngestionPointStructuresCreatorsInterface
from src.infra.vector_db.qdrant.ingestion_point_structures_creators.dense_ingestion_point_structures_creators import DenseIngestionPointStructuresCreator
from src.infra.vector_db.qdrant.ingestion_point_structures_creators.hybrid_ingestion_point_structures_creators import HybridIngestionPointStructuresCreator


class IngestionPointStructuresCreatorsFactory:
    def __init__(self, embeddings: IngestionEmbeddingsBase) -> None:
        self.embeddings = embeddings

    def produce(self) -> IngestionPointStructuresCreatorsInterface:
        if isinstance(self.embeddings, IngestionHybridEmbeddings):
            return HybridIngestionPointStructuresCreator(embeddings=self.embeddings)
        if isinstance(self.embeddings, IngestionDenseEmbeddings):
            return DenseIngestionPointStructuresCreator(embeddings=self.embeddings)
        else:
            raise TypeError(
                'Não há implementação para o tipo de IngestorEmbeddigs fornecido.')

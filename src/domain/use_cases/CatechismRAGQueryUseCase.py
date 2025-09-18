from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository

class CatholicCatechismRAGQueryUseCase:
    def __init__(self, repository: QdrantVectorDBRepository):
        self.repository = repository

    def query(self, query: str):
        self.repository.hybrid_data_search
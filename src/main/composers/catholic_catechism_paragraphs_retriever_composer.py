from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.domain.use_cases.CatholicCatechismParagraphsRetriever import CatholicCatechismParagraphsRetriever
from src.presentation.controllers.catholic_catechism_paragraphs_retriever_controller import CatholicCatechismRetrieverController


def catholic_catechism_paragraphs_retriever_composer() -> CatholicCatechismRetrieverController:
    collection_name = "Parágrafos do Catecismo (Semantic Search & Retrieve)"

    repository = QdrantVectorDBRepository(collection_name=collection_name)

    use_case = CatholicCatechismParagraphsRetriever(repository=repository)

    return CatholicCatechismRetrieverController(use_case=use_case)

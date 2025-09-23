from src.infra.fastembed_embedder.fastembed_embedder_factory import FastembedEmbedderFactory
from src.domain.use_cases.CatholicCatechismSearcher import CatholicCatechismSearcher
from src.infra.vector_db.qdrant.collection_creators.qdrant_collection_creator_factory import QdrantCollectionCreatorFactory
from src.infra.vector_db.qdrant.points_searchers.qdrant_points_searcher_factory import QdrantPointsSearcherFactory
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.presentation.controllers.catholic_catechism_searcher_controller import CatholicCatechismSeacherController


def catholic_catechism_hybrid_searcher_composer() -> CatholicCatechismSeacherController:
    search_type = "Híbrida"
    collection_name = "CatholicCatechismVDB"

    embedder = FastembedEmbedderFactory(
        search_type=search_type).produce()

    collection_creator = QdrantCollectionCreatorFactory(
        search_type=search_type).produce()
    points_searcher = QdrantPointsSearcherFactory(
        search_type=search_type).produce()

    repository = QdrantVectorDBRepository(collection_name=collection_name,
                                          collection_creator=collection_creator,
                                          points_searcher=points_searcher)

    use_case = CatholicCatechismSearcher(
        embedder=embedder, repository=repository)

    return CatholicCatechismSeacherController(use_case=use_case)

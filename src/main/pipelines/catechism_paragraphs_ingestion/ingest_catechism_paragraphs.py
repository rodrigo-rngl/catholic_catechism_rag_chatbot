import asyncio
from dotenv import load_dotenv
from src.domain.services.catechism_scrapper import CatechismScrapper
from src.domain.services.catechism_paragraphs_ingestor import CatechismParagraphsIngestor
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.infra.fastembed_embedder.fastembed_embedder_factory import FastembedEmbedderFactory
from src.infra.vector_db.qdrant.collection_creators. qdrant_collection_creator_factory import QdrantCollectionCreatorFactory


load_dotenv()


async def ingest() -> None:
    scrapper = CatechismScrapper()
    payloads = scrapper.scrape()

    collection_name = "CatholicCatechismParagraphs"
    search_type = "Híbrida"

    collection_creator = QdrantCollectionCreatorFactory(
        search_type=search_type).produce()

    repository = QdrantVectorDBRepository(
        collection_name=collection_name, collection_creator=collection_creator)
    await repository.create_collection()

    embedder = FastembedEmbedderFactory(search_type=search_type).produce()

    ingestor = CatechismParagraphsIngestor(
        embedder=embedder, repository=repository)
    await ingestor.ingest(payloads=payloads, batch_size=5)

asyncio.run(ingest())

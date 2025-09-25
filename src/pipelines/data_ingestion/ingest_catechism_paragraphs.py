import os
import asyncio
from dotenv import load_dotenv
from src.pipelines.data_ingestion.catechism_scrapper import CatechismScrapper
from src.pipelines.data_ingestion.catechism_ingestor import CatechismIngestor
from src.infra.vector_db.qdrant.qdrant_vector_db_repository import QdrantVectorDBRepository
from src.infra.fastembed_embedder.fastembed_embedder_factory import FastembedEmbedderFactory
from src.pipelines.data_ingestion.catechism_page_content_splitter import CatechismPageContentSplitter
from src.infra.vector_db.qdrant.collection_creators. qdrant_collection_creator_factory import QdrantCollectionCreatorFactory
import json

load_dotenv()


async def ingest() -> None:
    # catechism_page_content_splitter = CatechismPageContentSplitter()
    # scrapper = CatechismScrapper(
    #    catechism_page_content_splitter=catechism_page_content_splitter)
    # payloads = scrapper.scrape()

    with open('src/data/catechism_chunks.json', 'r', encoding="utf-8") as file:
        payloads = json.load(file)

    collection_name = str(os.getenv("collection_name"))
    search_type = "Híbrida"

    collection_creator = QdrantCollectionCreatorFactory(
        search_type=search_type).produce()

    repository = QdrantVectorDBRepository(
        collection_name=collection_name, collection_creator=collection_creator)
    await repository.create_collection()

    embedder = FastembedEmbedderFactory(search_type=search_type).produce()

    ingestor = CatechismIngestor(embedder=embedder, repository=repository)
    await ingestor.ingest(payloads=payloads, batch_size=5)

asyncio.run(ingest())

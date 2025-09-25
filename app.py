from dotenv import load_dotenv
from src.validators.models.Query import QueryIn, QueryOut
from src.main.composers.catholic_catechism_hybrid_searcher_composer import catholic_catechism_hybrid_searcher_composer
from src.errors.handle_errors import handle_errors
import json
import asyncio

load_dotenv()


async def hybrid_search(query: QueryIn) -> None:
    try:
        query = QueryOut(**query.model_dump())
        controller = catholic_catechism_hybrid_searcher_composer()
        http_response = await controller.handle(query=query)

        print(
            f'[{http_response.status_code}]:\n {json.dumps(http_response.body, indent=4, ensure_ascii=False)}')

    except Exception as exception:
        http_response = handle_errors(error=exception)
        print(
            f'[{http_response.status_code}]: {http_response.body}')


query = QueryIn(
    query='Quais são os frutos do Espírito Santo que devemos produzir?')

asyncio.run(hybrid_search(query=query))

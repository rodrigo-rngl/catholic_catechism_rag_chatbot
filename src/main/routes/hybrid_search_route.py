from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.errors.handle_errors import handle_errors
from src.validators.models.Query import QueryIn, QueryOut
from src.main.composers.catholic_catechism_hybrid_searcher_composer import catholic_catechism_hybrid_searcher_composer


hybrid_search_route = APIRouter()


@hybrid_search_route.get("/hybrid_search", summary='Busca Híbrida',
                         description="Endpoint responsável por realizar busca híbrida de 5 parágrafos do catecismo similares a Query enviada. ")
async def hybrid_search(query: QueryIn) -> JSONResponse:
    try:
        query = QueryOut(**query.model_dump())
        controller = catholic_catechism_hybrid_searcher_composer()
        http_response = await controller.handle(query=query)

        response = JSONResponse(
            content=http_response.body, status_code=http_response.status_code)
        return response

    except Exception as exception:
        http_response = handle_errors(error=exception)
        response = JSONResponse(
            content=http_response.body, status_code=http_response.status_code)
        return response

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.errors.handle_errors import handle_errors
from src.validators.models.HttpResponse import HttpResponseSearch
from src.validators.models.HttpRequest import HttpRequestInSearch, HttpRequestSearch
from src.main.composers.catholic_catechism_hybrid_searcher_composer import catholic_catechism_hybrid_searcher_composer

from src.config.logger_config import setup_logger
logger = setup_logger(name="search_routes")

search_routes = APIRouter(tags=["Search Routes"])


@search_routes.post("/hybrid_search",
                    summary="Busca Hídrida de Parágrafos do Catecismo",
                    description="Endpoint responsável por realizar busca híbrida de parágrafos do catecismo, similares ao questionamento enviado.",
                    response_model=HttpResponseSearch,
                    responses={
                        200: {"description": "OK (Successful Response)",
                              "model": HttpResponseSearch,
                              "content": {"application/json":
                                          {"example":
                                           {
                                               "id": "2ab4f3e8-6532-4020-b19f-2a4650295f30",
                                               "status_code": 200,
                                               "created_in": "2025-12-25T00:00:00.000000",
                                               "took_ms": 12000,
                                               "query": "Jesus Cristo é verdadeiro Deus e verdadeiro homem?",
                                               "top_k": 1,
                                               "body": {
                                                   "query_validation": {
                                                        "scope": "general_christian",
                                                        "category": "christology",
                                                        "confidence": 0.9,
                                                        "reasons": "A pergunta trata da natureza de Jesus Cristo (se é verdadeiro Deus e verdadeiro homem), que é uma questão de cristologia comum a tradições cristãs. Não menciona especificamente termos ou instituições católicas (Catecismo, Magistério, sacramentos, Maria, santos etc.), portanto é classificada como cristã geral.",
                                                        "action": "proceed_rag"
                                                   },
                                                   "points": [
                                                       {
                                                           "text": "480 . Jesus Cristo é verdadeiro Deus e verdadeiro homem, na unidade da sua Pessoa divina; por essa razão, Ele é o único mediador entre Deus e os homens.",
                                                           "localization": {
                                                               "PART": "PRIMEIRA PARTE - A PROFISSÃO DA FÉ",
                                                               "SECTION": "SEGUNDA SECÇÃO - A PROFISSÃO DA FÉ CRISTÃ",
                                                               "CHAPTER": "CAPÍTULO SEGUNDO - CREIO EM JESUS CRISTO, FILHO ÚNICO DE DEUS",
                                                               "ARTICLE": "ARTIGO 3 - «JESUS CRISTO FOI CONCEBIDO PELO PODER DO ESPÍRITO SANTO E NASCEU DA VIRGEM MARIA»",
                                                               "PARAGRAPHS_GROUP": "PARÁGRAFO 1 - O FILHO DE DEUS FEZ-SE HOMEM",
                                                               "INTERNAL_SECTION": "Resumindo:",
                                                               "THEMATIC_SUBSECTION": ""
                                                           },
                                                           "similarity_score": 18.371273040771484
                                                       }
                                                   ]
                                               }
                                           }}}},

                        207: {"description": " Multi-Status (Clarification Solicitation)",
                              "model": HttpResponseSearch,
                              "content": {"application/json":
                                          {"example":
                                           {
                                               "id": "74053019-7522-4243-95cd-5802e1862254",
                                               "status_code": 207,
                                               "created_in": "2025-12-25T00:00:00.000000",
                                               "took_ms": 1000,
                                               "query": "O católico praticante deve ir a ... todos os ... ?",
                                               "top_k": 1,
                                               "body": {
                                                   "query_validation": {
                                                        "scope": "ambiguous",
                                                        "category": "other",
                                                        "confidence": 0.42,
                                                        "reasons": "A pergunta está incompleta (usa reticências) e não especifica a que prática se refere — por exemplo: missa aos domingos, confissão, comunhão, participar de celebrações específicas etc. Por mencionar \"católico praticante\" sugere tema religioso/católico, mas a falta de termos concretos impede classificar com certeza numa categoria doutrinal específica.",
                                                        "action": "ask_clarifying"
                                                   }
                                               }
                                           }}}},
                        422: {"description": "Error: Unprocessable Entity (Validation Error)",
                              "model": HttpResponseSearch,
                              "content": {"application/json":
                                          {"example":
                                           {
                                               "id": "550f4c05-9fc5-4f83-9724-f0e4d525d301",
                                               "status_code": 422,
                                               "created_in": "2025-12-25T00:00:00.000000",
                                               "took_ms": 1,
                                               "query": "Jesus é verdadeiramente Deus e verdadeiramente homem?",
                                               "top_k": 0,
                                               "body": {
                                                   "error": {
                                                       "title": "Validation Error",
                                                       "detail": "Erro de validação no corpo da requisição.",
                                                       "validation_errors": [
                                                           {
                                                               "type": "greater_than_equal",
                                                               "loc": [
                                                                "top_k"
                                                               ],
                                                               "msg": "Input should be greater than or equal to 1",
                                                               "input": 0,
                                                               "ctx": {
                                                                   "ge": 1
                                                               }
                                                           }
                                                       ]
                                                   }
                                               }
                                           }}}},
                        406: {"description": "Error: Not Acceptable (Domain Error)",
                              "model": HttpResponseSearch,
                              "content": {"application/json":
                                          {"example":
                                           {
                                               "id": "1cae785b-9b21-423d-8e64-62cf85d4cbc2",
                                                     "status_code": 422,
                                                     "created_in": "2025-12-25T00:00:00.000000",
                                                     "took_ms": 5000,
                                                     "query": "Em que ano o Brasil ganhou a primeira Copa do Mundo?",
                                                     "top_k": 1,
                                                     "body": {
                                                         "error": {
                                                             "title": "Domain Error",
                                                             "detail": "A query enviada não possui relação de contexto para desta aplicação.",
                                                             "query_validation": {
                                                                 "scope": "off_topic",
                                                                 "category": "other",
                                                                 "confidence": 0.92,
                                                                 "reasons": "A pergunta refere-se a um fato histórico/esportivo sobre o Brasil ganhar a Copa do Mundo, sem qualquer relação com doutrina cristã ou temas religiosos; portanto está fora do escopo de validação doutrinária.",
                                                                 "action": "reject"
                                                             }
                                                         }
                                                     }
                                           }}}},
                        500: {"description": "Error: Internal Server Error (Server Error)",
                              "model": HttpResponseSearch,
                              "content": {"application/json":
                                          {"example":
                                           {"id": "dcc611fd-060b-484c-9feb-303e7f17cbf0",
                                                  "status_code": 500,
                                                  "created_in": "2025-12-25T00:00:00.000000",
                                                  "took_ms": 10000,
                                                  "query": "Jesus Cristo é verdadeiro Deus e verdadeiro homem?",
                                                  "top_k": 1,
                                                  "body": {
                                                      "error": [
                                                          {
                                                              "title": "Server Error",
                                                              "detail": "Interval Server Error"
                                                          }
                                                      ]
                                                  }
                                            }}}}})
async def hybrid_search(http_request: HttpRequestInSearch) -> JSONResponse:
    try:
        http_request = HttpRequestSearch(**http_request.model_dump())
        logger.info(f'Requisição recebida! ID: {http_request.id}')

        controller = catholic_catechism_hybrid_searcher_composer()
        http_response = await controller.handle(http_request=http_request)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))

    except Exception as exception:
        http_request = HttpRequestSearch(**http_request.model_dump())
        http_response = handle_errors(
            http_request=http_request, error=exception)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))

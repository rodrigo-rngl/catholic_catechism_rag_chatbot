from typing import Annotated
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from src.errors.handle_errors import handle_errors
from src.validators.models.HttpRequest import HttpRequestInRetrieve, HttpRequestRetrieve
from src.validators.models.HttpResponse import HttpResponseBase
from src.main.composers.catholic_catechism_paragraphs_retriever_composer import catholic_catechism_paragraphs_retriever_composer

from src.config.logger_config import setup_logger
logger = setup_logger(name="search_routes")


retrieve_routes = APIRouter(tags=["Retrieve Routes"])


@retrieve_routes.get("/catechism_paragraph/{paragraph_number}",
                     summary="Recuperação Parágrafo do Catecismo",
                     description="Endpoint responsável por recuperar um único parágrafo do catecismo por seu número.",
                     response_model=HttpResponseBase,
                     responses={
                         200: {"description": "OK (Successful Response)",
                               "model": HttpResponseBase,
                               "content": {"application/json":
                                           {"example":
                                            {
                                                "id": "e2414697-2dae-4949-a9b2-844e64519b3f",
                                                "status_code": 200,
                                                "created_in": "2025-12-04T14:51:24.584097-03:00",
                                                "took_ms": 5000,
                                                "body": {
                                                    "points": [
                                                        {
                                                            "text": "33 . O homem: Com a sua abertura à verdade e à beleza, com o seu sentido do bem moral, com a sua liberdade e a voz da sua consciência, com a sua ânsia de infinito e de felicidade, o homem interroga-se sobre a existência de Deus. Nestas aberturas, ele detecta sinais da sua alma espiritual. «Gérmen de eternidade que traz em si mesmo, irredutível à simples matéria» (10), a sua alma só em Deus pode ter origem.",
                                                            "localization": {
                                                                "SECTION": "PRIMEIRA SECÇÃO - «EU CREIO» – «NÓS CREMOS»",
                                                                "THEMATIC_SUBSECTION": "",
                                                                "PART": "PRIMEIRA PARTE - A PROFISSÃO DA FÉ",
                                                                "ARTICLE": "",
                                                                "INTERNAL_SECTION": "II. Os caminhos de acesso ao conhecimento de Deus",
                                                                "PARAGRAPHS_GROUP": "",
                                                                "CHAPTER": "CAPÍTULO PRIMEIRO - O HOMEM É «CAPAZ» DE DEUS"
                                                            }
                                                        }
                                                    ]
                                                }
                                            }}}},
                         422: {"description": "Error: Unprocessable Entity (Validation Error)",
                               "model": HttpResponseBase,
                               "content": {"application/json":
                                           {"example":
                                            {
                                                "id": "7fbafd1f-c159-4e78-b675-ea1705967de1",
                                                "status_code": 422,
                                                "created_in": "2025-12-25T00:00:00.000000",
                                                "took_ms": 1,
                                                "body": {
                                                    "error": {
                                                        "title": "Validation Error",
                                                        "detail": "Erro de validação no corpo da requisição.",
                                                        "validation_errors": [
                                                            {
                                                                "type": "greater_than_equal",
                                                                "loc": [
                                                                    "body",
                                                                    "paragraph_numbers",
                                                                    0
                                                                ],
                                                                "msg": "Input should be greater than or equal to 0",
                                                                "input": -1,
                                                                "ctx": {
                                                                    "ge": 0
                                                                }
                                                            },
                                                            {
                                                                "type": "less_than_equal",
                                                                "loc": [
                                                                    "body",
                                                                    "paragraph_numbers",
                                                                    1
                                                                ],
                                                                "msg": "Input should be less than or equal to 2865",
                                                                "input": 2866,
                                                                "ctx": {
                                                                    "le": 2865
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            }}}},
                         500: {"description": "Error: Internal Server Erro (Server Error)",
                               "model": HttpResponseBase,
                               "content": {"application/json":
                                           {"example":
                                            {"id": "dcc611fd-060b-484c-9feb-303e7f17cbf0",
                                              "status_code": 500,
                                              "created_in": "2025-12-25T00:00:00.000000",
                                              "took_ms": 5000,
                                              "body": {
                                                  "error": [
                                                      {
                                                          "title": "Server Error",
                                                          "detail": "Interval Server Error"
                                                      }
                                                  ]
                                              }
                                             }}}}})
async def retrieve_catechism_paragraph(paragraph_number: Annotated[int, Path(ge=1, le=2865)]) -> JSONResponse:
    paragraph_numbers = [paragraph_number]

    http_request = HttpRequestInRetrieve(paragraph_numbers=paragraph_numbers)

    try:
        http_request = HttpRequestRetrieve(**http_request.model_dump())
        logger.info(f'Requisição recebida! ID: {http_request.id}')

        controller = catholic_catechism_paragraphs_retriever_composer()
        http_response = await controller.handle(http_request=http_request)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))

    except Exception as exception:
        http_request = HttpRequestRetrieve(**http_request.model_dump())
        http_response = handle_errors(
            http_request=http_request, error=exception)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))


@retrieve_routes.post("/catechism_paragraphs",
                      summary="Recuperação de Parágrafos do Catecismo",
                      description="Endpoint responsável por recuperar parágrafos do catecismo por seus identificadores numéricos (paragraph_numbers).",
                      response_model=HttpResponseBase,
                      responses={
                          200: {"description": "OK (Successful Response)",
                                "model": HttpResponseBase,
                                "content": {"application/json":
                                            {"example":
                                             {
                                                 "id": "86e042af-9b4f-48dd-bc42-9665884e37d2",
                                                 "status_code": 200,
                                                 "created_in": "2025-12-25T00:00:00.000000",
                                                 "took_ms": 5000,
                                                 "body": {
                                                     "points": [
                                                         {
                                                             "text": "33 . O homem: Com a sua abertura à verdade e à beleza, com o seu sentido do bem moral, com a sua liberdade e a voz da sua consciência, com a sua ânsia de infinito e de felicidade, o homem interroga-se sobre a existência de Deus. Nestas aberturas, ele detecta sinais da sua alma espiritual. «Gérmen de eternidade que traz em si mesmo, irredutível à simples matéria» (10), a sua alma só em Deus pode ter origem.",
                                                             "localization": {
                                                                 "CHAPTER": "CAPÍTULO PRIMEIRO - O HOMEM É «CAPAZ» DE DEUS",
                                                                 "INTERNAL_SECTION": "II. Os caminhos de acesso ao conhecimento de Deus",
                                                                 "ARTICLE": "",
                                                                 "SECTION": "PRIMEIRA SECÇÃO - «EU CREIO» – «NÓS CREMOS»",
                                                                 "THEMATIC_SUBSECTION": "",
                                                                 "PART": "PRIMEIRA PARTE - A PROFISSÃO DA FÉ",
                                                                 "PARAGRAPHS_GROUP": ""
                                                             }
                                                         },
                                                         {
                                                             "text": "777. A palavra «Igreja» significa «convocação». Designa a assembleia daqueles que a Palavra de Deus convoca para formar o seu povo, e que, alimentados pelo Corpo de Cristo, se tornam, eles próprios, Corpo de Cristo.",
                                                             "localization": {
                                                                 "CHAPTER": "CAPÍTULO TERCEIRO - CREIO NO ESPÍRITO SANTO",
                                                                 "INTERNAL_SECTION": "Resumindo:",
                                                                 "ARTICLE": "ARTIGO 9 - «CREIO NA SANTA IGREJA CATÓLICA»",
                                                                 "SECTION": "SEGUNDA SECÇÃO - A PROFISSÃO DA FÉ CRISTÃ",
                                                                 "THEMATIC_SUBSECTION": "",
                                                                 "PART": "PRIMEIRA PARTE - A PROFISSÃO DA FÉ",
                                                                 "PARAGRAPHS_GROUP": "PARÁGRAFO 1 - A IGREJA NO DESÍGNIO DE DEUS"
                                                             }
                                                         },
                                                         {
                                                             "text": "490. Para vir a ser Mãe do Salvador, Maria «foi adornada por Deus com dons dignos de uma tão grande missão» (137). O anjo Gabriel, no momento da Anunciação, saúda-a como «cheia de graça»(138). Efectivamente, para poder dar o assentimento livre da sua fé ao anúncio da sua vocação, era necessário que Ela fosse totalmente movida pela graça de Deus.",
                                                             "localization": {
                                                                 "CHAPTER": "CAPÍTULO SEGUNDO - CREIO EM JESUS CRISTO, FILHO ÚNICO DE DEUS",
                                                                 "INTERNAL_SECTION": "II. ...nascido da Virgem Maria",
                                                                 "ARTICLE": "ARTIGO 3 - «JESUS CRISTO FOI CONCEBIDO PELO PODER DO ESPÍRITO SANTO E NASCEU DA VIRGEM MARIA»",
                                                                 "SECTION": "SEGUNDA SECÇÃO - A PROFISSÃO DA FÉ CRISTÃ",
                                                                 "THEMATIC_SUBSECTION": "A IMACULADA CONCEIÇÃO",
                                                                 "PART": "PRIMEIRA PARTE - A PROFISSÃO DA FÉ",
                                                                 "PARAGRAPHS_GROUP": "PARÁGRAFO 2 - «... CONCEBIDO PELO PODER DO ESPÍRITO SANTO, NASCIDO DA VIRGEM MARIA»"
                                                             }
                                                         }
                                                     ]
                                                 }
                                             }}}},
                          422: {"description": "Error: Unprocessable Entity (Validation Error)",
                                "model": HttpResponseBase,
                                "content": {"application/json":
                                            {"example":
                                             {
                                                 "id": "7fbafd1f-c159-4e78-b675-ea1705967de1",
                                                 "status_code": 422,
                                                 "created_in": "2025-12-25T00:00:00.000000",
                                                 "took_ms": 1,
                                                 "body": {
                                                     "error": {
                                                         "title": "Validation Error",
                                                         "detail": "Erro de validação no corpo da requisição.",
                                                         "validation_errors": [
                                                             {
                                                                 "type": "greater_than_equal",
                                                                 "loc": [
                                                                     "body",
                                                                     "paragraph_numbers",
                                                                     0
                                                                 ],
                                                                 "msg": "Input should be greater than or equal to 0",
                                                                 "input": -1,
                                                                 "ctx": {
                                                                     "ge": 0
                                                                 }
                                                             },
                                                             {
                                                                 "type": "less_than_equal",
                                                                 "loc": [
                                                                     "body",
                                                                     "paragraph_numbers",
                                                                     1
                                                                 ],
                                                                 "msg": "Input should be less than or equal to 2865",
                                                                 "input": 2866,
                                                                 "ctx": {
                                                                     "le": 2865
                                                                 }
                                                             }
                                                         ]

                                                     }
                                                 }
                                             }}}},
                          500: {"description": "Error: Internal Server Erro (Server Error)",
                                "model": HttpResponseBase,
                                "content": {"application/json":
                                            {"example":
                                             {"id": "dcc611fd-060b-484c-9feb-303e7f17cbf0",
                                              "status_code": 500,
                                              "created_in": "2025-12-25T00:00:00.000000",
                                              "took_ms": 5000,
                                              "body": {
                                                  "error": [
                                                      {
                                                          "title": "Server Error",
                                                          "detail": "Interval Server Error"
                                                      }
                                                  ]
                                              }
                                              }}}}})
async def retrive_catechism_paragraphs(http_request: HttpRequestInRetrieve) -> JSONResponse:
    try:
        http_request = HttpRequestRetrieve(**http_request.model_dump())
        logger.info(f'Requisição recebida! ID: {http_request.id}')

        controller = catholic_catechism_paragraphs_retriever_composer()
        http_response = await controller.handle(http_request=http_request)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))

    except Exception as exception:
        http_request = HttpRequestRetrieve(**http_request.model_dump())
        http_response = handle_errors(
            http_request=http_request, error=exception)

        return JSONResponse(status_code=http_response.status_code,
                            content=http_response.model_dump(mode="json"))

from datetime import datetime
from src.validators.models.HttpRequest import HttpRequestOut
from src.validators.models.HttpResponse import HttpResponse
from src.domain.use_cases.CatholicCatechismParagraphsSearcher import CatholicCatechismParagraphsSearcher
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.validators.models.SearchPipelineResult import SearchClarification

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatholicCatechismSeacherController")


class CatholicCatechismSeacherController(ControllerInterface):
    def __init__(self, use_case: CatholicCatechismParagraphsSearcher) -> None:
        self.use_case = use_case

    async def handle(self, http_request: HttpRequestOut) -> HttpResponse:
        query = http_request.query
        top_k = http_request.top_k

        request_created_in = http_request.created_in

        result = await self.use_case.search(query=query, top_k=top_k)

        took_ms = self.calculate_request_time(
            request_created_in=request_created_in)

        if isinstance(result, SearchClarification):
            logger.info("Resposta para melhorar/clarear a query passada foi retornada com sucesso!\n"
                        f"   - ID da Requisição: {http_request.id}\n"
                        f"   - Tempo de Execução: {took_ms}ms")
            return HttpResponse(id=http_request.id,
                                status_code=406,
                                created_in=http_request.created_in,
                                took_ms=took_ms,
                                query=http_request.query,
                                top_k=http_request.top_k,
                                body={"query_validation": result.query_validation.model_dump()})

        search_results_dicts = [output.model_dump()
                                for output in result.search_outputs]

        logger.info("Parágrafos do catecismo da Igreja Católica foram retornados com sucesso!\n"
                    f"   - ID da Requisição: {http_request.id}\n"
                    f"   - Tempo de Execução: {took_ms}ms")

        return HttpResponse(id=http_request.id,
                            status_code=200,
                            created_in=http_request.created_in,
                            took_ms=took_ms,
                            query=http_request.query,
                            top_k=http_request.top_k,
                            body={'query_validation': result.query_validation.model_dump(),
                                  'points': search_results_dicts})

    @classmethod
    def calculate_request_time(cls, request_created_in: datetime) -> int:
        end_time = datetime.now(tz=request_created_in.tzinfo)
        return int((end_time - request_created_in).total_seconds() * 1000)

from datetime import datetime
from src.validators.models.HttpRequest import HttpRequestRetrieve
from src.validators.models.HttpResponse import HttpResponseBase
from src.domain.use_cases.CatholicCatechismParagraphsRetriever import CatholicCatechismParagraphsRetriever
from src.presentation.interfaces.controller_interface import ControllerInterface

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatholicCatechismRetrieverController")


class CatholicCatechismRetrieverController(ControllerInterface[HttpRequestRetrieve, HttpResponseBase]):
    def __init__(self, use_case: CatholicCatechismParagraphsRetriever) -> None:
        self.use_case = use_case

    async def handle(self, http_request: HttpRequestRetrieve) -> HttpResponseBase:
        paragraph_numbers = http_request.paragraph_numbers

        request_created_in = http_request.created_in

        result = await self.use_case.retrieve(paragraph_numbers=paragraph_numbers)

        took_ms = self.calculate_request_time(
            request_created_in=request_created_in)

        retrieve_results_lists = [output.model_dump()
                                  for output in result.retrieve_output]

        logger.info("Parágrafos do catecismo da Igreja Católica foram retornados com sucesso!\n"
                    f"   - ID da Requisição: {http_request.id}\n"
                    f"   - Tempo de Execução: {took_ms}ms")

        return HttpResponseBase(id=http_request.id,
                                status_code=200,
                                created_in=http_request.created_in,
                                took_ms=took_ms,
                                body={'points': retrieve_results_lists})

    @classmethod
    def calculate_request_time(cls, request_created_in: datetime) -> int:
        end_time = datetime.now(tz=request_created_in.tzinfo)
        return int((end_time - request_created_in).total_seconds() * 1000)

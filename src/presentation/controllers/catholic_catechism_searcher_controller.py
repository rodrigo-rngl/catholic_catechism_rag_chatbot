from src.domain.use_cases.CatholicCatechismSearcher import CatholicCatechismSearcher
from src.presentation.interfaces.controller_interface import ControllerInterface
from src.validators.models.Query import QueryOut
from src.validators.models.HttpResponse import HttpResponse


class CatholicCatechismSeacherController(ControllerInterface):
    def __init__(self, use_case: CatholicCatechismSearcher) -> None:
        self.use_case = use_case

    async def handle(self, query: QueryOut) -> HttpResponse:

        search_results = await self.use_case.search(query=query.query)

        return HttpResponse(status_code=200,
                            body={'result': search_results})

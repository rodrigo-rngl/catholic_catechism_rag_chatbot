from typing import Sequence, Union
from pydantic import BaseModel
from src.validators.models.QueryValidation import QueryValidation
from src.validators.models.SearchOutput import SearchOutput


class SearchSuccess(BaseModel):
    query_validation: QueryValidation
    search_outputs: Sequence[SearchOutput]


class SearchClarification(BaseModel):
    query_validation: QueryValidation


SearchPipelineResult = Union[SearchSuccess, SearchClarification]

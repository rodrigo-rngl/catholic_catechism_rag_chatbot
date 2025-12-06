from typing import List
from pydantic import BaseModel
from src.validators.models.RetrieveOutput import RetrieveOutput


class RetrieveSuccess(BaseModel):
    retrieve_output: List[RetrieveOutput]

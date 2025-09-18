from typing import Mapping, Any
from pydantic import BaseModel

class Metadata(BaseModel):
    PARTE: str
    SECÇAO: str
    CAPITULO: str
    ARTIGO: str
    SECÇAO_INTERNA: str
    SUBSEÇAO_TEMATICA: str
    
class SearchOutput(BaseModel):
    text: str
    metadata: Metadata


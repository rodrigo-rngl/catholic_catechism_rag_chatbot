from typing import Dict, Optional
from pydantic import BaseModel


class RetrieveOutput(BaseModel):
    text: str
    localization: Optional[Dict[str, str]] = None

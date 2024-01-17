from pydantic import BaseModel
from typing import List, Optional

class AdzunaJob(BaseModel):
    id: int
    title: str
    redirect_url: str
    company : Optional[str]
    created : str










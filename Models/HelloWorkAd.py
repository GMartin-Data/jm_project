from pydantic import BaseModel
from typing import List, Optional

class HelloWorkAd(BaseModel):
    """Output class for a HelloWord scraped ad"""
    id: int
    title: str
    redirect_url: str
    company : Optional[str]
    created : str
    hw_url: str
    location: str
    contract: str
    education: Optional[List[str]]
    duration: Optional[List[str]]  
    remote: Optional[List[str]]        
    experience: Optional[List[str]]
    salary_min: Optional[str]
    salary_max: Optional[str]
    salary: Optional[str]
    salary_min_e: Optional[str]
    salary_med_e: Optional[str]
    salary_max_e: Optional[str]
    description: List[str] 
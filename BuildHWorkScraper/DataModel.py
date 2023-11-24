"""
 In this module, we define a data model using the Pydantic library. 
"""

from pydantic import BaseModel  
from rich import print  
from typing import List, Optional 


class OnlyId(BaseModel):
    """
       Output class if:
        - hellowork url is null
        - Invalid url
        - Not hellowork url
    """
    id: Optional[str]
    

class HelloWorkAd(BaseModel):
    """Output class for a HelloWork scraped ad"""
    id: str   # Given by adzuna_url's output
    url: str
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

"""
This module contains logic to transform extracted data,
to specially designed classes for Adzuna API and hellowork web page.
"""

import json
from typing import List, Optional
from pydantic import BaseModel
from rich import print
from utils import configure, create_client, get_timestamp, timer


########## ADZUNA ##########
class AdzunaJob(BaseModel):
    """
    Output class for Adzuna jobs.
    Based on the job_market_variables sheet (tiny link below).
    https://tinyurl.com/job-vars
    (order of attributes could nevertheless be rearranged.)
    """
    title: str
    created: str  # Switch to datetime?
    salary_is_predicted: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    location: str
    contract: Optional[str]
    area: List[str]
    id: str  # ⚠️ Use Union for retro-compatibility if needed
    adref: str
    redirect_url: str
    company: Optional[str]  # It's weird but it caused a bug, as a company wasn't specified
    description: str
    label: str
    tag: str


def filter_adzuna_job(job: dict) -> dict:
    """Filter a dict inputs to fit into an AdzunaJob's instance attributes"""
    return {
        'title': job.get('title'),
        'created': job.get('created'),
        'contract': job.get('contract_type'),
        'location': job.get('location', {}).get('display_name'),
        'salary_is_predicted': job.get('salary_is_predicted'),
        'salary_min': job.get('salary_min'),
        'salary_max': job.get('salary_max'),
        'description': job.get('description'),
        'latitude': job.get('latitude'),
        'longitude': job.get('longitude'),
        # 'hellowork_url' : urljob(job.get('redirect_url')),
        'area': job.get('location', {}).get('area'),
        'id': str(job.get('id', '')),  # ❓isn't `int` better? / NA managing
        'adref': job.get('adref'),
        'redirect_url': job.get('redirect_url'),
        'company': job.get('company', {}).get('display_name'),
        'label': job.get('category', {}).get('label'),
        'tag': job.get('category', {}).get('tag'),
    }
    
    
def model_adzuna_job_data(jobs: List[dict]) -> List[AdzunaJob]:
    """Map filter_adzuna_job to the list of dict inputs."""
    return [AdzunaJob(**filter_adzuna_job(job)) for job in jobs] 


  
########## HELLOWORK ##########
class HelloWorkAd(BaseModel):
    """Output class for a HelloWord scraped ad"""
    id: Optional[str]
    hellowork_url: Optional[str]
    file_name: Optional[str]
    title:Optional[str]
    redirect_url:Optional[str]
    company:Optional[str]
    created:Optional[str]
    area:Optional[List[str]]
    latitude: Optional[float]
    longitude: Optional[float]
    location: Optional[str]
    contract: Optional[str]
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
    description: Optional[List[str]] 

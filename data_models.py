import json
from typing import List, Optional

from pydantic import BaseModel
from rich import print


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
    area: List[str]
    
    id: str | int  # ⚠️ Use Union for retro-compatibility if needed
    adref: str
    redirect_url: str
    
    company: Optional[str]  # It's weird but it caused a bug, as a company wasn't specified
    description: str
    contract_type: Optional[str]
    contract_time: Optional[str]
    
    # Corresponds to 'category' in job_market_variables sheet
    label: str
    tag: str


def filter_adzuna_job(job: dict) -> dict:
    """Filter a dict inputs to fit into an AdzunaJob's instance attributes"""
    return {
        'title': job.get('title'),
        'created': job.get('created'),
        
        'salary_is_predicted': job.get('salary_is_predicted'),
        'salary_min': job.get('salary_min'),
        'salary_max': job.get('salary_max'),
        
        'latitude': job.get('latitude'),
        'longitude': job.get('longitude'),
        'location': job.get('location', {}).get('display_name'),
        'area': job.get('location', {}).get('area'),
        
        'id': str(job.get('id')),
        'adref': job.get('adref'),
        'redirect_url': job.get('redirect_url'),
        
        'company': job.get('company', {}).get('display_name'),
        'description': job.get('description'),
        'contract_type': job.get('contract_type'),
        'contract_time': job.get('contract_time'),        
        
        'label': job.get('category', {}).get('label'),
        'tag': job.get('category', {}).get('tag'),
    }
    
    
def model_adzuna_job_data(jobs: List[dict]) -> List[AdzunaJob]:
    """Map filter_adzuna_job to the list of dict inputs."""
    return [AdzunaJob(**filter_adzuna_job(job)) for job in jobs] 
    

########## THE MUSE ##########
class TheMuseJob(BaseModel):
    """
    Output class for The Muse jobs.
    Based on the job_market_variables sheet (tiny link below).
    https://tinyurl.com/job-vars
    (order of attributes could nevertheless be rearranged.)
    """
    name: str
    publication_date: str  # 👉 Switch to datetime?

    locations: List[str]
    
    id: int | str  # ⚠️ `Union` for retro-compatibility
    landing_page: str
    
    company: str  # There are additional infos commented below
    # company_id: int | str
    # company_short_name: str
    contents: str  # 😱 Contains HTML tags, to process rn or later
    type: str
    level: str  # Choice to make between `name` and `short_name`
    
 
if __name__ == '__main__':
    # Test model_adzuna_job_data
    with open('data/adzuna_jobs_2023-10-07-18:56:14.json', 'r') as load_file:
        jobs = json.load(load_file)['results']    
    
    adzuna_jobs = model_adzuna_job_data(jobs)
    
    for idx, job in enumerate(adzuna_jobs[:10]):
        print(f'[white]OFFER {idx}[/white]', '\t', job)
        
    print('SUCCESS!')
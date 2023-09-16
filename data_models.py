import json
from typing import List, Optional

from pydantic import BaseModel
from rich import print


class AdzunaJob(BaseModel):
    id: str | int
    adref: str
    redirect_url: str
    
    title: str
    description: str
    label: str
    tag: str
    company: str
    
    latitude: Optional[float]
    longitude: Optional[float]
    location: str
    area: List[str]
    
    salary_is_predicted: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    
    created: str


def filter_adzuna_job(job: dict):
    return {
        'id': str(job.get('id')),
        'adref': job.get('adref'),
        'redirect_url': job.get('redirect_url'),
        
        'title': job.get('title'),
        'description': job.get('description'),
        'label': job.get('category', {}).get('label'),
        'tag': job.get('category', {}).get('tag'),
        'company': job.get('company', {}).get('display_name'),
        
        'latitude': job.get('latitude'),
        'longitude': job.get('longitude'),
        'location': job.get('location', {}).get('display_name'),
        'area': job.get('location', {}).get('area'),
        
        'salary_is_predicted': job.get('salary_is_predicted'),
        'salary_min': job.get('salary_min'),
        'salary_max': job.get('salary_max'),
        'created': job.get('created')    
    }
    
def model_adzuna_job_data(jobs: List[dict]) -> List[AdzunaJob]:
    return [AdzunaJob(**filter_adzuna_job(job)) for job in jobs] 
    
    
if __name__ == '__main__':
    with open('data/adzuna_jobs_2023-09-16-10:31:39.json', 'r') as load_file:
        jobs = json.load(load_file)['results']    
    
    adzuna_jobs = model_adzuna_job_data(jobs)
    
    for idx, job in enumerate(adzuna_jobs[:10]):
        print(idx, '\t', job)
        
    print('SUCCESS!')
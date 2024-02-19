"""
@author: Greg 
@code-reviewer: lnasri

This module contains logic to extract data from Adzuna API.
Endpoints already implemented are those corresponding to
- ads
- categories,
- locations
"""

import json
import time
from typing import List, Optional, Tuple


from httpx import Client
from rich import print

from  data_models import *  
from utils import configure, create_client, get_timestamp, timer




def create_dump(dump_path, data):
    """Create dump"""
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        json.dump(data, dump_file, indent=4, ensure_ascii=False) 
    

def get_adzuna_ads_page(client: Client,
                        page: int,
                        what: Optional[str] = None,
                        cat_tag: Optional[str] = None) -> List[dict]:
    """Get the 50 results of one page from Adzuna API"""
    url = f'{ADZUNA_URL}/jobs/fr/search/{page}'
    custom_params = {
        'app_id': ADZUNA_ID,
        'app_key': ADZUNA_KEY,
        'results_per_page': 50
        }
    if what:
        custom_params['what'] = what
    if cat_tag:
        custom_params['category'] = cat_tag
    
    resp = client.get(
        url,
        params=custom_params
    )
    resp.raise_for_status()
    
    return resp.json()['results']


@timer
def get_adzuna_ads(what: Optional[str] = None,
                   cat_tag: str = 'it-jobs')-> Tuple[List[AdzunaJob], int]:
    """
    Requesting Adzuna API to get as much as possible relevant daily ads
    Parameters
    ----------
        - what: a topic to explore ('data', 'Python' for example)
        - cat_tag: a custom category tag from Adzuna (read the doc)
    Returns
    -------
        A 2-tuple with:
        - A list of AdzunaJob objects
        - The number of remaining daily calls  
    """
    THRESHOLD = 0.05  # tolerated duplicates ratio
    
    cli = create_client()
    adzuna_jobs = []
    errors = 0
    n_page = 1
    duplicates = []
    
    for step in range(1, 11):
        print(f"\t[white]Step {step}[/white]")
        for page in range(n_page, n_page + 25):
            # UPDATING 'id' SET
            ids = set(job['id'] for job in adzuna_jobs)
            # REQUESTING
            try:
                new_jobs = get_adzuna_ads_page(cli, page, what, cat_tag)
                print(f'Page {page} PROCESSED')    
            except BaseException as e:
                print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
                errors += 1    
            else:
                duplicates.extend([job['id'] for job in new_jobs if job['id'] in ids])
                adzuna_jobs.extend(new_jobs)
                dupl_ratio = len(duplicates) / len(adzuna_jobs)
                print(f'[cyan]=> DUPLICATES RATIO: {dupl_ratio:.2f}[cyan]')
                if dupl_ratio > THRESHOLD:
                    print("\t[orange]EXIT FOR DUPLICATES[/orange]")
                    print(f'\t[yellow]{page - errors} pages succesfully processed.[/yellow]')
                    remaining_calls = 250 - page
                    print(f"\t[yellow]{remaining_calls} remaining calls[/yellow]")
                    
                    return model_adzuna_job_data(adzuna_jobs)           
        # GOING OUT FROM STEP
        n_page += 25  # Updating the first page to begin with
        if step < 10:
            time.sleep(60)  # Going around minute rate limit
            print('*** WAITING FOR 60 S ***')
            
        
    # FULL PROCESS SUM-UP
    print(f'\t[yellow]{n_page - 1 - errors} pages succesfully processed.[/yellow]')
    print(f"\t[yellow]0 remaining calls[/yellow]")
    
    return model_adzuna_job_data(adzuna_jobs)
 
 




if __name__ == '__main__':
    ADZUNA_URL, ADZUNA_ID, ADZUNA_KEY, _, _ = configure()
    
    #
    jobs =  get_adzuna_ads(what='data')
    adzuna_api_list = []
    for job in jobs:
            adzuna_api_list.append(job.model_dump())

    #Generate 100 json files
    nbr_json_files = 100  # Number of output json files
    print("nbr_json_files", nbr_json_files)
    # 50 dumps per file
    chunk_size = len(adzuna_api_list) // nbr_json_files
    
    chunks = [adzuna_api_list[i:i+chunk_size] for i in range(0, len(adzuna_api_list), chunk_size)]
    ts= get_timestamp()
    i = 1
    for data in chunks:
        create_dump(f"data/adzuna_jobs/adzuna_job_{ts}-{i}.json" , data)
        i+=1
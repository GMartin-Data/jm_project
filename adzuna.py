"""
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

from data_models import AdzunaJob, model_adzuna_job_data
from utils import configure, create_client, get_timestamp, timer


def dump_adzuna_jobs(jobs: List[AdzunaJob]) -> None:
    """Dump data selected from Adzuna API response in a JSON file in data folder"""
    ts = get_timestamp()
    dump_path = f'data/adzuna_jobs_{ts}.json'
    # Converting AdzunaJob objects to dumpable dicts with pydantic method
    dumpable_jobs = [job.model_dump() for job in jobs]
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        # `ensure_ascii=False` to force display of non-ascii characters in JSON
        json.dump(dumpable_jobs, dump_file, indent=4, ensure_ascii=False) 
    print(f'\t[cyan]{dump_path} dumped![/cyan]')
    

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
                    
                    return model_adzuna_job_data(adzuna_jobs), remaining_calls            
        # GOING OUT FROM STEP
        n_page += 25  # Updating the first page to begin with
        if step < 10:
            time.sleep(60)  # Going around minute rate limit
            print('*** WAITING FOR 60 S ***')
            
        
    # FULL PROCESS SUM-UP
    print(f'\t[yellow]{n_page - 1 - errors} pages succesfully processed.[/yellow]')
    print(f"\t[yellow]0 remaining calls[/yellow]")
    
    return model_adzuna_job_data(adzuna_jobs), 0
 
 
@timer
def get_adzuna_cats() -> dict:
    """
    Get categories from Adzuna API.
    Save it, in data folder in a JSON file.
    Return a corresponding dict
    """
    url = f'{ADZUNA_URL}/jobs/fr/categories'
    cli = create_client()
    resp = cli.get(
        url,
        params = {
            'app_id': ADZUNA_ID,
            'app_key': ADZUNA_KEY
        }
    )
    
    resp.raise_for_status()
    cats = resp.json()['results']
    for cat in cats:
        try:
            del cat['__CLASS__']
        except KeyError:
            pass
    
    ts = get_timestamp()
    with open(f'data/adzuna_cats_{ts}.json', 'w', encoding='utf-8') as dump_file:
        # `ensure_ascii` to force display of non-ascii characters
        json.dump(cats, dump_file, indent=4, ensure_ascii=False)
    
    return cats
 

# # 🚸 SHOULD WE KEEP THIS? THIS HAS TO BE REWORKED 🚸
# @timer
# def get_adzuna_locs(cat_tag: str = 'it-jobs') -> dict:
#     """
#     Get salary data for locations in France,
#     corresponding to the default cat_tag 'it-jobs'.
#     Save it, in data folder in a json file.
#     Return a corresponding dict
#     """
#     url = f'{ADZUNA_URL}/jobs/fr/geodata'
#     cli = create_client()
#     resp = cli.get(
#         url,
#         params = {
#             'app_id': ADZUNA_ID,
#             'app_key': ADZUNA_KEY,
#             'category': cat_tag
#         }
#     )
#     resp.raise_for_status()
#     json_resp = resp.json()
    
#     ts = get_timestamp()
#     with open(f'data/adzuna_locs_{cat_tag}_{ts}.json',
#               'w', encoding='utf-8') as dump_file:
#         # `ensure_ascii` to force display of non-ascii characters
#         json.dump(json_resp, dump_file, indent=4, ensure_ascii=False)
    
#     return json_resp


if __name__ == '__main__':
    ADZUNA_URL, ADZUNA_ID, ADZUNA_KEY, _, _ = configure()
    
    # # Test get_adzuna_locs
    # l = get_adzuna_locs()
    # print(l)
    
    # # Test get_adzuna_cats
    # c = get_adzuna_cats()
    # print(c)
    
    # Test get_adzuna_ads and dump_adzuna_jobs
    jobs, remaining_calls = get_adzuna_ads(what='data')
    dump_adzuna_jobs(jobs)
    
    # # Test get_adzuna_ads_page
    # cli = create_client()
    # ad = get_adzuna_ads_page(cli, 1, what='data', cat_tag='it-jobs')
    # print(ad) 
    # ts = get_timestamp()
    # dump_path = f'data/adzuna_page_test_{ts}.json'
    # with open(dump_path, 'w', encoding='utf-8') as dump_file:
    #     # `ensure_ascii=False` to force display of non-ascii characters in JSON
    #     json.dump(ad, dump_file, indent=4, ensure_ascii=False) 
    # print(f'\t[cyan]{dump_path} dumped![/cyan]')

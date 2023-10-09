"""
This module contains logic to extract data from Adzuna API.
Endpoints already implemented are those corresponding to
- ads
- categories,
- locations
"""


import json
import time

import httpx
from rich import print

from utils import configure, create_client, get_timestamp, timer


@timer
def get_adzuna_ads_page(client: httpx.Client,
                        page: int,
                        cat_tag: str = 'it-jobs'):  # Update output annotation
    """
    Get the 50 results of one page from Azuna API.
    """
    url = f'{ADZUNA_URL}/jobs/fr/search/{page}'
    
    resp = client.get(
        url,
        params = {
            'app_id': ADZUNA_ID,
            'app_key': ADZUNA_KEY,
            'results_per_page': 50,
            'category': cat_tag 
        }
    )
    resp.raise_for_status()
    return resp.json()['results']
    

@timer
def get_adzuna_ads(cat_tag: str = 'it-jobs',
                   nb_pages: int = 25) -> None:
    """
    Get all job ads from Adzuna API.
    The rate limit enforces 25 requests per minute
    """
    cli = create_client()
    adzuna_jobs = {}
    adzuna_jobs['results'] = []
    errors = 0
    
    # Query Loop    
    for page in range(1, nb_pages + 1):    
        try:
            adzuna_jobs['results'].extend(get_adzuna_ads_page(cli, page, cat_tag))
            print(f'Page {page} PROCESSED')
        except BaseException as e:
            print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
            errors += 1
    print(f'\t[yellow]{nb_pages - errors} pages succesfully processed.[/yellow]')

    # Dump Results
    ts = get_timestamp()
    adzuna_jobs['created_at'] = ts
    dump_path = f'data/adzuna_jobs_{ts}.json'
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        # Last parameter `ensure_ascii` to force display of non-ascii characters
        json.dump(adzuna_jobs, dump_file, indent=4, ensure_ascii=False) 
    print(f'\t[cyan]{dump_path} dumped![/cyan]')
    
    return adzuna_jobs


@timer
def get_daily_adzuna_ads(cat_tag: str = 'it-jobs') -> 'JSON':
    """
    Get all job ads from Adzuna API, on a daily basis:
    - the daily rate being 250
    - the number of ads by page being 20
    This corresponds, to the max, to 50 000 ads.    
    """
    cli = create_client()
    adzuna_jobs = {}
    adzuna_jobs['results'] = []
    errors = 0
    n_page = 1
    
    for step in range(1, 11):
        print(f"\t[white]Step {step}[/white]")
        for page in range(n_page, n_page + 25):
            # REQUESTING
            try:
                adzuna_jobs['results'].extend(get_adzuna_ads_page(cli, page, cat_tag))
                print(f'Page {page} PROCESSED')
            except BaseException as e:
                print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
                errors += 1   
        # GOING OUT FROM STEP
        n_page += 25    # Updating number of first page
        time.sleep(61)  # Going around minute rate limit
    
    # SUM-UP
    print(f'\t[yellow]{n_page -1 - errors} pages succesfully processed.[/yellow]')
    
    # DUMPING RESULTS
    ts = get_timestamp()
    adzuna_jobs['created_at'] = ts
    dump_path = f'data/adzuna_jobs_{ts}.json'
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        # `ensure_ascii=False` to force display of non-ascii characters in JSON
        json.dump(adzuna_jobs, dump_file, indent=4, ensure_ascii=False) 
    print(f'\t[cyan]{dump_path} dumped![/cyan]')
    
    return adzuna_jobs


@timer
def get_adzuna_cats() -> dict:
    """
    Get categories from Adzuna.
    Save it, in data folder in a .json file.
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
    
    json_resp = resp.json()
    
    ts = get_timestamp()
    with open(f'data/adzuna_cats_{ts}.json',
              'w', encoding='utf-8') as resp_file:
        # Last parameter `ensure_ascii` to force display of non-ascii characters
        json.dump(json_resp, resp_file, indent=4, ensure_ascii=False)
        
    # print(f'[yellow]{resp.headers}[/yellow]')
    
    return json_resp
    

@timer
def get_adzuna_locs(cat_tag: str = 'it-jobs') -> dict:
    """
    Get salary data for locations in France,
    corresponding to the default cat_tag 'it-jobs'.
    Save it, in data folder in a json file.
    Return a corresponding dict
    """
    url = f'{ADZUNA_URL}/jobs/fr/geodata'
    cli = create_client()
    resp = cli.get(
        url,
        params = {
            'app_id': ADZUNA_ID,
            'app_key': ADZUNA_KEY,
            'category': cat_tag
        }
    )
    resp.raise_for_status()
    json_resp = resp.json()
    
    ts = get_timestamp()
    with open(f'data/adzuna_locs_{cat_tag}_{ts}.json',
              'w', encoding='utf-8') as resp_file:
        # Last parameter `ensure_ascii` to force display of non-ascii characters
        json.dump(json_resp, resp_file, indent=4, ensure_ascii=False)
        
    # print(f'[yellow]{resp.headers}[/yellow]')
    
    return json_resp


if __name__ == '__main__':
    ADZUNA_URL, ADZUNA_ID, ADZUNA_KEY, _, _ = configure()  
    
    # Test get_daily_adzuna_ads
    get_daily_adzuna_ads()
    
    # # Test get_adzuna_ads
    # get_adzuna_ads()
    
    # # Test get_adzuna_cats
    # get_adzuna_cats()
    
    # # Test get_adzuna_locs
    # locs = get_adzuna_locs()
    # print(locs)
    # print(type(locs))

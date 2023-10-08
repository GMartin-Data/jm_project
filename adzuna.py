import json
import os

from dotenv import load_dotenv
import httpx
from rich import print

from utils import get_timestamp, timer


def configure() -> None:
    """Set working environment"""
    load_dotenv()
    global ADZUNA_URL, ADZUNA_ID, ADZUNA_KEY
    ADZUNA_URL = os.getenv('adzuna_url')
    ADZUNA_ID = os.getenv('adzuna_id')
    ADZUNA_KEY = os.getenv('adzuna_key')
    
    
def create_client() -> httpx.Client:
    """Create and configure a httpx Client for requesting"""
    c = httpx.Client()
    c.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/116.0.0.0 Safari/537.36',
    })
    return c


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
    configure()  
    
    # # Test get_adzuna_ads
    # get_adzuna_ads()
    
    # # Test get_adzuna_cats
    # get_adzuna_cats()
    
    # Test get_adzuna_locs
    locs = get_adzuna_locs()
    print(locs)
    print(type(locs))

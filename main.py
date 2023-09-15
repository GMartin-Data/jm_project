import json
import os

from dotenv import load_dotenv
import httpx
from rich import print

from utils import get_timestamp


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


def get_adzuna_cats() -> None:
    """
    Display categories from Adzuna.
    Save it, in data folder in a .json file.
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
    print(json_resp)
    
    ts = get_timestamp()
    with open(f'data/adzuna_cats_{ts}.json', 'w') as resp_file:
        json.dump(json_resp, resp_file, indent=4)
        
    print(f'[white]{resp.headers}[/white]')
    
    
def get_adzuna_ads(nb_res: int = 100,
                   cat_tag: str = 'it-jobs') -> None:
    """
    Display job ads from Adzuna API.
    Save it, in data folder in a .json file.
    
    Params:
        nb_res (int)    : the number of results displayed
        cat_tag (str)   : the API category tag
    """
    url = f'{ADZUNA_URL}/jobs/fr/search/1'
    cli = create_client()
    resp = cli.get(
        url,
        params = {
            'app_id': ADZUNA_ID,
            'app_key': ADZUNA_KEY,
            'results_per_page': nb_res,
            'category': cat_tag 
        }
    )
    
    json_resp = resp.json()
    print(json_resp)
    
    ts = get_timestamp()
    filepath = f'data/adzuna_ads_{cat_tag}_{nb_res}_{ts}.json'
    with open(filepath, 'w') as resp_file:
        json.dump(json_resp, resp_file, indent=4)
        
    print(f'[white]{resp.headers}[/white]')
    

if __name__ == '__main__':
    configure()
    get_adzuna_ads() 

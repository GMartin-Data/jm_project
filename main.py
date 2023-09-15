import json
import os

from dotenv import load_dotenv
import httpx
from rich import print


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
    # print(f'[green]{json_resp}[/green]')
    with open('data/adzuna_cats.json', 'w') as resp_file:
        json.dump(json_resp, resp_file, indent=4)
    print(f'[white]{resp.headers}[/white]')
    

if __name__ == '__main__':
    configure()
    get_adzuna_cats() 

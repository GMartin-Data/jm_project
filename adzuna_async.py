"""
⚠️ 'FROZEN' MODULE
This module contains logic to extract data from The Muse API.
It was at first envisioned with implementing asynchronous requests.
As the Adzuna's API rate limiter is rather high, 
this module has been kept aside for the moment.

It should even at first get it's code factorized,
especially moving to utils a `create_async_client()` function.
"""


import asyncio
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
    
    
def create_client() -> httpx.AsyncClient:
    """Create and configure a httpx AsyncClient for requesting"""
    c = httpx.AsyncClient()
    c.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/116.0.0.0 Safari/537.36',
    })
    return c


async def get_adzuna_ads_page(client: httpx.AsyncClient,
                              url: str,
                              cat_tag: str) -> json:
    """
    Get the 50 results of one page from Azuna API.
    """
    resp = await client.get(
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
    

async def get_adzuna_ads(cat_tag: str = 'it-jobs',
                         nb_pages: int = 25) -> None:
    """
    Get all job ads from Adzuna API.
    """
    cli = create_client()
    async with cli:
        tasks = []
        errors = 0
        
        for page in range(1, nb_pages + 1):
            url = f'{ADZUNA_URL}/jobs/fr/search/{page}'
            try:
                tasks.append(get_adzuna_ads_page(cli, url, cat_tag))
            except BaseException as e:
                print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
                errors += 1
        print(f'[green]{nb_pages - errors} pages succesfully processed.[/green]')
        
        results = await asyncio.gather(*tasks)
        
        print(type(results))


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
    
    return json_resp
    

if __name__ == '__main__':
    configure()
    asyncio.run(get_adzuna_ads())

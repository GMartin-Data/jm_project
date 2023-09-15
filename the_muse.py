import json
import os
from typing import List, Optional

from dotenv import load_dotenv
import httpx
from rich import print

from utils import get_timestamp


CHOSEN_CATS = ['Computer and IT', 'IT',
               'Data and Analytics', 'Data Science',
               'Design and UX', 'UX',
               'Software Engineer', 'Software Engineering']


def configure() -> None:
    """Set working environment"""
    load_dotenv()
    global MUSE_KEY, MUSE_URL
    MUSE_KEY = os.getenv('muse_key')
    MUSE_URL = os.getenv('muse_url')
    

def create_client() -> httpx.Client:
    """Create a httpx Client, with configured headers"""
    c = httpx.Client()
    c.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': os.getenv('user_agent')
        })
    return c


def get_muse_jobs_page(client: httpx.Client,
                       page: int,
                       category: List[str],
                       company: Optional[List[str]] = None,
                       level: Optional[List[str]] = None,
                       location: Optional[List[str]] = None):
    """Get the 20 job results of one page from The Muse API"""
    base_params = {
            'api_key': MUSE_KEY,
            'page': page,
            'category': category, 
        }
    # Didn't find anything smarter for optional parameters update
    if company:
        base_params.update({'company': company})
    if level:
        base_params.update({'level': level})
    if location:
        base_params.update({'location': location})
    
    
    resp = client.get(
        MUSE_URL,
        params = base_params
    )
    resp.raise_for_status()
    json_resp = resp.json()
    
    print(json_resp['page_count'])
    print(f'[red]{resp.headers}[/red]')
    
    return json_resp
    

if __name__ == '__main__':
    configure()
    print(f'{MUSE_KEY = }')
    print(f'{MUSE_URL = }')
    cli = create_client()
    get_muse_jobs_page(cli, 1, CHOSEN_CATS)

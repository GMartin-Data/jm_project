import json
from typing import List, Optional

import httpx
from rich import print

from utils import configure, create_client, get_timestamp, timer


# (CONFIG) CONSTANTS
CHOSEN_CATS = ['Computer and IT', 'IT',
               'Data and Analytics', 'Data Science',
               'Design and UX', 'UX',
               'Software Engineer', 'Software Engineering']

with open('config_data/muse_towns_fr.json', 'r',
          encoding='utf-8') as read_file:
    MUSE_TOWNS_FR = json.load(read_file)


def get_muse_jobs_page(client: httpx.Client,
                       page: int,
                       category: List[str],
                       company: Optional[List[str]] = None,
                       level: Optional[List[str]] = None,
                       location: Optional[List[str]] = None): # Check type hint for JSON
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
    
    # print(f'[red]{resp.headers}[/red]')  # Logging headers
    
    return json_resp
    

@timer
def get_muse_jobs(category: List[str],
                  company: Optional[List[str]] = None,
                  level: Optional[List[str]] = None,
                  location: Optional[List[str]] = None):
    """
    Get all jobs from The Muse API
    """
    cli = create_client()
    muse_jobs = {}
    muse_jobs['results'] = []
    errors = 0
    
    # Initial request to set work
    # It seems there's a problem with loading pages after 99...
    # Temporary solution
    nb_pages = min(get_muse_jobs_page(cli, 1, category, level, location)['page_count'], 100)
    print(f'\t[white]Number of pages to proceed: {nb_pages}[/white]')
    
    # Query Loop
    for page in range(1, nb_pages + 1):
        try:
            muse_jobs['results'].extend(
                get_muse_jobs_page(cli, page, category, level, location)['results']
            )
            print(f'[green]Page {page} successfully proceeded[/green]')
        except BaseException as e:
            print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
            errors += 1
    print(f'\t[yellow]{nb_pages - errors} pages succesfully processed.[/yellow]')
    
    # Dump results
    ts = get_timestamp()
    muse_jobs['created_at'] = ts
    dump_path = f'data/the_muse_jobs_{ts}.json'
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        json.dump(muse_jobs, dump_file, indent=4, ensure_ascii=False)
    print(f'\t[cyan]{dump_path} dumped![/cyan]')
        
    return muse_jobs
    

if __name__ == '__main__':
    # Setup
    _, _, _, MUSE_KEY, MUSE_URL = configure()
    
    # # Testing get_muse_jods_page
    # c = create_client()
    # jobs = get_muse_jobs_page(c, 1, CHOSEN_CATS, location=MUSE_TOWNS_FR)
    # print(jobs)
    
    # Testing get_muse_jobs
    get_muse_jobs(CHOSEN_CATS, location=MUSE_TOWNS_FR)
    
    print("SUCCESS!")

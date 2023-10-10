"""
This module is designed to get the different urls
involved based on Adzuna API's response:
- the inner Adzuna url,
- the Hellowork page url.
"""


import json
import time

from bs4 import BeautifulSoup
import numpy as np
from rich import print

from utils import create_client, forge_adzuna_url, forge_hellowork_url, get_timestamp


# Loading dump
with open('data/adzuna_jobs_2023-10-09-11:26:07.json', 'r') as read_file:
     jobs = json.load(read_file)['results']

adzuna_url_jobs = []

for idx, job in enumerate(jobs[:10], 1):
    job_id = job['id']
    red_url = job['redirect_url']
    adzuna_url = forge_adzuna_url(red_url)
    
    # Requesting red_url to get the real HelloWork page
    cli = create_client()
    resp = cli.get(red_url)
    html = BeautifulSoup(resp.text, 'html.parser')
    try:
        ugly_url = (html
                    .find_all('meta')
                    [-1]
                    .attrs['content']
                    .split('https')
                    [-1]
                    )
        hellowork_url = forge_hellowork_url(ugly_url)
        print(f'Step {idx}: urls successfully generated')
    except BaseException as e:
        print(f'[red]Step {idx}: Exception {type(e)} for url {red_url}[/red]')
        hellowork_url = None
    adzuna_url_jobs.append({
        'id': job_id,
        'adzuna_url': adzuna_url,
        'hellowork_url': hellowork_url
    })
        
    # Temporizing next request
    pause = 3 + 4 * np.random.rand()
    print(f'\t[yellow]Gonna wait for {pause:.1f} seconds...')
    time.sleep(pause)
    
# Dumping results
ts = get_timestamp()
dump_path = f'data/adzuna_url_jobs_{ts}.json'
with open(dump_path, 'w', encoding='utf-8') as dump_file:
    json.dump(adzuna_url_jobs, dump_file, indent=4, ensure_ascii=False) 
print(f'\t[cyan]{dump_path} dumped![/cyan]')   
   
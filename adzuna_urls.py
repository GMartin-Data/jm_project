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

# When called, the file will ask the use for a path to the json dump of job vacancies collected adzuna.py
ads_api_path = input("Please provide the file path to the latest Adzuna jobs dump\n")

with open(ads_api_path, 'r') as read_file:
     jobs = json.load(read_file)

adzuna_url_jobs = []

for idx, job in enumerate(jobs[:50], 1):
    job_id = job['id']
    red_url = job['redirect_url']
    adzuna_url, is_redirected = forge_adzuna_url(red_url)
    
    if is_redirected:
        # Requesting red_url to get the Job Board's page,
        # Which is named hellowork_url as this is often the case.
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
            print(f'[green]Step {idx}: Redirection - Both urls successfully generated[/green]')
            # Temporizing before next request
            pause = 3 + 4 * np.random.rand()
            print(f'\t[yellow]Gonna wait for {pause:.1f} seconds...')
            time.sleep(pause)
        except BaseException as e:
            print(f'[red]Step {idx}: Exception {type(e)} for url {red_url}[/red]')
            hellowork_url = None
    else:
        print(f'[#F3B664]Step {idx}: No redirection - Only adzuna_url generated[/#F3B664]')
        hellowork_url = None
    
    adzuna_url_jobs.append({
        'id': job_id,
        'adzuna_url': adzuna_url,
        'hellowork_url': hellowork_url
    })

    
# Dumping results
# ts = get_timestamp()
ads_api_path_no_json = ads_api_path.split(".")[0]
dump_path = f'{ads_api_path}_urls_1.json'
with open(dump_path, 'w', encoding='utf-8') as dump_file:
    json.dump(adzuna_url_jobs, dump_file, indent=4, ensure_ascii=False) 
print(f'\t[cyan]{dump_path} dumped![/cyan]')   
   
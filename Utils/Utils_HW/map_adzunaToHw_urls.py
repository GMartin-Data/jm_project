"""
This module is designed to get the different urls
involved based on Adzuna API's response:
- the inner Adzuna url,
- the Hellowork page url.
"""

import re
from bs4 import BeautifulSoup
import httpx
import numpy as np
from rich import print
from Utils.Utils_Global import create_client


BASE = 'https://www.adzuna.fr/details/'  # Used in forge_adzuna_url
URL_MAPPING = {
    '%3A': ':',
    '%2F': '/',
    '%3F': '?',
    '%3D': '=',
    '%26': '&'
}  # Used in forge_hellowork_url


def forge_adzuna_url(redirect_url: str) -> str:
    """
    Transforms a redirecting unscrapable url
    to an unredirecting scrapable one
    """
    _, api, source, _ = redirect_url.split('&')
    id_ = re.search(r'\d{10}\?', redirect_url).group()
    new_url = BASE + id_ + '&'.join([api, source])

    return new_url


def forge_hellowork_url(url: str) -> str:
    '''
    Utility function to retrieve proper HelloWork url
    from a scraped string gotten from an AJAX request.
    '''
    for k, v in URL_MAPPING.items():
        url = url.replace(k, v)
    return 'https' + url
   
def get_hw_text(url: str):
    headers = {
                "Content-Type": "application/json",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                    AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/116.0.0.0 Safari/537.36',
            }
     
    resp = httpx.get(url, headers=headers)
    if resp.status_code == 200:
        return resp
    else:
        print(f"Erreur de requête sur l'url {url} : {resp.status_code}")
        return None

def get_HW_Url(job_id : str, redirect_url : str, env) -> str:

    adzuna_url = forge_adzuna_url(redirect_url)

    resp = get_hw_text(redirect_url)
    if(resp is not None):
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
            return hellowork_url
        except BaseException as e:
            print(f'[red]Exception {type(e)} for url {redirect_url}[/red]')
            hellowork_url = None
            return hellowork_url
    
    


   
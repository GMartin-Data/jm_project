"""
This module sums up different utilities used in the project,
helping to factorize the code.
This includes:
- client configuration and creation with httpx,
- timestamp creation for file logging/naming,
- timer to benchmark code.
"""


from datetime import datetime
import functools
import os
import re
import time
from typing import Tuple

from dotenv import load_dotenv
import httpx


BASE = 'https://www.adzuna.fr/details/'  # Used in forge_adzuna_url
URL_MAPPING = {
    '%3A': ':',
    '%2F': '/',
    '%3F': '?',
    '%3D': '=',
    '%26': '&'
}  # Used in forge_hellowork_url


def configure() -> None:
    """Set working environment"""
    load_dotenv()
    ADZUNA_URL = os.getenv('adzuna_url')
    ADZUNA_ID = os.getenv('adzuna_id')
    ADZUNA_KEY = os.getenv('adzuna_key')
    MUSE_KEY = os.getenv('muse_key')
    MUSE_URL = os.getenv('muse_url')
    return ADZUNA_URL, ADZUNA_ID, ADZUNA_KEY, MUSE_KEY, MUSE_URL
    

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


def forge_adzuna_url(redirect_url: str) -> Tuple[str, bool]:
    """
    Params
    ------
        redirect_url: corresponding to this field in Adzuna API's ad response
    Returns
    -------
    A tuple containing:
        - The URL of the ads webpage, being either Adzuna's one or a Job Board's one
        - A boolean indicating if there's a redirection or not.
    """
    try:
        # In this case, there's a redirection to another Job Board
        _, api, source, _ = redirect_url.split('&')
        id_ = re.search(r'\d{10}\?', redirect_url).group()
        new_url = BASE + id_ + '&'.join([api, source])
        return new_url, True
    
    except ValueError:
        # In this case, redirect_url is Adzuna's page
        # The API's terminology is poor as there's in fact NO redirection
        return redirect_url, False


def forge_hellowork_url(url: str) -> str:
    '''
    Utility function to retrieve proper HelloWork url
    from a scraped string gotten from an AJAX request.
    '''
    for k, v in URL_MAPPING.items():
        url = url.replace(k, v)
    return 'https' + url
   

def get_timestamp():
    """Help for file horodating"""
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


def timer(func):
  """Print the runtime of the decorated function"""
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    # Before
    start_time = time.perf_counter()
    # Calling the function and storing value to return
    value = func(*args, **kwargs)
    # After
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f"Finished {func.__name__!r} in {run_time: .4f} seconds.")
    return value
  return wrapper_timer

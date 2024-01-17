import datetime
from urllib.parse import urlparse
import httpx
from rich import print

def create_client(env) -> httpx.Client:
    """Create and configure a httpx Client for requesting"""
    c = httpx.Client()
    c.headers.update({
        'Content-Type': 'application/json',
        'User-Agent':  env['Global.USER_AGENT'] 
    })
    return c

def get_timestamp():
    """Help for file horodating"""
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

def eq_netloc(url : str, cible : str) -> bool:
    """Validating  url"""
    parts = urlparse(url)
    return parts.netloc == cible 
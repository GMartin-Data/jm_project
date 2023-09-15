import json
import os

from dotenv import load_dotenv
import httpx
from rich import print

from utils import get_timestamp


def configure() -> None:
    """Set working environment"""
    load_dotenv()
    global MUSE_PARAMS
    MUSE_PARAMS = {
        'api_key': os.getenv('muse_key')
        }
    

def create_client() -> httpx.Client:
    """Create a httpx Client, with configured headers"""
    c = httpx.Client()
    c.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': os.getenv('user_agent')
        })

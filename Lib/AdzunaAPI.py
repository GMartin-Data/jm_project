import os
import httpx
from rich import print

class AdzunaAPI:
    _instance = None

    def __new__(cls, env):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.url = env['API_ADZUNA.url']   
            cls._instance.app_id = env['API_ADZUNA.app_id'] 
            cls._instance.app_key = env['API_ADZUNA.app_key'] 

            cls._instance.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            cls._instance.params = {
                "app_id": env['API_ADZUNA.app_id'] ,
                "app_key": env['API_ADZUNA.app_key'],
                "results_per_page": env['API_ADZUNA.results_per_page'],
                "category":env['API_ADZUNA.category'],
                "what": env['API_ADZUNA.what']
            }
        return cls._instance

    def get_jobs(self, page):
        url = f'{self.url}/{page}'
        response = httpx.get(url, headers=self.headers, params=self.params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur de requête à la page {page} des offres d'emploi: {response.status_code}")
            return None
        
    
    
    
                
                
   
        

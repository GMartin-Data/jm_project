"""
@author: Greg 
@code-reviewer: lnasri

This module is created to obtain the URL of the
Hellowork page based on the Adzuna API response. 
If a Hellowork URL is available, a dumps is created 
containing all the Hellowork page information. 
Otherwise, dumps are generated from the Adzuna API data.

"""

import time
from GenAdzunaJobs import *
from GenHWJobs import * 
from data_models import *
from bs4 import BeautifulSoup
import numpy as np
from rich import print
from utils import *
from pathlib import Path


def gen_jobs(adzuna_jobs_path, all_jobs_fname):
    """In this function, we scan the azuna_jobs file directory, 
       then process a single file of 50 dumps.
       This process checks the existence of the hellowork url.

    Args:
        adzuna_jobs_path (str): path to the adzuna_jobs file directory 
        all_jobs_fname (list): a list of file names in the all_jobs directory.
                               

    Returns:
        tuple: liste of adzuna dumps, file name processed
    """
    

    # List of dictionaries, containing all adzuna api informations + 
    # Hellowork url + the name of the file to be processed
    adzuna_url_jobs = []

    # contains a single name from the azuna api json file
    adzuna_jobs_fname = []
   
    print(all_jobs_fname)
    for i in adzuna_jobs_path.iterdir():
        if os.path.exists(i):

            if len(adzuna_jobs_fname) >= 1:
                break

            elif i.name not in all_jobs_fname:
                adzuna_jobs_fname.append(i.name)
                with open(i, encoding="utf-8") as infile:
                    json_data_adzuna = json.load(infile)
                    for data in json_data_adzuna:
                        Id =  data['id']
                        red_url = data["redirect_url"] 
                        adzuna_url, is_redirected = forge_adzuna_url(red_url)
                        print(is_redirected)
                
                        if is_redirected == True:
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
                                print(hellowork_url)
                                print(f'[green]Step : Redirection - Both urls successfully generated[/green]')
                                # Temporizing before next request
                                pause = 3 + 4 * np.random.rand()
                                print(f'\t[yellow]Gonna wait for {pause:.1f} seconds...')
                                time.sleep(pause)
                            except BaseException as e:
                                print(f'[red]Step : Exception {type(e)} for url {red_url}[/red]')
                                hellowork_url = None
                        else:
                            print(f'[#F3B664]Step : No redirection - Only adzuna_url generated[/#F3B664]')
                            hellowork_url = None
                        
                        adzuna_url_jobs.append({
                        'id': Id,
                        'hellowork_url': hellowork_url,
                        'file_name' : i.name,
                        'title': data["title"] ,
                        'redirect_url': data["redirect_url"] ,
                        'company': data["company"] ,
                        'created': data["created"] ,
                        'area': data["area"] ,
                        'latitude': data["latitude"] ,
                        'longitude': data["longitude"] ,
                        'location': data["location"] ,
                        'contract': data["contract"] ,
                        'education': None,
                        'duration' :None,
                        'remote' : None,
                        'experience': None,
                        'salary_min': data["salary_min"] ,
                        'salary_max': data["salary_max"] ,
                        'salary' :None,
                        'salary_min_e' : None,
                        'salary_med_e' :None,
                        'salary_max_e' :None,
                        'description': data["description"] 
                        })
                
                     
    return adzuna_url_jobs, adzuna_jobs_fname[0]
       
        
if __name__ == "__main__":
    #
    adzuna_jobs_path = Path("/data/adzuna_jobs")  
    #
    all_jobs_path = Path("/data/all_jobs")
    #
    all_jobs_fname = [j.name for j in all_jobs_path.iterdir()]
    #
    jobs, file_name = gen_jobs(adzuna_jobs_path, all_jobs_fname)
    #
    liste_all_data = []
    
    for data in jobs:
        Id =  data['id']
        hellowork_url = data["hellowork_url"]  
        if IsValidHwUrl(hellowork_url).eq_netloc():
            model = scrape_hw_page(Id, hellowork_url, data)
            # print(model)
            if model is not None:
                liste_all_data.append(model.model_dump())
                time.sleep(2)
        else:
            liste_all_data.append(data)
             
    #Create dump         
    create_dump(f"/data/all_jobs/{file_name}", liste_all_data)















import time
from dotenv import load_dotenv
from threading import Timer
from Lib.AdzunaAPI import *
from Lib.HelloWorkScraper import *
from Models.AdzunaJob import *
from Utils.Utils_HW.map_adzunaToHw_urls import *
from Savers.json_dump import *
from rich import print
from envyaml import EnvYAML

# Fonction pour récupérer toutes les offres d'emploi

def get_all_jobs(env):

    adzuna_api = AdzunaAPI(env)
    scraper = HelloWorkScraper(env)

    
    jobs = []
    jobsToStore = []
    errors = 0
    n_page = 1
    nbr_pages = int(env['API_ADZUNA.nbr_pages'])
    nbr_steps = (2 if nbr_pages <= 25 else (nbr_pages//25)+1)
    for step in range(1, nbr_steps):
        
        print(f"\t[white]Step {step}[/white]")

        for page in range(n_page, n_page + 25):
            if page > nbr_pages :
                break
            # REQUESTING
            try:
                data = adzuna_api.get_jobs(page)
                if data is None or "results" not in data:
                    break
                new_jobs = [AdzunaJob(id= job["id"],
                                title=job["title"], 
                                redirect_url=job["redirect_url"],
                                company = job["company"]["display_name"],
                                created = job["created"]
                                ) for job in data["results"] if job not in jobs]
                for job in new_jobs:
                    redirect_url = job.redirect_url
                    id = job.id
                    time.sleep(30)
                    hw_url = get_HW_Url(id, redirect_url, env)

                    if hw_url is not None:
                        job_details = scraper.get_job_details(hw_url,job)
                        jobsToStore.append(job_details)
                        #job.__dict__.update(job_details)
                #jobs.extend(new_jobs)
                    
                print(f'Page {page} PROCESSED')
            except BaseException as e:
                print(f'[red]{type(e)}: Exception {e} occured![/red] on page {page}')
                errors += 1  
        n_page += 25    # Updating number of first page
        time.sleep(61)  # Going around minute rate limit

    #SUM-UP
    print(f'\t[yellow]{page -1 - errors} pages succesfully processed.[/yellow]')

    dict_jobs = [vars(obj) for obj in  jobsToStore]

    return dict_jobs

#ingest.py rename file 
def main():

    # read file env.yaml and parse config
    env = EnvYAML(os.path.realpath(os.path.join(os.path.dirname(__file__)  ,'env.yaml')),os.path.realpath(os.path.join(os.path.dirname(__file__)  ,'.env')))

    # Stocker les objets dans une liste
    all_jobs = get_all_jobs(env)

    #Dump to file
    json_Dump(all_jobs, env)

    #end
    print("END")
    

if __name__ == "__main__":
    main()


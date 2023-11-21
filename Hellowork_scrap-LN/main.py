
""" 
created on 17/11/2023 17:27
@author: lnasri

main.py is the main file, which you can use to test the application.
Run this file and you will see the JSON result in the data folder.

Firstly, you should add a url path, for example 
urls_path= "/Users/your_folder/adzuna_url_jobs.json"  
"""

from data import *
import os
from hellowork_scrap import hellowork_scrap


if __name__ == "__main__":
    #create an empty list to store dictionaries
    liste_data= []
    #Add urls file path 
    urls_path= "/Users/your_folder/adzuna_url_jobs.json" 
    #dump name
    dump_path= "data/adzuna_url_jobs.json"
    #load urls file path
    if os.path.exists(urls_path) :  
        with open(urls_path, encoding="utf-8") as infile:
            json_data_adzuna= json.load(infile)
            for data in range(len(json_data_adzuna)):
                Id= json_data_adzuna[data]['id']
                hellowork_url= json_data_adzuna[data]["hellowork_url"] 
                # add dictionary data to the liste
                liste_data.append(hellowork_scrap( hellowork_url, Id))
    #Create dump         
    create_dump(dump_path, liste_data)
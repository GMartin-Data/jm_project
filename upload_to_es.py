"""
This python script shows how to upload adzuna data to an elasticsearch database.
The steps are:
- Read in the adzuna data obtained from web-scraping
- create an index in elasticsearch (or check if one exists - up to you)
- upload data to the index
"""

#! /usr/bin/python

import json
from elasticsearch import Elasticsearch, helpers
from typing import List, Dict
from es_utils import delete_and_create_index, upload_jobs_to_es

# REMEMBER TO MODIFY THIS PATH:
path_to_dump = 'data/flow/hellowork_scrap_2023-11-24_3.json'

# Loading dump
with open(path_to_dump, 'r') as read_file:
     jobs = json.load(read_file)


# Connect to cluster
es = Elasticsearch(hosts = "http://elasticsearch:9200")

# Create a new index called jm_test. If it already exists, delete and recreate it.
# REMEMBER: if you don't want to delete an existing index, simply change: overwrite = False
delete_and_create_index(elasticsearch_connexion = es,
                        index_name = "jm_test",
                       overwrite = True)



# Upload the job vacancy data to the index
upload_jobs_to_es(elasticsearch_connexion = es, 
                  index_name = "jm_test", 
                  jobs_list = jobs)




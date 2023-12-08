"""
This module contains functions used to interact with the elasticsearch database. 
It includes:
- creating an index,
- uploading data to the index
- basic text queries to the index
"""

from elasticsearch import Elasticsearch, helpers
from typing import List, Dict


def delete_and_create_index(elasticsearch_connexion: Elasticsearch,
                            index_name: str,
                           overwrite: bool = False):
    """
    A function to create an index in elasticsearch. The function first checks if the index already exists.
    If user chooses overwrite == True, then it will delete the index, and recreate it.
    """

    if elasticsearch_connexion.indices.exists(index = index_name):

        n_docs_old = elasticsearch_connexion.count(index = index_name)["count"]
        print(f"Index {index_name} already exists with {n_docs_old} documents")

        if overwrite == True:
            elasticsearch_connexion.indices.delete(index = index_name)

            if elasticsearch_connexion.indices.exists(index = index_name) == False:
                print(f"Index {index_name} has been successfully deleted")
                elasticsearch_connexion.indices.create(index = index_name)
                n_docs_new = elasticsearch_connexion.count(index = index_name)["count"]
                print(f"Index {index_name} was successfully recreated and contains {n_docs_new} documents")
                
            else:
                print(f"Index {index_name} still exists. Deletion has failed, and index will not be recreated")
        else:
            print(f"User chose not to overwrite. Index {index_name} will not be deleted")





def upload_jobs_to_es(elasticsearch_connexion: Elasticsearch,
                      index_name: str,
                      jobs_list = List[Dict]):
    """
    A function to upload a list of job vacancy data to an elasticsearch index. 
    Note that the input requires a list of dictionaries.
    After upload, the function checks that the ids of the job vacancies are in the database 
    (although this doesn't currently account for duplicate ids)
    """

    print(f"{len(jobs_list)} new jobs from dump to upload to elasticsearch")
    
    helpers.bulk(elasticsearch_connexion, jobs_list, index = index_name)
    
    new_ids = [job["id"] for job in jobs_list]
    
    uploaded_query = {
    "query": {
        "bool": {
            "filter": {
                "terms": {"id": new_ids}
                }
            }
        }
    }
    
    upload_check_resp = elasticsearch_connexion.count(index = index_name, body = uploaded_query)

    n_uploaded = upload_check_resp["count"]
    
    print(f"{n_uploaded} jobs were effectively uploaded")   



def query_index(elasticsearch_connexion: Elasticsearch,
                query_term: str,
                field_name: str,
                index_name: str = 'jm_test'):
    """
    A function to count the number of documents in a given elasticsearch index that contains a specific string
    """
    my_query = {
        "match": {
            field_name: {
                "query": query_term
                }
        }
    }

    resp = elasticsearch_connexion.count(index = index_name, query = my_query)

    return resp["count"]



    
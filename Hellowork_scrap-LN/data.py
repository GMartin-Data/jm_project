from pymongo import MongoClient
import json
from hellowork_scrap import *



def create_db(data, db_name, db_col):
    """Create Mongodb database"""
    
    #Connexion MongoDB 
    client = MongoClient()
    
    db = client[db_name]
    print("Database is created !!")

    #Created or Switched to collection
    Collection = db[db_col]

    #Loading or Opening the json file
 
    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else insert_one is used
    if isinstance(data, list):
        Collection.insert_many(data) 
    else:
        Collection.insert_one(data)


def create_dict(Id, hellowork_url):
     #create data in dictionary format
    salry = salary(hellowork_url)
    dictionnaire = {"id": Id,  
                    "hellowork_url": hellowork_url,
                    "contract_type": contract_type_items(hellowork_url),
                    "Experience": expe_level_items(hellowork_url),
                    "Niveau_etude": study_level_items(hellowork_url), 
                    "city": city(hellowork_url), 
                    "dep": departement(hellowork_url),
                    "salary_min": salry[0]  if salry is not None else None ,
                    "salary_max": salry[1] if salry is not None else None
                    }  
    return  dictionnaire  

        
def create_dump(dump_path, data):
    
    dump_file = open(dump_path, 'w', encoding='utf-8') 
    json.dump(data, dump_file, indent=4, ensure_ascii=False) 


"""
    Generate output data
"""

from pymongo import MongoClient
import json

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

      
def create_dump(dump_path, data):
    """Create dump"""
    with open(dump_path, 'w', encoding='utf-8') as dump_file:
        json.dump(data, dump_file, indent=4, ensure_ascii=False) 
    
   
    


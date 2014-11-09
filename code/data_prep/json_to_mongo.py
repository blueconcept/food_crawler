from pymongo import MongoClient
import numpy as np
import pandas as pd
import json

def read_json(file_name):
    '''
    INPUT: String
    DESCRIPTION: Opens the json file and reads all of the json lines into a list
    OUTPUT: List
    '''
    with open(file_name, 'r') as fh:
        list_json = fh.readlines()
    return list_json

def load_json_to_mongo(file_name, db_name, collection_name):
    '''
    INPUT: String, String, String
    DESCRIPTION: Converts json file to mongodb
    OUTPUT: None
    '''
    list_of_json = read_json(file_name)
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    for json_item in list_of_json:
        doc = json.loads(json_item)
        collection.insert(doc)
        
def main():
    '''
    INPUT: None
    DESCRIPTION: setups the loading of json into mongo
    OUTPUT: None
    '''
    json_files = {"businesses":"business.json","reviews":"review.json","users":"user.json"}
    database = "foodcrawler"
    for collection, json_file in json_files.iteritems():
        load_json_to_mongo(json_file, database, collection)

if __name__ == '__main__':
    main()
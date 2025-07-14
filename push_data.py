import os
import sys
import json
import certifi
import pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from networksecurity.logging import logger
from networksecurity.exception import NetworkSecurityException

load_dotenv()

uri = os.getenv("MONGO_DB_URI")
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def cv_to_json_convertor(self, file):
        try:
            data = pd.read_csv(file)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logger.info(f"Data extracted from {file} and converted to JSON format")
            print(f"Data extracted from {file} and converted to JSON format")
            
            return records
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def push_data_to_mongo(self,records,database,collection):
        try:
            self.records = records
            self.database = database
            self.collection = collection
            
            self.client = pymongo.MongoClient(uri, tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            
            logger.info(f"Data pushed to MongoDB collection: {self.collection.name} in database: {self.database.name}")
            print(f"Data pushed to MongoDB collection: {self.collection.name} in database: {self.database.name}")
            
            return len(self.records)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    try:
        file = "Network_data\phisingData.csv"
        database = "network_security"
        collection = "network_data"
        
        extractor = NetworkDataExtract()
        records = extractor.cv_to_json_convertor(file)
        count = extractor.push_data_to_mongo(records, database, collection)
        
        print(f"Total records pushed: {count}")
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
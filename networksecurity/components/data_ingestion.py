from networksecurity.logging import logger
from networksecurity.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_from_mongo(self):
        """
        Export data from MongoDB collection to a pandas DataFrame.
        This method retrieves data from the specified MongoDB collection and converts it into a pandas DataFrame
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            collection = self.mongo_client[database_name][collection_name]

            data = pd.DataFrame(list(collection.find()))
            
            #if not data:
                #raise NetworkSecurityException("No data found in the MongoDB collection", sys)
            
            if "_id" in data.columns:
                data.drop(columns=["_id"], inplace=True)
            
            data.replace({"na":np.nan}, inplace=True)
            
            logger.info(f"Data exported from MongoDB collection: {self.data_ingestion_config.collection_name}")
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, data: pd.DataFrame):
        """
        Export the DataFrame into the feature store directory.
        This method saves the DataFrame to a CSV file in the feature store directory.
        """
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            os.makedirs(os.path.dirname(feature_store_dir), exist_ok=True)
            data.to_csv(feature_store_dir, index=False, header=True)
            
            logger.info(f"Data exported into feature store at: {feature_store_dir}")
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, data: pd.DataFrame):
        """
        Split the DataFrame into training and testing datasets.
        This method splits the data into training and testing sets based on the specified ratio.
        """
        try:
            train_set, test_set = train_test_split(data, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logger.info(f"Data split into train and test sets. Train set saved at: {self.data_ingestion_config.training_file_path}, Test set saved at: {self.data_ingestion_config.testing_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_data_from_mongo()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_data_path=self.data_ingestion_config.training_file_path,
                test_data_path=self.data_ingestion_config.testing_file_path
            )
            
            logger.info(f"Data ingestion artifact created: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
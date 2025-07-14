import os
import sys

"""
    Common Constants
"""

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "network_security_pipeline"
ARTIFACTS_DIR:str = "artifacts"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


"""
    Data ingestion config constants    
"""

DATA_INGESTION_COLLECTION_NAME:str = "network_data"
DATA_INGESTION_DATABASE_NAME:str = "network_security"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2
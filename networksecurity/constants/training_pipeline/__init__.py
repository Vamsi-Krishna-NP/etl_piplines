import os
import sys
import numpy as np

"""
    Common Constants
"""

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "network_security_pipeline"
ARTIFACTS_DIR:str = "artifacts"
FILE_NAME:str = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR:str = os.path.join("saved_model")
MODEL_FILE_NAME:str = "model.pkl"


"""
    Data ingestion config constants    
"""

DATA_INGESTION_COLLECTION_NAME:str = "network_data"
DATA_INGESTION_DATABASE_NAME:str = "network_security"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

"""
    Data validation config constants
"""

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

"""
    Data transformation config constants
"""

DATA_TRANSFOMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessor.pkl"

# knn imputer to replace missing values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    'missing_values': np.nan,
    'n_neighbors': 3,
    'weights': 'uniform'
}

"""
    Model training config constants
"""

MODEL_TRAINING_DIR_NAME:str = "model_training"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME:str = "model.pkl"
TRAINED_MODEL_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05
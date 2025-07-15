from datetime import datetime
import os
from networksecurity.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")):
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_dir = training_pipeline.ARTIFACTS_DIR
        self.timestamp = timestamp
        self.artifact_dir = os.path.join(self.artifacts_dir, f"{self.pipeline_name}_{self.timestamp}")
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_dir = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR_NAME, training_pipeline.FILE_NAME)
        self.training_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
        
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.validated_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.drift_report_dir = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.drift_report_file_path = os.path.join(self.drift_report_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        self.valid_training_file_path = os.path.join(self.validated_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_testing_file_path = os.path.join(self.validated_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_training_file_path = os.path.join(self.invalid_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_testing_file_path = os.path.join(self.invalid_dir, training_pipeline.TEST_FILE_NAME)
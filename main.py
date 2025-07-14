from networksecurity.logging import logger
from networksecurity.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

import sys


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        
        logger.info("Starting data ingestion process...")
        artifacts = data_ingestion.initiate_data_ingestion()
        print(f"Data ingestion completed. Artifacts: {artifacts}")
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
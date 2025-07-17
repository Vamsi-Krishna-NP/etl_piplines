from networksecurity.logging import logger
from networksecurity.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import (DataIngestionConfig, 
                                                  TrainingPipelineConfig, 
                                                  DataValidationConfig, 
                                                  DataTransformationConfig, 
                                                  ModelTrainerConfig)

import sys


if __name__ == "__main__":
    try:
        # Initialize the training pipeline configuration
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        
        # Start the data ingestion process
        logger.info("Starting data ingestion process...")
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logger.info("Data ingestion process completed successfully.")
        print(f"Data ingestion completed. Artifacts: {data_ingestion_artifacts}")
        
        # Initialize the data validation configuration
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_validation_config, training_pipeline_config)
        
        logger.info("Starting data validation process...")
        data_validation_artifacts = data_validation.initiate_data_validation(data_ingestion_artifacts)
        logger.info("Data validation process completed successfully.")
        print(f"Data validation completed. Artifacts: {data_validation_artifacts}")
        
        # Initialize the data transformation configuration
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifacts,data_transformation_config)
        
        logger.info("Starting data transformation process...")
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        logger.info("Data transformation process completed successfully.")
        print(f"Data transformation completed. Artifacts: {data_transformation_artifacts}")
        
        # Initialize the model trainer configuration
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifacts)
        logger.info("Starting model training process...")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.info("Model training process completed successfully.")
        print(f"Model training completed. Artifacts: {model_trainer_artifact}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
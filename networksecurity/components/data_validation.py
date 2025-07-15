from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.logging import logger
from networksecurity.exception import NetworkSecurityException
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import sys
import os

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_validation_config = data_validation_config
            self.training_pipeline_config = training_pipeline_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(f"Error initializing DataValidation: {e}", sys)
        
    @staticmethod
    def read_data(file_path: str):
        """
        Reads a CSV file and returns a DataFrame."""
        return pd.read_csv(file_path)
    
    def validate_column_count(self, data: pd.DataFrame) -> bool:
        """
        Validates if the number of columns in the data matches the expected schema.
        """
        try:
            expected_columns = self.schema_config['columns']
            actual_columns = data.columns.tolist()
            
            if len(expected_columns) != len(actual_columns):
                logger.error(f"Column count mismatch: expected {len(expected_columns)}, got {len(actual_columns)}")
                return False
            
            for col in expected_columns:
                if col not in actual_columns:
                    logger.error(f"Missing expected column: {col}")
                    return False
            
            return True
        
        except Exception as e:
            raise NetworkSecurityException(f"Error validating column count: {e}", sys)
        
    def validate_data_types(self, data: pd.DataFrame) -> bool:
        """
        Validates if the numerical columns in the data are of the correct data type.
        """
        try:
            numerical_columns = self.schema_config['numeric_features']
            for col in numerical_columns:
                if col not in data.columns:
                    logger.error(f"Missing numerical column: {col}")
                    return False
                
                if not pd.api.types.is_numeric_dtype(data[col]):
                    logger.error(f"Column {col} is not of numeric type")
                    return False
                
            return True
        except Exception as e:
            raise NetworkSecurityException(f"Error validating data types: {e}", sys)
    
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold:float = 0.5) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = True
                else:
                    is_found = False
                    status = False
                    logger.info(f"Data drift detected in column: {column}, p-value: {is_same_dist.pvalue}")
                
                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "same_distribution": is_found
                }})
                
            # create drift report directory if it doesn't exist
            drift_report_dir = self.data_validation_config.drift_report_dir
            dir_path = os.path.dirname(drift_report_dir)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_dir, report, replace=True)
            
            return status    
            
        except Exception as e:
            raise NetworkSecurityException(f"Error detecting data drift: {e}", sys)
        
        
    def initiate_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Initiates the data validation process.
        """
        try:
            # import the datasets
            train_data = data_ingestion_artifact.train_data_path
            test_data = data_ingestion_artifact.test_data_path
            
            # read the Data Set
            train_data = DataValidation.read_data(train_data)
            test_data = DataValidation.read_data(test_data)
            
            # validate the number of columns
            col_validation_status = self.validate_column_count(train_data) and self.validate_column_count(test_data)
            
            if not col_validation_status:
                raise NetworkSecurityException("Column validation failed", sys)
            
            # validate the numerical data types
            numerical_validation_status = self.validate_data_types(train_data) and self.validate_data_types(test_data)
            if not numerical_validation_status:
                raise NetworkSecurityException("Numerical data type validation failed", sys)
            
            # validate the data drift
            status = self.detect_data_drift(train_data, test_data)
            dir_path = os.path.dirname(self.data_validation_config.valid_training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_data.to_csv(self.data_validation_config.valid_training_file_path, index=False, header=True)
            test_data.to_csv(self.data_validation_config.valid_testing_file_path, index=False, header=True)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_training_file_path,
                valid_test_file_path=self.data_validation_config.valid_testing_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_dir
            )
            
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(f"Error during data validation: {e}", sys)
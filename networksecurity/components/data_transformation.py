import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (DataValidationArtifact, DataTransformationArtifact)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.utils.main_utils.utils import save_numpy_array,save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def get_data_transformation_object(self) -> Pipeline:
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor: Pipeline = Pipeline(steps=[
                ('imputer', imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Starting data transformation process.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            # train dataframe
            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            
            # test dataframe
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)
            
            # get transformation object
            transformation_object: Pipeline = self.get_data_transformation_object()
            
            preprocessor_object: Pipeline = transformation_object.fit(input_features_train_df)
            transformed_input_features_train = preprocessor_object.transform(input_features_train_df)
            transformed_input_features_test = preprocessor_object.transform(input_features_test_df)
            
            train_arr = np.c_[transformed_input_features_train, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_features_test, np.array(target_feature_test_df)]
            
            # save transformed data
            save_numpy_array(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object)
            
            # create and return artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            
            return data_transformation_artifact
            
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

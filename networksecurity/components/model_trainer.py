import os
import sys

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logger

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import load_object, save_object, load_numpy_array, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, x_train, y_train, x_test, y_test):
        model = {
            'Logistic Regression': LogisticRegression(verbose=1),
            'KNeighbors': KNeighborsClassifier(),
            'Decision Tree': DecisionTreeClassifier(),
            'Random Forest': RandomForestClassifier(verbose=1),
            'Gradient Boosting': GradientBoostingClassifier(verbose=1),
            'AdaBoost': AdaBoostClassifier()
        }
        
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'splitter': ['best', 'random'],
                'max_features': ['auto', 'sqrt', 'log2']
            },
            
            "Random Forest": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                'max_features': [None, 'sqrt', 'log2'],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            
            "Gradient Boosting": {
                'loss': ['log_loss', 'exponential'],
                'learning_rate': [.1, 0.1, 0.5, .001],
                'subsample': [0.6,0.7,0.75,0.8,0.85,0.9],
                'criterion': ['friedman_mse', 'squared_error'],
                'max_features': ['sqrt', 'log2'],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            
            "Logistic Regression": {},
            
            "AdaBoost": {
                "learning_rate": [.1, 0.1, 0.5, .001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            
            "KNeighbors": {
                'n_neighbors': [3, 5, 7, 9, 11],
                'weights': ['uniform', 'distance'],
                'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
            }
        }
        
        model_report = evaluate_models(x_train, y_train, x_test, y_test, models=model, params=params)
        
        best_model_score = max(sorted(model_report.values()))
        
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        
        best_model = model[best_model_name]
        
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        
        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)
        
        Network_Model= NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=Network_Model)
        
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        
        return model_trainer_artifact
        
    
    def initiate_model_trainer(self):
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            train_array = load_numpy_array(file_path=train_file_path)
            test_array = load_numpy_array(file_path=test_file_path)
            
            x_train, y_train, x_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
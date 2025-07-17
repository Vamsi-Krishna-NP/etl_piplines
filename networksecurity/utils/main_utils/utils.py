import yaml
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import os, sys
import numpy as np
import pickle

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(f"Error reading YAML file {file_path}: {e}", sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes a dictionary to a YAML file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
            
    except Exception as e:
        raise NetworkSecurityException(f"Error writing YAML file {file_path}: {e}", sys)
    
def save_numpy_array(file_path: str, array: np.ndarray) -> None:
    """
    Saves a numpy array to a specified file path."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(f"Error saving numpy array to {file_path}: {e}", sys)
    
def load_numpy_array(file_path: str) -> np.ndarray:
    """
    Loads a numpy array from a specified file path.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(f"Error loading numpy array from {file_path}: {e}", sys)
    
def save_object(file_path: str, obj: object) -> None:
    """
    Saves an object to a specified file path using pickle.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise NetworkSecurityException(f"Error saving object to {file_path}: {e}", sys)
    
def load_object(file_path: str) -> object:
    """
    Loads an object from a specified file path using pickle.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'rb') as file:
            print(file)
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(f"Error loading object from {file_path}: {e}", sys)

def evaluate_models(x_train, y_train, x_test, y_test, models: dict, params: dict) -> dict:
    try:
       report = {}
       
       for i in range(len(list(models))):
           model = list(models.values())[i]
           para = params[list(models.keys())[i]]
           
           gs = GridSearchCV(model, para, cv=3)
           gs.fit(x_train, y_train)
           
           model.set_params(**gs.best_params_)
           model.fit(x_train, y_train)
           
           y_train_pred = model.predict(x_train)
           y_test_pred = model.predict(x_test)
           
           train_model_score = r2_score(y_train, y_train_pred)
           test_model_score = r2_score(y_test, y_test_pred)
           
           report[list(models.keys())[i]] = test_model_score
           
       return report
       
    except Exception as e:
        raise NetworkSecurityException(f"Error evaluating models: {e}", sys)
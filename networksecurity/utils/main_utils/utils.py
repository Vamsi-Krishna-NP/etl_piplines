import yaml
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logger
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
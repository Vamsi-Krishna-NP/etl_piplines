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
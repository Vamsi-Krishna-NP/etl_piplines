from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os, sys

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logger

class NetworkModel:
    def __init__(self, model, preprocessor):
        try:
            self.model = model
            self.preprocessor = preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def predict(self, x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transformed)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

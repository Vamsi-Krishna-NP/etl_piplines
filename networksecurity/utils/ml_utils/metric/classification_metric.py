from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception import NetworkSecurityException
from sklearn.metrics import precision_score, recall_score, f1_score
import sys

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)

        return ClassificationMetricArtifact(precision=precision, recall=recall, f1_score=f1)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
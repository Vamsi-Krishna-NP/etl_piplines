from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_data_path: str
    test_data_path: str
    
@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    
@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

@dataclass
class ClassificationMetricArtifact:
    precision: float
    recall: float
    f1_score: float
    
@dataclass
class ModelTrainerArtifact:
    trained_model_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
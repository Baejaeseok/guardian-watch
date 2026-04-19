"""
Machine Learning Models and AI System
====================================
Module 6: Advanced Analytics

Comprehensive machine learning and artificial intelligence system for One Health applications,
providing advanced ML models, automated learning, and intelligent decision support.

NIW Focus: ML intelligence enabling automated pattern recognition, prediction, and 
decision support across One Health surveillance and response operations.
"""

import json
import math
import statistics
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable, Set
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque, Counter
import itertools
import random
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLModelType(Enum):
    """Machine learning model types."""
    SUPERVISED_CLASSIFICATION = "supervised_classification"    # Classification models
    SUPERVISED_REGRESSION = "supervised_regression"           # Regression models
    UNSUPERVISED_CLUSTERING = "unsupervised_clustering"       # Clustering models
    UNSUPERVISED_ASSOCIATION = "unsupervised_association"     # Association rules
    REINFORCEMENT_LEARNING = "reinforcement_learning"        # RL models
    DEEP_LEARNING = "deep_learning"                          # Deep neural networks
    ENSEMBLE_LEARNING = "ensemble_learning"                  # Ensemble methods
    TRANSFER_LEARNING = "transfer_learning"                  # Transfer learning

class MLAlgorithm(Enum):
    """Supported ML algorithms."""
    RANDOM_FOREST = "random_forest"                          # Random Forest
    GRADIENT_BOOSTING = "gradient_boosting"                  # Gradient Boosting
    SUPPORT_VECTOR_MACHINE = "svm"                           # SVM
    NEURAL_NETWORK = "neural_network"                        # Neural Networks
    DECISION_TREE = "decision_tree"                          # Decision Trees
    LOGISTIC_REGRESSION = "logistic_regression"              # Logistic Regression
    K_MEANS = "k_means"                                      # K-Means Clustering
    LSTM = "lstm"                                           # LSTM Networks
    CNN = "cnn"                                             # Convolutional NN
    TRANSFORMER = "transformer"                              # Transformer models

class MLTaskType(Enum):
    """ML task types for One Health applications."""
    DISEASE_PREDICTION = "disease_prediction"                # Disease outbreak prediction
    RISK_ASSESSMENT = "risk_assessment"                      # Risk scoring
    PATTERN_RECOGNITION = "pattern_recognition"              # Pattern detection
    ANOMALY_DETECTION = "anomaly_detection"                  # Anomaly identification
    CLASSIFICATION = "classification"                        # Multi-class classification
    TIME_SERIES_FORECASTING = "time_series_forecasting"      # Time series prediction
    NATURAL_LANGUAGE_PROCESSING = "nlp"                     # Text analysis
    IMAGE_ANALYSIS = "image_analysis"                        # Medical/diagnostic imaging

class MLModelStatus(Enum):
    """ML model lifecycle status."""
    DEVELOPMENT = "development"                              # Under development
    TRAINING = "training"                                    # Currently training
    VALIDATION = "validation"                               # Under validation
    TESTING = "testing"                                     # Testing phase
    DEPLOYED = "deployed"                                   # Production deployment
    RETIRED = "retired"                                     # Retired from use
    FAILED = "failed"                                       # Training/validation failed

class DataQuality(Enum):
    """Data quality levels for ML."""
    EXCELLENT = "excellent"                                  # >95% quality
    GOOD = "good"                                           # 85-95% quality
    ACCEPTABLE = "acceptable"                               # 70-85% quality
    POOR = "poor"                                           # <70% quality

@dataclass
class MLDataset:
    """Machine learning dataset definition."""
    
    dataset_id: str
    dataset_name: str
    data_domain: str                                        # One Health domain
    
    # Dataset characteristics
    total_samples: int
    feature_count: int
    target_variables: List[str] = field(default_factory=list)
    categorical_features: List[str] = field(default_factory=list)
    numerical_features: List[str] = field(default_factory=list)
    
    # Data quality metrics
    data_quality: DataQuality = DataQuality.GOOD
    missing_value_percentage: float = 0.0
    outlier_percentage: float = 0.0
    class_balance_score: float = 1.0                        # 1.0 = perfectly balanced
    
    # Temporal characteristics
    temporal_coverage_days: int = 365
    update_frequency: str = "daily"                         # How often data is updated
    last_updated: datetime = field(default_factory=datetime.now)
    
    # Privacy and compliance
    contains_pii: bool = False                              # Contains personal data
    privacy_level: str = "public"                          # "public", "restricted", "confidential"
    compliance_requirements: List[str] = field(default_factory=list)
    
    # Preprocessing status
    is_preprocessed: bool = False
    preprocessing_steps: List[str] = field(default_factory=list)
    feature_engineering_applied: bool = False

@dataclass
class MLModel:
    """Comprehensive ML model definition."""
    
    model_id: str
    model_name: str
    model_type: MLModelType
    algorithm: MLAlgorithm
    task_type: MLTaskType
    
    # Model architecture
    model_description: str
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    feature_selection_method: Optional[str] = None
    
    # Training configuration
    dataset_id: str = ""
    training_split: float = 0.7                            # Training data percentage
    validation_split: float = 0.15                         # Validation data percentage
    test_split: float = 0.15                              # Test data percentage
    
    # Model lifecycle
    status: MLModelStatus = MLModelStatus.DEVELOPMENT
    created_date: datetime = field(default_factory=datetime.now)
    training_start_date: Optional[datetime] = None
    training_end_date: Optional[datetime] = None
    deployment_date: Optional[datetime] = None
    
    # Performance metrics
    training_accuracy: float = 0.0
    validation_accuracy: float = 0.0
    test_accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    auc_roc: float = 0.0                                   # Area Under ROC Curve
    
    # Regression metrics (if applicable)
    rmse: float = 0.0                                      # Root Mean Square Error
    mae: float = 0.0                                       # Mean Absolute Error
    r_squared: float = 0.0                                 # R-squared
    
    # Model interpretability
    feature_importance: Dict[str, float] = field(default_factory=dict)
    shap_values_available: bool = False                    # SHAP interpretability
    lime_analysis_available: bool = False                  # LIME interpretability
    interpretability_score: float = 0.0                   # Overall interpretability
    
    # Production metrics
    prediction_count: int = 0                              # Total predictions made
    average_inference_time_ms: float = 0.0                # Inference time
    model_drift_score: float = 0.0                        # Data drift detection
    
    # Fairness and bias
    bias_assessment_score: float = 0.0                     # Bias evaluation
    fairness_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Model metadata
    version: str = "1.0"
    tags: List[str] = field(default_factory=list)
    created_by: str = "ml_system"

@dataclass
class MLPipeline:
    """End-to-end ML pipeline definition."""
    
    pipeline_id: str
    pipeline_name: str
    description: str
    
    # Pipeline components
    data_ingestion: Dict[str, Any] = field(default_factory=dict)
    data_preprocessing: Dict[str, Any] = field(default_factory=dict)
    feature_engineering: Dict[str, Any] = field(default_factory=dict)
    model_training: Dict[str, Any] = field(default_factory=dict)
    model_evaluation: Dict[str, Any] = field(default_factory=dict)
    model_deployment: Dict[str, Any] = field(default_factory=dict)
    
    # Pipeline execution
    is_automated: bool = True                              # Automated execution
    schedule: str = "weekly"                               # Execution schedule
    last_execution: Optional[datetime] = None
    execution_count: int = 0
    success_rate: float = 0.0
    
    # Associated models
    models: List[str] = field(default_factory=list)        # Model IDs
    datasets: List[str] = field(default_factory=list)      # Dataset IDs
    
    # Monitoring and alerts
    performance_threshold: float = 0.8                     # Minimum acceptable performance
    drift_threshold: float = 0.1                          # Maximum acceptable drift
    alert_recipients: List[str] = field(default_factory=list)

@dataclass
class MLExperiment:
    """ML experiment tracking."""
    
    experiment_id: str
    experiment_name: str
    description: str
    experiment_type: str                                   # "model_comparison", "hyperparameter_tuning", etc.
    
    # Experiment configuration
    models_tested: List[str] = field(default_factory=list) # Model IDs
    datasets_used: List[str] = field(default_factory=list) # Dataset IDs
    metrics_tracked: List[str] = field(default_factory=list)
    
    # Execution details
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    duration_hours: float = 0.0
    computational_cost: float = 0.0                        # Cost in compute units
    
    # Results
    best_model_id: Optional[str] = None
    best_performance: float = 0.0
    performance_comparison: Dict[str, float] = field(default_factory=dict)
    
    # Insights and learnings
    key_findings: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    
    # Reproducibility
    random_seed: int = 42
    environment_snapshot: Dict[str, Any] = field(default_factory=dict)
    code_version: str = ""

class MachineLearningManager:
    """Comprehensive machine learning management system for One Health."""
    
    def __init__(self):
        self.datasets: Dict[str, MLDataset] = {}
        self.models: Dict[str, MLModel] = {}
        self.pipelines: Dict[str, MLPipeline] = {}
        self.experiments: List[MLExperiment] = []
        
        # ML capabilities and configurations
        self.supported_algorithms = {
            MLModelType.SUPERVISED_CLASSIFICATION: [
                MLAlgorithm.RANDOM_FOREST, MLAlgorithm.GRADIENT_BOOSTING,
                MLAlgorithm.SUPPORT_VECTOR_MACHINE, MLAlgorithm.LOGISTIC_REGRESSION
            ],
            MLModelType.SUPERVISED_REGRESSION: [
                MLAlgorithm.RANDOM_FOREST, MLAlgorithm.GRADIENT_BOOSTING,
                MLAlgorithm.SUPPORT_VECTOR_MACHINE, MLAlgorithm.NEURAL_NETWORK
            ],
            MLModelType.DEEP_LEARNING: [
                MLAlgorithm.NEURAL_NETWORK, MLAlgorithm.LSTM, 
                MLAlgorithm.CNN, MLAlgorithm.TRANSFORMER
            ],
            MLModelType.UNSUPERVISED_CLUSTERING: [
                MLAlgorithm.K_MEANS
            ]
        }
        
        # Initialize ML framework
        self._initialize_ml_framework()
        
        logger.info("Machine Learning Manager initialized for One Health")
    
    def _initialize_ml_framework(self):
        """Initialize ML framework with sample datasets and models."""
        
        # Sample datasets for One Health applications
        sample_datasets = [
            {
                "name": "Zoonotic Disease Surveillance Dataset", "domain": "zoonotic",
                "samples": 5000, "features": 25, "quality": DataQuality.EXCELLENT,
                "targets": ["outbreak_risk", "transmission_probability"]
            },
            {
                "name": "Environmental Health Monitoring", "domain": "environmental", 
                "samples": 8000, "features": 35, "quality": DataQuality.GOOD,
                "targets": ["health_impact_score", "pollution_level"]
            },
            {
                "name": "AMR Pattern Recognition Dataset", "domain": "antimicrobial_resistance",
                "samples": 3000, "features": 18, "quality": DataQuality.EXCELLENT,
                "targets": ["resistance_pattern", "treatment_efficacy"]
            },
            {
                "name": "Food Safety Risk Assessment Data", "domain": "food_safety",
                "samples": 6000, "features": 22, "quality": DataQuality.GOOD,
                "targets": ["contamination_risk", "safety_score"]
            },
            {
                "name": "One Health Clinical Decision Support", "domain": "clinical_decision",
                "samples": 12000, "features": 45, "quality": DataQuality.EXCELLENT,
                "targets": ["diagnosis_prediction", "treatment_recommendation"]
            }
        ]
        
        # Create datasets
        for dataset_data in sample_datasets:
            dataset_id = f"DATASET_{random.randint(100000, 999999)}"
            
            dataset = MLDataset(
                dataset_id=dataset_id,
                dataset_name=dataset_data["name"],
                data_domain=dataset_data["domain"],
                total_samples=dataset_data["samples"],
                feature_count=dataset_data["features"],
                target_variables=dataset_data["targets"],
                data_quality=dataset_data["quality"],
                missing_value_percentage=random.uniform(0, 5),
                outlier_percentage=random.uniform(0, 3),
                class_balance_score=random.uniform(0.7, 1.0),
                temporal_coverage_days=random.randint(180, 730),
                is_preprocessed=True,
                preprocessing_steps=[
                    "Missing value imputation",
                    "Outlier detection and treatment",
                    "Feature scaling and normalization",
                    "Categorical encoding"
                ],
                feature_engineering_applied=True
            )
            
            # Generate feature lists
            num_categorical = random.randint(3, 8)
            dataset.categorical_features = [f"categorical_feature_{i}" for i in range(num_categorical)]
            dataset.numerical_features = [f"numerical_feature_{i}" for i in range(dataset.feature_count - num_categorical)]
            
            self.datasets[dataset_id] = dataset
        
        # Sample ML models for One Health applications
        sample_models = [
            {
                "name": "Zoonotic Outbreak Predictor", "type": MLModelType.SUPERVISED_CLASSIFICATION,
                "algorithm": MLAlgorithm.RANDOM_FOREST, "task": MLTaskType.DISEASE_PREDICTION,
                "description": "Predicts zoonotic disease outbreak probability"
            },
            {
                "name": "Environmental Health Impact Estimator", "type": MLModelType.SUPERVISED_REGRESSION,
                "algorithm": MLAlgorithm.GRADIENT_BOOSTING, "task": MLTaskType.RISK_ASSESSMENT,
                "description": "Estimates environmental factors impact on health outcomes"
            },
            {
                "name": "AMR Pattern Classifier", "type": MLModelType.DEEP_LEARNING,
                "algorithm": MLAlgorithm.NEURAL_NETWORK, "task": MLTaskType.PATTERN_RECOGNITION,
                "description": "Classifies antimicrobial resistance patterns"
            },
            {
                "name": "Food Safety Anomaly Detector", "type": MLModelType.UNSUPERVISED_CLUSTERING,
                "algorithm": MLAlgorithm.K_MEANS, "task": MLTaskType.ANOMALY_DETECTION,
                "description": "Detects anomalies in food safety monitoring data"
            },
            {
                "name": "One Health Time Series Forecaster", "type": MLModelType.DEEP_LEARNING,
                "algorithm": MLAlgorithm.LSTM, "task": MLTaskType.TIME_SERIES_FORECASTING,
                "description": "Forecasts health trends across One Health domains"
            },
            {
                "name": "Clinical Decision Support System", "type": MLModelType.ENSEMBLE_LEARNING,
                "algorithm": MLAlgorithm.GRADIENT_BOOSTING, "task": MLTaskType.CLASSIFICATION,
                "description": "Provides AI-powered clinical decision support"
            }
        ]
        
        # Create ML models
        for model_data in sample_models:
            model_id = f"MODEL_{random.randint(100000, 999999)}"
            dataset_id = random.choice(list(self.datasets.keys()))
            
            model = MLModel(
                model_id=model_id,
                model_name=model_data["name"],
                model_type=model_data["type"],
                algorithm=model_data["algorithm"],
                task_type=model_data["task"],
                model_description=model_data["description"],
                dataset_id=dataset_id,
                status=random.choice([MLModelStatus.DEPLOYED, MLModelStatus.VALIDATION, MLModelStatus.TRAINING]),
                training_accuracy=random.uniform(0.75, 0.95),
                validation_accuracy=random.uniform(0.70, 0.90),
                test_accuracy=random.uniform(0.65, 0.85),
                precision=random.uniform(0.70, 0.90),
                recall=random.uniform(0.65, 0.88),
                f1_score=random.uniform(0.70, 0.89),
                auc_roc=random.uniform(0.75, 0.95)
            )
            
            # Generate hyperparameters based on algorithm
            if model.algorithm == MLAlgorithm.RANDOM_FOREST:
                model.hyperparameters = {
                    "n_estimators": random.randint(100, 500),
                    "max_depth": random.randint(5, 20),
                    "min_samples_split": random.randint(2, 10)
                }
            elif model.algorithm == MLAlgorithm.GRADIENT_BOOSTING:
                model.hyperparameters = {
                    "n_estimators": random.randint(100, 300),
                    "learning_rate": random.uniform(0.01, 0.3),
                    "max_depth": random.randint(3, 10)
                }
            elif model.algorithm == MLAlgorithm.NEURAL_NETWORK:
                model.hyperparameters = {
                    "hidden_layers": random.randint(2, 5),
                    "neurons_per_layer": random.randint(64, 256),
                    "learning_rate": random.uniform(0.001, 0.01),
                    "dropout_rate": random.uniform(0.1, 0.5)
                }
            
            # Generate feature importance
            dataset = self.datasets[dataset_id]
            all_features = dataset.categorical_features + dataset.numerical_features
            total_importance = 0
            for feature in all_features[:10]:  # Top 10 features
                importance = random.uniform(0.01, 0.2)
                model.feature_importance[feature] = importance
                total_importance += importance
            
            # Normalize feature importance
            for feature in model.feature_importance:
                model.feature_importance[feature] /= total_importance
            
            # Set interpretability score
            interpretability_scores = {
                MLAlgorithm.DECISION_TREE: 0.9,
                MLAlgorithm.LOGISTIC_REGRESSION: 0.8,
                MLAlgorithm.RANDOM_FOREST: 0.7,
                MLAlgorithm.GRADIENT_BOOSTING: 0.6,
                MLAlgorithm.SUPPORT_VECTOR_MACHINE: 0.5,
                MLAlgorithm.NEURAL_NETWORK: 0.3,
                MLAlgorithm.LSTM: 0.2
            }
            model.interpretability_score = interpretability_scores.get(model.algorithm, 0.5)
            
            # Set production metrics for deployed models
            if model.status == MLModelStatus.DEPLOYED:
                model.prediction_count = random.randint(1000, 10000)
                model.average_inference_time_ms = random.uniform(10, 100)
                model.model_drift_score = random.uniform(0, 0.1)
                model.deployment_date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            self.models[model_id] = model
        
        # Sample ML pipelines
        pipeline_configs = [
            {
                "name": "One Health Disease Surveillance Pipeline",
                "description": "End-to-end pipeline for disease surveillance ML models"
            },
            {
                "name": "Environmental Health Monitoring Pipeline", 
                "description": "Automated pipeline for environmental health risk assessment"
            },
            {
                "name": "AMR Pattern Recognition Pipeline",
                "description": "Pipeline for antimicrobial resistance pattern analysis"
            }
        ]
        
        # Create ML pipelines
        for pipeline_data in pipeline_configs:
            pipeline_id = f"PIPELINE_{random.randint(100000, 999999)}"
            
            pipeline = MLPipeline(
                pipeline_id=pipeline_id,
                pipeline_name=pipeline_data["name"],
                description=pipeline_data["description"],
                models=random.sample(list(self.models.keys()), random.randint(1, 3)),
                datasets=random.sample(list(self.datasets.keys()), random.randint(1, 2)),
                execution_count=random.randint(5, 50),
                success_rate=random.uniform(0.85, 0.98),
                last_execution=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            
            # Configure pipeline components
            pipeline.data_ingestion = {
                "source_type": "database",
                "update_frequency": "daily",
                "data_validation_enabled": True
            }
            
            pipeline.data_preprocessing = {
                "missing_value_strategy": "imputation",
                "outlier_detection": "isolation_forest",
                "feature_scaling": "standard_scaling"
            }
            
            pipeline.feature_engineering = {
                "feature_selection": "recursive_feature_elimination",
                "dimensionality_reduction": "pca",
                "feature_creation": "polynomial_features"
            }
            
            pipeline.model_training = {
                "cross_validation_folds": 5,
                "hyperparameter_tuning": "grid_search",
                "early_stopping": True
            }
            
            pipeline.model_evaluation = {
                "metrics": ["accuracy", "precision", "recall", "f1_score"],
                "validation_strategy": "stratified_k_fold",
                "performance_threshold": 0.8
            }
            
            pipeline.model_deployment = {
                "deployment_strategy": "blue_green",
                "monitoring_enabled": True,
                "auto_rollback": True
            }
            
            self.pipelines[pipeline_id] = pipeline
        
        logger.info(f"Initialized {len(self.datasets)} datasets, {len(self.models)} models, and {len(self.pipelines)} pipelines")
    
    def train_model(self, model_id: str, dataset_id: str) -> Dict[str, Any]:
        """Train machine learning model."""
        
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        if dataset_id not in self.datasets:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        model = self.models[model_id]
        dataset = self.datasets[dataset_id]
        
        # Update model status
        model.status = MLModelStatus.TRAINING
        model.training_start_date = datetime.now()
        model.dataset_id = dataset_id
        
        # Simulate training process
        training_duration_minutes = random.uniform(10, 120)  # 10 minutes to 2 hours
        
        # Simulate training results based on algorithm and data quality
        base_performance = 0.6
        
        # Algorithm performance multipliers
        algorithm_multipliers = {
            MLAlgorithm.RANDOM_FOREST: 0.85,
            MLAlgorithm.GRADIENT_BOOSTING: 0.90,
            MLAlgorithm.NEURAL_NETWORK: 0.88,
            MLAlgorithm.LSTM: 0.82,
            MLAlgorithm.SUPPORT_VECTOR_MACHINE: 0.83,
            MLAlgorithm.LOGISTIC_REGRESSION: 0.80
        }
        
        # Data quality multipliers
        quality_multipliers = {
            DataQuality.EXCELLENT: 1.1,
            DataQuality.GOOD: 1.0,
            DataQuality.ACCEPTABLE: 0.9,
            DataQuality.POOR: 0.7
        }
        
        algorithm_factor = algorithm_multipliers.get(model.algorithm, 0.8)
        quality_factor = quality_multipliers.get(dataset.data_quality, 1.0)
        
        # Calculate performance metrics
        training_performance = base_performance * algorithm_factor * quality_factor + random.uniform(0, 0.2)
        model.training_accuracy = min(training_performance, 0.98)
        
        # Validation performance (typically slightly lower)
        model.validation_accuracy = model.training_accuracy * random.uniform(0.85, 0.95)
        model.test_accuracy = model.validation_accuracy * random.uniform(0.9, 0.98)
        
        # Calculate other metrics for classification tasks
        if model.model_type in [MLModelType.SUPERVISED_CLASSIFICATION, MLModelType.DEEP_LEARNING]:
            model.precision = model.test_accuracy * random.uniform(0.95, 1.05)
            model.recall = model.test_accuracy * random.uniform(0.90, 1.10)
            model.f1_score = 2 * (model.precision * model.recall) / (model.precision + model.recall)
            model.auc_roc = model.test_accuracy * random.uniform(1.0, 1.15)
            
            # Ensure metrics are within valid ranges
            model.precision = min(model.precision, 1.0)
            model.recall = min(model.recall, 1.0)
            model.auc_roc = min(model.auc_roc, 1.0)
        
        # Calculate regression metrics if applicable
        if model.model_type == MLModelType.SUPERVISED_REGRESSION:
            model.rmse = random.uniform(0.1, 2.0)
            model.mae = model.rmse * random.uniform(0.6, 0.8)
            model.r_squared = model.test_accuracy
        
        # Update training completion
        model.training_end_date = datetime.now()
        
        # Determine training success
        if model.test_accuracy >= 0.6:
            model.status = MLModelStatus.VALIDATION
            training_result = "success"
        else:
            model.status = MLModelStatus.FAILED
            training_result = "failed"
        
        # Calculate overfitting score
        overfitting = model.training_accuracy - model.validation_accuracy
        model.overfitting_score = max(0, overfitting)
        
        # Generate training summary
        training_summary = {
            "result": training_result,
            "training_duration_minutes": training_duration_minutes,
            "final_training_accuracy": model.training_accuracy,
            "final_validation_accuracy": model.validation_accuracy,
            "final_test_accuracy": model.test_accuracy,
            "overfitting_score": model.overfitting_score,
            "data_quality": dataset.data_quality.value,
            "sample_size": dataset.total_samples,
            "feature_count": dataset.feature_count
        }
        
        logger.info(f"Model training completed: {model_id} - {training_result} ({model.test_accuracy:.3f} accuracy)")
        
        return training_summary
    
    def deploy_model(self, model_id: str) -> Dict[str, Any]:
        """Deploy ML model to production."""
        
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        # Check if model is ready for deployment
        if model.status not in [MLModelStatus.VALIDATION, MLModelStatus.TESTING]:
            return {"status": "error", "message": "Model not ready for deployment"}
        
        if model.test_accuracy < 0.7:  # Minimum accuracy threshold
            return {"status": "error", "message": "Model accuracy too low for deployment"}
        
        # Deploy model
        model.status = MLModelStatus.DEPLOYED
        model.deployment_date = datetime.now()
        model.is_deployed = True
        
        # Initialize production metrics
        model.prediction_count = 0
        model.average_inference_time_ms = random.uniform(10, 50)
        model.model_drift_score = 0.0
        
        deployment_summary = {
            "status": "success",
            "deployment_date": model.deployment_date,
            "model_accuracy": model.test_accuracy,
            "expected_inference_time_ms": model.average_inference_time_ms,
            "monitoring_enabled": True,
            "auto_scaling_enabled": True
        }
        
        logger.info(f"Model deployed: {model_id} - {model.test_accuracy:.3f} accuracy")
        
        return deployment_summary
    
    def make_prediction(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction using deployed ML model."""
        
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        if model.status != MLModelStatus.DEPLOYED:
            return {"status": "error", "message": "Model not deployed"}
        
        # Simulate prediction process
        prediction_start_time = datetime.now()
        
        # Generate prediction based on model type
        if model.model_type == MLModelType.SUPERVISED_CLASSIFICATION:
            # Classification prediction
            class_probabilities = {
                "class_0": random.uniform(0.1, 0.8),
                "class_1": random.uniform(0.1, 0.8)
            }
            # Normalize probabilities
            total_prob = sum(class_probabilities.values())
            class_probabilities = {k: v/total_prob for k, v in class_probabilities.items()}
            
            predicted_class = max(class_probabilities, key=class_probabilities.get)
            confidence = max(class_probabilities.values())
            
            prediction_result = {
                "prediction_type": "classification",
                "predicted_class": predicted_class,
                "confidence": confidence,
                "class_probabilities": class_probabilities
            }
            
        elif model.model_type == MLModelType.SUPERVISED_REGRESSION:
            # Regression prediction
            predicted_value = random.uniform(10, 100)
            prediction_interval = (predicted_value * 0.9, predicted_value * 1.1)
            
            prediction_result = {
                "prediction_type": "regression", 
                "predicted_value": predicted_value,
                "prediction_interval": prediction_interval,
                "confidence": random.uniform(0.8, 0.95)
            }
            
        elif model.task_type == MLTaskType.ANOMALY_DETECTION:
            # Anomaly detection
            anomaly_score = random.uniform(0, 1)
            is_anomaly = anomaly_score > 0.7
            
            prediction_result = {
                "prediction_type": "anomaly_detection",
                "is_anomaly": is_anomaly,
                "anomaly_score": anomaly_score,
                "confidence": random.uniform(0.7, 0.9)
            }
            
        else:
            # Generic prediction
            prediction_result = {
                "prediction_type": "generic",
                "predicted_value": random.uniform(0, 1),
                "confidence": random.uniform(0.6, 0.9)
            }
        
        # Calculate prediction time
        prediction_time_ms = (datetime.now() - prediction_start_time).total_seconds() * 1000
        
        # Update model metrics
        model.prediction_count += 1
        
        # Update average inference time (running average)
        if model.average_inference_time_ms == 0:
            model.average_inference_time_ms = prediction_time_ms
        else:
            model.average_inference_time_ms = (
                model.average_inference_time_ms * 0.9 + prediction_time_ms * 0.1
            )
        
        # Add metadata
        prediction_result.update({
            "model_id": model_id,
            "model_name": model.model_name,
            "prediction_timestamp": datetime.now(),
            "inference_time_ms": prediction_time_ms,
            "model_version": model.version
        })
        
        return prediction_result
    
    def run_experiment(self, experiment_name: str, model_ids: List[str], 
                      dataset_ids: List[str], experiment_type: str = "model_comparison") -> MLExperiment:
        """Run ML experiment to compare models or tune hyperparameters."""
        
        experiment_id = f"EXP_{random.randint(100000, 999999)}"
        
        experiment = MLExperiment(
            experiment_id=experiment_id,
            experiment_name=experiment_name,
            description=f"{experiment_type} experiment with {len(model_ids)} models",
            experiment_type=experiment_type,
            models_tested=model_ids.copy(),
            datasets_used=dataset_ids.copy(),
            metrics_tracked=["accuracy", "precision", "recall", "f1_score"]
        )
        
        # Simulate experiment execution
        experiment.duration_hours = random.uniform(1, 12)
        experiment.computational_cost = experiment.duration_hours * random.uniform(10, 50)
        
        # Compare model performances
        best_performance = 0
        best_model = None
        
        for model_id in model_ids:
            if model_id in self.models:
                model = self.models[model_id]
                # Use test accuracy as experiment performance
                performance = model.test_accuracy + random.uniform(-0.05, 0.05)  # Add some variance
                experiment.performance_comparison[model_id] = performance
                
                if performance > best_performance:
                    best_performance = performance
                    best_model = model_id
        
        experiment.best_model_id = best_model
        experiment.best_performance = best_performance
        experiment.end_date = experiment.start_date + timedelta(hours=experiment.duration_hours)
        
        # Generate findings based on experiment type
        if experiment_type == "model_comparison":
            experiment.key_findings = [
                f"Best performing model: {self.models[best_model].model_name if best_model else 'None'}",
                f"Performance difference: {(max(experiment.performance_comparison.values()) - min(experiment.performance_comparison.values())):.3f}",
                "Random Forest and Gradient Boosting show consistent performance across datasets"
            ]
        elif experiment_type == "hyperparameter_tuning":
            experiment.key_findings = [
                "Learning rate significantly impacts model convergence",
                "Optimal tree depth found to be between 8-12 for this dataset",
                "Regularization helps prevent overfitting"
            ]
        
        experiment.lessons_learned = [
            "Data quality has major impact on model performance",
            "Cross-validation is essential for reliable performance estimation",
            "Feature engineering provides substantial improvements"
        ]
        
        experiment.next_steps = [
            "Deploy best performing model to production",
            "Collect more training data for underperforming categories",
            "Implement model monitoring and drift detection"
        ]
        
        self.experiments.append(experiment)
        
        logger.info(f"ML experiment completed: {experiment_id} - Best model: {best_model} ({best_performance:.3f})")
        
        return experiment
    
    def monitor_model_performance(self, model_id: str) -> Dict[str, Any]:
        """Monitor deployed model performance and detect drift."""
        
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        
        if model.status != MLModelStatus.DEPLOYED:
            return {"status": "error", "message": "Model not deployed"}
        
        # Simulate performance monitoring
        monitoring_results = {
            "model_id": model_id,
            "model_name": model.model_name,
            "monitoring_timestamp": datetime.now(),
            "deployment_duration_days": (datetime.now() - model.deployment_date).days if model.deployment_date else 0,
            "total_predictions": model.prediction_count,
            "average_inference_time_ms": model.average_inference_time_ms
        }
        
        # Performance metrics
        current_accuracy = model.test_accuracy + random.uniform(-0.1, 0.05)  # Simulate some performance drift
        accuracy_degradation = model.test_accuracy - current_accuracy
        
        monitoring_results.update({
            "original_test_accuracy": model.test_accuracy,
            "current_estimated_accuracy": current_accuracy,
            "accuracy_degradation": accuracy_degradation,
            "performance_status": "degraded" if accuracy_degradation > 0.05 else "stable"
        })
        
        # Data drift detection
        model.model_drift_score = random.uniform(0, 0.15)
        drift_status = "high" if model.model_drift_score > 0.1 else "low" if model.model_drift_score < 0.05 else "medium"
        
        monitoring_results.update({
            "data_drift_score": model.model_drift_score,
            "drift_status": drift_status,
            "drift_alert": model.model_drift_score > 0.1
        })
        
        # Fairness monitoring
        model.bias_assessment_score = random.uniform(0, 0.3)
        bias_status = "high" if model.bias_assessment_score > 0.2 else "acceptable"
        
        monitoring_results.update({
            "bias_assessment_score": model.bias_assessment_score,
            "bias_status": bias_status,
            "bias_alert": model.bias_assessment_score > 0.2
        })
        
        # Generate recommendations
        recommendations = []
        if accuracy_degradation > 0.05:
            recommendations.append("Consider retraining model with recent data")
        if model.model_drift_score > 0.1:
            recommendations.append("Investigate data distribution changes")
        if model.bias_assessment_score > 0.2:
            recommendations.append("Review model fairness and bias mitigation strategies")
        if not recommendations:
            recommendations.append("Model performance is stable - continue monitoring")
        
        monitoring_results["recommendations"] = recommendations
        
        return monitoring_results
    
    def get_ml_summary(self) -> Dict[str, Any]:
        """Get comprehensive ML system summary."""
        
        # Dataset analysis
        datasets_by_domain = Counter(d.data_domain for d in self.datasets.values())
        datasets_by_quality = Counter(d.data_quality for d in self.datasets.values())
        
        # Model analysis
        models_by_type = Counter(m.model_type for m in self.models.values())
        models_by_algorithm = Counter(m.algorithm for m in self.models.values())
        models_by_status = Counter(m.status for m in self.models.values())
        models_by_task = Counter(m.task_type for m in self.models.values())
        
        # Performance analysis
        deployed_models = [m for m in self.models.values() if m.status == MLModelStatus.DEPLOYED]
        if deployed_models:
            avg_accuracy = statistics.mean(m.test_accuracy for m in deployed_models)
            avg_inference_time = statistics.mean(m.average_inference_time_ms for m in deployed_models if m.average_inference_time_ms > 0)
            total_predictions = sum(m.prediction_count for m in deployed_models)
        else:
            avg_accuracy = avg_inference_time = total_predictions = 0
        
        # Pipeline analysis
        pipeline_success_rates = [p.success_rate for p in self.pipelines.values() if p.success_rate > 0]
        avg_pipeline_success = statistics.mean(pipeline_success_rates) if pipeline_success_rates else 0
        
        return {
            "datasets": {
                "total_datasets": len(self.datasets),
                "by_domain": dict(datasets_by_domain),
                "by_quality": {q.value: count for q, count in datasets_by_quality.items()},
                "total_samples": sum(d.total_samples for d in self.datasets.values()),
                "avg_features": statistics.mean(d.feature_count for d in self.datasets.values()) if self.datasets else 0
            },
            "models": {
                "total_models": len(self.models),
                "by_type": {t.value: count for t, count in models_by_type.items()},
                "by_algorithm": {a.value: count for a, count in models_by_algorithm.items()},
                "by_status": {s.value: count for s, count in models_by_status.items()},
                "by_task": {t.value: count for t, count in models_by_task.items()}
            },
            "performance": {
                "deployed_models": len(deployed_models),
                "average_model_accuracy": avg_accuracy,
                "average_inference_time_ms": avg_inference_time,
                "total_predictions_served": total_predictions
            },
            "pipelines": {
                "total_pipelines": len(self.pipelines),
                "average_success_rate": avg_pipeline_success,
                "automated_pipelines": len([p for p in self.pipelines.values() if p.is_automated])
            },
            "experiments": {
                "total_experiments": len(self.experiments),
                "completed_experiments": len([e for e in self.experiments if e.end_date])
            }
        }

def run_demonstration() -> MachineLearningManager:
    """Run comprehensive ML system demonstration."""
    
    print("🤖 One Health Machine Learning System - Demonstration")
    print("=" * 70)
    
    ml_manager = MachineLearningManager()
    
    print(f"\n🤖 ML Framework:")
    print(f"  Model Types: {len(MLModelType)}")
    print(f"  Algorithms: {len(MLAlgorithm)}")
    print(f"  Task Types: {len(MLTaskType)}")
    print(f"  Datasets: {len(ml_manager.datasets)}")
    print(f"  Models: {len(ml_manager.models)}")
    print(f"  Pipelines: {len(ml_manager.pipelines)}")
    
    # Display datasets by domain
    datasets_by_domain = defaultdict(list)
    for dataset in ml_manager.datasets.values():
        datasets_by_domain[dataset.data_domain].append(dataset.dataset_name)
    
    print(f"\n📊 ML Datasets by Domain:")
    for domain, datasets in datasets_by_domain.items():
        print(f"  {domain.replace('_', ' ').title()}: {len(datasets)}")
        for dataset in datasets[:1]:  # Show first dataset
            print(f"    • {dataset}")
    
    print(f"\n🏋️ Training ML Models...")
    
    # Train some models
    training_results = []
    sample_models = list(ml_manager.models.keys())[:3]  # Train first 3 models
    sample_datasets = list(ml_manager.datasets.keys())
    
    for model_id in sample_models:
        dataset_id = random.choice(sample_datasets)
        result = ml_manager.train_model(model_id, dataset_id)
        training_results.append((model_id, result))
        
        model_name = ml_manager.models[model_id].model_name
        if result["result"] == "success":
            print(f"  ✅ {model_name}: {result['final_test_accuracy']:.1%} accuracy")
        else:
            print(f"  ❌ {model_name}: Training failed")
    
    print(f"\n🚀 Deploying ML Models...")
    
    # Deploy successful models
    deployed_models = []
    for model_id, result in training_results:
        if result["result"] == "success":
            deploy_result = ml_manager.deploy_model(model_id)
            if deploy_result["status"] == "success":
                deployed_models.append(model_id)
                model_name = ml_manager.models[model_id].model_name
                print(f"  🚀 {model_name}: Deployed ({deploy_result['model_accuracy']:.1%} accuracy)")
    
    print(f"\n🔮 Making Predictions...")
    
    # Make predictions with deployed models
    prediction_results = []
    for model_id in deployed_models:
        sample_input = {"feature_1": 1.5, "feature_2": 2.3, "feature_3": 0.8}
        prediction = ml_manager.make_prediction(model_id, sample_input)
        prediction_results.append(prediction)
        
        model_name = prediction["model_name"]
        prediction_type = prediction["prediction_type"]
        confidence = prediction.get("confidence", 0)
        print(f"  🔮 {model_name}: {prediction_type} ({confidence:.1%} confidence)")
    
    print(f"\n🧪 Running ML Experiment...")
    
    # Run model comparison experiment
    experiment = ml_manager.run_experiment(
        "One Health Model Comparison Experiment",
        sample_models,
        sample_datasets[:2],
        "model_comparison"
    )
    
    best_model_name = ml_manager.models[experiment.best_model_id].model_name if experiment.best_model_id else "None"
    print(f"  🧪 Experiment: {experiment.experiment_name}")
    print(f"  🏆 Best Model: {best_model_name} ({experiment.best_performance:.1%})")
    print(f"  ⏱️ Duration: {experiment.duration_hours:.1f} hours")
    
    print(f"\n📊 Monitoring Model Performance...")
    
    # Monitor deployed models
    for model_id in deployed_models[:2]:  # Monitor first 2 deployed models
        monitoring_result = ml_manager.monitor_model_performance(model_id)
        model_name = monitoring_result["model_name"]
        
        performance_status = monitoring_result["performance_status"]
        drift_status = monitoring_result["drift_status"]
        
        status_icon = "✅" if performance_status == "stable" else "⚠️"
        print(f"  {status_icon} {model_name}: {performance_status} performance, {drift_status} drift")
    
    return ml_manager

def display_ml_results(ml_manager: MachineLearningManager):
    """Display comprehensive ML results."""
    
    print(f"\n🤖 Machine Learning Results:")
    
    # System summary
    summary = ml_manager.get_ml_summary()
    
    print(f"\n📊 ML System Summary:")
    
    datasets = summary["datasets"]
    print(f"  Datasets: {datasets['total_datasets']} ({datasets['total_samples']:,} total samples)")
    print(f"  Avg Features per Dataset: {datasets['avg_features']:.0f}")
    
    models = summary["models"]
    print(f"  Models: {models['total_models']}")
    
    performance = summary["performance"]
    print(f"  Deployed Models: {performance['deployed_models']}")
    print(f"  Avg Model Accuracy: {performance['average_model_accuracy']:.1%}")
    print(f"  Avg Inference Time: {performance['average_inference_time_ms']:.1f}ms")
    print(f"  Total Predictions: {performance['total_predictions_served']:,}")
    
    pipelines = summary["pipelines"]
    print(f"  ML Pipelines: {pipelines['total_pipelines']} ({pipelines['automated_pipelines']} automated)")
    print(f"  Avg Pipeline Success: {pipelines['average_success_rate']:.1%}")
    
    experiments = summary["experiments"]
    print(f"  Experiments: {experiments['total_experiments']} total, {experiments['completed_experiments']} completed")
    
    # Model performance details
    print(f"\n🎯 Model Performance by Type:")
    for model_type, count in models["by_type"].items():
        print(f"  {model_type.replace('_', ' ').title()}: {count} models")
    
    print(f"\n🔧 Models by Algorithm:")
    for algorithm, count in models["by_algorithm"].items():
        print(f"  {algorithm.replace('_', ' ').title()}: {count} models")
    
    print(f"\n📈 Model Status Distribution:")
    for status, count in models["by_status"].items():
        print(f"  {status.replace('_', ' ').title()}: {count} models")
    
    # Dataset analysis
    print(f"\n📊 Dataset Analysis:")
    print(f"  Datasets by Domain:")
    for domain, count in datasets["by_domain"].items():
        print(f"    {domain.replace('_', ' ').title()}: {count}")
    
    print(f"  Data Quality Distribution:")
    for quality, count in datasets["by_quality"].items():
        print(f"    {quality.title()}: {count}")
    
    # Recent experiments
    if ml_manager.experiments:
        print(f"\n🧪 Recent Experiments:")
        for experiment in ml_manager.experiments[-2:]:  # Show last 2 experiments
            print(f"  {experiment.experiment_name}:")
            print(f"    Best Performance: {experiment.best_performance:.1%}")
            print(f"    Duration: {experiment.duration_hours:.1f} hours")
            print(f"    Models Tested: {len(experiment.models_tested)}")
    
    # Top performing models
    deployed_models = [m for m in ml_manager.models.values() if m.status == MLModelStatus.DEPLOYED]
    if deployed_models:
        print(f"\n🏆 TOP PERFORMING Deployed Models:")
        
        # Sort by test accuracy
        top_models = sorted(deployed_models, key=lambda m: m.test_accuracy, reverse=True)[:3]
        
        for i, model in enumerate(top_models, 1):
            print(f"  {i}. {model.model_name}")
            print(f"     Algorithm: {model.algorithm.value.replace('_', ' ').title()}")
            print(f"     Test Accuracy: {model.test_accuracy:.1%}")
            print(f"     Predictions: {model.prediction_count:,}")
            print(f"     Avg Inference: {model.average_inference_time_ms:.1f}ms")
            print(f"     Interpretability: {model.interpretability_score:.1%}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    ml_manager = run_demonstration()
    display_ml_results(ml_manager)
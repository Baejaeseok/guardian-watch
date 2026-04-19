"""
Model Validation System
========================
Module 3: Analysis & Modeling Tools

Advanced model validation and performance evaluation system for One Health surveillance,
providing cross-validation, performance metrics, and model reliability assessment.

NIW Focus: Validation intelligence ensuring model accuracy and deployment readiness.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
import itertools
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValidationType(Enum):
    """Types of validation."""
    CROSS_VALIDATION = "cross_validation"       # K-fold cross validation
    HOLDOUT_VALIDATION = "holdout_validation"   # Train/test split
    TEMPORAL_VALIDATION = "temporal_validation" # Time-based validation
    BOOTSTRAP_VALIDATION = "bootstrap_validation" # Bootstrap validation
    ENSEMBLE_VALIDATION = "ensemble_validation" # Multiple model validation
    EXTERNAL_VALIDATION = "external_validation" # External dataset validation

class ModelType(Enum):
    """Types of models to validate."""
    CLASSIFICATION = "classification"           # Classification models
    REGRESSION = "regression"                   # Regression models
    FORECASTING = "forecasting"                # Time series forecasting
    CLUSTERING = "clustering"                  # Clustering models
    OUTBREAK_DETECTION = "outbreak_detection"   # Outbreak detection
    RISK_PREDICTION = "risk_prediction"        # Risk prediction models

class MetricType(Enum):
    """Types of performance metrics."""
    ACCURACY = "accuracy"                      # Classification accuracy
    PRECISION = "precision"                    # Precision
    RECALL = "recall"                          # Recall/Sensitivity
    F1_SCORE = "f1_score"                     # F1 score
    AUC_ROC = "auc_roc"                       # Area under ROC curve
    MAE = "mae"                               # Mean Absolute Error
    RMSE = "rmse"                             # Root Mean Square Error
    R_SQUARED = "r_squared"                    # R-squared
    MAPE = "mape"                             # Mean Absolute Percentage Error

@dataclass
class ValidationDataset:
    """Dataset for validation."""
    dataset_id: str
    features: List[List[float]]                # Feature matrix
    targets: List[Union[float, int, str]]      # Target values
    timestamps: Optional[List[datetime]] = None # Time information
    metadata: Optional[Dict[str, Any]] = None   # Additional metadata
    
    def __post_init__(self):
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def size(self) -> int:
        """Dataset size."""
        return len(self.features)
    
    def split(self, train_ratio: float = 0.8) -> Tuple['ValidationDataset', 'ValidationDataset']:
        """Split dataset into train and test sets."""
        split_idx = int(len(self.features) * train_ratio)
        
        train_dataset = ValidationDataset(
            dataset_id=f"{self.dataset_id}_train",
            features=self.features[:split_idx],
            targets=self.targets[:split_idx],
            timestamps=self.timestamps[:split_idx] if self.timestamps else None,
            metadata=self.metadata.copy()
        )
        
        test_dataset = ValidationDataset(
            dataset_id=f"{self.dataset_id}_test",
            features=self.features[split_idx:],
            targets=self.targets[split_idx:],
            timestamps=self.timestamps[split_idx:] if self.timestamps else None,
            metadata=self.metadata.copy()
        )
        
        return train_dataset, test_dataset

@dataclass
class ModelPrediction:
    """Model prediction with metadata."""
    prediction_id: str
    predicted_values: List[Union[float, int, str]]
    actual_values: List[Union[float, int, str]]
    confidence_scores: Optional[List[float]] = None
    prediction_timestamps: Optional[List[datetime]] = None
    model_metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize metadata if None."""
        if self.model_metadata is None:
            self.model_metadata = {}

@dataclass
class PerformanceMetric:
    """Performance metric result."""
    metric_type: MetricType
    metric_name: str
    metric_value: float
    confidence_interval: Optional[Tuple[float, float]] = None
    statistical_significance: Optional[float] = None
    interpretation: Optional[str] = None

@dataclass
class ValidationResult:
    """Result of model validation."""
    
    validation_id: str
    validation_type: ValidationType
    model_type: ModelType
    validation_timestamp: datetime
    
    # Dataset information
    dataset_size: int
    train_size: Optional[int] = None
    test_size: Optional[int] = None
    
    # Performance metrics
    performance_metrics: List[PerformanceMetric] = field(default_factory=list)
    cross_validation_scores: Optional[List[float]] = None
    
    # Statistical analysis
    mean_performance: Optional[float] = None
    std_performance: Optional[float] = None
    confidence_interval_95: Optional[Tuple[float, float]] = None
    
    # Model reliability
    stability_score: Optional[float] = None        # Consistency across folds
    robustness_score: Optional[float] = None       # Performance under noise
    generalization_score: Optional[float] = None   # Performance on unseen data
    
    # Detailed analysis
    confusion_matrix: Optional[List[List[int]]] = None
    feature_importance: Optional[Dict[str, float]] = None
    validation_curves: Optional[Dict[str, List[float]]] = None
    
    # Performance summary
    validation_duration_seconds: float = 0.0
    model_quality: str = "unknown"                 # "poor", "fair", "good", "excellent"
    deployment_readiness: str = "unknown"          # "not_ready", "needs_improvement", "ready"
    
    # Key insights
    key_findings: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
class PerformanceCalculator:
    """Calculates various performance metrics."""
    
    @staticmethod
    def calculate_classification_metrics(y_true: List[Union[int, str]], 
                                       y_pred: List[Union[int, str]],
                                       y_prob: Optional[List[float]] = None) -> List[PerformanceMetric]:
        """Calculate classification performance metrics."""
        
        if len(y_true) != len(y_pred):
            raise ValueError("True and predicted values must have same length")
        
        metrics = []
        
        # Get unique classes
        unique_classes = sorted(list(set(y_true + y_pred)))
        n_classes = len(unique_classes)
        
        # Create confusion matrix
        confusion_matrix = [[0 for _ in range(n_classes)] for _ in range(n_classes)]
        class_to_idx = {cls: idx for idx, cls in enumerate(unique_classes)}
        
        for true_val, pred_val in zip(y_true, y_pred):
            true_idx = class_to_idx[true_val]
            pred_idx = class_to_idx[pred_val]
            confusion_matrix[true_idx][pred_idx] += 1
        
        # Calculate accuracy
        correct_predictions = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        accuracy = correct_predictions / len(y_true)
        
        metrics.append(PerformanceMetric(
            metric_type=MetricType.ACCURACY,
            metric_name="Accuracy",
            metric_value=accuracy,
            interpretation=PerformanceCalculator._interpret_accuracy(accuracy)
        ))
        
        # For binary classification, calculate additional metrics
        if n_classes == 2:
            # Assume positive class is the second one
            tp = confusion_matrix[1][1]  # True positives
            fp = confusion_matrix[0][1]  # False positives
            tn = confusion_matrix[0][0]  # True negatives
            fn = confusion_matrix[1][0]  # False negatives
            
            # Precision
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            metrics.append(PerformanceMetric(
                metric_type=MetricType.PRECISION,
                metric_name="Precision",
                metric_value=precision,
                interpretation=PerformanceCalculator._interpret_precision(precision)
            ))
            
            # Recall (Sensitivity)
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            metrics.append(PerformanceMetric(
                metric_type=MetricType.RECALL,
                metric_name="Recall",
                metric_value=recall,
                interpretation=PerformanceCalculator._interpret_recall(recall)
            ))
            
            # F1 Score
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            metrics.append(PerformanceMetric(
                metric_type=MetricType.F1_SCORE,
                metric_name="F1 Score",
                metric_value=f1_score,
                interpretation=PerformanceCalculator._interpret_f1_score(f1_score)
            ))
            
            # AUC-ROC (if probabilities provided)
            if y_prob and len(y_prob) == len(y_true):
                auc_roc = PerformanceCalculator._calculate_auc_roc(y_true, y_prob, unique_classes[1])
                metrics.append(PerformanceMetric(
                    metric_type=MetricType.AUC_ROC,
                    metric_name="AUC-ROC",
                    metric_value=auc_roc,
                    interpretation=PerformanceCalculator._interpret_auc_roc(auc_roc)
                ))
        
        return metrics
    
    @staticmethod
    def calculate_regression_metrics(y_true: List[float], 
                                   y_pred: List[float]) -> List[PerformanceMetric]:
        """Calculate regression performance metrics."""
        
        if len(y_true) != len(y_pred):
            raise ValueError("True and predicted values must have same length")
        
        metrics = []
        n = len(y_true)
        
        # Mean Absolute Error
        mae = sum(abs(t - p) for t, p in zip(y_true, y_pred)) / n
        metrics.append(PerformanceMetric(
            metric_type=MetricType.MAE,
            metric_name="Mean Absolute Error",
            metric_value=mae,
            interpretation=f"Average absolute error: {mae:.3f}"
        ))
        
        # Root Mean Square Error
        mse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / n
        rmse = math.sqrt(mse)
        metrics.append(PerformanceMetric(
            metric_type=MetricType.RMSE,
            metric_name="Root Mean Square Error",
            metric_value=rmse,
            interpretation=f"RMS error: {rmse:.3f}"
        ))
        
        # R-squared
        y_mean = statistics.mean(y_true)
        ss_tot = sum((t - y_mean) ** 2 for t in y_true)
        ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        metrics.append(PerformanceMetric(
            metric_type=MetricType.R_SQUARED,
            metric_name="R-squared",
            metric_value=r_squared,
            interpretation=PerformanceCalculator._interpret_r_squared(r_squared)
        ))
        
        # Mean Absolute Percentage Error (if no zero values)
        if all(t != 0 for t in y_true):
            mape = sum(abs((t - p) / t) for t, p in zip(y_true, y_pred)) / n * 100
            metrics.append(PerformanceMetric(
                metric_type=MetricType.MAPE,
                metric_name="Mean Absolute Percentage Error",
                metric_value=mape,
                interpretation=f"Average percentage error: {mape:.1f}%"
            ))
        
        return metrics
    
    @staticmethod
    def _calculate_auc_roc(y_true: List[Union[int, str]], 
                          y_prob: List[float], 
                          positive_class: Union[int, str]) -> float:
        """Calculate AUC-ROC using trapezoidal rule."""
        
        # Convert to binary labels
        binary_true = [1 if label == positive_class else 0 for label in y_true]
        
        # Sort by probability (descending)
        sorted_pairs = sorted(zip(y_prob, binary_true), reverse=True)
        
        # Calculate ROC curve points
        tpr_values = []  # True Positive Rate
        fpr_values = []  # False Positive Rate
        
        pos_count = sum(binary_true)
        neg_count = len(binary_true) - pos_count
        
        if pos_count == 0 or neg_count == 0:
            return 0.5  # No discrimination possible
        
        tp = fp = 0
        
        for i, (prob, label) in enumerate(sorted_pairs):
            if label == 1:
                tp += 1
            else:
                fp += 1
            
            tpr = tp / pos_count
            fpr = fp / neg_count
            
            tpr_values.append(tpr)
            fpr_values.append(fpr)
        
        # Calculate AUC using trapezoidal rule
        auc = 0.0
        for i in range(1, len(fpr_values)):
            auc += (fpr_values[i] - fpr_values[i-1]) * (tpr_values[i] + tpr_values[i-1]) / 2
        
        return auc
    
    @staticmethod
    def _interpret_accuracy(accuracy: float) -> str:
        """Interpret accuracy score."""
        if accuracy >= 0.95:
            return "Excellent accuracy"
        elif accuracy >= 0.85:
            return "Good accuracy"
        elif accuracy >= 0.70:
            return "Fair accuracy"
        else:
            return "Poor accuracy"
    
    @staticmethod
    def _interpret_precision(precision: float) -> str:
        """Interpret precision score."""
        if precision >= 0.90:
            return "Excellent precision - very few false positives"
        elif precision >= 0.75:
            return "Good precision - acceptable false positive rate"
        elif precision >= 0.60:
            return "Fair precision - moderate false positives"
        else:
            return "Poor precision - high false positive rate"
    
    @staticmethod
    def _interpret_recall(recall: float) -> str:
        """Interpret recall score."""
        if recall >= 0.90:
            return "Excellent recall - captures most positive cases"
        elif recall >= 0.75:
            return "Good recall - captures majority of positive cases"
        elif recall >= 0.60:
            return "Fair recall - misses some positive cases"
        else:
            return "Poor recall - misses many positive cases"
    
    @staticmethod
    def _interpret_f1_score(f1_score: float) -> str:
        """Interpret F1 score."""
        if f1_score >= 0.90:
            return "Excellent balance of precision and recall"
        elif f1_score >= 0.75:
            return "Good balance of precision and recall"
        elif f1_score >= 0.60:
            return "Fair balance of precision and recall"
        else:
            return "Poor balance of precision and recall"
    
    @staticmethod
    def _interpret_auc_roc(auc_roc: float) -> str:
        """Interpret AUC-ROC score."""
        if auc_roc >= 0.95:
            return "Excellent discrimination ability"
        elif auc_roc >= 0.85:
            return "Good discrimination ability"
        elif auc_roc >= 0.70:
            return "Fair discrimination ability"
        elif auc_roc >= 0.60:
            return "Poor discrimination ability"
        else:
            return "No discrimination ability"
    
    @staticmethod
    def _interpret_r_squared(r_squared: float) -> str:
        """Interpret R-squared score."""
        if r_squared >= 0.90:
            return "Excellent model fit - explains most variance"
        elif r_squared >= 0.70:
            return "Good model fit - explains substantial variance"
        elif r_squared >= 0.50:
            return "Fair model fit - explains moderate variance"
        else:
            return "Poor model fit - explains little variance"

class CrossValidator:
    """Performs cross-validation of models."""
    
    @staticmethod
    def k_fold_cross_validation(dataset: ValidationDataset,
                               model_function: Callable,
                               k_folds: int = 5,
                               model_type: ModelType = ModelType.CLASSIFICATION) -> List[float]:
        """Perform k-fold cross validation."""
        
        if k_folds < 2:
            raise ValueError("Number of folds must be at least 2")
        
        fold_size = len(dataset.features) // k_folds
        fold_scores = []
        
        # Create indices for k-fold splits
        indices = list(range(len(dataset.features)))
        random.shuffle(indices)  # Shuffle for random splits
        
        for fold in range(k_folds):
            # Define test indices for this fold
            start_idx = fold * fold_size
            end_idx = start_idx + fold_size if fold < k_folds - 1 else len(dataset.features)
            test_indices = set(indices[start_idx:end_idx])
            train_indices = [i for i in indices if i not in test_indices]
            
            # Create train and test sets
            train_features = [dataset.features[i] for i in train_indices]
            train_targets = [dataset.targets[i] for i in train_indices]
            test_features = [dataset.features[i] for i in test_indices]
            test_targets = [dataset.targets[i] for i in test_indices]
            
            # Train model and make predictions
            try:
                predictions = model_function(train_features, train_targets, test_features)
                
                # Calculate performance for this fold
                if model_type == ModelType.CLASSIFICATION:
                    # Classification accuracy
                    correct = sum(1 for true, pred in zip(test_targets, predictions) if true == pred)
                    fold_score = correct / len(test_targets)
                else:
                    # Regression R-squared
                    y_mean = statistics.mean(test_targets)
                    ss_tot = sum((y - y_mean) ** 2 for y in test_targets)
                    ss_res = sum((y - pred) ** 2 for y, pred in zip(test_targets, predictions))
                    fold_score = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
                
                fold_scores.append(fold_score)
                
            except Exception as e:
                logger.warning(f"Fold {fold} failed: {e}")
                fold_scores.append(0.0)
        
        return fold_scores
    
    @staticmethod
    def temporal_validation(dataset: ValidationDataset,
                          model_function: Callable,
                          n_splits: int = 5,
                          model_type: ModelType = ModelType.FORECASTING) -> List[float]:
        """Perform temporal validation with expanding window."""
        
        if not dataset.timestamps:
            raise ValueError("Temporal validation requires timestamps")
        
        # Sort by timestamp
        sorted_indices = sorted(range(len(dataset.timestamps)), key=lambda i: dataset.timestamps[i])
        
        split_scores = []
        initial_size = len(dataset.features) // (n_splits + 1)
        
        for split in range(n_splits):
            # Expanding window: train on data up to split point, test on next portion
            train_end = initial_size + split * (len(dataset.features) // n_splits)
            test_start = train_end
            test_end = test_start + (len(dataset.features) // n_splits)
            
            if test_end > len(dataset.features):
                test_end = len(dataset.features)
            
            train_indices = sorted_indices[:train_end]
            test_indices = sorted_indices[test_start:test_end]
            
            if not test_indices:
                continue
            
            # Create train and test sets
            train_features = [dataset.features[i] for i in train_indices]
            train_targets = [dataset.targets[i] for i in train_indices]
            test_features = [dataset.features[i] for i in test_indices]
            test_targets = [dataset.targets[i] for i in test_indices]
            
            try:
                predictions = model_function(train_features, train_targets, test_features)
                
                # Calculate MAE for temporal validation
                mae = sum(abs(true - pred) for true, pred in zip(test_targets, predictions)) / len(test_targets)
                split_scores.append(1.0 / (1.0 + mae))  # Convert to higher-is-better score
                
            except Exception as e:
                logger.warning(f"Temporal split {split} failed: {e}")
                split_scores.append(0.0)
        
        return split_scores

class OneHealthModelValidator:
    """Main validator for One Health models."""
    
    def __init__(self):
        self.validation_results: List[ValidationResult] = []
        self.validation_log: List[Dict] = []
        
        logger.info("One Health Model Validator initialized")
    
    def comprehensive_model_validation(self, 
                                     dataset: ValidationDataset,
                                     model_function: Callable,
                                     model_type: ModelType = ModelType.CLASSIFICATION,
                                     validation_types: List[ValidationType] = None) -> List[ValidationResult]:
        """Perform comprehensive model validation."""
        
        validation_start = datetime.now()
        results = []
        
        if validation_types is None:
            validation_types = [
                ValidationType.CROSS_VALIDATION,
                ValidationType.HOLDOUT_VALIDATION
            ]
        
        logger.info(f"Starting comprehensive model validation")
        
        # Perform different validation types
        for validation_type in validation_types:
            try:
                if validation_type == ValidationType.CROSS_VALIDATION:
                    result = self._perform_cross_validation(dataset, model_function, model_type)
                elif validation_type == ValidationType.HOLDOUT_VALIDATION:
                    result = self._perform_holdout_validation(dataset, model_function, model_type)
                elif validation_type == ValidationType.TEMPORAL_VALIDATION:
                    if dataset.timestamps:
                        result = self._perform_temporal_validation(dataset, model_function, model_type)
                    else:
                        continue
                elif validation_type == ValidationType.BOOTSTRAP_VALIDATION:
                    result = self._perform_bootstrap_validation(dataset, model_function, model_type)
                else:
                    continue
                
                if result:
                    results.append(result)
                    
            except Exception as e:
                logger.error(f"Error in {validation_type.value} validation: {e}")
        
        # Store results
        self.validation_results.extend(results)
        
        # Log performance
        validation_time = (datetime.now() - validation_start).total_seconds()
        self.validation_log.append({
            "validation_timestamp": validation_start.isoformat(),
            "validation_duration": validation_time,
            "validations_completed": len(results),
            "dataset_size": dataset.size,
            "model_type": model_type.value
        })
        
        logger.info(f"Model validation completed: {len(results)} validations in {validation_time:.2f}s")
        
        return results
    
    def _perform_cross_validation(self, dataset: ValidationDataset,
                                model_function: Callable,
                                model_type: ModelType) -> Optional[ValidationResult]:
        """Perform cross-validation."""
        
        validation_start = datetime.now()
        k_folds = min(5, max(3, dataset.size // 20))  # Adaptive number of folds
        
        # Perform k-fold cross validation
        cv_scores = CrossValidator.k_fold_cross_validation(
            dataset, model_function, k_folds, model_type
        )
        
        if not cv_scores:
            return None
        
        # Calculate statistics
        mean_score = statistics.mean(cv_scores)
        std_score = statistics.stdev(cv_scores) if len(cv_scores) > 1 else 0.0
        
        # Calculate confidence interval (approximate)
        if len(cv_scores) > 1:
            margin_error = 1.96 * std_score / math.sqrt(len(cv_scores))  # 95% CI
            ci_lower = max(0, mean_score - margin_error)
            ci_upper = min(1, mean_score + margin_error)
            confidence_interval = (ci_lower, ci_upper)
        else:
            confidence_interval = None
        
        # Create performance metric
        primary_metric = PerformanceMetric(
            metric_type=MetricType.ACCURACY if model_type == ModelType.CLASSIFICATION else MetricType.R_SQUARED,
            metric_name="Cross-Validation Score",
            metric_value=mean_score,
            confidence_interval=confidence_interval,
            interpretation=self._interpret_cv_score(mean_score, std_score)
        )
        
        # Assess model quality and deployment readiness
        model_quality, deployment_readiness = self._assess_model_quality(mean_score, std_score)
        
        # Generate insights
        key_findings = []
        key_findings.append(f"Cross-validation mean score: {mean_score:.3f} (±{std_score:.3f})")
        
        if std_score < 0.05:
            key_findings.append("Model shows consistent performance across folds")
        elif std_score > 0.15:
            key_findings.append("Model performance varies significantly across folds")
        
        recommendations = []
        if mean_score < 0.7:
            recommendations.append("Consider feature engineering or different algorithms")
        if std_score > 0.10:
            recommendations.append("Investigate model stability - consider ensemble methods")
        
        limitations = []
        if dataset.size < 100:
            limitations.append("Small dataset size may limit validation reliability")
        
        validation_duration = (datetime.now() - validation_start).total_seconds()
        
        return ValidationResult(
            validation_id=f"CV_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            validation_type=ValidationType.CROSS_VALIDATION,
            model_type=model_type,
            validation_timestamp=validation_start,
            dataset_size=dataset.size,
            performance_metrics=[primary_metric],
            cross_validation_scores=cv_scores,
            mean_performance=mean_score,
            std_performance=std_score,
            confidence_interval_95=confidence_interval,
            stability_score=1.0 - min(std_score / mean_score if mean_score > 0 else 1.0, 1.0),
            validation_duration_seconds=validation_duration,
            model_quality=model_quality,
            deployment_readiness=deployment_readiness,
            key_findings=key_findings,
            recommendations=recommendations,
            limitations=limitations
        )
    
    def _perform_holdout_validation(self, dataset: ValidationDataset,
                                  model_function: Callable,
                                  model_type: ModelType) -> Optional[ValidationResult]:
        """Perform holdout validation."""
        
        validation_start = datetime.now()
        
        # Split dataset
        train_dataset, test_dataset = dataset.split(train_ratio=0.8)
        
        try:
            # Train model and make predictions
            predictions = model_function(
                train_dataset.features, train_dataset.targets, test_dataset.features
            )
            
            # Calculate performance metrics
            if model_type == ModelType.CLASSIFICATION:
                metrics = PerformanceCalculator.calculate_classification_metrics(
                    test_dataset.targets, predictions
                )
                primary_score = metrics[0].metric_value  # Accuracy
            else:
                metrics = PerformanceCalculator.calculate_regression_metrics(
                    test_dataset.targets, predictions
                )
                primary_score = next((m.metric_value for m in metrics if m.metric_type == MetricType.R_SQUARED), 0.0)
            
            # Assess quality
            model_quality, deployment_readiness = self._assess_model_quality(primary_score, 0.0)
            
            # Generate insights
            key_findings = []
            key_findings.append(f"Holdout validation score: {primary_score:.3f}")
            
            for metric in metrics:
                if metric.interpretation:
                    key_findings.append(metric.interpretation)
            
            recommendations = []
            if primary_score < 0.8:
                recommendations.append("Consider collecting more training data")
            
            validation_duration = (datetime.now() - validation_start).total_seconds()
            
            return ValidationResult(
                validation_id=f"HOLDOUT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                validation_type=ValidationType.HOLDOUT_VALIDATION,
                model_type=model_type,
                validation_timestamp=validation_start,
                dataset_size=dataset.size,
                train_size=len(train_dataset.features),
                test_size=len(test_dataset.features),
                performance_metrics=metrics,
                mean_performance=primary_score,
                std_performance=0.0,
                generalization_score=primary_score,
                validation_duration_seconds=validation_duration,
                model_quality=model_quality,
                deployment_readiness=deployment_readiness,
                key_findings=key_findings,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Holdout validation failed: {e}")
            return None
    
    def _perform_temporal_validation(self, dataset: ValidationDataset,
                                   model_function: Callable,
                                   model_type: ModelType) -> Optional[ValidationResult]:
        """Perform temporal validation."""
        
        validation_start = datetime.now()
        
        try:
            # Perform temporal validation
            temporal_scores = CrossValidator.temporal_validation(
                dataset, model_function, n_splits=3, model_type=model_type
            )
            
            if not temporal_scores:
                return None
            
            mean_score = statistics.mean(temporal_scores)
            std_score = statistics.stdev(temporal_scores) if len(temporal_scores) > 1 else 0.0
            
            # Create primary metric
            primary_metric = PerformanceMetric(
                metric_type=MetricType.ACCURACY if model_type == ModelType.CLASSIFICATION else MetricType.MAE,
                metric_name="Temporal Validation Score",
                metric_value=mean_score,
                interpretation=f"Average temporal validation score: {mean_score:.3f}"
            )
            
            # Assess quality
            model_quality, deployment_readiness = self._assess_model_quality(mean_score, std_score)
            
            key_findings = []
            key_findings.append(f"Temporal validation demonstrates time-series performance")
            key_findings.append(f"Mean temporal score: {mean_score:.3f}")
            
            validation_duration = (datetime.now() - validation_start).total_seconds()
            
            return ValidationResult(
                validation_id=f"TEMPORAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                validation_type=ValidationType.TEMPORAL_VALIDATION,
                model_type=model_type,
                validation_timestamp=validation_start,
                dataset_size=dataset.size,
                performance_metrics=[primary_metric],
                cross_validation_scores=temporal_scores,
                mean_performance=mean_score,
                std_performance=std_score,
                validation_duration_seconds=validation_duration,
                model_quality=model_quality,
                deployment_readiness=deployment_readiness,
                key_findings=key_findings
            )
            
        except Exception as e:
            logger.error(f"Temporal validation failed: {e}")
            return None
    
    def _perform_bootstrap_validation(self, dataset: ValidationDataset,
                                    model_function: Callable,
                                    model_type: ModelType) -> Optional[ValidationResult]:
        """Perform bootstrap validation."""
        
        validation_start = datetime.now()
        n_bootstrap = min(100, max(20, dataset.size // 10))  # Adaptive bootstrap samples
        
        bootstrap_scores = []
        
        for bootstrap_iter in range(n_bootstrap):
            try:
                # Create bootstrap sample
                bootstrap_indices = [random.randint(0, dataset.size - 1) for _ in range(dataset.size)]
                
                # Out-of-bag samples for testing
                oob_indices = [i for i in range(dataset.size) if i not in set(bootstrap_indices)]
                
                if not oob_indices:  # Skip if no out-of-bag samples
                    continue
                
                # Create bootstrap training set
                bootstrap_features = [dataset.features[i] for i in bootstrap_indices]
                bootstrap_targets = [dataset.targets[i] for i in bootstrap_indices]
                
                # Out-of-bag test set
                oob_features = [dataset.features[i] for i in oob_indices]
                oob_targets = [dataset.targets[i] for i in oob_indices]
                
                # Train and predict
                predictions = model_function(bootstrap_features, bootstrap_targets, oob_features)
                
                # Calculate score
                if model_type == ModelType.CLASSIFICATION:
                    correct = sum(1 for true, pred in zip(oob_targets, predictions) if true == pred)
                    score = correct / len(oob_targets)
                else:
                    mae = sum(abs(true - pred) for true, pred in zip(oob_targets, predictions)) / len(oob_targets)
                    score = 1.0 / (1.0 + mae)
                
                bootstrap_scores.append(score)
                
            except Exception as e:
                continue  # Skip failed bootstrap iterations
        
        if not bootstrap_scores:
            return None
        
        mean_score = statistics.mean(bootstrap_scores)
        std_score = statistics.stdev(bootstrap_scores) if len(bootstrap_scores) > 1 else 0.0
        
        # Bootstrap confidence interval
        if len(bootstrap_scores) >= 20:
            sorted_scores = sorted(bootstrap_scores)
            ci_lower = sorted_scores[int(0.025 * len(sorted_scores))]
            ci_upper = sorted_scores[int(0.975 * len(sorted_scores))]
            confidence_interval = (ci_lower, ci_upper)
        else:
            confidence_interval = None
        
        # Create primary metric
        primary_metric = PerformanceMetric(
            metric_type=MetricType.ACCURACY if model_type == ModelType.CLASSIFICATION else MetricType.R_SQUARED,
            metric_name="Bootstrap Validation Score",
            metric_value=mean_score,
            confidence_interval=confidence_interval,
            interpretation=f"Bootstrap validation with {len(bootstrap_scores)} samples"
        )
        
        # Assess quality
        model_quality, deployment_readiness = self._assess_model_quality(mean_score, std_score)
        
        key_findings = []
        key_findings.append(f"Bootstrap validation across {len(bootstrap_scores)} samples")
        key_findings.append(f"Mean bootstrap score: {mean_score:.3f} (±{std_score:.3f})")
        
        validation_duration = (datetime.now() - validation_start).total_seconds()
        
        return ValidationResult(
            validation_id=f"BOOTSTRAP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            validation_type=ValidationType.BOOTSTRAP_VALIDATION,
            model_type=model_type,
            validation_timestamp=validation_start,
            dataset_size=dataset.size,
            performance_metrics=[primary_metric],
            mean_performance=mean_score,
            std_performance=std_score,
            confidence_interval_95=confidence_interval,
            robustness_score=1.0 - min(std_score / mean_score if mean_score > 0 else 1.0, 1.0),
            validation_duration_seconds=validation_duration,
            model_quality=model_quality,
            deployment_readiness=deployment_readiness,
            key_findings=key_findings
        )
    
    def _interpret_cv_score(self, mean_score: float, std_score: float) -> str:
        """Interpret cross-validation score."""
        base_interpretation = f"Mean CV score: {mean_score:.3f}"
        
        if std_score < 0.05:
            stability = "very stable"
        elif std_score < 0.10:
            stability = "stable"
        elif std_score < 0.20:
            stability = "moderately stable"
        else:
            stability = "unstable"
        
        return f"{base_interpretation} ({stability} across folds)"
    
    def _assess_model_quality(self, score: float, std_score: float) -> Tuple[str, str]:
        """Assess overall model quality and deployment readiness."""
        
        # Quality assessment
        if score >= 0.90:
            quality = "excellent"
        elif score >= 0.80:
            quality = "good"
        elif score >= 0.70:
            quality = "fair"
        else:
            quality = "poor"
        
        # Deployment readiness
        if score >= 0.85 and std_score <= 0.10:
            readiness = "ready"
        elif score >= 0.70 and std_score <= 0.15:
            readiness = "needs_improvement"
        else:
            readiness = "not_ready"
        
        return quality, readiness
    
    def get_validation_summary(self) -> Dict:
        """Get summary of validation results."""
        
        if not self.validation_results:
            return {"message": "No validations performed"}
        
        # Aggregate statistics
        total_validations = len(self.validation_results)
        
        # Performance statistics
        mean_performances = [r.mean_performance for r in self.validation_results]
        overall_mean = statistics.mean(mean_performances)
        overall_std = statistics.stdev(mean_performances) if len(mean_performances) > 1 else 0.0
        
        # Quality distribution
        quality_counts = defaultdict(int)
        readiness_counts = defaultdict(int)
        
        for result in self.validation_results:
            quality_counts[result.model_quality] += 1
            readiness_counts[result.deployment_readiness] += 1
        
        # Validation types used
        validation_types = [r.validation_type.value for r in self.validation_results]
        
        # Performance metrics
        validation_times = [r.validation_duration_seconds for r in self.validation_results]
        
        return {
            "total_validations": total_validations,
            "validation_types": list(set(validation_types)),
            "overall_performance": {
                "mean_score": overall_mean,
                "std_score": overall_std
            },
            "quality_distribution": dict(quality_counts),
            "deployment_readiness": dict(readiness_counts),
            "performance": {
                "average_validation_time": statistics.mean(validation_times) if validation_times else 0,
                "total_validation_time": sum(validation_times)
            }
        }
    
    def get_best_models(self, top_n: int = 5) -> List[Dict]:
        """Get top performing models from validation results."""
        
        # Sort by mean performance
        sorted_results = sorted(
            self.validation_results, 
            key=lambda r: r.mean_performance, 
            reverse=True
        )
        
        best_models = []
        
        for result in sorted_results[:top_n]:
            model_info = {
                'validation_id': result.validation_id,
                'validation_type': result.validation_type.value,
                'model_type': result.model_type.value,
                'mean_performance': result.mean_performance,
                'std_performance': result.std_performance,
                'model_quality': result.model_quality,
                'deployment_readiness': result.deployment_readiness,
                'stability_score': result.stability_score,
                'generalization_score': result.generalization_score
            }
            best_models.append(model_info)
        
        return best_models

# Mock model functions for demonstration
def mock_classification_model(train_features: List[List[float]], 
                            train_targets: List[Union[int, str]], 
                            test_features: List[List[float]]) -> List[Union[int, str]]:
    """Mock classification model for testing."""
    
    # Simple mock model based on first feature
    predictions = []
    
    # Calculate threshold from training data
    if train_features and len(train_features[0]) > 0:
        feature_values = [features[0] for features in train_features]
        threshold = statistics.median(feature_values)
    else:
        threshold = 0.5
    
    for features in test_features:
        if len(features) > 0:
            if features[0] > threshold:
                predictions.append("positive")
            else:
                predictions.append("negative")
        else:
            predictions.append("negative")
    
    return predictions

def mock_regression_model(train_features: List[List[float]], 
                        train_targets: List[float], 
                        test_features: List[List[float]]) -> List[float]:
    """Mock regression model for testing."""
    
    # Simple linear model based on first feature
    predictions = []
    
    if train_features and len(train_features[0]) > 0:
        # Calculate simple linear relationship
        x_values = [features[0] for features in train_features]
        y_values = train_targets
        
        if len(x_values) > 1:
            # Simple linear regression
            x_mean = statistics.mean(x_values)
            y_mean = statistics.mean(y_values)
            
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
            denominator = sum((x - x_mean) ** 2 for x in x_values)
            
            slope = numerator / denominator if denominator != 0 else 0
            intercept = y_mean - slope * x_mean
        else:
            slope = 0
            intercept = statistics.mean(y_values) if y_values else 0
    else:
        slope = 0
        intercept = 0
    
    for features in test_features:
        if len(features) > 0:
            prediction = slope * features[0] + intercept
            # Add some noise
            prediction += random.uniform(-0.1, 0.1)
            predictions.append(prediction)
        else:
            predictions.append(intercept)
    
    return predictions

# Mock data generator
def generate_mock_validation_data():
    """Generate mock data for validation testing."""
    
    # Classification dataset
    classification_features = []
    classification_targets = []
    
    for i in range(200):
        # Generate features with some pattern
        feature1 = random.uniform(0, 10)
        feature2 = random.uniform(0, 5)
        feature3 = random.uniform(-2, 2)
        
        features = [feature1, feature2, feature3]
        
        # Target based on features with noise
        decision_value = feature1 * 0.5 + feature2 * 0.3 - feature3 * 0.2 + random.uniform(-1, 1)
        target = "positive" if decision_value > 2.5 else "negative"
        
        classification_features.append(features)
        classification_targets.append(target)
    
    classification_dataset = ValidationDataset(
        dataset_id="mock_classification",
        features=classification_features,
        targets=classification_targets
    )
    
    # Regression dataset
    regression_features = []
    regression_targets = []
    
    for i in range(150):
        # Generate features
        feature1 = random.uniform(0, 10)
        feature2 = random.uniform(0, 5)
        
        features = [feature1, feature2]
        
        # Target with linear relationship plus noise
        target = 2.0 * feature1 + 1.5 * feature2 + 3.0 + random.uniform(-2, 2)
        
        regression_features.append(features)
        regression_targets.append(target)
    
    regression_dataset = ValidationDataset(
        dataset_id="mock_regression",
        features=regression_features,
        targets=regression_targets
    )
    
    # Temporal dataset
    temporal_features = []
    temporal_targets = []
    temporal_timestamps = []
    
    base_date = datetime.now() - timedelta(days=100)
    
    for i in range(100):
        date = base_date + timedelta(days=i)
        
        # Features with temporal trend
        feature1 = 5 + i * 0.05 + random.uniform(-1, 1)  # Trend
        feature2 = 2 + 2 * math.sin(i * 0.1) + random.uniform(-0.5, 0.5)  # Seasonal
        
        features = [feature1, feature2]
        
        # Target based on trend
        target = feature1 + 0.5 * feature2 + random.uniform(-1, 1)
        
        temporal_features.append(features)
        temporal_targets.append(target)
        temporal_timestamps.append(date)
    
    temporal_dataset = ValidationDataset(
        dataset_id="mock_temporal",
        features=temporal_features,
        targets=temporal_targets,
        timestamps=temporal_timestamps
    )
    
    return classification_dataset, regression_dataset, temporal_dataset

def run_demonstration():
    """Run demonstration of model validation system."""
    print("🔬 One Health Model Validation System - Demonstration")
    print("=" * 60)
    
    # Initialize validator
    validator = OneHealthModelValidator()
    
    # Generate mock datasets
    classification_data, regression_data, temporal_data = generate_mock_validation_data()
    
    print(f"\n📊 Validation Datasets:")
    print(f"  Classification Dataset: {classification_data.size} samples")
    print(f"  Regression Dataset: {regression_data.size} samples")
    print(f"  Temporal Dataset: {temporal_data.size} samples")
    
    # Perform comprehensive validation
    print(f"\n🔬 Running Comprehensive Model Validation...")
    
    # 1. Classification model validation
    print(f"\n1. Classification Model Validation")
    classification_results = validator.comprehensive_model_validation(
        dataset=classification_data,
        model_function=mock_classification_model,
        model_type=ModelType.CLASSIFICATION,
        validation_types=[
            ValidationType.CROSS_VALIDATION,
            ValidationType.HOLDOUT_VALIDATION,
            ValidationType.BOOTSTRAP_VALIDATION
        ]
    )
    
    # 2. Regression model validation
    print(f"\n2. Regression Model Validation")
    regression_results = validator.comprehensive_model_validation(
        dataset=regression_data,
        model_function=mock_regression_model,
        model_type=ModelType.REGRESSION,
        validation_types=[
            ValidationType.CROSS_VALIDATION,
            ValidationType.HOLDOUT_VALIDATION
        ]
    )
    
    # 3. Temporal model validation
    print(f"\n3. Temporal Model Validation")
    temporal_results = validator.comprehensive_model_validation(
        dataset=temporal_data,
        model_function=mock_regression_model,
        model_type=ModelType.FORECASTING,
        validation_types=[
            ValidationType.TEMPORAL_VALIDATION,
            ValidationType.CROSS_VALIDATION
        ]
    )
    
    # Display validation results
    all_results = classification_results + regression_results + temporal_results
    print(f"\n📊 Model Validation Results ({len(all_results)} total):")
    
    for i, result in enumerate(all_results, 1):
        print(f"\n{i}. {result.validation_type.value.replace('_', ' ').title()}")
        print(f"   Model Type: {result.model_type.value.replace('_', ' ').title()}")
        print(f"   Dataset Size: {result.dataset_size}")
        if result.train_size:
            print(f"   Train/Test Split: {result.train_size}/{result.test_size}")
        
        print(f"   Mean Performance: {result.mean_performance:.3f}")
        print(f"   Std Performance: {result.std_performance:.3f}")
        
        if result.confidence_interval_95:
            ci_lower, ci_upper = result.confidence_interval_95
            print(f"   95% Confidence Interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
        
        if result.stability_score:
            print(f"   Stability Score: {result.stability_score:.3f}")
        
        if result.generalization_score:
            print(f"   Generalization Score: {result.generalization_score:.3f}")
        
        if result.robustness_score:
            print(f"   Robustness Score: {result.robustness_score:.3f}")
        
        print(f"   Model Quality: {result.model_quality.upper()}")
        print(f"   Deployment Ready: {result.deployment_readiness.replace('_', ' ').upper()}")
        print(f"   Validation Duration: {result.validation_duration_seconds:.3f}s")
        
        # Performance metrics
        if result.performance_metrics:
            print(f"   Performance Metrics ({len(result.performance_metrics)}):")
            for metric in result.performance_metrics:
                print(f"     • {metric.metric_name}: {metric.metric_value:.3f}")
                if metric.interpretation:
                    print(f"       {metric.interpretation}")
        
        # Cross-validation scores
        if result.cross_validation_scores:
            scores_str = ", ".join([f"{score:.3f}" for score in result.cross_validation_scores])
            print(f"   CV Scores: [{scores_str}]")
        
        # Key findings
        if result.key_findings:
            print(f"   Key Findings ({len(result.key_findings)}):")
            for finding in result.key_findings:
                print(f"     • {finding}")
        
        # Recommendations
        if result.recommendations:
            print(f"   Recommendations ({len(result.recommendations)}):")
            for rec in result.recommendations:
                print(f"     • {rec}")
        
        # Limitations
        if result.limitations:
            print(f"   Limitations ({len(result.limitations)}):")
            for limit in result.limitations:
                print(f"     • {limit}")
    
    # Validation summary
    summary = validator.get_validation_summary()
    print(f"\n📊 Validation Summary:")
    print(f"  Total Validations: {summary['total_validations']}")
    print(f"  Validation Types: {', '.join(summary['validation_types'])}")
    
    perf = summary['overall_performance']
    print(f"  Overall Mean Performance: {perf['mean_score']:.3f} (±{perf['std_score']:.3f})")
    
    print(f"\n📈 Quality Distribution:")
    quality_dist = summary['quality_distribution']
    for quality, count in quality_dist.items():
        print(f"  {quality.title()}: {count}")
    
    print(f"\n🚀 Deployment Readiness:")
    readiness_dist = summary['deployment_readiness']
    for readiness, count in readiness_dist.items():
        print(f"  {readiness.replace('_', ' ').title()}: {count}")
    
    print(f"\n⚡ Performance:")
    perf_stats = summary['performance']
    print(f"  Average Validation Time: {perf_stats['average_validation_time']:.3f}s")
    print(f"  Total Validation Time: {perf_stats['total_validation_time']:.3f}s")
    
    # Best models
    best_models = validator.get_best_models(top_n=3)
    if best_models:
        print(f"\n🏆 TOP PERFORMING Models ({len(best_models)}):")
        for i, model in enumerate(best_models, 1):
            print(f"  {i}. {model['validation_type'].replace('_', ' ').title()}")
            print(f"     Model Type: {model['model_type'].replace('_', ' ').title()}")
            print(f"     Performance: {model['mean_performance']:.3f}")
            print(f"     Quality: {model['model_quality'].title()}")
            print(f"     Deployment Ready: {model['deployment_readiness'].replace('_', ' ').title()}")
            if model['stability_score']:
                print(f"     Stability: {model['stability_score']:.3f}")
    
    return validator

if __name__ == "__main__":
    validator = run_demonstration()
"""
Predictive Modeling and Forecasting System
==========================================
Module 6: Advanced Analytics

Advanced predictive modeling system for One Health applications, providing sophisticated
forecasting models, risk prediction, and scenario analysis capabilities.

NIW Focus: Predictive intelligence enabling proactive One Health surveillance, 
risk assessment, and strategic planning across human, animal, and environmental health.
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

class PredictionType(Enum):
    """Types of predictive modeling."""
    CLASSIFICATION = "classification"              # Predict categories/classes
    REGRESSION = "regression"                      # Predict continuous values
    TIME_SERIES = "time_series"                   # Time-based predictions
    SURVIVAL_ANALYSIS = "survival_analysis"        # Time-to-event predictions
    RISK_SCORING = "risk_scoring"                 # Risk assessment models
    PROBABILITY_ESTIMATION = "probability"         # Probability predictions
    MULTI_OUTPUT = "multi_output"                 # Multiple target predictions

class ModelingTechnique(Enum):
    """Predictive modeling techniques."""
    LINEAR_MODELS = "linear_models"               # Linear/logistic regression
    TREE_BASED = "tree_based"                    # Decision trees, RF, GBM
    NEURAL_NETWORKS = "neural_networks"          # Deep learning models
    BAYESIAN_MODELS = "bayesian_models"          # Bayesian approaches
    ENSEMBLE_METHODS = "ensemble_methods"        # Model ensembles
    TIME_SERIES_MODELS = "time_series_models"    # ARIMA, Prophet, etc.
    SURVIVAL_MODELS = "survival_models"          # Cox, parametric survival
    CAUSAL_INFERENCE = "causal_inference"        # Causal modeling

class PredictionHorizon(Enum):
    """Prediction time horizons."""
    REAL_TIME = "real_time"                      # Immediate predictions
    SHORT_TERM = "short_term"                    # Days to weeks
    MEDIUM_TERM = "medium_term"                  # Weeks to months
    LONG_TERM = "long_term"                      # Months to years
    STRATEGIC = "strategic"                      # Multi-year forecasts

class UncertaintyType(Enum):
    """Types of prediction uncertainty."""
    ALEATORY = "aleatory"                        # Natural randomness
    EPISTEMIC = "epistemic"                      # Knowledge uncertainty
    PARAMETER = "parameter"                      # Parameter uncertainty
    MODEL = "model"                             # Model uncertainty
    DATA = "data"                               # Data quality uncertainty

@dataclass
class PredictionRequest:
    """Prediction request specification."""
    
    request_id: str
    request_name: str
    prediction_type: PredictionType
    modeling_technique: ModelingTechnique
    
    # Prediction target
    target_variable: str
    target_description: str
    prediction_horizon: PredictionHorizon
    
    # Input specification
    input_features: List[str] = field(default_factory=list)
    feature_types: Dict[str, str] = field(default_factory=dict)  # "numerical", "categorical"
    temporal_features: List[str] = field(default_factory=list)
    
    # Request configuration
    confidence_level: float = 0.95
    prediction_intervals: bool = True
    uncertainty_quantification: bool = True
    feature_importance: bool = True
    
    # Domain context
    health_domain: str = "general"               # "human", "animal", "environmental"
    application_context: str = ""               # Specific use case
    
    # Request metadata
    requested_by: str = "prediction_system"
    request_date: datetime = field(default_factory=datetime.now)
    priority: str = "medium"                    # "low", "medium", "high", "critical"
    deadline: Optional[datetime] = None

@dataclass
class PredictiveModel:
    """Predictive model specification and metadata."""
    
    model_id: str
    model_name: str
    prediction_type: PredictionType
    technique: ModelingTechnique
    
    # Model specification
    algorithm_details: str
    model_parameters: Dict[str, Any] = field(default_factory=dict)
    feature_set: List[str] = field(default_factory=list)
    target_variable: str = ""
    
    # Training details
    training_data_size: int = 0
    training_period: Tuple[datetime, datetime] = (datetime.now(), datetime.now())
    validation_method: str = "cross_validation"
    
    # Performance metrics
    accuracy_metrics: Dict[str, float] = field(default_factory=dict)
    error_metrics: Dict[str, float] = field(default_factory=dict)
    calibration_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Uncertainty quantification
    uncertainty_method: str = "bootstrap"       # Method for uncertainty estimation
    prediction_intervals_available: bool = False
    confidence_scores_available: bool = False
    
    # Model validation
    cross_validation_score: float = 0.0
    holdout_test_score: float = 0.0
    temporal_validation_score: float = 0.0      # For time series models
    
    # Interpretability
    interpretability_score: float = 0.0
    feature_importance_available: bool = False
    shap_values_available: bool = False
    
    # Model lifecycle
    model_status: str = "development"           # "development", "validated", "deployed"
    deployment_date: Optional[datetime] = None
    last_retrained: Optional[datetime] = None
    model_version: str = "1.0"

@dataclass
class PredictionResult:
    """Comprehensive prediction result."""
    
    prediction_id: str
    request_id: str
    model_id: str
    prediction_timestamp: datetime
    
    # Prediction outputs
    predicted_value: Union[float, str, List[float]] = None
    prediction_probability: Optional[float] = None
    predicted_class: Optional[str] = None
    class_probabilities: Dict[str, float] = field(default_factory=dict)
    
    # Uncertainty quantification
    confidence_interval: Optional[Tuple[float, float]] = None
    prediction_std: Optional[float] = None
    uncertainty_breakdown: Dict[UncertaintyType, float] = field(default_factory=dict)
    
    # Risk assessment (for risk scoring models)
    risk_score: Optional[float] = None
    risk_category: Optional[str] = None
    risk_factors: List[str] = field(default_factory=list)
    
    # Feature contributions
    feature_importance: Dict[str, float] = field(default_factory=dict)
    feature_values: Dict[str, Any] = field(default_factory=dict)
    
    # Prediction quality
    model_confidence: float = 0.0               # Model's confidence in prediction
    prediction_reliability: float = 0.0        # Overall reliability score
    data_quality_score: float = 0.0           # Input data quality
    
    # Contextual information
    prediction_horizon_used: PredictionHorizon = PredictionHorizon.SHORT_TERM
    prediction_basis: str = ""                 # What the prediction is based on
    assumptions: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)

@dataclass
class ScenarioAnalysis:
    """Scenario-based predictive analysis."""
    
    scenario_id: str
    scenario_name: str
    description: str
    
    # Scenario configuration
    base_scenario: Dict[str, Any] = field(default_factory=dict)
    scenario_variations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Analysis parameters
    model_id: str = ""
    prediction_horizon: PredictionHorizon = PredictionHorizon.MEDIUM_TERM
    uncertainty_analysis: bool = True
    
    # Scenario results
    scenario_predictions: Dict[str, PredictionResult] = field(default_factory=dict)
    comparison_matrix: Dict[Tuple[str, str], float] = field(default_factory=dict)
    
    # Risk assessment
    scenario_risks: Dict[str, float] = field(default_factory=dict)
    risk_ranking: List[Tuple[str, float]] = field(default_factory=list)
    
    # Decision support
    recommended_scenario: Optional[str] = None
    decision_criteria: List[str] = field(default_factory=list)
    trade_off_analysis: Dict[str, Any] = field(default_factory=dict)
    
    # Analysis metadata
    analysis_date: datetime = field(default_factory=datetime.now)
    analyzed_by: str = "scenario_system"
    confidence_in_analysis: float = 0.0

class PredictiveModelingEngine:
    """Comprehensive predictive modeling and forecasting engine."""
    
    def __init__(self):
        self.prediction_requests: Dict[str, PredictionRequest] = {}
        self.predictive_models: Dict[str, PredictiveModel] = {}
        self.prediction_results: List[PredictionResult] = []
        self.scenario_analyses: List[ScenarioAnalysis] = []
        
        # Modeling capabilities
        self.technique_algorithms = {
            ModelingTechnique.LINEAR_MODELS: ["linear_regression", "logistic_regression", "ridge", "lasso"],
            ModelingTechnique.TREE_BASED: ["random_forest", "gradient_boosting", "xgboost", "decision_tree"],
            ModelingTechnique.NEURAL_NETWORKS: ["mlp", "lstm", "gru", "transformer"],
            ModelingTechnique.TIME_SERIES_MODELS: ["arima", "prophet", "seasonal_naive", "exponential_smoothing"],
            ModelingTechnique.ENSEMBLE_METHODS: ["voting_classifier", "stacking", "bagging", "boosting"]
        }
        
        # Initialize framework
        self._initialize_predictive_framework()
        
        logger.info("Predictive Modeling Engine initialized for One Health")
    
    def _initialize_predictive_framework(self):
        """Initialize predictive modeling framework."""
        
        # Sample prediction requests
        sample_requests = [
            {
                "name": "Zoonotic Disease Outbreak Prediction", 
                "type": PredictionType.CLASSIFICATION, "technique": ModelingTechnique.ENSEMBLE_METHODS,
                "target": "outbreak_probability", "horizon": PredictionHorizon.SHORT_TERM,
                "domain": "zoonotic", "context": "Early warning system"
            },
            {
                "name": "Environmental Health Risk Forecasting",
                "type": PredictionType.REGRESSION, "technique": ModelingTechnique.TIME_SERIES_MODELS,
                "target": "health_risk_score", "horizon": PredictionHorizon.MEDIUM_TERM,
                "domain": "environmental", "context": "Public health planning"
            },
            {
                "name": "AMR Prevalence Prediction",
                "type": PredictionType.TIME_SERIES, "technique": ModelingTechnique.NEURAL_NETWORKS,
                "target": "resistance_rate", "horizon": PredictionHorizon.LONG_TERM,
                "domain": "antimicrobial", "context": "Antimicrobial stewardship"
            },
            {
                "name": "Food Safety Risk Assessment",
                "type": PredictionType.RISK_SCORING, "technique": ModelingTechnique.TREE_BASED,
                "target": "contamination_risk", "horizon": PredictionHorizon.REAL_TIME,
                "domain": "food_safety", "context": "Supply chain monitoring"
            },
            {
                "name": "Vector-Borne Disease Spread Modeling",
                "type": PredictionType.PROBABILITY_ESTIMATION, "technique": ModelingTechnique.BAYESIAN_MODELS,
                "target": "transmission_probability", "horizon": PredictionHorizon.STRATEGIC,
                "domain": "vector_borne", "context": "Climate change adaptation"
            }
        ]
        
        # Create prediction requests
        for request_data in sample_requests:
            request_id = f"REQ_{random.randint(100000, 999999)}"
            
            request = PredictionRequest(
                request_id=request_id,
                request_name=request_data["name"],
                prediction_type=request_data["type"],
                modeling_technique=request_data["technique"],
                target_variable=request_data["target"],
                target_description=f"Prediction of {request_data['target']} for {request_data['context']}",
                prediction_horizon=request_data["horizon"],
                health_domain=request_data["domain"],
                application_context=request_data["context"],
                deadline=datetime.now() + timedelta(days=random.randint(7, 30))
            )
            
            # Add sample features
            request.input_features = [
                "temporal_trend", "geographic_location", "population_density",
                "climate_factors", "surveillance_data", "intervention_history"
            ]
            
            request.feature_types = {
                "temporal_trend": "numerical",
                "geographic_location": "categorical", 
                "population_density": "numerical",
                "climate_factors": "numerical",
                "surveillance_data": "numerical",
                "intervention_history": "categorical"
            }
            
            request.temporal_features = ["temporal_trend", "surveillance_data"]
            
            self.prediction_requests[request_id] = request
        
        # Sample predictive models
        sample_models = [
            {
                "name": "Zoonotic Outbreak Early Warning Model",
                "type": PredictionType.CLASSIFICATION, "technique": ModelingTechnique.ENSEMBLE_METHODS,
                "algorithm": "Gradient Boosting Classifier with Random Forest ensemble",
                "target": "outbreak_risk_level"
            },
            {
                "name": "Environmental Health Impact Forecaster", 
                "type": PredictionType.REGRESSION, "technique": ModelingTechnique.TIME_SERIES_MODELS,
                "algorithm": "Prophet with environmental covariates",
                "target": "health_impact_index"
            },
            {
                "name": "AMR Trend Predictor",
                "type": PredictionType.TIME_SERIES, "technique": ModelingTechnique.NEURAL_NETWORKS,
                "algorithm": "LSTM with attention mechanism",
                "target": "resistance_prevalence"
            },
            {
                "name": "Real-time Food Safety Monitor",
                "type": PredictionType.RISK_SCORING, "technique": ModelingTechnique.TREE_BASED,
                "algorithm": "XGBoost with SHAP interpretability",
                "target": "safety_risk_score"
            }
        ]
        
        # Create predictive models
        for model_data in sample_models:
            model_id = f"PRED_MODEL_{random.randint(100000, 999999)}"
            
            model = PredictiveModel(
                model_id=model_id,
                model_name=model_data["name"],
                prediction_type=model_data["type"],
                technique=model_data["technique"],
                algorithm_details=model_data["algorithm"],
                target_variable=model_data["target"],
                training_data_size=random.randint(1000, 10000),
                validation_method="temporal_cross_validation",
                cross_validation_score=random.uniform(0.75, 0.92),
                holdout_test_score=random.uniform(0.70, 0.88),
                temporal_validation_score=random.uniform(0.65, 0.85)
            )
            
            # Set performance metrics based on prediction type
            if model.prediction_type == PredictionType.CLASSIFICATION:
                model.accuracy_metrics = {
                    "accuracy": random.uniform(0.75, 0.90),
                    "precision": random.uniform(0.70, 0.88),
                    "recall": random.uniform(0.72, 0.86),
                    "f1_score": random.uniform(0.73, 0.87),
                    "auc_roc": random.uniform(0.80, 0.93)
                }
            elif model.prediction_type == PredictionType.REGRESSION:
                model.error_metrics = {
                    "rmse": random.uniform(0.1, 0.5),
                    "mae": random.uniform(0.05, 0.3),
                    "mape": random.uniform(5, 15),
                    "r_squared": random.uniform(0.70, 0.85)
                }
            elif model.prediction_type == PredictionType.TIME_SERIES:
                model.error_metrics = {
                    "mase": random.uniform(0.5, 1.2),  # Mean Absolute Scaled Error
                    "smape": random.uniform(8, 20),    # Symmetric MAPE
                    "msis": random.uniform(10, 30)     # Mean Scaled Interval Score
                }
            
            # Calibration metrics
            model.calibration_metrics = {
                "brier_score": random.uniform(0.05, 0.20),
                "calibration_slope": random.uniform(0.85, 1.15),
                "calibration_intercept": random.uniform(-0.1, 0.1)
            }
            
            # Set capabilities
            model.prediction_intervals_available = True
            model.confidence_scores_available = True
            model.feature_importance_available = True
            model.uncertainty_method = random.choice(["bootstrap", "bayesian", "ensemble", "quantile"])
            
            # Set interpretability
            interpretability_scores = {
                ModelingTechnique.LINEAR_MODELS: random.uniform(0.85, 0.95),
                ModelingTechnique.TREE_BASED: random.uniform(0.70, 0.85),
                ModelingTechnique.ENSEMBLE_METHODS: random.uniform(0.60, 0.75),
                ModelingTechnique.NEURAL_NETWORKS: random.uniform(0.30, 0.50),
                ModelingTechnique.TIME_SERIES_MODELS: random.uniform(0.50, 0.70)
            }
            model.interpretability_score = interpretability_scores.get(model.technique, 0.6)
            
            # Model status
            model.model_status = random.choice(["validated", "deployed"])
            if model.model_status == "deployed":
                model.deployment_date = datetime.now() - timedelta(days=random.randint(30, 365))
                model.last_retrained = datetime.now() - timedelta(days=random.randint(7, 60))
            
            self.predictive_models[model_id] = model
        
        logger.info(f"Initialized {len(self.prediction_requests)} requests and {len(self.predictive_models)} predictive models")
    
    def create_prediction_request(self, request_name: str, prediction_type: PredictionType,
                                technique: ModelingTechnique, target_variable: str,
                                input_features: List[str]) -> PredictionRequest:
        """Create new prediction request."""
        
        request_id = f"REQ_{random.randint(100000, 999999)}"
        
        request = PredictionRequest(
            request_id=request_id,
            request_name=request_name,
            prediction_type=prediction_type,
            modeling_technique=technique,
            target_variable=target_variable,
            target_description=f"Prediction request for {target_variable}",
            input_features=input_features.copy()
        )
        
        # Infer feature types (simplified)
        for feature in input_features:
            if any(keyword in feature.lower() for keyword in ["time", "date", "trend"]):
                request.feature_types[feature] = "numerical"
                request.temporal_features.append(feature)
            elif any(keyword in feature.lower() for keyword in ["location", "category", "type"]):
                request.feature_types[feature] = "categorical"
            else:
                request.feature_types[feature] = "numerical"
        
        self.prediction_requests[request_id] = request
        
        logger.info(f"Prediction request created: {request_id}")
        
        return request
    
    def generate_prediction(self, request_id: str, model_id: str, 
                          input_data: Dict[str, Any]) -> PredictionResult:
        """Generate prediction using specified model."""
        
        if request_id not in self.prediction_requests:
            raise ValueError(f"Prediction request {request_id} not found")
        
        if model_id not in self.predictive_models:
            raise ValueError(f"Predictive model {model_id} not found")
        
        request = self.prediction_requests[request_id]
        model = self.predictive_models[model_id]
        
        prediction_id = f"PRED_{random.randint(100000, 999999)}"
        
        result = PredictionResult(
            prediction_id=prediction_id,
            request_id=request_id,
            model_id=model_id,
            prediction_timestamp=datetime.now(),
            prediction_horizon_used=request.prediction_horizon,
            feature_values=input_data.copy()
        )
        
        # Generate prediction based on type
        if request.prediction_type == PredictionType.CLASSIFICATION:
            # Classification prediction
            classes = ["low_risk", "medium_risk", "high_risk"]
            class_probs = [random.uniform(0.1, 0.8) for _ in classes]
            total_prob = sum(class_probs)
            class_probs = [p/total_prob for p in class_probs]
            
            result.class_probabilities = {cls: prob for cls, prob in zip(classes, class_probs)}
            result.predicted_class = max(result.class_probabilities, key=result.class_probabilities.get)
            result.prediction_probability = result.class_probabilities[result.predicted_class]
            
        elif request.prediction_type == PredictionType.REGRESSION:
            # Regression prediction
            result.predicted_value = random.uniform(10, 100)
            result.prediction_std = random.uniform(2, 10)
            
            # Confidence interval
            confidence_margin = 1.96 * result.prediction_std  # 95% CI
            result.confidence_interval = (
                result.predicted_value - confidence_margin,
                result.predicted_value + confidence_margin
            )
            
        elif request.prediction_type == PredictionType.TIME_SERIES:
            # Time series prediction (multiple future points)
            forecast_horizon = 12  # 12 time steps
            base_value = random.uniform(20, 80)
            trend = random.uniform(-0.5, 0.5)
            
            result.predicted_value = [
                base_value + trend * i + random.uniform(-5, 5)
                for i in range(forecast_horizon)
            ]
            
        elif request.prediction_type == PredictionType.RISK_SCORING:
            # Risk score prediction
            result.risk_score = random.uniform(0, 100)
            
            if result.risk_score < 30:
                result.risk_category = "low"
            elif result.risk_score < 70:
                result.risk_category = "medium"
            else:
                result.risk_category = "high"
            
            # Risk factors
            result.risk_factors = [
                "Environmental conditions",
                "Population vulnerability", 
                "Historical patterns",
                "Intervention effectiveness"
            ]
            
        elif request.prediction_type == PredictionType.PROBABILITY_ESTIMATION:
            # Probability estimation
            result.predicted_value = random.uniform(0, 1)
            result.prediction_probability = result.predicted_value
            
        # Uncertainty quantification
        if request.uncertainty_quantification:
            result.uncertainty_breakdown = {
                UncertaintyType.ALEATORY: random.uniform(0.1, 0.4),
                UncertaintyType.EPISTEMIC: random.uniform(0.05, 0.3),
                UncertaintyType.PARAMETER: random.uniform(0.02, 0.2),
                UncertaintyType.MODEL: random.uniform(0.05, 0.25)
            }
        
        # Feature importance
        if request.feature_importance:
            total_importance = 0
            for feature in request.input_features:
                importance = random.uniform(0.05, 0.3)
                result.feature_importance[feature] = importance
                total_importance += importance
            
            # Normalize
            for feature in result.feature_importance:
                result.feature_importance[feature] /= total_importance
        
        # Quality scores
        result.model_confidence = random.uniform(0.7, 0.95)
        result.prediction_reliability = random.uniform(0.65, 0.90)
        result.data_quality_score = random.uniform(0.75, 0.95)
        
        # Prediction basis and assumptions
        result.prediction_basis = f"Based on {len(request.input_features)} features using {model.technique.value}"
        result.assumptions = [
            "Historical patterns continue to hold",
            "Input data quality is maintained",
            "No major structural changes in the system"
        ]
        
        result.limitations = [
            f"Prediction horizon limited to {request.prediction_horizon.value}",
            "Subject to model uncertainty",
            "Requires regular model updates"
        ]
        
        self.prediction_results.append(result)
        
        logger.info(f"Prediction generated: {prediction_id} using model {model_id}")
        
        return result
    
    def run_scenario_analysis(self, scenario_name: str, base_scenario: Dict[str, Any],
                            variations: List[Dict[str, Any]], model_id: str) -> ScenarioAnalysis:
        """Run comprehensive scenario analysis."""
        
        scenario_id = f"SCENARIO_{random.randint(100000, 999999)}"
        
        analysis = ScenarioAnalysis(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            description=f"Scenario analysis comparing {len(variations)} variations",
            base_scenario=base_scenario.copy(),
            scenario_variations=variations.copy(),
            model_id=model_id
        )
        
        # Generate predictions for each scenario
        all_scenarios = [{"name": "baseline", "data": base_scenario}]
        for i, variation in enumerate(variations):
            all_scenarios.append({"name": f"scenario_{i+1}", "data": variation})
        
        # Create dummy request for scenario analysis
        dummy_request_id = f"SCENARIO_REQ_{random.randint(100000, 999999)}"
        dummy_request = PredictionRequest(
            request_id=dummy_request_id,
            request_name=f"Scenario Analysis: {scenario_name}",
            prediction_type=PredictionType.PROBABILITY_ESTIMATION,
            modeling_technique=ModelingTechnique.ENSEMBLE_METHODS,
            target_variable="scenario_outcome",
            target_description="Scenario analysis outcome"
        )
        self.prediction_requests[dummy_request_id] = dummy_request
        
        # Generate predictions for each scenario
        for scenario in all_scenarios:
            prediction = self.generate_prediction(dummy_request_id, model_id, scenario["data"])
            analysis.scenario_predictions[scenario["name"]] = prediction
            
            # Calculate scenario risk
            if hasattr(prediction, 'risk_score') and prediction.risk_score:
                analysis.scenario_risks[scenario["name"]] = prediction.risk_score
            elif prediction.predicted_value is not None:
                if isinstance(prediction.predicted_value, (int, float)):
                    analysis.scenario_risks[scenario["name"]] = float(prediction.predicted_value) * 100
                else:
                    analysis.scenario_risks[scenario["name"]] = random.uniform(20, 80)
            else:
                analysis.scenario_risks[scenario["name"]] = random.uniform(20, 80)
        
        # Risk ranking
        analysis.risk_ranking = sorted(analysis.scenario_risks.items(), 
                                     key=lambda x: x[1], reverse=True)
        
        # Comparison matrix
        scenario_names = list(analysis.scenario_risks.keys())
        for i, scenario1 in enumerate(scenario_names):
            for scenario2 in scenario_names[i+1:]:
                risk_diff = abs(analysis.scenario_risks[scenario1] - analysis.scenario_risks[scenario2])
                analysis.comparison_matrix[(scenario1, scenario2)] = risk_diff
        
        # Decision support
        analysis.recommended_scenario = min(analysis.scenario_risks, key=analysis.scenario_risks.get)
        
        analysis.decision_criteria = [
            "Minimize overall risk",
            "Maximize intervention effectiveness", 
            "Consider resource constraints",
            "Account for implementation feasibility"
        ]
        
        analysis.trade_off_analysis = {
            "risk_vs_cost": "Lower risk scenarios may require higher investment",
            "short_vs_long_term": "Short-term gains may compromise long-term sustainability",
            "certainty_vs_impact": "High-certainty scenarios may have lower potential impact"
        }
        
        analysis.confidence_in_analysis = random.uniform(0.7, 0.9)
        
        self.scenario_analyses.append(analysis)
        
        logger.info(f"Scenario analysis completed: {scenario_id} - {len(variations)} scenarios analyzed")
        
        return analysis
    
    def evaluate_prediction_performance(self, actual_values: List[float], 
                                      predictions: List[PredictionResult],
                                      prediction_type: PredictionType) -> Dict[str, float]:
        """Evaluate prediction performance against actual values."""
        
        if len(actual_values) != len(predictions):
            raise ValueError("Number of actual values must match number of predictions")
        
        performance_metrics = {}
        
        if prediction_type == PredictionType.REGRESSION:
            # Extract predicted values
            predicted_values = []
            for pred in predictions:
                if isinstance(pred.predicted_value, (int, float)):
                    predicted_values.append(pred.predicted_value)
                else:
                    predicted_values.append(0)  # Default for non-numeric
            
            # Calculate regression metrics
            errors = [actual - pred for actual, pred in zip(actual_values, predicted_values)]
            squared_errors = [e**2 for e in errors]
            absolute_errors = [abs(e) for e in errors]
            
            performance_metrics["mse"] = statistics.mean(squared_errors)
            performance_metrics["rmse"] = math.sqrt(performance_metrics["mse"])
            performance_metrics["mae"] = statistics.mean(absolute_errors)
            
            # R-squared
            actual_mean = statistics.mean(actual_values)
            ss_tot = sum((actual - actual_mean)**2 for actual in actual_values)
            ss_res = sum(squared_errors)
            performance_metrics["r_squared"] = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
        elif prediction_type == PredictionType.CLASSIFICATION:
            # For classification, convert actual values to classes
            actual_classes = ["low" if v < 0.33 else "medium" if v < 0.67 else "high" for v in actual_values]
            predicted_classes = [pred.predicted_class for pred in predictions]
            
            # Calculate accuracy
            correct = sum(1 for actual, pred in zip(actual_classes, predicted_classes) if actual == pred)
            performance_metrics["accuracy"] = correct / len(actual_classes)
            
        # Coverage metrics for prediction intervals
        if all(pred.confidence_interval for pred in predictions):
            coverage_count = 0
            for actual, pred in zip(actual_values, predictions):
                if pred.confidence_interval:
                    lower, upper = pred.confidence_interval
                    if lower <= actual <= upper:
                        coverage_count += 1
            
            performance_metrics["coverage_probability"] = coverage_count / len(actual_values)
        
        # Calibration metrics
        confidence_scores = [pred.model_confidence for pred in predictions]
        if confidence_scores:
            performance_metrics["average_confidence"] = statistics.mean(confidence_scores)
        
        return performance_metrics
    
    def get_modeling_summary(self) -> Dict[str, Any]:
        """Get comprehensive predictive modeling summary."""
        
        # Request analysis
        requests_by_type = Counter(req.prediction_type for req in self.prediction_requests.values())
        requests_by_technique = Counter(req.modeling_technique for req in self.prediction_requests.values())
        requests_by_horizon = Counter(req.prediction_horizon for req in self.prediction_requests.values())
        
        # Model analysis
        models_by_technique = Counter(model.technique for model in self.predictive_models.values())
        models_by_status = Counter(model.model_status for model in self.predictive_models.values())
        
        # Performance analysis
        if self.predictive_models:
            cv_scores = [model.cross_validation_score for model in self.predictive_models.values() if model.cross_validation_score > 0]
            avg_cv_score = statistics.mean(cv_scores) if cv_scores else 0
            
            interpretability_scores = [model.interpretability_score for model in self.predictive_models.values()]
            avg_interpretability = statistics.mean(interpretability_scores) if interpretability_scores else 0
        else:
            avg_cv_score = avg_interpretability = 0
        
        # Results analysis
        if self.prediction_results:
            confidence_scores = [result.model_confidence for result in self.prediction_results]
            reliability_scores = [result.prediction_reliability for result in self.prediction_results]
            avg_confidence = statistics.mean(confidence_scores)
            avg_reliability = statistics.mean(reliability_scores)
        else:
            avg_confidence = avg_reliability = 0
        
        return {
            "prediction_requests": {
                "total_requests": len(self.prediction_requests),
                "by_type": {t.value: count for t, count in requests_by_type.items()},
                "by_technique": {t.value: count for t, count in requests_by_technique.items()},
                "by_horizon": {h.value: count for h, count in requests_by_horizon.items()}
            },
            "predictive_models": {
                "total_models": len(self.predictive_models),
                "by_technique": {t.value: count for t, count in models_by_technique.items()},
                "by_status": dict(models_by_status),
                "average_cv_score": avg_cv_score,
                "average_interpretability": avg_interpretability
            },
            "prediction_results": {
                "total_predictions": len(self.prediction_results),
                "average_confidence": avg_confidence,
                "average_reliability": avg_reliability
            },
            "scenario_analyses": {
                "total_analyses": len(self.scenario_analyses),
                "average_scenarios_per_analysis": statistics.mean([len(sa.scenario_variations) + 1 for sa in self.scenario_analyses]) if self.scenario_analyses else 0
            }
        }

def run_demonstration() -> PredictiveModelingEngine:
    """Run comprehensive predictive modeling demonstration."""
    
    print("🔮 One Health Predictive Modeling - Demonstration")
    print("=" * 70)
    
    engine = PredictiveModelingEngine()
    
    print(f"\n🔮 Predictive Modeling Framework:")
    print(f"  Prediction Types: {len(PredictionType)}")
    print(f"  Modeling Techniques: {len(ModelingTechnique)}")
    print(f"  Prediction Horizons: {len(PredictionHorizon)}")
    print(f"  Prediction Requests: {len(engine.prediction_requests)}")
    print(f"  Predictive Models: {len(engine.predictive_models)}")
    
    # Display requests by type
    requests_by_type = defaultdict(list)
    for request in engine.prediction_requests.values():
        requests_by_type[request.prediction_type].append(request.request_name)
    
    print(f"\n📊 Prediction Requests by Type:")
    for pred_type, requests in requests_by_type.items():
        print(f"  {pred_type.value.replace('_', ' ').title()}: {len(requests)}")
        for request in requests[:1]:  # Show first request
            print(f"    • {request}")
    
    print(f"\n🔮 Generating Predictions...")
    
    # Generate predictions for sample requests
    sample_predictions = []
    for i, (request_id, request) in enumerate(list(engine.prediction_requests.items())[:3]):
        # Use appropriate model
        suitable_models = [m for m in engine.predictive_models.values() 
                          if m.prediction_type == request.prediction_type]
        if suitable_models:
            model = suitable_models[0]
            
            # Create sample input data
            sample_input = {}
            for feature in request.input_features:
                if request.feature_types.get(feature) == "categorical":
                    sample_input[feature] = random.choice(["low", "medium", "high"])
                else:
                    sample_input[feature] = random.uniform(0, 100)
            
            prediction = engine.generate_prediction(request_id, model.model_id, sample_input)
            sample_predictions.append(prediction)
            
            confidence = prediction.model_confidence
            print(f"  🔮 {request.request_name}: {confidence:.1%} confidence")
            
            if prediction.predicted_class:
                print(f"    Predicted Class: {prediction.predicted_class}")
            if prediction.predicted_value is not None:
                if isinstance(prediction.predicted_value, list):
                    print(f"    Time Series: {len(prediction.predicted_value)} forecasts")
                else:
                    print(f"    Predicted Value: {prediction.predicted_value:.2f}")
            if prediction.risk_score is not None:
                print(f"    Risk Score: {prediction.risk_score:.1f}")
    
    print(f"\n📋 Running Scenario Analysis...")
    
    # Run scenario analysis
    base_scenario = {
        "environmental_factor": 50,
        "population_density": 1000,
        "intervention_level": 0.3
    }
    
    scenario_variations = [
        {"environmental_factor": 30, "population_density": 1000, "intervention_level": 0.5},
        {"environmental_factor": 70, "population_density": 1500, "intervention_level": 0.3},
        {"environmental_factor": 60, "population_density": 800, "intervention_level": 0.7}
    ]
    
    suitable_model = list(engine.predictive_models.values())[0]
    scenario_analysis = engine.run_scenario_analysis(
        "One Health Intervention Strategy Analysis",
        base_scenario,
        scenario_variations,
        suitable_model.model_id
    )
    
    print(f"  📋 Scenario Analysis: {len(scenario_variations) + 1} scenarios")
    print(f"  🎯 Recommended Scenario: {scenario_analysis.recommended_scenario}")
    print(f"  📊 Confidence: {scenario_analysis.confidence_in_analysis:.1%}")
    
    # Display risk ranking
    print(f"  Risk Ranking:")
    for i, (scenario, risk) in enumerate(scenario_analysis.risk_ranking[:3], 1):
        print(f"    {i}. {scenario}: {risk:.1f} risk score")
    
    return engine

def display_modeling_results(engine: PredictiveModelingEngine):
    """Display comprehensive modeling results."""
    
    print(f"\n🔮 Predictive Modeling Results:")
    
    # System summary
    summary = engine.get_modeling_summary()
    
    print(f"\n📊 Modeling System Summary:")
    
    requests = summary["prediction_requests"]
    print(f"  Prediction Requests: {requests['total_requests']}")
    
    print(f"  Requests by Type:")
    for pred_type, count in requests["by_type"].items():
        print(f"    {pred_type.replace('_', ' ').title()}: {count}")
    
    print(f"  Requests by Technique:")
    for technique, count in requests["by_technique"].items():
        print(f"    {technique.replace('_', ' ').title()}: {count}")
    
    models = summary["predictive_models"]
    print(f"\n  Predictive Models:")
    print(f"    Total Models: {models['total_models']}")
    print(f"    Avg CV Score: {models['average_cv_score']:.1%}")
    print(f"    Avg Interpretability: {models['average_interpretability']:.1%}")
    
    results = summary["prediction_results"]
    print(f"\n  Prediction Results:")
    print(f"    Total Predictions: {results['total_predictions']}")
    print(f"    Avg Confidence: {results['average_confidence']:.1%}")
    print(f"    Avg Reliability: {results['average_reliability']:.1%}")
    
    scenarios = summary["scenario_analyses"]
    print(f"\n  Scenario Analyses:")
    print(f"    Total Analyses: {scenarios['total_analyses']}")
    if scenarios['total_analyses'] > 0:
        print(f"    Avg Scenarios: {scenarios['average_scenarios_per_analysis']:.1f}")
    
    # Model performance details
    print(f"\n🎯 Model Performance by Technique:")
    for technique, count in models["by_technique"].items():
        print(f"  {technique.replace('_', ' ').title()}: {count} models")
    
    print(f"\n📈 Model Status Distribution:")
    for status, count in models["by_status"].items():
        print(f"  {status.replace('_', ' ').title()}: {count} models")
    
    # Recent predictions
    if engine.prediction_results:
        print(f"\n🔮 Recent Predictions:")
        for i, result in enumerate(engine.prediction_results[-3:], 1):
            print(f"  {i}. Prediction {result.prediction_id}:")
            print(f"     Confidence: {result.model_confidence:.1%}")
            print(f"     Reliability: {result.prediction_reliability:.1%}")
            if result.predicted_class:
                print(f"     Class: {result.predicted_class}")
            if result.risk_score is not None:
                print(f"     Risk Score: {result.risk_score:.1f}")
    
    # Latest scenario analysis
    if engine.scenario_analyses:
        latest_scenario = engine.scenario_analyses[-1]
        print(f"\n📋 Latest Scenario Analysis:")
        print(f"  Analysis: {latest_scenario.scenario_name}")
        print(f"  Scenarios: {len(latest_scenario.scenario_variations) + 1}")
        print(f"  Recommended: {latest_scenario.recommended_scenario}")
        print(f"  Confidence: {latest_scenario.confidence_in_analysis:.1%}")
        
        print(f"  Risk Ranking:")
        for i, (scenario, risk) in enumerate(latest_scenario.risk_ranking[:3], 1):
            print(f"    {i}. {scenario}: {risk:.1f}")
    
    # Top performing models
    deployed_models = [m for m in engine.predictive_models.values() if m.model_status == "deployed"]
    if deployed_models:
        print(f"\n🏆 TOP PERFORMING Models:")
        
        # Sort by cross-validation score
        top_models = sorted(deployed_models, key=lambda m: m.cross_validation_score, reverse=True)[:3]
        
        for i, model in enumerate(top_models, 1):
            print(f"  {i}. {model.model_name}")
            print(f"     Technique: {model.technique.value.replace('_', ' ').title()}")
            print(f"     CV Score: {model.cross_validation_score:.1%}")
            print(f"     Interpretability: {model.interpretability_score:.1%}")
            print(f"     Target: {model.target_variable}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    modeling_engine = run_demonstration()
    display_modeling_results(modeling_engine)
"""
Predictive Modeling System
==========================
Module 2: Essential Epidemiologic Tools

Advanced predictive modeling system for One Health surveillance, providing
future disease trend forecasting, outbreak prediction, and risk projection models.

NIW Focus: Predictive intelligence enabling proactive public health interventions.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import itertools
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PredictionModel(Enum):
    """Types of prediction models."""
    LINEAR_TREND = "linear_trend"               # Simple linear extrapolation
    EXPONENTIAL = "exponential"                # Exponential growth/decay
    SEASONAL_ARIMA = "seasonal_arima"          # Seasonal autoregressive model
    SIR_EPIDEMIC = "sir_epidemic"              # SIR epidemic model
    MACHINE_LEARNING = "machine_learning"      # ML-based prediction
    ENSEMBLE = "ensemble"                      # Combined model predictions

class PredictionType(Enum):
    """Types of predictions."""
    CASE_COUNT = "case_count"                  # Disease case numbers
    OUTBREAK_RISK = "outbreak_risk"           # Outbreak probability
    TREND_DIRECTION = "trend_direction"       # Increasing/decreasing trend
    PEAK_TIMING = "peak_timing"               # When outbreak will peak
    RESOURCE_DEMAND = "resource_demand"       # Healthcare resource needs

class ConfidenceLevel(Enum):
    """Confidence levels for predictions."""
    LOW = "low"                               # Limited historical data
    MEDIUM = "medium"                         # Adequate data quality
    HIGH = "high"                            # Strong data foundation
    VERY_HIGH = "very_high"                  # Extensive validation

@dataclass
class PredictionResult:
    """Result of predictive modeling analysis."""
    
    prediction_id: str
    model_type: PredictionModel
    prediction_type: PredictionType
    analysis_timestamp: datetime
    
    # Prediction details
    target_variable: str
    target_domain: str                        # "animal", "human", "environmental"
    prediction_horizon_days: int
    
    # Predicted values
    predicted_values: List[Tuple[datetime, float]]  # (date, predicted_value)
    confidence_intervals: List[Tuple[datetime, float, float]]  # (date, lower_ci, upper_ci)
    prediction_probabilities: Optional[List[Tuple[datetime, float]]] = None  # For risk predictions
    
    # Model performance
    model_accuracy: Optional[float] = None     # Validation accuracy (0-1)
    mean_absolute_error: Optional[float] = None
    root_mean_square_error: Optional[float] = None
    r_squared: Optional[float] = None
    
    # Model characteristics
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    model_parameters: Optional[Dict] = None
    feature_importance: Optional[Dict[str, float]] = None
    
    # Validation details
    training_data_points: int = 0
    validation_method: Optional[str] = None    # "holdout", "cross_validation", "time_series_split"
    overfitting_risk: Optional[str] = None     # "low", "medium", "high"
    
    # Temporal context
    data_period_start: Optional[datetime] = None
    data_period_end: Optional[datetime] = None
    seasonal_pattern_detected: bool = False
    trend_strength: Optional[float] = None
    
    # Interpretation and recommendations
    key_insights: List[str] = None
    prediction_scenarios: Optional[Dict[str, List[float]]] = None  # "best", "worst", "most_likely"
    recommended_actions: List[str] = None
    monitoring_indicators: List[str] = None
    
    # Risk assessment
    outbreak_probability: Optional[float] = None
    peak_date_estimate: Optional[datetime] = None
    peak_intensity_estimate: Optional[float] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.key_insights is None:
            self.key_insights = []
        if self.recommended_actions is None:
            self.recommended_actions = []
        if self.monitoring_indicators is None:
            self.monitoring_indicators = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['model_type'] = self.model_type.value
        data['prediction_type'] = self.prediction_type.value
        data['confidence_level'] = self.confidence_level.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        
        # Convert datetime lists to ISO strings
        data['predicted_values'] = [(dt.isoformat(), val) for dt, val in self.predicted_values]
        data['confidence_intervals'] = [(dt.isoformat(), lower, upper) 
                                       for dt, lower, upper in self.confidence_intervals]
        
        if self.prediction_probabilities:
            data['prediction_probabilities'] = [(dt.isoformat(), prob) 
                                               for dt, prob in self.prediction_probabilities]
        
        if self.data_period_start:
            data['data_period_start'] = self.data_period_start.isoformat()
        if self.data_period_end:
            data['data_period_end'] = self.data_period_end.isoformat()
        if self.peak_date_estimate:
            data['peak_date_estimate'] = self.peak_date_estimate.isoformat()
            
        return data

class TrendPredictor:
    """Predicts future trends using various statistical methods."""
    
    @staticmethod
    def linear_trend_prediction(time_series: List[Tuple[datetime, float]],
                              prediction_days: int = 14,
                              variable_name: str = "cases",
                              domain: str = "unknown") -> PredictionResult:
        """Predict future values using linear trend extrapolation."""
        
        if len(time_series) < 3:
            raise ValueError("Need at least 3 data points for trend prediction")
        
        # Convert to numeric format for regression
        time_series.sort(key=lambda x: x[0])
        start_date = time_series[0][0]
        
        x_values = [(dt - start_date).days for dt, _ in time_series]
        y_values = [val for _, val in time_series]
        
        # Calculate linear regression parameters
        slope, intercept = TrendPredictor._calculate_linear_regression(x_values, y_values)
        
        # Calculate R-squared
        y_mean = statistics.mean(y_values)
        ss_tot = sum((y - y_mean) ** 2 for y in y_values)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_values, y_values))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Calculate prediction error estimates
        residuals = [(y - (slope * x + intercept)) for x, y in zip(x_values, y_values)]
        rmse = math.sqrt(statistics.mean([r**2 for r in residuals])) if residuals else 1.0
        mae = statistics.mean([abs(r) for r in residuals]) if residuals else 1.0
        
        # Generate future predictions
        predicted_values = []
        confidence_intervals = []
        
        last_date = time_series[-1][0]
        
        for i in range(1, prediction_days + 1):
            future_date = last_date + timedelta(days=i)
            future_x = (future_date - start_date).days
            
            predicted_value = slope * future_x + intercept
            
            # Simple confidence interval (±2 standard errors)
            prediction_error = rmse * math.sqrt(1 + 1/len(time_series) + 
                                              (future_x - statistics.mean(x_values))**2 / 
                                              sum((x - statistics.mean(x_values))**2 for x in x_values))
            
            lower_ci = predicted_value - 2 * prediction_error
            upper_ci = predicted_value + 2 * prediction_error
            
            predicted_values.append((future_date, max(0, predicted_value)))
            confidence_intervals.append((future_date, max(0, lower_ci), max(0, upper_ci)))
        
        # Determine confidence level based on R-squared
        if r_squared > 0.8:
            confidence_level = ConfidenceLevel.HIGH
        elif r_squared > 0.6:
            confidence_level = ConfidenceLevel.MEDIUM
        else:
            confidence_level = ConfidenceLevel.LOW
        
        # Generate insights
        insights = []
        if slope > 0.1:
            insights.append(f"Strong increasing trend detected ({slope:.2f} units/day)")
        elif slope < -0.1:
            insights.append(f"Strong decreasing trend detected ({slope:.2f} units/day)")
        else:
            insights.append("Stable trend with minimal change")
        
        insights.append(f"Model explains {r_squared*100:.1f}% of variance")
        
        result = PredictionResult(
            prediction_id=f"LINEAR_TREND_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=PredictionModel.LINEAR_TREND,
            prediction_type=PredictionType.CASE_COUNT,
            analysis_timestamp=datetime.now(),
            target_variable=variable_name,
            target_domain=domain,
            prediction_horizon_days=prediction_days,
            predicted_values=predicted_values,
            confidence_intervals=confidence_intervals,
            model_accuracy=r_squared,
            root_mean_square_error=rmse,
            mean_absolute_error=mae,
            r_squared=r_squared,
            confidence_level=confidence_level,
            model_parameters={"slope": slope, "intercept": intercept},
            training_data_points=len(time_series),
            data_period_start=time_series[0][0],
            data_period_end=time_series[-1][0],
            trend_strength=abs(slope),
            key_insights=insights
        )
        
        return result
    
    @staticmethod
    def exponential_growth_prediction(time_series: List[Tuple[datetime, float]],
                                    prediction_days: int = 14,
                                    variable_name: str = "cases",
                                    domain: str = "unknown") -> PredictionResult:
        """Predict future values using exponential growth model."""
        
        if len(time_series) < 4:
            raise ValueError("Need at least 4 data points for exponential prediction")
        
        # Filter out zero/negative values for log transformation
        positive_series = [(dt, val) for dt, val in time_series if val > 0]
        
        if len(positive_series) < 3:
            # Fallback to linear prediction if insufficient positive data
            return TrendPredictor.linear_trend_prediction(
                time_series, prediction_days, variable_name, domain
            )
        
        positive_series.sort(key=lambda x: x[0])
        start_date = positive_series[0][0]
        
        # Log-transform for exponential regression
        x_values = [(dt - start_date).days for dt, _ in positive_series]
        y_log_values = [math.log(val) for _, val in positive_series]
        
        # Linear regression on log-transformed data
        slope, intercept = TrendPredictor._calculate_linear_regression(x_values, y_log_values)
        
        # Calculate model performance
        y_log_mean = statistics.mean(y_log_values)
        ss_tot = sum((y - y_log_mean) ** 2 for y in y_log_values)
        ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(x_values, y_log_values))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Calculate error metrics on original scale
        predicted_log = [slope * x + intercept for x in x_values]
        predicted_original = [math.exp(log_val) for log_val in predicted_log]
        original_values = [val for _, val in positive_series]
        
        residuals = [orig - pred for orig, pred in zip(original_values, predicted_original)]
        rmse = math.sqrt(statistics.mean([r**2 for r in residuals])) if residuals else 1.0
        mae = statistics.mean([abs(r) for r in residuals]) if residuals else 1.0
        
        # Generate future predictions
        predicted_values = []
        confidence_intervals = []
        
        last_date = positive_series[-1][0]
        
        for i in range(1, prediction_days + 1):
            future_date = last_date + timedelta(days=i)
            future_x = (future_date - start_date).days
            
            # Predict on log scale then transform back
            log_prediction = slope * future_x + intercept
            predicted_value = math.exp(log_prediction)
            
            # Confidence interval (simplified)
            log_error = rmse / statistics.mean(original_values) if original_values else 0.1
            lower_ci = math.exp(log_prediction - 2 * log_error)
            upper_ci = math.exp(log_prediction + 2 * log_error)
            
            predicted_values.append((future_date, predicted_value))
            confidence_intervals.append((future_date, lower_ci, upper_ci))
        
        # Calculate growth rate
        daily_growth_rate = math.exp(slope) - 1
        doubling_time = math.log(2) / slope if slope > 0 else float('inf')
        
        # Generate insights
        insights = []
        if daily_growth_rate > 0.05:  # 5% daily growth
            insights.append(f"Exponential growth detected ({daily_growth_rate*100:.1f}% daily)")
            if doubling_time < 30:
                insights.append(f"Doubling time: {doubling_time:.1f} days")
        elif daily_growth_rate < -0.05:
            insights.append(f"Exponential decay detected ({daily_growth_rate*100:.1f}% daily)")
        else:
            insights.append("Minimal exponential trend")
        
        insights.append(f"Exponential model R²: {r_squared:.3f}")
        
        result = PredictionResult(
            prediction_id=f"EXPONENTIAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=PredictionModel.EXPONENTIAL,
            prediction_type=PredictionType.CASE_COUNT,
            analysis_timestamp=datetime.now(),
            target_variable=variable_name,
            target_domain=domain,
            prediction_horizon_days=prediction_days,
            predicted_values=predicted_values,
            confidence_intervals=confidence_intervals,
            model_accuracy=r_squared,
            root_mean_square_error=rmse,
            mean_absolute_error=mae,
            r_squared=r_squared,
            confidence_level=ConfidenceLevel.HIGH if r_squared > 0.7 else ConfidenceLevel.MEDIUM,
            model_parameters={"growth_rate": daily_growth_rate, "doubling_time": doubling_time},
            training_data_points=len(positive_series),
            data_period_start=positive_series[0][0],
            data_period_end=positive_series[-1][0],
            trend_strength=abs(daily_growth_rate),
            key_insights=insights
        )
        
        return result
    
    @staticmethod
    def _calculate_linear_regression(x_values: List[float], 
                                   y_values: List[float]) -> Tuple[float, float]:
        """Calculate linear regression slope and intercept."""
        
        if len(x_values) != len(y_values) or len(x_values) == 0:
            return 0.0, 0.0
        
        n = len(x_values)
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = y_mean - slope * x_mean
        
        return slope, intercept

class EpidemicModelPredictor:
    """Predicts epidemic dynamics using epidemiological models."""
    
    @staticmethod
    def sir_model_prediction(case_data: List[Tuple[datetime, int]],
                           population_size: int = 100000,
                           prediction_days: int = 30,
                           variable_name: str = "cases",
                           domain: str = "human") -> PredictionResult:
        """Predict epidemic progression using SIR model."""
        
        if len(case_data) < 5:
            raise ValueError("Need at least 5 data points for SIR model")
        
        case_data.sort(key=lambda x: x[0])
        
        # Extract daily case counts
        daily_cases = [count for _, count in case_data]
        cumulative_cases = []
        total = 0
        for cases in daily_cases:
            total += cases
            cumulative_cases.append(total)
        
        # Estimate SIR parameters (simplified approach)
        max_cases = max(cumulative_cases)
        current_cases = cumulative_cases[-1]
        
        # Estimate basic reproduction number (R0)
        if len(cumulative_cases) >= 5:
            early_growth = cumulative_cases[4] / max(cumulative_cases[1], 1)
            r0_estimate = max(1.1, min(5.0, early_growth))  # Constrain R0
        else:
            r0_estimate = 2.0  # Default assumption
        
        # Estimate recovery rate (gamma) - assume 14-day infectious period
        gamma = 1/14
        
        # Estimate transmission rate (beta)
        beta = r0_estimate * gamma / population_size
        
        # Current state estimates
        infected_current = max(1, sum(daily_cases[-7:]))  # Last week's cases as active
        recovered_current = max(0, current_cases - infected_current)
        susceptible_current = population_size - infected_current - recovered_current
        
        # SIR simulation
        predicted_values = []
        confidence_intervals = []
        
        S, I, R = susceptible_current, infected_current, recovered_current
        last_date = case_data[-1][0]
        
        daily_predictions = []
        
        for day in range(1, prediction_days + 1):
            future_date = last_date + timedelta(days=day)
            
            # SIR differential equations (Euler method)
            dS = -beta * S * I
            dI = beta * S * I - gamma * I
            dR = gamma * I
            
            S += dS
            I += dI  
            R += dR
            
            # Ensure non-negative values
            S = max(0, S)
            I = max(0, I)
            R = max(0, R)
            
            # Daily new cases (incidence)
            new_cases = max(0, beta * S * I)
            daily_predictions.append(new_cases)
            
            # Simple confidence interval based on model uncertainty
            uncertainty = new_cases * 0.3  # 30% uncertainty
            lower_ci = max(0, new_cases - uncertainty)
            upper_ci = new_cases + uncertainty
            
            predicted_values.append((future_date, new_cases))
            confidence_intervals.append((future_date, lower_ci, upper_ci))
        
        # Find peak timing
        max_pred_value = max(daily_predictions)
        peak_day = daily_predictions.index(max_pred_value) + 1
        peak_date = last_date + timedelta(days=peak_day)
        
        # Calculate model performance (simplified)
        model_accuracy = min(0.8, max(0.3, 1 - abs(r0_estimate - 2.0) / 3.0))
        
        # Generate insights
        insights = []
        insights.append(f"Estimated R0: {r0_estimate:.2f}")
        insights.append(f"Predicted peak in {peak_day} days")
        insights.append(f"Peak daily cases: {max_pred_value:.0f}")
        
        if r0_estimate > 1.5:
            insights.append("High transmission rate - aggressive intervention needed")
        elif r0_estimate > 1.1:
            insights.append("Moderate transmission rate - sustained control measures needed")
        else:
            insights.append("Low transmission rate - epidemic likely contained")
        
        # Calculate attack rate
        final_recovered = R + sum(daily_predictions)
        attack_rate = final_recovered / population_size
        insights.append(f"Estimated attack rate: {attack_rate*100:.1f}%")
        
        result = PredictionResult(
            prediction_id=f"SIR_MODEL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=PredictionModel.SIR_EPIDEMIC,
            prediction_type=PredictionType.CASE_COUNT,
            analysis_timestamp=datetime.now(),
            target_variable=variable_name,
            target_domain=domain,
            prediction_horizon_days=prediction_days,
            predicted_values=predicted_values,
            confidence_intervals=confidence_intervals,
            model_accuracy=model_accuracy,
            confidence_level=ConfidenceLevel.MEDIUM,
            model_parameters={
                "R0": r0_estimate,
                "beta": beta,
                "gamma": gamma,
                "population_size": population_size
            },
            training_data_points=len(case_data),
            data_period_start=case_data[0][0],
            data_period_end=case_data[-1][0],
            peak_date_estimate=peak_date,
            peak_intensity_estimate=max_pred_value,
            key_insights=insights
        )
        
        return result

class OutbreakRiskPredictor:
    """Predicts outbreak probability and risk levels."""
    
    @staticmethod
    def risk_probability_prediction(risk_indicators: List[Dict],
                                  prediction_days: int = 7,
                                  domain: str = "integrated") -> PredictionResult:
        """Predict outbreak risk probabilities."""
        
        if len(risk_indicators) < 3:
            raise ValueError("Need at least 3 risk indicator records")
        
        # Extract risk scores and trends
        risk_scores = []
        timestamps = []
        
        for indicator in risk_indicators:
            timestamp = indicator.get('timestamp')
            risk_score = indicator.get('risk_score', indicator.get('overall_risk_score', 50))
            
            if timestamp and isinstance(risk_score, (int, float)):
                try:
                    dt = datetime.fromisoformat(timestamp[:19])
                    timestamps.append(dt)
                    risk_scores.append(float(risk_score))
                except ValueError:
                    continue
        
        if len(risk_scores) < 3:
            raise ValueError("Insufficient valid risk data")
        
        # Sort by timestamp
        combined = list(zip(timestamps, risk_scores))
        combined.sort(key=lambda x: x[0])
        timestamps, risk_scores = zip(*combined)
        
        # Calculate risk trend
        recent_scores = risk_scores[-3:]
        risk_trend = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
        
        # Current risk level
        current_risk = risk_scores[-1]
        
        # Generate probability predictions
        predicted_probabilities = []
        predicted_values = []
        confidence_intervals = []
        
        last_date = timestamps[-1]
        
        for day in range(1, prediction_days + 1):
            future_date = last_date + timedelta(days=day)
            
            # Project risk score based on trend
            projected_risk = current_risk + (risk_trend * day)
            projected_risk = max(0, min(100, projected_risk))  # Constrain to 0-100
            
            # Convert risk score to outbreak probability
            # Using logistic function: P = 1 / (1 + e^(-(risk-50)/10))
            outbreak_probability = 1 / (1 + math.exp(-(projected_risk - 50) / 10))
            
            # Add some uncertainty
            uncertainty = 0.1 + (day * 0.02)  # Increasing uncertainty over time
            lower_prob = max(0, outbreak_probability - uncertainty)
            upper_prob = min(1, outbreak_probability + uncertainty)
            
            predicted_probabilities.append((future_date, outbreak_probability))
            predicted_values.append((future_date, projected_risk))
            confidence_intervals.append((future_date, 
                                       projected_risk - (uncertainty * 50),
                                       projected_risk + (uncertainty * 50)))
        
        # Determine overall outbreak probability
        max_probability = max(prob for _, prob in predicted_probabilities)
        
        # Generate insights
        insights = []
        if max_probability > 0.7:
            insights.append("HIGH outbreak probability detected")
            insights.append("Immediate intervention recommended")
        elif max_probability > 0.4:
            insights.append("MODERATE outbreak probability")
            insights.append("Enhanced surveillance recommended")
        else:
            insights.append("LOW outbreak probability")
            insights.append("Continue routine monitoring")
        
        insights.append(f"Risk trend: {risk_trend:+.1f} points/day")
        insights.append(f"Peak probability: {max_probability*100:.1f}%")
        
        # Risk scenarios
        scenarios = {
            "best_case": [max(0, val * 0.7) for _, val in predicted_values],
            "most_likely": [val for _, val in predicted_values], 
            "worst_case": [min(100, val * 1.3) for _, val in predicted_values]
        }
        
        result = PredictionResult(
            prediction_id=f"RISK_PROB_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=PredictionModel.MACHINE_LEARNING,
            prediction_type=PredictionType.OUTBREAK_RISK,
            analysis_timestamp=datetime.now(),
            target_variable="outbreak_risk",
            target_domain=domain,
            prediction_horizon_days=prediction_days,
            predicted_values=predicted_values,
            confidence_intervals=confidence_intervals,
            prediction_probabilities=predicted_probabilities,
            confidence_level=ConfidenceLevel.MEDIUM,
            model_parameters={"risk_trend": risk_trend, "current_risk": current_risk},
            training_data_points=len(risk_indicators),
            data_period_start=timestamps[0],
            data_period_end=timestamps[-1],
            outbreak_probability=max_probability,
            key_insights=insights,
            prediction_scenarios=scenarios
        )
        
        return result

class OneHealthPredictiveEngine:
    """Main predictive engine for One Health surveillance."""
    
    def __init__(self):
        self.prediction_results: List[PredictionResult] = []
        self.model_performance_log: List[Dict] = []
        
        logger.info("One Health Predictive Engine initialized")
    
    def comprehensive_prediction_analysis(self, animal_data: List[Dict],
                                        human_data: List[Dict],
                                        environmental_data: List[Dict],
                                        risk_assessments: List[Dict] = None) -> List[PredictionResult]:
        """Perform comprehensive predictive analysis across all domains."""
        
        analysis_start = datetime.now()
        predictions = []
        
        logger.info(f"Starting comprehensive prediction analysis")
        
        # Extract time series for prediction
        domain_time_series = {
            "animal": self._extract_time_series(animal_data, "mortality_count"),
            "human": self._extract_time_series(human_data, "case_count"),
            "environmental": self._extract_time_series(environmental_data, "value")
        }
        
        # Predict each domain using multiple methods
        for domain, time_series in domain_time_series.items():
            if len(time_series) >= 3:
                
                variable_name = {
                    "animal": "mortality_count",
                    "human": "case_count", 
                    "environmental": "environmental_value"
                }[domain]
                
                try:
                    # Linear trend prediction
                    linear_pred = TrendPredictor.linear_trend_prediction(
                        time_series, prediction_days=14, variable_name=variable_name, domain=domain
                    )
                    predictions.append(linear_pred)
                    
                    # Exponential growth prediction (for case counts)
                    if domain in ["animal", "human"] and len(time_series) >= 4:
                        exp_pred = TrendPredictor.exponential_growth_prediction(
                            time_series, prediction_days=14, variable_name=variable_name, domain=domain
                        )
                        predictions.append(exp_pred)
                    
                    # SIR epidemic model (for human cases)
                    if domain == "human" and len(time_series) >= 5:
                        # Convert to integer case counts for SIR model
                        case_series = [(dt, int(val)) for dt, val in time_series if val > 0]
                        if len(case_series) >= 5:
                            sir_pred = EpidemicModelPredictor.sir_model_prediction(
                                case_series, population_size=100000, prediction_days=21,
                                variable_name=variable_name, domain=domain
                            )
                            predictions.append(sir_pred)
                            
                except Exception as e:
                    logger.error(f"Error in {domain} prediction: {e}")
        
        # Outbreak risk prediction
        if risk_assessments and len(risk_assessments) >= 3:
            try:
                risk_pred = OutbreakRiskPredictor.risk_probability_prediction(
                    risk_assessments, prediction_days=7, domain="integrated"
                )
                predictions.append(risk_pred)
                
            except Exception as e:
                logger.error(f"Error in risk prediction: {e}")
        
        # Ensemble prediction (combine multiple models)
        human_predictions = [p for p in predictions 
                           if p.target_domain == "human" and p.prediction_type == PredictionType.CASE_COUNT]
        
        if len(human_predictions) >= 2:
            try:
                ensemble_pred = self._create_ensemble_prediction(human_predictions)
                predictions.append(ensemble_pred)
                
            except Exception as e:
                logger.error(f"Error in ensemble prediction: {e}")
        
        # Store results
        self.prediction_results.extend(predictions)
        
        # Log performance
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.model_performance_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "predictions_generated": len(predictions),
            "domains_analyzed": len([d for d, ts in domain_time_series.items() if len(ts) >= 3]),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data),
                "risk_assessments": len(risk_assessments) if risk_assessments else 0
            }
        })
        
        logger.info(f"Prediction analysis completed: {len(predictions)} predictions in {analysis_time:.2f}s")
        
        return predictions
    
    def _extract_time_series(self, data: List[Dict], value_field: str) -> List[Tuple[datetime, float]]:
        """Extract time series from surveillance data."""
        
        time_series = []
        
        for record in data:
            timestamp_str = record.get('timestamp')
            value = record.get(value_field)
            
            # Handle environmental data with parameter-specific values
            if value_field == "value" and record.get('parameter'):
                if record.get('parameter') not in ['temperature', 'humidity']:
                    continue
                value = record.get('value')
            
            if timestamp_str and value is not None:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str[:19])
                    time_series.append((timestamp, float(value)))
                except (ValueError, TypeError):
                    continue
        
        # Sort by timestamp
        time_series.sort(key=lambda x: x[0])
        
        return time_series
    
    def _create_ensemble_prediction(self, predictions: List[PredictionResult]) -> PredictionResult:
        """Create ensemble prediction from multiple models."""
        
        if len(predictions) < 2:
            raise ValueError("Need at least 2 predictions for ensemble")
        
        # Find common prediction dates
        all_dates = set()
        for pred in predictions:
            all_dates.update(dt for dt, _ in pred.predicted_values)
        
        common_dates = sorted(all_dates)
        
        # Calculate ensemble predictions (simple average)
        ensemble_values = []
        ensemble_confidence = []
        
        for date in common_dates:
            date_predictions = []
            date_lower_cis = []
            date_upper_cis = []
            
            for pred in predictions:
                # Find prediction for this date
                for pred_date, pred_value in pred.predicted_values:
                    if pred_date == date:
                        date_predictions.append(pred_value)
                        break
                
                # Find confidence interval for this date
                for ci_date, lower, upper in pred.confidence_intervals:
                    if ci_date == date:
                        date_lower_cis.append(lower)
                        date_upper_cis.append(upper)
                        break
            
            if date_predictions:
                ensemble_value = statistics.mean(date_predictions)
                ensemble_lower = statistics.mean(date_lower_cis) if date_lower_cis else ensemble_value * 0.8
                ensemble_upper = statistics.mean(date_upper_cis) if date_upper_cis else ensemble_value * 1.2
                
                ensemble_values.append((date, ensemble_value))
                ensemble_confidence.append((date, ensemble_lower, ensemble_upper))
        
        # Calculate ensemble performance metrics
        ensemble_accuracy = statistics.mean([p.model_accuracy or 0.5 for p in predictions])
        ensemble_rmse = statistics.mean([p.root_mean_square_error or 1.0 for p in predictions])
        
        # Combine insights from all models
        all_insights = []
        for pred in predictions:
            all_insights.extend(pred.key_insights)
        
        # Remove duplicates and select most important
        unique_insights = list(set(all_insights))[:5]
        unique_insights.append(f"Ensemble of {len(predictions)} models")
        
        result = PredictionResult(
            prediction_id=f"ENSEMBLE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            model_type=PredictionModel.ENSEMBLE,
            prediction_type=PredictionType.CASE_COUNT,
            analysis_timestamp=datetime.now(),
            target_variable=predictions[0].target_variable,
            target_domain=predictions[0].target_domain,
            prediction_horizon_days=len(ensemble_values),
            predicted_values=ensemble_values,
            confidence_intervals=ensemble_confidence,
            model_accuracy=ensemble_accuracy,
            root_mean_square_error=ensemble_rmse,
            confidence_level=ConfidenceLevel.HIGH,
            training_data_points=max(p.training_data_points for p in predictions),
            data_period_start=min(p.data_period_start for p in predictions if p.data_period_start),
            data_period_end=max(p.data_period_end for p in predictions if p.data_period_end),
            key_insights=unique_insights,
            model_parameters={"component_models": len(predictions)}
        )
        
        return result
    
    def get_prediction_summary(self) -> Dict:
        """Get summary of prediction analysis results."""
        
        if not self.prediction_results:
            return {"message": "No predictions generated"}
        
        # Group by model type and prediction type
        by_model = defaultdict(list)
        by_prediction_type = defaultdict(list)
        by_domain = defaultdict(list)
        
        for result in self.prediction_results:
            by_model[result.model_type.value].append(result)
            by_prediction_type[result.prediction_type.value].append(result)
            by_domain[result.target_domain].append(result)
        
        # Find high-confidence predictions
        high_confidence = [r for r in self.prediction_results 
                          if r.confidence_level in [ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH]]
        
        # Find high-risk predictions
        high_risk = [r for r in self.prediction_results 
                    if r.outbreak_probability and r.outbreak_probability > 0.5]
        
        # Calculate performance statistics
        accuracies = [r.model_accuracy for r in self.prediction_results if r.model_accuracy]
        
        summary = {
            "total_predictions": len(self.prediction_results),
            "high_confidence_predictions": len(high_confidence),
            "high_risk_predictions": len(high_risk),
            "model_types": {mtype: len(results) for mtype, results in by_model.items()},
            "prediction_types": {ptype: len(results) for ptype, results in by_prediction_type.items()},
            "domains": {domain: len(results) for domain, results in by_domain.items()},
            "performance_metrics": {
                "average_accuracy": statistics.mean(accuracies) if accuracies else None,
                "max_accuracy": max(accuracies) if accuracies else None,
                "min_accuracy": min(accuracies) if accuracies else None
            },
            "analysis_performance": {
                "total_analyses": len(self.model_performance_log),
                "average_duration": statistics.mean([
                    log['analysis_duration'] for log in self.model_performance_log
                ]) if self.model_performance_log else 0
            }
        }
        
        return summary
    
    def get_high_risk_predictions(self) -> List[PredictionResult]:
        """Get predictions indicating high outbreak risk."""
        
        high_risk = []
        
        for result in self.prediction_results:
            # High risk criteria
            if (result.outbreak_probability and result.outbreak_probability > 0.6) or \
               (result.prediction_type == PredictionType.CASE_COUNT and 
                result.predicted_values and result.predicted_values[-1][1] > 50):
                high_risk.append(result)
        
        return sorted(high_risk, 
                     key=lambda r: r.outbreak_probability or 0, 
                     reverse=True)

# Mock data generator
def generate_mock_prediction_data():
    """Generate mock data for prediction testing."""
    
    base_date = datetime.now() - timedelta(days=21)
    
    # Generate animal data with exponential growth pattern
    animal_data = []
    for i in range(21):
        date = base_date + timedelta(days=i)
        
        # Exponential growth: starting low, accelerating
        base_mortality = 2
        growth_factor = 1.05 ** i  # 5% daily growth
        mortality = int(base_mortality * growth_factor + random.uniform(-1, 1))
        
        animal_data.append({
            "animal_id": f"PRED_FARM_{i:03d}",
            "timestamp": date.isoformat(),
            "species": "poultry",
            "mortality_count": max(0, mortality)
        })
    
    # Generate human data with delayed exponential growth
    human_data = []
    for i in range(19):  # Start 2 days later
        date = base_date + timedelta(days=i+2)
        
        # Human cases following animal pattern with 2-day lag
        base_cases = 1
        growth_factor = 1.08 ** i  # 8% daily growth (faster human spread)
        cases = int(base_cases * growth_factor + random.uniform(0, 1))
        
        human_data.append({
            "case_id": f"PRED_HUM_{i:03d}",
            "timestamp": date.isoformat(),
            "case_classification": "confirmed",
            "case_count": max(0, cases)
        })
    
    # Generate environmental data with seasonal pattern
    environmental_data = []
    for i in range(21):
        date = base_date + timedelta(days=i)
        
        # Temperature with slight warming trend
        base_temp = 25
        seasonal = 3 * math.sin(2 * math.pi * i / 30)
        trend = i * 0.2  # Warming trend
        temp = base_temp + seasonal + trend + random.uniform(-1, 1)
        
        environmental_data.append({
            "record_id": f"PRED_ENV_{i:03d}",
            "timestamp": date.isoformat(),
            "parameter": "temperature",
            "value": temp
        })
    
    # Generate mock risk assessments with increasing risk
    risk_assessments = []
    for i in range(15):
        date = base_date + timedelta(days=i+5)
        
        # Increasing risk over time
        base_risk = 30
        risk_increase = i * 3
        risk_score = min(95, base_risk + risk_increase + random.uniform(-5, 5))
        
        risk_assessments.append({
            "assessment_id": f"RISK_{i:03d}",
            "timestamp": date.isoformat(),
            "overall_risk_score": risk_score,
            "risk_level": "high" if risk_score > 70 else "moderate" if risk_score > 40 else "low"
        })
    
    return animal_data, human_data, environmental_data, risk_assessments

def run_demonstration():
    """Run demonstration of predictive modeling system."""
    print("🔮 One Health Predictive Modeling System - Demonstration")
    print("=" * 60)
    
    # Initialize engine
    engine = OneHealthPredictiveEngine()
    
    # Generate mock data with prediction patterns
    animal_data, human_data, env_data, risk_data = generate_mock_prediction_data()
    
    print(f"\n📈 Prediction Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    print(f"  Risk Assessments: {len(risk_data)}")
    
    # Run comprehensive prediction analysis
    print(f"\n🔮 Running Comprehensive Prediction Analysis...")
    predictions = engine.comprehensive_prediction_analysis(
        animal_data, human_data, env_data, risk_data
    )
    
    # Display prediction results
    print(f"\n📊 Prediction Results ({len(predictions)} total):")
    
    for i, result in enumerate(predictions, 1):
        print(f"\n{i}. {result.model_type.value.replace('_', ' ').title()} Model")
        print(f"   Prediction ID: {result.prediction_id}")
        print(f"   Target: {result.target_variable} ({result.target_domain})")
        print(f"   Type: {result.prediction_type.value.replace('_', ' ').title()}")
        print(f"   Horizon: {result.prediction_horizon_days} days")
        print(f"   Confidence: {result.confidence_level.value.upper()}")
        
        if result.model_accuracy:
            print(f"   Accuracy: {result.model_accuracy:.3f}")
        
        if result.r_squared:
            print(f"   R²: {result.r_squared:.3f}")
        
        if result.outbreak_probability:
            print(f"   Outbreak Probability: {result.outbreak_probability*100:.1f}%")
        
        if result.peak_date_estimate:
            days_to_peak = (result.peak_date_estimate - datetime.now()).days
            print(f"   Peak Date: {days_to_peak} days from now")
            print(f"   Peak Intensity: {result.peak_intensity_estimate:.1f}")
        
        # Show sample predictions
        if result.predicted_values:
            sample_predictions = result.predicted_values[:3]  # First 3 days
            print(f"   Sample Predictions:")
            for date, value in sample_predictions:
                days_ahead = (date - datetime.now()).days
                print(f"     Day +{days_ahead}: {value:.1f}")
        
        if result.key_insights:
            print(f"   Key Insights ({len(result.key_insights)}):")
            for insight in result.key_insights[:3]:  # Top 3 insights
                print(f"     • {insight}")
    
    # Prediction summary
    summary = engine.get_prediction_summary()
    print(f"\n📊 Prediction Summary:")
    print(f"  Total Predictions: {summary['total_predictions']}")
    print(f"  High Confidence: {summary['high_confidence_predictions']}")
    print(f"  High Risk: {summary['high_risk_predictions']}")
    
    if summary['performance_metrics']['average_accuracy']:
        print(f"  Average Accuracy: {summary['performance_metrics']['average_accuracy']:.3f}")
    
    print(f"\n🔮 By Model Type:")
    for model_type, count in summary['model_types'].items():
        print(f"  {model_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n📈 By Prediction Type:")
    for pred_type, count in summary['prediction_types'].items():
        print(f"  {pred_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n🏥 By Domain:")
    for domain, count in summary['domains'].items():
        print(f"  {domain.title()}: {count}")
    
    # High-risk predictions
    high_risk = engine.get_high_risk_predictions()
    if high_risk:
        print(f"\n🚨 HIGH RISK Predictions ({len(high_risk)}):")
        for result in high_risk:
            risk_desc = f"{result.outbreak_probability*100:.0f}%" if result.outbreak_probability else "High cases"
            print(f"  • {result.target_variable} ({result.target_domain}): {risk_desc}")
            if result.peak_date_estimate:
                days_to_peak = (result.peak_date_estimate - datetime.now()).days
                print(f"    Peak in {days_to_peak} days")
    
    print(f"\n⚡ Performance: {summary['analysis_performance']['average_duration']:.3f}s average")
    
    return engine

if __name__ == "__main__":
    engine = run_demonstration()
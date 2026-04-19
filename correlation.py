"""
Advanced Correlation Analysis Engine
====================================
Module 2: Essential Epidemiologic Tools

Sophisticated correlation analysis system for One Health surveillance, providing
advanced statistical correlation methods, multivariate analysis, and dynamic correlation tracking.

NIW Focus: Deep correlation insights revealing complex epidemiological relationships.
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

class CorrelationType(Enum):
    """Types of correlation analysis."""
    PEARSON = "pearson"                  # Linear correlation
    SPEARMAN = "spearman"               # Rank correlation  
    KENDALL = "kendall"                 # Rank correlation (tau)
    PARTIAL = "partial"                 # Partial correlation
    LAGGED = "lagged"                   # Time-lagged correlation
    ROLLING = "rolling"                 # Rolling window correlation
    NONLINEAR = "nonlinear"             # Non-linear relationships
    THRESHOLD = "threshold"             # Threshold/breakpoint correlation

class CorrelationStrength(Enum):
    """Correlation strength categories."""
    NEGLIGIBLE = "negligible"           # |r| < 0.1
    WEAK = "weak"                       # 0.1 <= |r| < 0.3
    MODERATE = "moderate"               # 0.3 <= |r| < 0.7
    STRONG = "strong"                   # 0.7 <= |r| < 0.9
    VERY_STRONG = "very_strong"         # |r| >= 0.9

class CorrelationDirection(Enum):
    """Direction of correlation relationship."""
    POSITIVE = "positive"               # Variables increase together
    NEGATIVE = "negative"               # One increases, other decreases
    BIDIRECTIONAL = "bidirectional"     # Mutual influence
    UNIDIRECTIONAL = "unidirectional"   # One-way influence

@dataclass
class CorrelationResult:
    """Result of correlation analysis."""
    
    analysis_id: str
    correlation_type: CorrelationType
    analysis_timestamp: datetime
    
    # Variables analyzed
    variable_1_name: str
    variable_2_name: str
    variable_1_domain: str              # "animal", "human", "environmental"
    variable_2_domain: str
    
    # Correlation statistics
    correlation_coefficient: float
    p_value: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    sample_size: int = 0
    degrees_of_freedom: Optional[int] = None
    
    # Classification
    strength: CorrelationStrength = CorrelationStrength.NEGLIGIBLE
    direction: CorrelationDirection = CorrelationDirection.POSITIVE
    statistical_significance: bool = False
    
    # Advanced metrics
    r_squared: Optional[float] = None           # Coefficient of determination
    adjusted_r_squared: Optional[float] = None  # Adjusted R²
    effect_size: Optional[str] = None           # "small", "medium", "large"
    
    # Temporal characteristics
    lag_days: Optional[int] = None              # For lagged correlations
    optimal_lag: Optional[int] = None           # Best lag period found
    window_size_days: Optional[int] = None      # For rolling correlations
    
    # Non-linear characteristics
    curve_type: Optional[str] = None            # "exponential", "logarithmic", "polynomial"
    curve_parameters: Optional[Dict] = None     # Curve fitting parameters
    threshold_value: Optional[float] = None     # For threshold correlations
    
    # Context information
    data_period_start: Optional[datetime] = None
    data_period_end: Optional[datetime] = None
    outliers_detected: int = 0
    missing_data_percent: float = 0.0
    
    # Interpretation
    biological_plausibility: Optional[str] = None    # "high", "moderate", "low"
    epidemiological_relevance: Optional[str] = None  # "direct", "indirect", "confounded"
    recommended_followup: List[str] = None
    
    def __post_init__(self):
        """Initialize derived values."""
        if self.recommended_followup is None:
            self.recommended_followup = []
        
        # Calculate R-squared if not provided
        if self.r_squared is None and self.correlation_coefficient is not None:
            self.r_squared = self.correlation_coefficient ** 2
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['correlation_type'] = self.correlation_type.value
        data['strength'] = self.strength.value
        data['direction'] = self.direction.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        
        if self.data_period_start:
            data['data_period_start'] = self.data_period_start.isoformat()
        if self.data_period_end:
            data['data_period_end'] = self.data_period_end.isoformat()
            
        return data

class PearsonCorrelationAnalyzer:
    """Performs Pearson correlation analysis."""
    
    @staticmethod
    def calculate_correlation(data1: List[float], data2: List[float],
                            variable_names: Tuple[str, str],
                            domain_names: Tuple[str, str]) -> CorrelationResult:
        """Calculate Pearson correlation between two variables."""
        
        if len(data1) != len(data2):
            raise ValueError("Data arrays must have same length")
        
        if len(data1) < 3:
            raise ValueError("Need at least 3 data points for correlation")
        
        # Remove missing data pairs
        clean_data = [(x, y) for x, y in zip(data1, data2) 
                     if x is not None and y is not None and 
                     not (math.isnan(x) if isinstance(x, float) else False) and
                     not (math.isnan(y) if isinstance(y, float) else False)]
        
        if len(clean_data) < 3:
            raise ValueError("Insufficient clean data for correlation")
        
        clean_x, clean_y = zip(*clean_data)
        missing_percent = (len(data1) - len(clean_data)) / len(data1) * 100
        
        # Calculate Pearson correlation
        try:
            correlation = statistics.correlation(clean_x, clean_y)
        except statistics.StatisticsError:
            correlation = 0.0
        
        # Calculate statistical significance (simplified t-test)
        n = len(clean_data)
        df = n - 2
        
        if abs(correlation) == 1.0:
            p_value = 0.0
        elif n <= 2:
            p_value = 1.0
        else:
            t_stat = correlation * math.sqrt(df / (1 - correlation**2))
            p_value = PearsonCorrelationAnalyzer._t_test_p_value(abs(t_stat), df)
        
        # Calculate confidence interval (Fisher transformation)
        confidence_interval = PearsonCorrelationAnalyzer._calculate_confidence_interval(
            correlation, n, confidence_level=0.95
        )
        
        # Classify strength and direction
        strength = PearsonCorrelationAnalyzer._classify_strength(correlation)
        direction = CorrelationDirection.POSITIVE if correlation >= 0 else CorrelationDirection.NEGATIVE
        
        # Calculate effect size
        effect_size = PearsonCorrelationAnalyzer._classify_effect_size(correlation)
        
        return CorrelationResult(
            analysis_id=f"PEARSON_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            correlation_type=CorrelationType.PEARSON,
            analysis_timestamp=datetime.now(),
            variable_1_name=variable_names[0],
            variable_2_name=variable_names[1],
            variable_1_domain=domain_names[0],
            variable_2_domain=domain_names[1],
            correlation_coefficient=correlation,
            p_value=p_value,
            confidence_interval=confidence_interval,
            sample_size=n,
            degrees_of_freedom=df,
            strength=strength,
            direction=direction,
            statistical_significance=p_value < 0.05 if p_value else False,
            effect_size=effect_size,
            missing_data_percent=missing_percent
        )
    
    @staticmethod
    def _t_test_p_value(t_stat: float, df: int) -> float:
        """Simplified p-value calculation for t-test."""
        # Critical values for common significance levels
        if df >= 30:
            critical_01 = 2.576
            critical_05 = 1.96
        elif df >= 10:
            critical_01 = 2.8 + (2.576 - 2.8) * (df - 10) / 20
            critical_05 = 2.2 + (1.96 - 2.2) * (df - 10) / 20
        else:
            critical_01 = 3.5
            critical_05 = 2.5
        
        if t_stat > critical_01:
            return 0.001
        elif t_stat > critical_05:
            return 0.05 if t_stat > critical_05 else 0.1
        else:
            return 0.2
    
    @staticmethod
    def _calculate_confidence_interval(r: float, n: int, 
                                     confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval using Fisher transformation."""
        if abs(r) >= 1.0 or n <= 3:
            return (-1.0, 1.0)
        
        # Fisher transformation
        z_r = 0.5 * math.log((1 + r) / (1 - r))
        se_z = 1 / math.sqrt(n - 3)
        
        # Z critical value for confidence level
        alpha = 1 - confidence_level
        z_critical = 1.96 if confidence_level == 0.95 else 2.576  # Simplified
        
        # Confidence interval for z
        z_lower = z_r - z_critical * se_z
        z_upper = z_r + z_critical * se_z
        
        # Transform back to correlation scale
        r_lower = (math.exp(2 * z_lower) - 1) / (math.exp(2 * z_lower) + 1)
        r_upper = (math.exp(2 * z_upper) - 1) / (math.exp(2 * z_upper) + 1)
        
        return (max(-1.0, r_lower), min(1.0, r_upper))
    
    @staticmethod
    def _classify_strength(correlation: float) -> CorrelationStrength:
        """Classify correlation strength."""
        abs_corr = abs(correlation)
        
        if abs_corr >= 0.9:
            return CorrelationStrength.VERY_STRONG
        elif abs_corr >= 0.7:
            return CorrelationStrength.STRONG
        elif abs_corr >= 0.3:
            return CorrelationStrength.MODERATE
        elif abs_corr >= 0.1:
            return CorrelationStrength.WEAK
        else:
            return CorrelationStrength.NEGLIGIBLE
    
    @staticmethod
    def _classify_effect_size(correlation: float) -> str:
        """Classify effect size according to Cohen's conventions."""
        abs_corr = abs(correlation)
        
        if abs_corr >= 0.5:
            return "large"
        elif abs_corr >= 0.3:
            return "medium"
        elif abs_corr >= 0.1:
            return "small"
        else:
            return "negligible"

class LaggedCorrelationAnalyzer:
    """Analyzes time-lagged correlations."""
    
    @staticmethod
    def analyze_lagged_correlation(time_series_1: List[Tuple[datetime, float]],
                                 time_series_2: List[Tuple[datetime, float]],
                                 variable_names: Tuple[str, str],
                                 domain_names: Tuple[str, str],
                                 max_lag_days: int = 30) -> CorrelationResult:
        """Analyze correlation with various time lags."""
        
        if len(time_series_1) < 5 or len(time_series_2) < 5:
            raise ValueError("Need at least 5 time points for lagged correlation")
        
        # Convert to daily aggregated data
        daily_data_1 = LaggedCorrelationAnalyzer._aggregate_daily(time_series_1)
        daily_data_2 = LaggedCorrelationAnalyzer._aggregate_daily(time_series_2)
        
        # Test different lag periods
        best_correlation = 0.0
        best_lag = 0
        best_p_value = 1.0
        lag_results = []
        
        for lag_days in range(-max_lag_days, max_lag_days + 1):
            correlation, p_value, sample_size = LaggedCorrelationAnalyzer._calculate_lag_correlation(
                daily_data_1, daily_data_2, lag_days
            )
            
            lag_results.append({
                'lag_days': lag_days,
                'correlation': correlation,
                'p_value': p_value,
                'sample_size': sample_size
            })
            
            if abs(correlation) > abs(best_correlation):
                best_correlation = correlation
                best_lag = lag_days
                best_p_value = p_value
        
        # Classify strength and direction
        strength = PearsonCorrelationAnalyzer._classify_strength(best_correlation)
        direction = CorrelationDirection.POSITIVE if best_correlation >= 0 else CorrelationDirection.NEGATIVE
        
        # Calculate confidence interval for best correlation
        best_sample_size = next(r['sample_size'] for r in lag_results if r['lag_days'] == best_lag)
        confidence_interval = PearsonCorrelationAnalyzer._calculate_confidence_interval(
            best_correlation, best_sample_size
        )
        
        # Determine data period
        all_dates_1 = [date for date, _ in time_series_1]
        all_dates_2 = [date for date, _ in time_series_2]
        period_start = min(min(all_dates_1), min(all_dates_2))
        period_end = max(max(all_dates_1), max(all_dates_2))
        
        result = CorrelationResult(
            analysis_id=f"LAGGED_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            correlation_type=CorrelationType.LAGGED,
            analysis_timestamp=datetime.now(),
            variable_1_name=variable_names[0],
            variable_2_name=variable_names[1],
            variable_1_domain=domain_names[0],
            variable_2_domain=domain_names[1],
            correlation_coefficient=best_correlation,
            p_value=best_p_value,
            confidence_interval=confidence_interval,
            sample_size=best_sample_size,
            strength=strength,
            direction=direction,
            statistical_significance=best_p_value < 0.05 if best_p_value else False,
            lag_days=best_lag,
            optimal_lag=best_lag,
            data_period_start=period_start,
            data_period_end=period_end
        )
        
        # Add interpretation
        if abs(best_lag) > 0:
            if best_lag > 0:
                result.recommended_followup.append(f"{variable_names[0]} leads {variable_names[1]} by {best_lag} days")
            else:
                result.recommended_followup.append(f"{variable_names[1]} leads {variable_names[0]} by {abs(best_lag)} days")
        
        return result
    
    @staticmethod
    def _aggregate_daily(time_series: List[Tuple[datetime, float]]) -> Dict[str, float]:
        """Aggregate time series data by day."""
        daily_data = defaultdict(list)
        
        for timestamp, value in time_series:
            date_key = timestamp.date().strftime('%Y-%m-%d')
            daily_data[date_key].append(value)
        
        # Average values for each day
        return {date: statistics.mean(values) for date, values in daily_data.items()}
    
    @staticmethod
    def _calculate_lag_correlation(data_1: Dict[str, float], 
                                 data_2: Dict[str, float], 
                                 lag_days: int) -> Tuple[float, float, int]:
        """Calculate correlation with specific lag."""
        
        # Adjust dates for lag
        adjusted_data_2 = {}
        for date_str, value in data_2.items():
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                adjusted_date = date_obj + timedelta(days=lag_days)
                adjusted_data_2[adjusted_date.strftime('%Y-%m-%d')] = value
            except ValueError:
                continue
        
        # Find overlapping dates
        common_dates = set(data_1.keys()) & set(adjusted_data_2.keys())
        
        if len(common_dates) < 3:
            return 0.0, 1.0, 0
        
        values_1 = [data_1[date] for date in common_dates]
        values_2 = [adjusted_data_2[date] for date in common_dates]
        
        try:
            correlation = statistics.correlation(values_1, values_2)
            
            # Calculate p-value
            n = len(common_dates)
            if n > 2 and abs(correlation) < 1.0:
                df = n - 2
                t_stat = correlation * math.sqrt(df / (1 - correlation**2))
                p_value = PearsonCorrelationAnalyzer._t_test_p_value(abs(t_stat), df)
            else:
                p_value = 1.0
                
            return correlation, p_value, n
            
        except statistics.StatisticsError:
            return 0.0, 1.0, len(common_dates)

class PartialCorrelationAnalyzer:
    """Analyzes partial correlations controlling for confounding variables."""
    
    @staticmethod
    def calculate_partial_correlation(primary_data: List[float],
                                    secondary_data: List[float],
                                    control_data: List[float],
                                    variable_names: Tuple[str, str, str],
                                    domain_names: Tuple[str, str, str]) -> CorrelationResult:
        """Calculate partial correlation controlling for third variable."""
        
        if len(primary_data) != len(secondary_data) or len(primary_data) != len(control_data):
            raise ValueError("All data arrays must have same length")
        
        if len(primary_data) < 4:
            raise ValueError("Need at least 4 data points for partial correlation")
        
        # Remove missing data
        clean_data = [(x, y, z) for x, y, z in zip(primary_data, secondary_data, control_data) 
                     if all(val is not None for val in [x, y, z]) and
                     all(not (math.isnan(val) if isinstance(val, float) else False) for val in [x, y, z])]
        
        if len(clean_data) < 4:
            raise ValueError("Insufficient clean data for partial correlation")
        
        clean_x, clean_y, clean_z = zip(*clean_data)
        n = len(clean_data)
        
        try:
            # Calculate pairwise correlations
            r_xy = statistics.correlation(clean_x, clean_y)
            r_xz = statistics.correlation(clean_x, clean_z)
            r_yz = statistics.correlation(clean_y, clean_z)
            
            # Calculate partial correlation: r_xy.z
            numerator = r_xy - (r_xz * r_yz)
            denominator = math.sqrt((1 - r_xz**2) * (1 - r_yz**2))
            
            if denominator == 0:
                partial_correlation = 0.0
            else:
                partial_correlation = numerator / denominator
                
        except (statistics.StatisticsError, ZeroDivisionError):
            partial_correlation = 0.0
        
        # Calculate statistical significance
        df = n - 3  # Degrees of freedom for partial correlation
        if df > 0 and abs(partial_correlation) < 1.0:
            t_stat = partial_correlation * math.sqrt(df / (1 - partial_correlation**2))
            p_value = PearsonCorrelationAnalyzer._t_test_p_value(abs(t_stat), df)
        else:
            p_value = 1.0
        
        # Calculate confidence interval
        confidence_interval = PearsonCorrelationAnalyzer._calculate_confidence_interval(
            partial_correlation, n - 1  # Adjusted for control variable
        )
        
        # Classify results
        strength = PearsonCorrelationAnalyzer._classify_strength(partial_correlation)
        direction = CorrelationDirection.POSITIVE if partial_correlation >= 0 else CorrelationDirection.NEGATIVE
        
        result = CorrelationResult(
            analysis_id=f"PARTIAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            correlation_type=CorrelationType.PARTIAL,
            analysis_timestamp=datetime.now(),
            variable_1_name=variable_names[0],
            variable_2_name=variable_names[1],
            variable_1_domain=domain_names[0],
            variable_2_domain=domain_names[1],
            correlation_coefficient=partial_correlation,
            p_value=p_value,
            confidence_interval=confidence_interval,
            sample_size=n,
            degrees_of_freedom=df,
            strength=strength,
            direction=direction,
            statistical_significance=p_value < 0.05 if p_value else False,
            missing_data_percent=(len(primary_data) - n) / len(primary_data) * 100
        )
        
        # Add interpretation about control variable effect
        raw_correlation = r_xy
        control_effect = abs(raw_correlation) - abs(partial_correlation)
        
        if control_effect > 0.1:
            result.recommended_followup.append(f"Control variable '{variable_names[2]}' explains significant variance")
        elif control_effect < -0.1:
            result.recommended_followup.append(f"Control variable '{variable_names[2]}' may be suppressing correlation")
        else:
            result.recommended_followup.append(f"Control variable '{variable_names[2]}' has minimal effect")
        
        return result

class RollingCorrelationAnalyzer:
    """Analyzes time-varying correlations using rolling windows."""
    
    @staticmethod
    def analyze_rolling_correlation(time_series_1: List[Tuple[datetime, float]],
                                  time_series_2: List[Tuple[datetime, float]],
                                  variable_names: Tuple[str, str],
                                  domain_names: Tuple[str, str],
                                  window_days: int = 30) -> CorrelationResult:
        """Analyze correlation using rolling time windows."""
        
        # Merge and align time series
        aligned_data = RollingCorrelationAnalyzer._align_time_series(
            time_series_1, time_series_2
        )
        
        if len(aligned_data) < window_days + 5:
            raise ValueError(f"Need at least {window_days + 5} aligned data points")
        
        # Calculate rolling correlations
        rolling_correlations = []
        window_start_dates = []
        
        for i in range(len(aligned_data) - window_days + 1):
            window_data = aligned_data[i:i + window_days]
            window_dates = [item[0] for item in window_data]
            window_values_1 = [item[1] for item in window_data if item[1] is not None]
            window_values_2 = [item[2] for item in window_data if item[2] is not None]
            
            if len(window_values_1) >= 3 and len(window_values_2) >= 3:
                try:
                    correlation = statistics.correlation(window_values_1, window_values_2)
                    rolling_correlations.append(correlation)
                    window_start_dates.append(window_dates[0])
                except statistics.StatisticsError:
                    rolling_correlations.append(0.0)
                    window_start_dates.append(window_dates[0])
        
        if not rolling_correlations:
            raise ValueError("No valid rolling correlations calculated")
        
        # Calculate summary statistics
        mean_correlation = statistics.mean(rolling_correlations)
        correlation_std = statistics.stdev(rolling_correlations) if len(rolling_correlations) > 1 else 0.0
        max_correlation = max(rolling_correlations)
        min_correlation = min(rolling_correlations)
        
        # Detect correlation stability
        correlation_range = max_correlation - min_correlation
        stability = "stable" if correlation_range < 0.2 else "variable" if correlation_range < 0.5 else "highly_variable"
        
        # Calculate overall statistical significance (using mean correlation)
        n_windows = len(rolling_correlations)
        effective_n = len(aligned_data)  # Total data points
        
        if effective_n > 2 and abs(mean_correlation) < 1.0:
            df = effective_n - 2
            t_stat = mean_correlation * math.sqrt(df / (1 - mean_correlation**2))
            p_value = PearsonCorrelationAnalyzer._t_test_p_value(abs(t_stat), df)
        else:
            p_value = 1.0
        
        # Classify strength
        strength = PearsonCorrelationAnalyzer._classify_strength(mean_correlation)
        direction = CorrelationDirection.POSITIVE if mean_correlation >= 0 else CorrelationDirection.NEGATIVE
        
        # Determine data period
        all_dates = [item[0] for item in aligned_data]
        period_start = min(all_dates)
        period_end = max(all_dates)
        
        result = CorrelationResult(
            analysis_id=f"ROLLING_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            correlation_type=CorrelationType.ROLLING,
            analysis_timestamp=datetime.now(),
            variable_1_name=variable_names[0],
            variable_2_name=variable_names[1],
            variable_1_domain=domain_names[0],
            variable_2_domain=domain_names[1],
            correlation_coefficient=mean_correlation,
            p_value=p_value,
            sample_size=effective_n,
            strength=strength,
            direction=direction,
            statistical_significance=p_value < 0.05 if p_value else False,
            window_size_days=window_days,
            data_period_start=period_start,
            data_period_end=period_end
        )
        
        # Add interpretation about correlation dynamics
        result.recommended_followup.append(f"Correlation stability: {stability}")
        result.recommended_followup.append(f"Correlation range: {min_correlation:.3f} to {max_correlation:.3f}")
        
        if correlation_std > 0.3:
            result.recommended_followup.append("High correlation variability detected - investigate temporal factors")
        
        return result
    
    @staticmethod
    def _align_time_series(ts1: List[Tuple[datetime, float]], 
                         ts2: List[Tuple[datetime, float]]) -> List[Tuple[datetime, Optional[float], Optional[float]]]:
        """Align two time series by date."""
        
        # Create dictionaries for quick lookup
        dict1 = {date.date(): value for date, value in ts1}
        dict2 = {date.date(): value for date, value in ts2}
        
        # Get all unique dates
        all_dates = sorted(set(dict1.keys()) | set(dict2.keys()))
        
        # Create aligned data
        aligned = []
        for date in all_dates:
            value1 = dict1.get(date)
            value2 = dict2.get(date)
            aligned.append((datetime.combine(date, datetime.min.time()), value1, value2))
        
        return aligned

class AdvancedCorrelationEngine:
    """Main engine for advanced correlation analysis."""
    
    def __init__(self):
        self.correlation_results: List[CorrelationResult] = []
        self.analysis_log: List[Dict] = []
        
        logger.info("Advanced Correlation Engine initialized")
    
    def comprehensive_correlation_analysis(self, animal_data: List[Dict],
                                         human_data: List[Dict],
                                         environmental_data: List[Dict]) -> List[CorrelationResult]:
        """Perform comprehensive correlation analysis across all domains."""
        
        analysis_start = datetime.now()
        results = []
        
        logger.info(f"Starting comprehensive correlation analysis")
        
        # Extract time series for each domain
        domain_data = {
            "animal": self._extract_domain_variables(animal_data, "animal"),
            "human": self._extract_domain_variables(human_data, "human"),
            "environmental": self._extract_domain_variables(environmental_data, "environmental")
        }
        
        # Cross-domain correlation analysis
        domain_pairs = [
            ("animal", "human"),
            ("animal", "environmental"),
            ("human", "environmental")
        ]
        
        for domain1, domain2 in domain_pairs:
            data1 = domain_data[domain1]
            data2 = domain_data[domain2]
            
            if not data1 or not data2:
                continue
            
            try:
                # Pearson correlation
                pearson_result = self._analyze_domain_pair_pearson(
                    data1, data2, domain1, domain2
                )
                if pearson_result:
                    results.append(pearson_result)
                
                # Lagged correlation
                lagged_result = self._analyze_domain_pair_lagged(
                    data1, data2, domain1, domain2
                )
                if lagged_result:
                    results.append(lagged_result)
                
                # Rolling correlation
                rolling_result = self._analyze_domain_pair_rolling(
                    data1, data2, domain1, domain2
                )
                if rolling_result:
                    results.append(rolling_result)
                    
            except Exception as e:
                logger.error(f"Error in correlation analysis for {domain1}-{domain2}: {e}")
        
        # Partial correlation analysis (using environmental as control)
        if (domain_data["animal"] and domain_data["human"] and 
            domain_data["environmental"]):
            
            try:
                partial_result = self._analyze_partial_correlation(
                    domain_data["animal"], domain_data["human"], 
                    domain_data["environmental"]
                )
                if partial_result:
                    results.append(partial_result)
                    
            except Exception as e:
                logger.error(f"Error in partial correlation analysis: {e}")
        
        # Store results
        self.correlation_results.extend(results)
        
        # Log analysis
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "correlations_calculated": len(results),
            "domain_pairs_analyzed": len(domain_pairs),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            }
        })
        
        logger.info(f"Correlation analysis completed: {len(results)} correlations in {analysis_time:.2f}s")
        
        return results
    
    def _extract_domain_variables(self, data: List[Dict], domain: str) -> Dict[str, List[Tuple[datetime, float]]]:
        """Extract time series variables from domain data."""
        
        time_series = {}
        
        for record in data:
            timestamp_str = record.get('timestamp')
            if not timestamp_str:
                continue
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str[:19])
            except ValueError:
                continue
            
            # Extract relevant variables based on domain
            if domain == "animal":
                variables = {
                    'mortality_count': record.get('mortality_count', 0),
                    'morbidity_count': record.get('morbidity_count', 0)
                }
            elif domain == "human":
                variables = {
                    'case_count': record.get('case_count', 0),
                    'severity_score': self._calculate_severity_score(record)
                }
            elif domain == "environmental":
                variables = {
                    'temperature': record.get('value') if record.get('parameter') == 'temperature' else None,
                    'humidity': record.get('value') if record.get('parameter') == 'humidity' else None,
                    'vector_count': record.get('total_collected', 0) if 'vector' in record.get('survey_id', '') else None
                }
            else:
                variables = {}
            
            # Add variables to time series
            for var_name, value in variables.items():
                if value is not None and isinstance(value, (int, float)):
                    if var_name not in time_series:
                        time_series[var_name] = []
                    time_series[var_name].append((timestamp, float(value)))
        
        # Sort time series by timestamp
        for var_name in time_series:
            time_series[var_name].sort(key=lambda x: x[0])
        
        return time_series
    
    def _calculate_severity_score(self, human_record: Dict) -> float:
        """Calculate severity score for human cases."""
        severity = human_record.get('severity', '').lower()
        healthcare_level = human_record.get('healthcare_level', '').lower()
        
        score = 0.0
        
        # Severity scoring
        if severity == 'critical':
            score += 4.0
        elif severity == 'severe':
            score += 3.0
        elif severity == 'moderate':
            score += 2.0
        elif severity == 'mild':
            score += 1.0
        
        # Healthcare level scoring
        if healthcare_level == 'deceased':
            score += 5.0
        elif healthcare_level == 'icu':
            score += 3.0
        elif healthcare_level == 'hospitalized':
            score += 2.0
        elif healthcare_level == 'emergency_department':
            score += 1.0
        
        return score
    
    def _analyze_domain_pair_pearson(self, data1: Dict, data2: Dict,
                                   domain1: str, domain2: str) -> Optional[CorrelationResult]:
        """Analyze Pearson correlation between domain pair."""
        
        # Find best variable pair
        best_result = None
        best_correlation = 0.0
        
        for var1_name, ts1 in data1.items():
            for var2_name, ts2 in data2.items():
                if len(ts1) >= 3 and len(ts2) >= 3:
                    try:
                        # Extract values (simple approach - could be improved with alignment)
                        values1 = [val for _, val in ts1]
                        values2 = [val for _, val in ts2]
                        
                        # Use shorter series length
                        min_len = min(len(values1), len(values2))
                        values1 = values1[:min_len]
                        values2 = values2[:min_len]
                        
                        if min_len >= 3:
                            result = PearsonCorrelationAnalyzer.calculate_correlation(
                                values1, values2,
                                (var1_name, var2_name),
                                (domain1, domain2)
                            )
                            
                            if abs(result.correlation_coefficient) > abs(best_correlation):
                                best_correlation = result.correlation_coefficient
                                best_result = result
                                
                    except Exception as e:
                        continue
        
        return best_result
    
    def _analyze_domain_pair_lagged(self, data1: Dict, data2: Dict,
                                  domain1: str, domain2: str) -> Optional[CorrelationResult]:
        """Analyze lagged correlation between domain pair."""
        
        # Find best variable pair for lagged analysis
        best_result = None
        best_correlation = 0.0
        
        for var1_name, ts1 in data1.items():
            for var2_name, ts2 in data2.items():
                if len(ts1) >= 5 and len(ts2) >= 5:
                    try:
                        result = LaggedCorrelationAnalyzer.analyze_lagged_correlation(
                            ts1, ts2,
                            (var1_name, var2_name),
                            (domain1, domain2)
                        )
                        
                        if abs(result.correlation_coefficient) > abs(best_correlation):
                            best_correlation = result.correlation_coefficient
                            best_result = result
                            
                    except Exception as e:
                        continue
        
        return best_result
    
    def _analyze_domain_pair_rolling(self, data1: Dict, data2: Dict,
                                   domain1: str, domain2: str) -> Optional[CorrelationResult]:
        """Analyze rolling correlation between domain pair."""
        
        # Find best variable pair for rolling analysis
        best_result = None
        best_correlation = 0.0
        
        for var1_name, ts1 in data1.items():
            for var2_name, ts2 in data2.items():
                if len(ts1) >= 15 and len(ts2) >= 15:  # Need enough data for rolling window
                    try:
                        result = RollingCorrelationAnalyzer.analyze_rolling_correlation(
                            ts1, ts2,
                            (var1_name, var2_name),
                            (domain1, domain2),
                            window_days=7  # 1-week rolling window
                        )
                        
                        if abs(result.correlation_coefficient) > abs(best_correlation):
                            best_correlation = result.correlation_coefficient
                            best_result = result
                            
                    except Exception as e:
                        continue
        
        return best_result
    
    def _analyze_partial_correlation(self, animal_data: Dict, human_data: Dict,
                                   env_data: Dict) -> Optional[CorrelationResult]:
        """Analyze partial correlation controlling for environmental factors."""
        
        # Find suitable variables
        animal_var = None
        human_var = None
        env_var = None
        
        # Get most suitable variables (with most data points)
        if animal_data:
            animal_var_name = max(animal_data.keys(), key=lambda k: len(animal_data[k]))
            animal_var = [val for _, val in animal_data[animal_var_name]]
        
        if human_data:
            human_var_name = max(human_data.keys(), key=lambda k: len(human_data[k]))
            human_var = [val for _, val in human_data[human_var_name]]
        
        if env_data:
            env_var_name = max(env_data.keys(), key=lambda k: len(env_data[k]))
            env_var = [val for _, val in env_data[env_var_name]]
        
        if not (animal_var and human_var and env_var):
            return None
        
        # Align data lengths
        min_len = min(len(animal_var), len(human_var), len(env_var))
        if min_len < 4:
            return None
        
        animal_var = animal_var[:min_len]
        human_var = human_var[:min_len]
        env_var = env_var[:min_len]
        
        try:
            return PartialCorrelationAnalyzer.calculate_partial_correlation(
                animal_var, human_var, env_var,
                (animal_var_name, human_var_name, env_var_name),
                ("animal", "human", "environmental")
            )
        except Exception as e:
            logger.error(f"Error in partial correlation calculation: {e}")
            return None
    
    def get_correlation_summary(self) -> Dict:
        """Get summary of correlation analysis results."""
        
        if not self.correlation_results:
            return {"message": "No correlation analyses performed"}
        
        # Group by correlation type
        by_type = defaultdict(list)
        by_strength = defaultdict(list)
        by_domain_pair = defaultdict(list)
        
        for result in self.correlation_results:
            by_type[result.correlation_type.value].append(result)
            by_strength[result.strength.value].append(result)
            
            domain_pair = f"{result.variable_1_domain}-{result.variable_2_domain}"
            by_domain_pair[domain_pair].append(result)
        
        # Find significant correlations
        significant_results = [r for r in self.correlation_results if r.statistical_significance]
        strong_correlations = [r for r in self.correlation_results 
                             if r.strength in [CorrelationStrength.STRONG, CorrelationStrength.VERY_STRONG]]
        
        # Calculate summary statistics
        correlation_values = [r.correlation_coefficient for r in self.correlation_results]
        
        summary = {
            "total_correlations": len(self.correlation_results),
            "significant_correlations": len(significant_results),
            "strong_correlations": len(strong_correlations),
            "correlation_types": {ctype: len(results) for ctype, results in by_type.items()},
            "strength_distribution": {strength: len(results) for strength, results in by_strength.items()},
            "domain_pairs": {pair: len(results) for pair, results in by_domain_pair.items()},
            "correlation_statistics": {
                "mean_correlation": statistics.mean([abs(c) for c in correlation_values]),
                "max_correlation": max([abs(c) for c in correlation_values]),
                "min_correlation": min([abs(c) for c in correlation_values])
            } if correlation_values else {},
            "analysis_performance": {
                "total_analyses": len(self.analysis_log),
                "average_duration": statistics.mean([
                    log['analysis_duration'] for log in self.analysis_log
                ]) if self.analysis_log else 0
            }
        }
        
        return summary
    
    def get_strongest_correlations(self, top_n: int = 5) -> List[CorrelationResult]:
        """Get the strongest correlations found."""
        
        return sorted(self.correlation_results, 
                     key=lambda r: abs(r.correlation_coefficient), 
                     reverse=True)[:top_n]

# Mock data generator
def generate_mock_correlation_data():
    """Generate mock data with known correlations for testing."""
    
    base_date = datetime.now() - timedelta(days=30)
    
    # Generate animal data with temperature-dependent pattern
    animal_data = []
    temperature_series = []
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Temperature with seasonal pattern
        temp = 25 + 5 * math.sin(2 * math.pi * i / 30) + random.uniform(-2, 2)
        temperature_series.append(temp)
        
        # Animal mortality correlated with temperature (high temp = more deaths)
        base_mortality = 2
        temp_effect = max(0, (temp - 30) * 0.5)  # Mortality increases when temp > 30
        mortality = int(base_mortality + temp_effect + random.uniform(-1, 1))
        
        animal_data.append({
            "animal_id": f"CORR_FARM_{i:03d}",
            "timestamp": date.isoformat(),
            "species": "poultry",
            "mortality_count": max(0, mortality),
            "morbidity_count": mortality * 2
        })
    
    # Generate human data with lag correlation to animal data
    human_data = []
    for i in range(28):  # Start 2 days later
        date = base_date + timedelta(days=i+2)
        
        # Human cases correlated with animal mortality from 2 days ago
        if i < len(animal_data) - 2:
            animal_mortality_2days_ago = animal_data[i]['mortality_count']
            base_cases = 1
            animal_effect = animal_mortality_2days_ago * 0.3
            cases = int(base_cases + animal_effect + random.uniform(0, 1))
        else:
            cases = 1
        
        human_data.append({
            "case_id": f"CORR_HUM_{i:03d}",
            "timestamp": date.isoformat(),
            "case_classification": "confirmed",
            "case_count": max(0, cases),
            "severity": "moderate" if cases > 2 else "mild"
        })
    
    # Generate environmental data
    environmental_data = []
    for i, temp in enumerate(temperature_series):
        date = base_date + timedelta(days=i)
        
        environmental_data.append({
            "record_id": f"CORR_ENV_{i:03d}",
            "timestamp": date.isoformat(),
            "parameter": "temperature",
            "value": temp
        })
        
        # Add humidity data (negatively correlated with temperature)
        humidity = 80 - (temp - 25) * 1.5 + random.uniform(-5, 5)
        environmental_data.append({
            "record_id": f"CORR_HUM_{i:03d}",
            "timestamp": date.isoformat(),
            "parameter": "humidity",
            "value": max(0, min(100, humidity))
        })
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of advanced correlation analysis."""
    print("📊 Advanced Correlation Analysis Engine - Demonstration")
    print("=" * 60)
    
    # Initialize engine
    engine = AdvancedCorrelationEngine()
    
    # Generate mock data with known correlations
    animal_data, human_data, env_data = generate_mock_correlation_data()
    
    print(f"\n📈 Correlation Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run comprehensive correlation analysis
    print(f"\n📊 Running Comprehensive Correlation Analysis...")
    results = engine.comprehensive_correlation_analysis(animal_data, human_data, env_data)
    
    # Display correlation results
    print(f"\n📈 Correlation Results ({len(results)} total):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.correlation_type.value.title()} Correlation")
        print(f"   Analysis ID: {result.analysis_id}")
        print(f"   Variables: {result.variable_1_name} ({result.variable_1_domain}) ↔ {result.variable_2_name} ({result.variable_2_domain})")
        print(f"   Correlation: {result.correlation_coefficient:.3f}")
        print(f"   Strength: {result.strength.value.upper()}")
        print(f"   Direction: {result.direction.value}")
        print(f"   P-value: {result.p_value:.3f}" if result.p_value else "")
        print(f"   Significant: {'Yes' if result.statistical_significance else 'No'}")
        print(f"   Sample Size: {result.sample_size}")
        
        if result.confidence_interval:
            ci_lower, ci_upper = result.confidence_interval
            print(f"   95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
        
        if result.lag_days is not None:
            print(f"   Optimal Lag: {result.lag_days} days")
        
        if result.window_size_days:
            print(f"   Window Size: {result.window_size_days} days")
        
        if result.effect_size:
            print(f"   Effect Size: {result.effect_size}")
        
        if result.recommended_followup:
            print(f"   Recommendations: {len(result.recommended_followup)}")
            for rec in result.recommended_followup:
                print(f"     • {rec}")
    
    # Correlation summary
    summary = engine.get_correlation_summary()
    print(f"\n📊 Correlation Summary:")
    print(f"  Total Correlations: {summary['total_correlations']}")
    print(f"  Significant Results: {summary['significant_correlations']}")
    print(f"  Strong Correlations: {summary['strong_correlations']}")
    
    if 'correlation_statistics' in summary:
        stats = summary['correlation_statistics']
        print(f"  Mean |Correlation|: {stats['mean_correlation']:.3f}")
        print(f"  Max |Correlation|: {stats['max_correlation']:.3f}")
    
    print(f"\n📋 By Correlation Type:")
    for ctype, count in summary['correlation_types'].items():
        print(f"  {ctype.title()}: {count}")
    
    print(f"\n💪 By Strength:")
    for strength, count in summary['strength_distribution'].items():
        if count > 0:
            print(f"  {strength.replace('_', ' ').title()}: {count}")
    
    print(f"\n🔗 By Domain Pairs:")
    for pair, count in summary['domain_pairs'].items():
        print(f"  {pair}: {count}")
    
    # Strongest correlations
    strongest = engine.get_strongest_correlations(3)
    if strongest:
        print(f"\n🏆 Strongest Correlations:")
        for i, result in enumerate(strongest, 1):
            print(f"  {i}. {result.variable_1_name} ↔ {result.variable_2_name}: {result.correlation_coefficient:.3f}")
            print(f"     Type: {result.correlation_type.value}, Strength: {result.strength.value}")
            if result.lag_days is not None:
                print(f"     Lag: {result.lag_days} days")
    
    print(f"\n⚡ Performance: {summary['analysis_performance']['average_duration']:.3f}s average")
    
    return engine

if __name__ == "__main__":
    engine = run_demonstration()
"""
Temporal Analysis System
========================
Module 3: Analysis & Modeling Tools

Advanced temporal analysis system for One Health surveillance, providing
time series analysis, trend detection, seasonality analysis, and temporal forecasting.

NIW Focus: Temporal intelligence revealing time-based disease patterns and trends.
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

class TemporalAnalysisType(Enum):
    """Types of temporal analysis."""
    TREND_ANALYSIS = "trend_analysis"           # Long-term trend detection
    SEASONALITY = "seasonality"                 # Seasonal pattern analysis
    PERIODICITY = "periodicity"                 # Periodic pattern detection
    ANOMALY_DETECTION = "anomaly_detection"     # Temporal anomaly detection
    CHANGEPOINT = "changepoint"                 # Change point detection
    FORECASTING = "forecasting"                 # Time series forecasting
    AUTOCORRELATION = "autocorrelation"         # Temporal autocorrelation

class TrendType(Enum):
    """Types of trends."""
    INCREASING = "increasing"                   # Upward trend
    DECREASING = "decreasing"                   # Downward trend
    STABLE = "stable"                          # No significant trend
    CYCLICAL = "cyclical"                      # Cyclical pattern
    VOLATILE = "volatile"                      # High variability
    EXPONENTIAL = "exponential"                # Exponential growth/decay

class SeasonalityType(Enum):
    """Types of seasonality."""
    WEEKLY = "weekly"                          # 7-day cycle
    MONTHLY = "monthly"                        # Monthly patterns
    QUARTERLY = "quarterly"                    # 3-month cycles
    ANNUAL = "annual"                          # Yearly patterns
    CUSTOM = "custom"                          # Custom period

class AnomalyType(Enum):
    """Types of temporal anomalies."""
    SPIKE = "spike"                            # Sudden increase
    DIP = "dip"                               # Sudden decrease
    SHIFT = "shift"                           # Level shift
    TREND_CHANGE = "trend_change"             # Trend direction change
    SEASONAL_SHIFT = "seasonal_shift"         # Seasonal pattern change

@dataclass
class TimePoint:
    """Represents a single time point with value."""
    timestamp: datetime
    value: float
    attributes: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.attributes is None:
            self.attributes = {}
        if self.weight is None:
            self.weight = 1.0

@dataclass
class TemporalTrend:
    """Represents a detected temporal trend."""
    trend_id: str
    trend_type: TrendType
    start_date: datetime
    end_date: datetime
    
    # Trend characteristics
    slope: float                               # Rate of change per day
    r_squared: float                          # Goodness of fit
    p_value: Optional[float] = None           # Statistical significance
    confidence_interval: Optional[Tuple[float, float]] = None
    
    # Trend magnitude
    total_change: Optional[float] = None      # Total change over period
    percent_change: Optional[float] = None    # Percentage change
    doubling_time_days: Optional[float] = None # For exponential trends
    
    # Statistical measures
    correlation_coefficient: Optional[float] = None
    standard_error: Optional[float] = None
    
    # Interpretation
    strength: str = "moderate"                # "weak", "moderate", "strong"
    significance: str = "moderate"            # Statistical significance level
    
    def __post_init__(self):
        """Calculate derived metrics."""
        if self.total_change is None and hasattr(self, '_start_value') and hasattr(self, '_end_value'):
            self.total_change = self._end_value - self._start_value
            
        if self.percent_change is None and hasattr(self, '_start_value') and self._start_value > 0:
            self.percent_change = (self.total_change / self._start_value) * 100
            
        # Classify strength based on R-squared
        if self.r_squared >= 0.8:
            self.strength = "strong"
        elif self.r_squared >= 0.5:
            self.strength = "moderate"
        else:
            self.strength = "weak"

@dataclass
class SeasonalPattern:
    """Represents a detected seasonal pattern."""
    pattern_id: str
    seasonality_type: SeasonalityType
    period_days: int
    amplitude: float                          # Peak-to-trough difference
    phase_offset_days: Optional[int] = None   # Phase offset from reference
    
    # Pattern statistics
    autocorrelation: Optional[float] = None   # Lag autocorrelation
    periodogram_power: Optional[float] = None # Spectral power
    pattern_strength: str = "moderate"        # "weak", "moderate", "strong"
    
    # Pattern details
    peak_dates: List[datetime] = None
    trough_dates: List[datetime] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.peak_dates is None:
            self.peak_dates = []
        if self.trough_dates is None:
            self.trough_dates = []

@dataclass
class TemporalAnomaly:
    """Represents a detected temporal anomaly."""
    anomaly_id: str
    anomaly_type: AnomalyType
    detection_date: datetime
    
    # Anomaly characteristics
    magnitude: float                          # How far from expected
    z_score: Optional[float] = None          # Standardized magnitude
    p_value: Optional[float] = None          # Probability of occurrence
    
    # Anomaly context
    expected_value: Optional[float] = None    # Expected value
    observed_value: float = 0.0              # Actual observed value
    confidence_level: float = 0.95           # Detection confidence
    
    # Duration and impact
    duration_days: Optional[int] = None       # How long anomaly lasted
    recovery_days: Optional[int] = None       # Time to return to normal
    
    # Severity classification
    severity: str = "moderate"                # "mild", "moderate", "severe", "critical"

@dataclass
class TemporalAnalysisResult:
    """Result of temporal analysis."""
    
    analysis_id: str
    analysis_type: TemporalAnalysisType
    analysis_timestamp: datetime
    
    # Data characteristics
    data_points: int
    time_span_days: int
    data_frequency: str                       # "daily", "weekly", "monthly"
    data_period_start: datetime
    data_period_end: datetime
    
    # Analysis results
    trends_detected: List[TemporalTrend]
    seasonal_patterns: List[SeasonalPattern]
    anomalies_detected: List[TemporalAnomaly]
    
    # Statistical measures
    temporal_autocorrelation: Optional[float] = None
    stationarity_test: Optional[str] = None   # "stationary", "non-stationary"
    noise_level: Optional[float] = None       # Signal-to-noise ratio
    
    # Forecasting results
    forecast_values: Optional[List[Tuple[datetime, float]]] = None
    forecast_confidence: Optional[List[Tuple[datetime, float, float]]] = None
    
    # Performance metrics
    analysis_duration_seconds: float = 0.0
    model_accuracy: Optional[float] = None    # For forecasting models
    
    # Key insights
    dominant_pattern: Optional[str] = None    # Primary pattern type
    key_findings: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.key_findings is None:
            self.key_findings = []
        if self.recommendations is None:
            self.recommendations = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['analysis_type'] = self.analysis_type.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        data['data_period_start'] = self.data_period_start.isoformat()
        data['data_period_end'] = self.data_period_end.isoformat()
        
        # Convert trends
        data['trends_detected'] = [
            {
                'trend_id': t.trend_id,
                'trend_type': t.trend_type.value,
                'slope': t.slope,
                'r_squared': t.r_squared,
                'strength': t.strength,
                'start_date': t.start_date.isoformat(),
                'end_date': t.end_date.isoformat()
            }
            for t in self.trends_detected
        ]
        
        # Convert seasonal patterns
        data['seasonal_patterns'] = [
            {
                'pattern_id': p.pattern_id,
                'seasonality_type': p.seasonality_type.value,
                'period_days': p.period_days,
                'amplitude': p.amplitude,
                'pattern_strength': p.pattern_strength
            }
            for p in self.seasonal_patterns
        ]
        
        # Convert anomalies
        data['anomalies_detected'] = [
            {
                'anomaly_id': a.anomaly_id,
                'anomaly_type': a.anomaly_type.value,
                'detection_date': a.detection_date.isoformat(),
                'magnitude': a.magnitude,
                'severity': a.severity
            }
            for a in self.anomalies_detected
        ]
        
        return data

class TrendAnalyzer:
    """Analyzes temporal trends in time series data."""
    
    @staticmethod
    def detect_linear_trends(time_points: List[TimePoint], 
                           min_period_days: int = 7) -> List[TemporalTrend]:
        """Detect linear trends in time series."""
        
        if len(time_points) < min_period_days:
            return []
        
        # Sort by timestamp
        sorted_points = sorted(time_points, key=lambda p: p.timestamp)
        
        # Convert to numeric format for regression
        start_date = sorted_points[0].timestamp
        x_values = [(p.timestamp - start_date).days for p in sorted_points]
        y_values = [p.value for p in sorted_points]
        
        # Calculate linear regression
        slope, intercept, r_squared = TrendAnalyzer._linear_regression(x_values, y_values)
        
        # Calculate statistical significance
        n = len(sorted_points)
        if n > 2 and r_squared < 1.0:
            # Calculate t-statistic for slope
            y_pred = [slope * x + intercept for x in x_values]
            residuals = [y - y_pred[i] for i, y in enumerate(y_values)]
            mse = sum(r**2 for r in residuals) / (n - 2)
            
            x_mean = statistics.mean(x_values)
            ss_x = sum((x - x_mean)**2 for x in x_values)
            se_slope = math.sqrt(mse / ss_x) if ss_x > 0 else float('inf')
            
            t_stat = abs(slope / se_slope) if se_slope > 0 else 0
            p_value = TrendAnalyzer._t_test_p_value(t_stat, n - 2)
        else:
            p_value = 1.0
        
        # Determine trend type and strength
        if abs(slope) < 0.01:  # Minimal slope
            trend_type = TrendType.STABLE
        elif slope > 0:
            # Check for exponential growth pattern
            if TrendAnalyzer._is_exponential_growth(y_values):
                trend_type = TrendType.EXPONENTIAL
            else:
                trend_type = TrendType.INCREASING
        else:
            if TrendAnalyzer._is_exponential_decay(y_values):
                trend_type = TrendType.EXPONENTIAL
            else:
                trend_type = TrendType.DECREASING
        
        # Calculate additional metrics
        start_value = y_values[0]
        end_value = y_values[-1]
        total_change = end_value - start_value
        percent_change = (total_change / start_value * 100) if start_value != 0 else 0
        
        # Calculate doubling time for exponential trends
        doubling_time = None
        if trend_type == TrendType.EXPONENTIAL and slope > 0:
            # Approximate doubling time
            daily_growth_rate = slope / statistics.mean(y_values) if statistics.mean(y_values) > 0 else 0
            if daily_growth_rate > 0:
                doubling_time = math.log(2) / daily_growth_rate
        
        trend = TemporalTrend(
            trend_id=f"TREND_{start_date.strftime('%Y%m%d')}",
            trend_type=trend_type,
            start_date=sorted_points[0].timestamp,
            end_date=sorted_points[-1].timestamp,
            slope=slope,
            r_squared=r_squared,
            p_value=p_value,
            total_change=total_change,
            percent_change=percent_change,
            doubling_time_days=doubling_time,
            correlation_coefficient=math.sqrt(r_squared) if slope >= 0 else -math.sqrt(r_squared)
        )
        
        # Set private attributes for post_init calculations
        trend._start_value = start_value
        trend._end_value = end_value
        
        return [trend] if r_squared > 0.1 else []  # Only return if meaningful trend
    
    @staticmethod
    def _linear_regression(x_values: List[float], y_values: List[float]) -> Tuple[float, float, float]:
        """Calculate linear regression parameters."""
        
        if len(x_values) != len(y_values) or len(x_values) == 0:
            return 0.0, 0.0, 0.0
        
        n = len(x_values)
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        # Calculate slope and intercept
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean)**2 for x in x_values)
        
        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = y_mean - slope * x_mean
        
        # Calculate R-squared
        y_pred = [slope * x + intercept for x in x_values]
        ss_res = sum((y - y_pred[i])**2 for i, y in enumerate(y_values))
        ss_tot = sum((y - y_mean)**2 for y in y_values)
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        return slope, intercept, max(0.0, r_squared)
    
    @staticmethod
    def _is_exponential_growth(values: List[float]) -> bool:
        """Check if data follows exponential growth pattern."""
        if len(values) < 5:
            return False
        
        # Test if log-transformed data is more linear
        positive_values = [v for v in values if v > 0]
        if len(positive_values) < len(values) * 0.8:  # Need mostly positive values
            return False
        
        try:
            log_values = [math.log(v) for v in positive_values]
            x_values = list(range(len(log_values)))
            
            _, _, r_squared_log = TrendAnalyzer._linear_regression(x_values, log_values)
            _, _, r_squared_linear = TrendAnalyzer._linear_regression(x_values, positive_values)
            
            # Exponential if log transformation improves linearity significantly
            return r_squared_log > r_squared_linear + 0.1
            
        except (ValueError, OverflowError):
            return False
    
    @staticmethod
    def _is_exponential_decay(values: List[float]) -> bool:
        """Check if data follows exponential decay pattern."""
        if len(values) < 5:
            return False
        
        # For decay, values should be decreasing and positive
        if not all(v > 0 for v in values):
            return False
        
        if values[0] <= values[-1]:  # Not decreasing overall
            return False
        
        return TrendAnalyzer._is_exponential_growth(values)
    
    @staticmethod
    def _t_test_p_value(t_stat: float, df: int) -> float:
        """Calculate approximate p-value for t-test."""
        abs_t = abs(t_stat)
        
        # Critical values for common significance levels
        if df >= 30:
            if abs_t > 2.576:
                return 0.01
            elif abs_t > 1.96:
                return 0.05
            elif abs_t > 1.64:
                return 0.10
        else:
            # Adjust for smaller degrees of freedom
            critical_05 = 2.0 + (2.5 - 2.0) * max(0, (30 - df) / 30)
            critical_01 = 2.5 + (3.0 - 2.5) * max(0, (30 - df) / 30)
            
            if abs_t > critical_01:
                return 0.01
            elif abs_t > critical_05:
                return 0.05
        
        return 0.20

class SeasonalityAnalyzer:
    """Analyzes seasonal patterns in time series data."""
    
    @staticmethod
    def detect_seasonal_patterns(time_points: List[TimePoint], 
                                max_period_days: int = 365) -> List[SeasonalPattern]:
        """Detect seasonal patterns using autocorrelation."""
        
        if len(time_points) < 14:  # Need minimum data
            return []
        
        sorted_points = sorted(time_points, key=lambda p: p.timestamp)
        values = [p.value for p in sorted_points]
        
        patterns = []
        
        # Test common periods
        test_periods = [7, 14, 30, 90, 365]  # Weekly, bi-weekly, monthly, quarterly, annual
        test_periods = [p for p in test_periods if p <= max_period_days and p < len(values)]
        
        for period in test_periods:
            autocorr = SeasonalityAnalyzer._calculate_autocorrelation(values, period)
            
            if autocorr > 0.3:  # Significant autocorrelation threshold
                # Calculate amplitude
                amplitude = SeasonalityAnalyzer._calculate_seasonal_amplitude(values, period)
                
                # Determine seasonality type
                if period == 7:
                    seasonality_type = SeasonalityType.WEEKLY
                elif period <= 31:
                    seasonality_type = SeasonalityType.MONTHLY
                elif period <= 100:
                    seasonality_type = SeasonalityType.QUARTERLY
                elif period >= 300:
                    seasonality_type = SeasonalityType.ANNUAL
                else:
                    seasonality_type = SeasonalityType.CUSTOM
                
                # Find peaks and troughs
                peaks, troughs = SeasonalityAnalyzer._find_peaks_troughs(sorted_points, period)
                
                # Classify pattern strength
                if autocorr >= 0.7:
                    strength = "strong"
                elif autocorr >= 0.5:
                    strength = "moderate"
                else:
                    strength = "weak"
                
                pattern = SeasonalPattern(
                    pattern_id=f"SEASONAL_{period}DAY",
                    seasonality_type=seasonality_type,
                    period_days=period,
                    amplitude=amplitude,
                    autocorrelation=autocorr,
                    pattern_strength=strength,
                    peak_dates=peaks,
                    trough_dates=troughs
                )
                
                patterns.append(pattern)
        
        # Sort by autocorrelation strength
        return sorted(patterns, key=lambda p: p.autocorrelation or 0, reverse=True)
    
    @staticmethod
    def _calculate_autocorrelation(values: List[float], lag: int) -> float:
        """Calculate autocorrelation at specified lag."""
        
        if lag >= len(values) or lag <= 0:
            return 0.0
        
        n = len(values) - lag
        if n <= 1:
            return 0.0
        
        # Calculate autocorrelation
        x = values[:-lag]
        y = values[lag:]
        
        try:
            correlation = statistics.correlation(x, y)
            return correlation
        except statistics.StatisticsError:
            return 0.0
    
    @staticmethod
    def _calculate_seasonal_amplitude(values: List[float], period: int) -> float:
        """Calculate seasonal amplitude."""
        
        if period >= len(values):
            return 0.0
        
        # Group values by position within period
        groups = defaultdict(list)
        for i, value in enumerate(values):
            position = i % period
            groups[position].append(value)
        
        # Calculate mean for each position
        position_means = []
        for position in range(period):
            if position in groups and groups[position]:
                position_means.append(statistics.mean(groups[position]))
        
        if len(position_means) < 2:
            return 0.0
        
        # Amplitude is peak-to-trough difference
        return max(position_means) - min(position_means)
    
    @staticmethod
    def _find_peaks_troughs(time_points: List[TimePoint], period: int) -> Tuple[List[datetime], List[datetime]]:
        """Find peak and trough dates in seasonal pattern."""
        
        if period >= len(time_points):
            return [], []
        
        # Simple peak/trough detection using local maxima/minima
        values = [p.value for p in time_points]
        timestamps = [p.timestamp for p in time_points]
        
        peaks = []
        troughs = []
        
        # Look for local peaks and troughs
        for i in range(period, len(values) - period):
            window = values[i-period//2:i+period//2+1]
            
            if values[i] == max(window) and len(set(window)) > 1:  # Local maximum
                peaks.append(timestamps[i])
            elif values[i] == min(window) and len(set(window)) > 1:  # Local minimum
                troughs.append(timestamps[i])
        
        return peaks[:5], troughs[:5]  # Limit to first 5 of each

class AnomalyDetector:
    """Detects temporal anomalies in time series data."""
    
    @staticmethod
    def detect_statistical_anomalies(time_points: List[TimePoint],
                                   window_size: int = 14,
                                   z_threshold: float = 2.5) -> List[TemporalAnomaly]:
        """Detect anomalies using statistical methods."""
        
        if len(time_points) < window_size * 2:
            return []
        
        sorted_points = sorted(time_points, key=lambda p: p.timestamp)
        anomalies = []
        
        for i in range(window_size, len(sorted_points)):
            # Calculate baseline statistics from preceding window
            baseline_values = [p.value for p in sorted_points[i-window_size:i]]
            
            if len(baseline_values) < 3:
                continue
            
            baseline_mean = statistics.mean(baseline_values)
            baseline_std = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 1.0
            
            current_point = sorted_points[i]
            current_value = current_point.value
            
            # Calculate z-score
            z_score = (current_value - baseline_mean) / baseline_std if baseline_std > 0 else 0
            
            if abs(z_score) > z_threshold:
                # Determine anomaly type
                if z_score > z_threshold:
                    anomaly_type = AnomalyType.SPIKE
                else:
                    anomaly_type = AnomalyType.DIP
                
                # Calculate severity
                if abs(z_score) >= 4.0:
                    severity = "critical"
                elif abs(z_score) >= 3.0:
                    severity = "severe"
                elif abs(z_score) >= 2.5:
                    severity = "moderate"
                else:
                    severity = "mild"
                
                # Calculate p-value (approximate)
                p_value = AnomalyDetector._z_score_to_p_value(abs(z_score))
                
                # Estimate duration and recovery
                duration_days, recovery_days = AnomalyDetector._estimate_anomaly_duration(
                    sorted_points, i, baseline_mean, baseline_std
                )
                
                anomaly = TemporalAnomaly(
                    anomaly_id=f"ANOMALY_{current_point.timestamp.strftime('%Y%m%d')}",
                    anomaly_type=anomaly_type,
                    detection_date=current_point.timestamp,
                    magnitude=abs(current_value - baseline_mean),
                    z_score=z_score,
                    p_value=p_value,
                    expected_value=baseline_mean,
                    observed_value=current_value,
                    duration_days=duration_days,
                    recovery_days=recovery_days,
                    severity=severity
                )
                
                anomalies.append(anomaly)
        
        return anomalies
    
    @staticmethod
    def detect_changepoints(time_points: List[TimePoint],
                          min_segment_length: int = 5) -> List[TemporalAnomaly]:
        """Detect change points in time series."""
        
        if len(time_points) < min_segment_length * 2:
            return []
        
        sorted_points = sorted(time_points, key=lambda p: p.timestamp)
        values = [p.value for p in sorted_points]
        changepoints = []
        
        for i in range(min_segment_length, len(values) - min_segment_length):
            # Test for significant change in mean
            before_segment = values[max(0, i-min_segment_length):i]
            after_segment = values[i:i+min_segment_length]
            
            if len(before_segment) >= 2 and len(after_segment) >= 2:
                before_mean = statistics.mean(before_segment)
                after_mean = statistics.mean(after_segment)
                before_std = statistics.stdev(before_segment)
                after_std = statistics.stdev(after_segment)
                
                # Pooled standard deviation
                pooled_std = math.sqrt((before_std**2 + after_std**2) / 2)
                
                if pooled_std > 0:
                    # Calculate effect size
                    effect_size = abs(after_mean - before_mean) / pooled_std
                    
                    if effect_size > 1.5:  # Large effect size threshold
                        # Determine change type
                        if after_mean > before_mean * 1.5:
                            anomaly_type = AnomalyType.SHIFT
                        elif after_mean < before_mean * 0.5:
                            anomaly_type = AnomalyType.SHIFT
                        else:
                            anomaly_type = AnomalyType.TREND_CHANGE
                        
                        changepoint = TemporalAnomaly(
                            anomaly_id=f"CHANGEPOINT_{sorted_points[i].timestamp.strftime('%Y%m%d')}",
                            anomaly_type=anomaly_type,
                            detection_date=sorted_points[i].timestamp,
                            magnitude=abs(after_mean - before_mean),
                            expected_value=before_mean,
                            observed_value=after_mean,
                            severity="moderate" if effect_size < 2.0 else "severe"
                        )
                        
                        changepoints.append(changepoint)
        
        return changepoints
    
    @staticmethod
    def _z_score_to_p_value(z_score: float) -> float:
        """Convert z-score to approximate p-value."""
        if z_score >= 4.0:
            return 0.0001
        elif z_score >= 3.0:
            return 0.001
        elif z_score >= 2.58:
            return 0.01
        elif z_score >= 1.96:
            return 0.05
        else:
            return 0.10
    
    @staticmethod
    def _estimate_anomaly_duration(time_points: List[TimePoint], anomaly_index: int,
                                 baseline_mean: float, baseline_std: float) -> Tuple[int, int]:
        """Estimate anomaly duration and recovery time."""
        
        duration = 1
        recovery = None
        
        # Look forward to see how long anomaly persists
        for i in range(anomaly_index + 1, len(time_points)):
            value = time_points[i].value
            z_score = abs(value - baseline_mean) / baseline_std if baseline_std > 0 else 0
            
            if z_score > 1.5:  # Still anomalous
                duration += 1
            else:
                # Returned to normal
                recovery = i - anomaly_index
                break
        
        return duration, recovery

class OneHealthTemporalAnalyzer:
    """Main temporal analyzer for One Health surveillance."""
    
    def __init__(self):
        self.analysis_results: List[TemporalAnalysisResult] = []
        self.analysis_log: List[Dict] = []
        
        logger.info("One Health Temporal Analyzer initialized")
    
    def comprehensive_temporal_analysis(self, animal_data: List[Dict],
                                      human_data: List[Dict],
                                      environmental_data: List[Dict]) -> List[TemporalAnalysisResult]:
        """Perform comprehensive temporal analysis across all domains."""
        
        analysis_start = datetime.now()
        results = []
        
        logger.info(f"Starting comprehensive temporal analysis")
        
        # Convert data to time points for each domain
        domain_time_series = {
            "animal": self._extract_time_points(animal_data, "animal"),
            "human": self._extract_time_points(human_data, "human"),
            "environmental": self._extract_time_points(environmental_data, "environmental")
        }
        
        # Analyze each domain
        for domain, time_points in domain_time_series.items():
            if len(time_points) >= 7:  # Minimum for meaningful analysis
                try:
                    result = self._analyze_domain_temporal_patterns(time_points, domain)
                    if result:
                        results.append(result)
                        
                except Exception as e:
                    logger.error(f"Error in {domain} temporal analysis: {e}")
        
        # Combined analysis across all domains
        all_time_points = []
        for time_points in domain_time_series.values():
            all_time_points.extend(time_points)
        
        if len(all_time_points) >= 10:
            try:
                combined_result = self._analyze_domain_temporal_patterns(all_time_points, "integrated")
                if combined_result:
                    results.append(combined_result)
                    
            except Exception as e:
                logger.error(f"Error in integrated temporal analysis: {e}")
        
        # Store results
        self.analysis_results.extend(results)
        
        # Log performance
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "analyses_completed": len(results),
            "total_points_analyzed": len(all_time_points),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            }
        })
        
        logger.info(f"Temporal analysis completed: {len(results)} analyses in {analysis_time:.2f}s")
        
        return results
    
    def _extract_time_points(self, data: List[Dict], domain: str) -> List[TimePoint]:
        """Extract time points from surveillance data."""
        
        time_points = []
        
        for record in data:
            timestamp_str = record.get('timestamp')
            if not timestamp_str:
                continue
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str[:19])
            except ValueError:
                continue
            
            # Extract value based on domain
            if domain == "animal":
                value = record.get('mortality_count', record.get('morbidity_count', 0))
                weight = value if value > 0 else 1.0
            elif domain == "human":
                value = record.get('case_count', 1)
                
                # Adjust value based on severity
                severity = record.get('severity', '').lower()
                if severity == 'critical':
                    value *= 4
                elif severity == 'severe':
                    value *= 2.5
                elif severity == 'moderate':
                    value *= 1.5
                    
                weight = value
            elif domain == "environmental":
                value = record.get('value', record.get('total_collected', 0))
                weight = 1.0
            else:
                value = 1.0
                weight = 1.0
            
            if isinstance(value, (int, float)) and value >= 0:
                time_point = TimePoint(
                    timestamp=timestamp,
                    value=float(value),
                    attributes=record,
                    weight=float(weight)
                )
                
                time_points.append(time_point)
        
        # Sort by timestamp
        return sorted(time_points, key=lambda p: p.timestamp)
    
    def _analyze_domain_temporal_patterns(self, time_points: List[TimePoint], 
                                        domain: str) -> Optional[TemporalAnalysisResult]:
        """Analyze temporal patterns for a specific domain."""
        
        if len(time_points) < 5:
            return None
        
        analysis_start = datetime.now()
        
        # Trend analysis
        trends = TrendAnalyzer.detect_linear_trends(time_points)
        
        # Seasonality analysis
        seasonal_patterns = SeasonalityAnalyzer.detect_seasonal_patterns(time_points)
        
        # Anomaly detection
        anomalies_statistical = AnomalyDetector.detect_statistical_anomalies(time_points)
        changepoints = AnomalyDetector.detect_changepoints(time_points)
        all_anomalies = anomalies_statistical + changepoints
        
        # Calculate autocorrelation
        values = [p.value for p in time_points]
        autocorr = self._calculate_temporal_autocorrelation(values)
        
        # Determine data characteristics
        timestamps = [p.timestamp for p in time_points]
        time_span = (max(timestamps) - min(timestamps)).days
        
        # Estimate data frequency
        if len(timestamps) > 1:
            intervals = [(timestamps[i+1] - timestamps[i]).days for i in range(len(timestamps)-1)]
            avg_interval = statistics.mean([i for i in intervals if i > 0]) if intervals else 1
            
            if avg_interval <= 1.5:
                data_frequency = "daily"
            elif avg_interval <= 8:
                data_frequency = "weekly"
            elif avg_interval <= 32:
                data_frequency = "monthly"
            else:
                data_frequency = "irregular"
        else:
            data_frequency = "single"
        
        # Determine dominant pattern
        dominant_pattern = None
        if trends and trends[0].strength == "strong":
            dominant_pattern = f"{trends[0].trend_type.value} trend"
        elif seasonal_patterns and seasonal_patterns[0].pattern_strength == "strong":
            dominant_pattern = f"{seasonal_patterns[0].seasonality_type.value} seasonality"
        elif len(all_anomalies) > len(time_points) * 0.1:  # >10% anomalies
            dominant_pattern = "highly variable"
        else:
            dominant_pattern = "stable"
        
        # Generate key findings
        key_findings = []
        
        if trends:
            strong_trends = [t for t in trends if t.strength == "strong"]
            if strong_trends:
                trend = strong_trends[0]
                direction = "increasing" if trend.slope > 0 else "decreasing"
                key_findings.append(f"Strong {direction} trend detected (R² = {trend.r_squared:.3f})")
                
                if trend.percent_change:
                    key_findings.append(f"Total change: {trend.percent_change:.1f}% over {time_span} days")
        
        if seasonal_patterns:
            strong_seasonal = [p for p in seasonal_patterns if p.pattern_strength == "strong"]
            if strong_seasonal:
                pattern = strong_seasonal[0]
                key_findings.append(f"Strong {pattern.seasonality_type.value} seasonality ({pattern.period_days} days)")
        
        if all_anomalies:
            severe_anomalies = [a for a in all_anomalies if a.severity in ["severe", "critical"]]
            key_findings.append(f"Detected {len(all_anomalies)} anomalies ({len(severe_anomalies)} severe)")
        else:
            severe_anomalies = []
        
        if autocorr and abs(autocorr) > 0.5:
            autocorr_type = "positive" if autocorr > 0 else "negative"
            key_findings.append(f"Strong {autocorr_type} autocorrelation ({autocorr:.3f})")
        
        # Generate recommendations
        recommendations = []
        
        if trends and any(t.trend_type == TrendType.EXPONENTIAL for t in trends):
            recommendations.append("Monitor for exponential growth - consider early intervention")
        
        if len(severe_anomalies) > 0:
            recommendations.append("Investigate recent anomalies for outbreak signals")
        
        if seasonal_patterns:
            recommendations.append("Adjust surveillance intensity for seasonal patterns")
        
        if dominant_pattern == "highly variable":
            recommendations.append("Increase data collection frequency due to high variability")
        
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        
        result = TemporalAnalysisResult(
            analysis_id=f"TEMPORAL_{domain.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=TemporalAnalysisType.TREND_ANALYSIS,
            analysis_timestamp=analysis_start,
            data_points=len(time_points),
            time_span_days=time_span,
            data_frequency=data_frequency,
            data_period_start=min(timestamps),
            data_period_end=max(timestamps),
            trends_detected=trends,
            seasonal_patterns=seasonal_patterns,
            anomalies_detected=all_anomalies,
            temporal_autocorrelation=autocorr,
            stationarity_test="non-stationary" if trends else "stationary",
            noise_level=statistics.stdev(values) / statistics.mean(values) if statistics.mean(values) > 0 else 0,
            analysis_duration_seconds=analysis_duration,
            dominant_pattern=dominant_pattern,
            key_findings=key_findings,
            recommendations=recommendations
        )
        
        return result
    
    def _calculate_temporal_autocorrelation(self, values: List[float], lag: int = 1) -> Optional[float]:
        """Calculate temporal autocorrelation."""
        
        if len(values) <= lag:
            return None
        
        x = values[:-lag]
        y = values[lag:]
        
        try:
            return statistics.correlation(x, y)
        except statistics.StatisticsError:
            return None
    
    def get_temporal_summary(self) -> Dict:
        """Get summary of temporal analysis results."""
        
        if not self.analysis_results:
            return {"message": "No temporal analyses performed"}
        
        # Aggregate statistics
        total_trends = sum(len(r.trends_detected) for r in self.analysis_results)
        total_seasonal = sum(len(r.seasonal_patterns) for r in self.analysis_results)
        total_anomalies = sum(len(r.anomalies_detected) for r in self.analysis_results)
        total_points = sum(r.data_points for r in self.analysis_results)
        
        # Pattern distribution
        dominant_patterns = defaultdict(int)
        for result in self.analysis_results:
            if result.dominant_pattern:
                dominant_patterns[result.dominant_pattern] += 1
        
        # Trend types
        trend_types = defaultdict(int)
        for result in self.analysis_results:
            for trend in result.trends_detected:
                trend_types[trend.trend_type.value] += 1
        
        # Performance statistics
        analysis_times = [r.analysis_duration_seconds for r in self.analysis_results]
        
        return {
            "total_analyses": len(self.analysis_results),
            "total_data_points": total_points,
            "total_trends_detected": total_trends,
            "total_seasonal_patterns": total_seasonal,
            "total_anomalies_detected": total_anomalies,
            "dominant_patterns": dict(dominant_patterns),
            "trend_types": dict(trend_types),
            "performance": {
                "average_analysis_time": statistics.mean(analysis_times) if analysis_times else 0,
                "total_analysis_time": sum(analysis_times)
            }
        }
    
    def get_critical_findings(self) -> List[Dict]:
        """Get critical temporal findings requiring attention."""
        
        critical_findings = []
        
        for result in self.analysis_results:
            # Critical trends
            for trend in result.trends_detected:
                if trend.trend_type == TrendType.EXPONENTIAL and trend.r_squared > 0.8:
                    critical_findings.append({
                        'type': 'exponential_trend',
                        'domain': result.analysis_id.split('_')[1].lower(),
                        'description': f"Exponential {trend.trend_type.value} with R² = {trend.r_squared:.3f}",
                        'urgency': 'high',
                        'doubling_time_days': trend.doubling_time_days
                    })
            
            # Critical anomalies
            for anomaly in result.anomalies_detected:
                if anomaly.severity == "critical":
                    critical_findings.append({
                        'type': 'critical_anomaly',
                        'domain': result.analysis_id.split('_')[1].lower(),
                        'description': f"{anomaly.anomaly_type.value} on {anomaly.detection_date.date()}",
                        'magnitude': anomaly.magnitude,
                        'urgency': 'immediate'
                    })
        
        return sorted(critical_findings, key=lambda f: f.get('urgency') == 'immediate', reverse=True)

# Mock data generator
def generate_mock_temporal_data():
    """Generate mock temporal data for testing."""
    
    base_date = datetime.now() - timedelta(days=60)
    
    # Generate animal data with seasonal pattern and trend
    animal_data = []
    for i in range(60):
        date = base_date + timedelta(days=i)
        
        # Base trend (increasing)
        trend_value = 2 + (i * 0.05)
        
        # Weekly seasonal pattern
        seasonal_factor = 1 + 0.3 * math.sin(2 * math.pi * i / 7)
        
        # Add some noise
        noise = random.uniform(-0.5, 0.5)
        
        # Add occasional spikes (anomalies)
        spike = 0
        if i in [15, 35, 48]:  # Specific days with anomalies
            spike = random.uniform(5, 10)
        
        mortality_count = max(1, int(trend_value * seasonal_factor + noise + spike))
        
        animal_data.append({
            "animal_id": f"TEMPORAL_FARM_{i:03d}",
            "timestamp": date.isoformat(),
            "species": "poultry",
            "mortality_count": mortality_count,
            "morbidity_count": mortality_count * 2
        })
    
    # Generate human data with different pattern
    human_data = []
    for i in range(50):  # Shorter time series
        date = base_date + timedelta(days=i+5)
        
        # Exponential growth pattern
        expo_value = 1.5 * (1.03 ** i)  # 3% daily growth
        
        # Add noise
        noise = random.uniform(-0.2, 0.2)
        
        case_count = max(1, int(expo_value + noise))
        
        # Add severity variation
        severity_options = ["mild", "moderate", "severe"]
        severity_weights = [0.6, 0.3, 0.1]
        severity = random.choices(severity_options, weights=severity_weights)[0]
        
        human_data.append({
            "case_id": f"TEMPORAL_HUM_{i:03d}",
            "timestamp": date.isoformat(),
            "case_classification": "confirmed",
            "case_count": case_count,
            "severity": severity
        })
    
    # Generate environmental data with different patterns
    environmental_data = []
    for i in range(60):
        date = base_date + timedelta(days=i)
        
        # Temperature with annual cycle
        temp_base = 25
        annual_cycle = 5 * math.sin(2 * math.pi * i / 365)
        daily_variation = random.uniform(-2, 2)
        
        temperature = temp_base + annual_cycle + daily_variation
        
        environmental_data.append({
            "record_id": f"TEMPORAL_ENV_{i:03d}",
            "timestamp": date.isoformat(),
            "parameter": "temperature",
            "value": temperature
        })
        
        # Humidity (inverse relationship with temperature)
        humidity = 80 - (temperature - 25) * 1.2 + random.uniform(-3, 3)
        humidity = max(0, min(100, humidity))
        
        environmental_data.append({
            "record_id": f"TEMPORAL_HUM_{i:03d}",
            "timestamp": date.isoformat(),
            "parameter": "humidity",
            "value": humidity
        })
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of temporal analysis system."""
    print("📅 One Health Temporal Analysis System - Demonstration")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OneHealthTemporalAnalyzer()
    
    # Generate mock temporal data
    animal_data, human_data, env_data = generate_mock_temporal_data()
    
    print(f"\n📈 Temporal Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run comprehensive temporal analysis
    print(f"\n📅 Running Comprehensive Temporal Analysis...")
    results = analyzer.comprehensive_temporal_analysis(animal_data, human_data, env_data)
    
    # Display temporal analysis results
    print(f"\n📊 Temporal Analysis Results ({len(results)} total):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Temporal Analysis - {result.analysis_id}")
        print(f"   Data Points: {result.data_points}")
        print(f"   Time Span: {result.time_span_days} days")
        print(f"   Data Frequency: {result.data_frequency}")
        print(f"   Dominant Pattern: {result.dominant_pattern}")
        
        if result.temporal_autocorrelation:
            print(f"   Autocorrelation: {result.temporal_autocorrelation:.3f}")
        
        if result.noise_level:
            print(f"   Noise Level: {result.noise_level:.3f}")
        
        print(f"   Trends Detected: {len(result.trends_detected)}")
        
        # Show trend details
        for j, trend in enumerate(result.trends_detected[:2], 1):  # Top 2
            print(f"     {j}. {trend.trend_type.value.title()} Trend")
            print(f"        Slope: {trend.slope:.4f} units/day")
            print(f"        R²: {trend.r_squared:.3f}")
            print(f"        Strength: {trend.strength}")
            if trend.percent_change:
                print(f"        Total Change: {trend.percent_change:.1f}%")
            if trend.doubling_time_days:
                print(f"        Doubling Time: {trend.doubling_time_days:.1f} days")
        
        print(f"   Seasonal Patterns: {len(result.seasonal_patterns)}")
        
        # Show seasonal details
        for j, pattern in enumerate(result.seasonal_patterns[:2], 1):  # Top 2
            print(f"     {j}. {pattern.seasonality_type.value.title()} Pattern")
            print(f"        Period: {pattern.period_days} days")
            print(f"        Amplitude: {pattern.amplitude:.2f}")
            print(f"        Strength: {pattern.pattern_strength}")
            if pattern.autocorrelation:
                print(f"        Autocorrelation: {pattern.autocorrelation:.3f}")
        
        print(f"   Anomalies Detected: {len(result.anomalies_detected)}")
        
        # Show anomaly details
        for j, anomaly in enumerate(result.anomalies_detected[:3], 1):  # Top 3
            print(f"     {j}. {anomaly.anomaly_type.value.title()} Anomaly")
            print(f"        Date: {anomaly.detection_date.date()}")
            print(f"        Severity: {anomaly.severity}")
            print(f"        Magnitude: {anomaly.magnitude:.2f}")
            if anomaly.z_score:
                print(f"        Z-Score: {anomaly.z_score:.2f}")
        
        print(f"   Analysis Duration: {result.analysis_duration_seconds:.3f}s")
        
        if result.key_findings:
            print(f"   Key Findings ({len(result.key_findings)}):")
            for finding in result.key_findings:
                print(f"     • {finding}")
        
        if result.recommendations:
            print(f"   Recommendations ({len(result.recommendations)}):")
            for rec in result.recommendations:
                print(f"     • {rec}")
    
    # Temporal analysis summary
    summary = analyzer.get_temporal_summary()
    print(f"\n📊 Temporal Analysis Summary:")
    if "message" in summary:
        print(f"  {summary['message']}")
    else:
        print(f"  Total Analyses: {summary['total_analyses']}")
        print(f"  Total Data Points: {summary['total_data_points']}")
        print(f"  Trends Detected: {summary['total_trends_detected']}")
        print(f"  Seasonal Patterns: {summary['total_seasonal_patterns']}")
        print(f"  Anomalies Detected: {summary['total_anomalies_detected']}")
        
        if summary['dominant_patterns']:
            print(f"\n📈 Dominant Patterns:")
            for pattern, count in summary['dominant_patterns'].items():
                print(f"  {pattern.title()}: {count}")
        
        if summary['trend_types']:
            print(f"\n📊 Trend Types:")
            for trend_type, count in summary['trend_types'].items():
                print(f"  {trend_type.title()}: {count}")
        
        print(f"\n⚡ Performance:")
        perf = summary['performance']
        print(f"  Average Analysis Time: {perf['average_analysis_time']:.3f}s")
        print(f"  Total Analysis Time: {perf['total_analysis_time']:.3f}s")
    
    # Critical findings
    critical_findings = analyzer.get_critical_findings()
    if critical_findings:
        print(f"\n🚨 CRITICAL Findings ({len(critical_findings)}):")
        for i, finding in enumerate(critical_findings[:5], 1):  # Top 5
            print(f"  {i}. {finding['type'].replace('_', ' ').title()} ({finding['domain']})")
            print(f"     Description: {finding['description']}")
            print(f"     Urgency: {finding['urgency'].upper()}")
            if 'doubling_time_days' in finding:
                print(f"     Doubling Time: {finding['doubling_time_days']:.1f} days")
    
    return analyzer

if __name__ == "__main__":
    analyzer = run_demonstration()
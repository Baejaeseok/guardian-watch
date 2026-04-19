"""
Pattern Recognition System
==========================
Module 2: Essential Epidemiologic Tools

Advanced pattern recognition and anomaly detection system for One Health surveillance,
identifying unusual patterns, trends, and outbreaks across temporal and spatial dimensions.

NIW Focus: Intelligent pattern recognition enabling early detection of emerging threats.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PatternType(Enum):
    """Types of patterns that can be detected."""
    TREND = "trend"                    # Increasing/decreasing trend
    SEASONAL = "seasonal"              # Seasonal/cyclical patterns
    OUTBREAK = "outbreak"              # Sudden surge in cases
    ANOMALY = "anomaly"               # Statistical outliers
    CLUSTERING = "clustering"          # Spatial clustering
    PERIODICITY = "periodicity"        # Regular cycles
    CHANGEPOINT = "changepoint"        # Sudden changes
    CORRELATION = "correlation"        # Inter-variable patterns

class AnomalyType(Enum):
    """Types of anomalies that can be detected."""
    SPIKE = "spike"                   # Sudden increase
    DROP = "drop"                     # Sudden decrease
    PLATEAU = "plateau"               # Sustained high level
    OSCILLATION = "oscillation"       # Unusual oscillations
    DRIFT = "drift"                   # Gradual shift
    MISSING = "missing"               # Missing data patterns

class PatternSeverity(Enum):
    """Severity levels for detected patterns."""
    LOW = "low"                       # Minor deviation
    MODERATE = "moderate"             # Notable deviation
    HIGH = "high"                     # Significant deviation
    CRITICAL = "critical"             # Extreme deviation

@dataclass
class PatternDetection:
    """Result of pattern detection analysis."""
    
    pattern_id: str
    pattern_type: PatternType
    anomaly_type: Optional[AnomalyType] = None
    severity: PatternSeverity = PatternSeverity.LOW
    
    # Temporal information
    detection_date: datetime = None
    pattern_start: Optional[datetime] = None
    pattern_end: Optional[datetime] = None
    duration_days: Optional[int] = None
    
    # Spatial information
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    affected_area_km: Optional[float] = None
    
    # Statistical measures
    baseline_value: Optional[float] = None
    observed_value: Optional[float] = None
    deviation_score: Optional[float] = None  # Z-score or similar
    confidence_score: float = 0.0            # 0-1 confidence in detection
    
    # Pattern characteristics
    amplitude: Optional[float] = None         # Magnitude of pattern
    frequency: Optional[float] = None         # Frequency (for periodic patterns)
    trend_slope: Optional[float] = None       # Slope (for trend patterns)
    
    # Context information
    data_domain: str = "unknown"             # "animal", "human", "environmental"
    affected_variables: List[str] = None
    related_patterns: List[str] = None       # IDs of related patterns
    
    # Interpretation
    description: str = ""
    risk_assessment: str = "unknown"         # "low", "moderate", "high", "critical"
    recommended_actions: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.detection_date is None:
            self.detection_date = datetime.now()
        if self.affected_variables is None:
            self.affected_variables = []
        if self.related_patterns is None:
            self.related_patterns = []
        if self.recommended_actions is None:
            self.recommended_actions = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['pattern_type'] = self.pattern_type.value
        data['severity'] = self.severity.value
        data['detection_date'] = self.detection_date.isoformat()
        
        if self.anomaly_type:
            data['anomaly_type'] = self.anomaly_type.value
        if self.pattern_start:
            data['pattern_start'] = self.pattern_start.isoformat()
        if self.pattern_end:
            data['pattern_end'] = self.pattern_end.isoformat()
            
        return data

class TimeSeriesPatternDetector:
    """Detects patterns in time series health data."""
    
    @staticmethod
    def detect_trend_patterns(time_series: List[Tuple[datetime, float]], 
                            window_size: int = 7) -> List[PatternDetection]:
        """Detect trend patterns in time series data."""
        
        if len(time_series) < window_size * 2:
            return []
        
        patterns = []
        
        # Calculate moving averages and slopes
        moving_slopes = []
        for i in range(len(time_series) - window_size + 1):
            window_data = time_series[i:i + window_size]
            
            # Convert dates to numeric values for slope calculation
            x_values = [(dt - time_series[0][0]).days for dt, _ in window_data]
            y_values = [val for _, val in window_data]
            
            if len(set(x_values)) > 1:  # Avoid division by zero
                slope = TimeSeriesPatternDetector._calculate_slope(x_values, y_values)
                moving_slopes.append((window_data[-1][0], slope))
        
        # Detect significant trends
        if moving_slopes:
            slope_values = [slope for _, slope in moving_slopes]
            slope_mean = statistics.mean(slope_values)
            slope_stdev = statistics.stdev(slope_values) if len(slope_values) > 1 else 0
            
            for timestamp, slope in moving_slopes:
                if slope_stdev > 0:
                    z_score = abs((slope - slope_mean) / slope_stdev)
                    
                    if z_score > 2.0:  # Significant trend
                        severity = PatternSeverity.HIGH if z_score > 3.0 else PatternSeverity.MODERATE
                        
                        pattern = PatternDetection(
                            pattern_id=f"TREND_{timestamp.strftime('%Y%m%d_%H%M')}",
                            pattern_type=PatternType.TREND,
                            severity=severity,
                            pattern_start=timestamp - timedelta(days=window_size),
                            pattern_end=timestamp,
                            duration_days=window_size,
                            trend_slope=slope,
                            deviation_score=z_score,
                            confidence_score=min(z_score / 4.0, 1.0),
                            description=f"{'Increasing' if slope > 0 else 'Decreasing'} trend detected",
                            affected_variables=["time_series_value"]
                        )
                        
                        patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def detect_outbreak_patterns(time_series: List[Tuple[datetime, float]],
                               baseline_days: int = 14) -> List[PatternDetection]:
        """Detect outbreak patterns (sudden spikes)."""
        
        if len(time_series) < baseline_days + 3:
            return []
        
        patterns = []
        
        # Calculate baseline statistics
        baseline_values = [val for _, val in time_series[:baseline_days]]
        baseline_mean = statistics.mean(baseline_values)
        baseline_stdev = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 1
        
        # Check subsequent values for spikes
        for i in range(baseline_days, len(time_series)):
            timestamp, value = time_series[i]
            
            # Calculate Z-score relative to baseline
            z_score = (value - baseline_mean) / baseline_stdev if baseline_stdev > 0 else 0
            
            if z_score > 2.5:  # Significant spike
                severity = PatternSeverity.CRITICAL if z_score > 4.0 else \
                          PatternSeverity.HIGH if z_score > 3.0 else PatternSeverity.MODERATE
                
                # Determine outbreak duration
                outbreak_end = timestamp
                for j in range(i + 1, len(time_series)):
                    future_timestamp, future_value = time_series[j]
                    future_z = (future_value - baseline_mean) / baseline_stdev
                    
                    if future_z <= 1.5:  # Back to normal
                        break
                    outbreak_end = future_timestamp
                
                pattern = PatternDetection(
                    pattern_id=f"OUTBREAK_{timestamp.strftime('%Y%m%d_%H%M')}",
                    pattern_type=PatternType.OUTBREAK,
                    anomaly_type=AnomalyType.SPIKE,
                    severity=severity,
                    pattern_start=timestamp,
                    pattern_end=outbreak_end,
                    duration_days=(outbreak_end - timestamp).days + 1,
                    baseline_value=baseline_mean,
                    observed_value=value,
                    deviation_score=z_score,
                    confidence_score=min(z_score / 5.0, 1.0),
                    amplitude=value - baseline_mean,
                    description=f"Outbreak spike: {value:.1f} vs baseline {baseline_mean:.1f}",
                    risk_assessment="high" if z_score > 3.0 else "moderate",
                    affected_variables=["case_count"],
                    recommended_actions=TimeSeriesPatternDetector._get_outbreak_recommendations(severity)
                )
                
                patterns.append(pattern)
                
                # Update baseline to include recent data (adaptive)
                if i >= baseline_days + 7:  # After some new data
                    recent_normal = [val for _, val in time_series[i-7:i] if 
                                   abs((val - baseline_mean) / baseline_stdev) < 1.5]
                    if recent_normal:
                        baseline_values.extend(recent_normal)
                        baseline_mean = statistics.mean(baseline_values[-baseline_days:])
                        baseline_stdev = statistics.stdev(baseline_values[-baseline_days:])
        
        return patterns
    
    @staticmethod
    def detect_seasonal_patterns(time_series: List[Tuple[datetime, float]],
                               cycle_length: int = 7) -> List[PatternDetection]:
        """Detect seasonal/cyclical patterns."""
        
        if len(time_series) < cycle_length * 3:  # Need at least 3 cycles
            return []
        
        patterns = []
        
        # Group data by cycle position (e.g., day of week)
        cycle_groups = defaultdict(list)
        for timestamp, value in time_series:
            cycle_pos = timestamp.weekday() if cycle_length == 7 else timestamp.day % cycle_length
            cycle_groups[cycle_pos].append(value)
        
        # Calculate cycle statistics
        cycle_means = {}
        cycle_stdevs = {}
        
        for cycle_pos, values in cycle_groups.items():
            if len(values) >= 2:
                cycle_means[cycle_pos] = statistics.mean(values)
                cycle_stdevs[cycle_pos] = statistics.stdev(values)
        
        if len(cycle_means) < cycle_length:
            return []
        
        # Check for significant cyclical variation
        all_means = list(cycle_means.values())
        mean_variation = statistics.stdev(all_means) if len(all_means) > 1 else 0
        overall_mean = statistics.mean(all_means)
        
        if mean_variation > overall_mean * 0.2:  # 20% variation threshold
            # Find peak and trough days
            max_day = max(cycle_means.keys(), key=lambda k: cycle_means[k])
            min_day = min(cycle_means.keys(), key=lambda k: cycle_means[k])
            
            amplitude = cycle_means[max_day] - cycle_means[min_day]
            frequency = 1.0 / cycle_length  # Cycles per day
            
            pattern = PatternDetection(
                pattern_id=f"SEASONAL_{cycle_length}DAY",
                pattern_type=PatternType.SEASONAL,
                severity=PatternSeverity.MODERATE,
                pattern_start=time_series[0][0],
                pattern_end=time_series[-1][0],
                duration_days=(time_series[-1][0] - time_series[0][0]).days,
                amplitude=amplitude,
                frequency=frequency,
                confidence_score=min(mean_variation / (overall_mean + 1), 1.0),
                description=f"{cycle_length}-day cyclical pattern detected",
                affected_variables=["time_series_value"]
            )
            
            patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def detect_changepoint_patterns(time_series: List[Tuple[datetime, float]],
                                  min_segment_length: int = 5) -> List[PatternDetection]:
        """Detect sudden change points in time series."""
        
        if len(time_series) < min_segment_length * 2:
            return []
        
        patterns = []
        values = [val for _, val in time_series]
        
        # Simple changepoint detection using sliding window variance
        for i in range(min_segment_length, len(time_series) - min_segment_length):
            
            before_segment = values[max(0, i - min_segment_length):i]
            after_segment = values[i:i + min_segment_length]
            
            if len(before_segment) >= 2 and len(after_segment) >= 2:
                before_mean = statistics.mean(before_segment)
                after_mean = statistics.mean(after_segment)
                before_stdev = statistics.stdev(before_segment)
                after_stdev = statistics.stdev(after_segment)
                
                # Test for significant change in mean
                pooled_stdev = math.sqrt((before_stdev**2 + after_stdev**2) / 2)
                if pooled_stdev > 0:
                    t_stat = abs(after_mean - before_mean) / pooled_stdev
                    
                    if t_stat > 2.0:  # Significant change
                        severity = PatternSeverity.HIGH if t_stat > 3.0 else PatternSeverity.MODERATE
                        
                        pattern = PatternDetection(
                            pattern_id=f"CHANGEPOINT_{time_series[i][0].strftime('%Y%m%d')}",
                            pattern_type=PatternType.CHANGEPOINT,
                            severity=severity,
                            pattern_start=time_series[i][0],
                            baseline_value=before_mean,
                            observed_value=after_mean,
                            deviation_score=t_stat,
                            confidence_score=min(t_stat / 4.0, 1.0),
                            description=f"Change point: {before_mean:.1f} → {after_mean:.1f}",
                            affected_variables=["time_series_value"]
                        )
                        
                        patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def _calculate_slope(x_values: List[float], y_values: List[float]) -> float:
        """Calculate linear regression slope."""
        n = len(x_values)
        if n == 0:
            return 0.0
        
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        return numerator / denominator if denominator != 0 else 0.0
    
    @staticmethod
    def _get_outbreak_recommendations(severity: PatternSeverity) -> List[str]:
        """Get recommendations based on outbreak severity."""
        if severity == PatternSeverity.CRITICAL:
            return [
                "Activate emergency response protocols",
                "Implement immediate control measures",
                "Notify public health authorities",
                "Enhance active surveillance"
            ]
        elif severity == PatternSeverity.HIGH:
            return [
                "Investigate outbreak source",
                "Increase surveillance frequency", 
                "Prepare response resources",
                "Alert healthcare facilities"
            ]
        else:
            return [
                "Monitor closely",
                "Verify data quality",
                "Review surveillance protocols"
            ]

class SpatialPatternDetector:
    """Detects spatial patterns in geographic health data."""
    
    @staticmethod
    def detect_spatial_clusters(events: List[Dict],
                              cluster_radius_km: float = 25,
                              min_cluster_size: int = 3) -> List[PatternDetection]:
        """Detect spatial clustering patterns."""
        
        if len(events) < min_cluster_size:
            return []
        
        # Extract coordinates
        locations = []
        for event in events:
            if event.get('location_lat') and event.get('location_lon'):
                locations.append({
                    'lat': event['location_lat'],
                    'lon': event['location_lon'],
                    'timestamp': event.get('timestamp'),
                    'value': event.get('case_count', event.get('mortality_count', 1))
                })
        
        if len(locations) < min_cluster_size:
            return []
        
        patterns = []
        used_locations = set()
        
        # Find clusters using simple distance-based clustering
        for i, location in enumerate(locations):
            if i in used_locations:
                continue
            
            cluster_locations = [location]
            cluster_indices = {i}
            
            for j, other_location in enumerate(locations):
                if j <= i or j in used_locations:
                    continue
                
                distance = SpatialPatternDetector._calculate_distance(
                    location['lat'], location['lon'],
                    other_location['lat'], other_location['lon']
                )
                
                if distance <= cluster_radius_km:
                    cluster_locations.append(other_location)
                    cluster_indices.add(j)
            
            # Create pattern if cluster is significant
            if len(cluster_locations) >= min_cluster_size:
                center_lat = statistics.mean([loc['lat'] for loc in cluster_locations])
                center_lon = statistics.mean([loc['lon'] for loc in cluster_locations])
                
                total_cases = sum(loc['value'] for loc in cluster_locations)
                
                # Calculate cluster density
                max_distance = max(
                    SpatialPatternDetector._calculate_distance(
                        center_lat, center_lon, loc['lat'], loc['lon']
                    ) for loc in cluster_locations
                )
                
                pattern = PatternDetection(
                    pattern_id=f"SPATIAL_CLUSTER_{len(patterns) + 1}",
                    pattern_type=PatternType.CLUSTERING,
                    severity=PatternSeverity.HIGH if len(cluster_locations) >= 5 else PatternSeverity.MODERATE,
                    location_lat=center_lat,
                    location_lon=center_lon,
                    affected_area_km=max_distance,
                    observed_value=total_cases,
                    confidence_score=min(len(cluster_locations) / 10.0, 1.0),
                    description=f"Spatial cluster: {len(cluster_locations)} events in {max_distance:.1f}km",
                    affected_variables=["geographic_location"],
                    data_domain="spatial"
                )
                
                patterns.append(pattern)
                used_locations.update(cluster_indices)
        
        return patterns
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers."""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c

class AnomalyDetector:
    """Detects various types of anomalies in health data."""
    
    @staticmethod
    def detect_statistical_anomalies(data: List[float],
                                    z_threshold: float = 2.5) -> List[PatternDetection]:
        """Detect statistical outliers using Z-score method."""
        
        if len(data) < 3:
            return []
        
        patterns = []
        
        mean_val = statistics.mean(data)
        stdev_val = statistics.stdev(data) if len(data) > 1 else 0
        
        if stdev_val == 0:
            return []
        
        for i, value in enumerate(data):
            z_score = abs((value - mean_val) / stdev_val)
            
            if z_score > z_threshold:
                severity = PatternSeverity.CRITICAL if z_score > 4.0 else \
                          PatternSeverity.HIGH if z_score > 3.0 else PatternSeverity.MODERATE
                
                anomaly_type = AnomalyType.SPIKE if value > mean_val else AnomalyType.DROP
                
                pattern = PatternDetection(
                    pattern_id=f"ANOMALY_{i}_{datetime.now().strftime('%H%M%S')}",
                    pattern_type=PatternType.ANOMALY,
                    anomaly_type=anomaly_type,
                    severity=severity,
                    baseline_value=mean_val,
                    observed_value=value,
                    deviation_score=z_score,
                    confidence_score=min(z_score / 5.0, 1.0),
                    description=f"Statistical outlier: {value:.1f} (Z={z_score:.2f})",
                    affected_variables=["measurement_value"]
                )
                
                patterns.append(pattern)
        
        return patterns
    
    @staticmethod
    def detect_missing_data_patterns(timestamps: List[datetime],
                                   expected_interval_hours: int = 24) -> List[PatternDetection]:
        """Detect patterns in missing data."""
        
        if len(timestamps) < 2:
            return []
        
        patterns = []
        timestamps.sort()
        
        expected_interval = timedelta(hours=expected_interval_hours)
        tolerance = timedelta(hours=expected_interval_hours * 0.5)  # 50% tolerance
        
        gap_start = None
        
        for i in range(1, len(timestamps)):
            current_gap = timestamps[i] - timestamps[i-1]
            
            if current_gap > expected_interval + tolerance:
                # Found a gap
                if gap_start is None:
                    gap_start = timestamps[i-1]
                
                # Check if this is the end of the gap
                if i == len(timestamps) - 1 or \
                   timestamps[i+1] - timestamps[i] <= expected_interval + tolerance:
                    
                    gap_duration = timestamps[i] - gap_start
                    
                    severity = PatternSeverity.CRITICAL if gap_duration.days > 7 else \
                              PatternSeverity.HIGH if gap_duration.days > 3 else PatternSeverity.MODERATE
                    
                    pattern = PatternDetection(
                        pattern_id=f"MISSING_DATA_{gap_start.strftime('%Y%m%d')}",
                        pattern_type=PatternType.ANOMALY,
                        anomaly_type=AnomalyType.MISSING,
                        severity=severity,
                        pattern_start=gap_start,
                        pattern_end=timestamps[i],
                        duration_days=gap_duration.days,
                        description=f"Data gap: {gap_duration.days} days missing",
                        affected_variables=["data_availability"]
                    )
                    
                    patterns.append(pattern)
                    gap_start = None
            else:
                gap_start = None
        
        return patterns

class OneHealthPatternRecognizer:
    """Main pattern recognition system for One Health surveillance."""
    
    def __init__(self):
        self.detected_patterns: List[PatternDetection] = []
        self.pattern_history: List[Dict] = []
        
        logger.info("One Health Pattern Recognizer initialized")
    
    def analyze_patterns(self, animal_data: List[Dict],
                        human_data: List[Dict],
                        environmental_data: List[Dict]) -> List[PatternDetection]:
        """Comprehensive pattern analysis across all domains."""
        
        analysis_start = datetime.now()
        patterns = []
        
        logger.info(f"Starting pattern analysis with {len(animal_data)} animal, "
                   f"{len(human_data)} human, {len(environmental_data)} environmental records")
        
        # Convert data to time series
        animal_ts = self._extract_time_series(animal_data, 'mortality_count')
        human_ts = self._extract_time_series(human_data, 'case_count')
        env_ts = self._extract_time_series(environmental_data, 'value')
        
        # Time series pattern detection
        for domain_name, time_series in [
            ("animal", animal_ts),
            ("human", human_ts), 
            ("environmental", env_ts)
        ]:
            if len(time_series) >= 5:
                try:
                    # Trend patterns
                    trend_patterns = TimeSeriesPatternDetector.detect_trend_patterns(time_series)
                    for pattern in trend_patterns:
                        pattern.data_domain = domain_name
                    patterns.extend(trend_patterns)
                    
                    # Outbreak patterns
                    outbreak_patterns = TimeSeriesPatternDetector.detect_outbreak_patterns(time_series)
                    for pattern in outbreak_patterns:
                        pattern.data_domain = domain_name
                    patterns.extend(outbreak_patterns)
                    
                    # Seasonal patterns
                    seasonal_patterns = TimeSeriesPatternDetector.detect_seasonal_patterns(time_series)
                    for pattern in seasonal_patterns:
                        pattern.data_domain = domain_name
                    patterns.extend(seasonal_patterns)
                    
                    # Change point patterns
                    changepoint_patterns = TimeSeriesPatternDetector.detect_changepoint_patterns(time_series)
                    for pattern in changepoint_patterns:
                        pattern.data_domain = domain_name
                    patterns.extend(changepoint_patterns)
                    
                except Exception as e:
                    logger.error(f"Error in time series analysis for {domain_name}: {e}")
        
        # Spatial pattern detection
        try:
            all_spatial_data = animal_data + human_data + environmental_data
            spatial_patterns = SpatialPatternDetector.detect_spatial_clusters(all_spatial_data)
            patterns.extend(spatial_patterns)
            
        except Exception as e:
            logger.error(f"Error in spatial analysis: {e}")
        
        # Anomaly detection
        try:
            for domain_name, data_list in [
                ("animal", animal_data),
                ("human", human_data),
                ("environmental", environmental_data)
            ]:
                if data_list:
                    # Extract numeric values
                    values = []
                    timestamps = []
                    
                    for record in data_list:
                        value = record.get('mortality_count', 
                                         record.get('case_count',
                                                   record.get('value', 0)))
                        if isinstance(value, (int, float)):
                            values.append(float(value))
                        
                        timestamp_str = record.get('timestamp')
                        if timestamp_str:
                            try:
                                timestamps.append(datetime.fromisoformat(timestamp_str[:19]))
                            except ValueError:
                                pass
                    
                    # Statistical anomalies
                    if values:
                        anomaly_patterns = AnomalyDetector.detect_statistical_anomalies(values)
                        for pattern in anomaly_patterns:
                            pattern.data_domain = domain_name
                        patterns.extend(anomaly_patterns)
                    
                    # Missing data patterns
                    if timestamps:
                        missing_patterns = AnomalyDetector.detect_missing_data_patterns(timestamps)
                        for pattern in missing_patterns:
                            pattern.data_domain = domain_name
                        patterns.extend(missing_patterns)
                        
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
        
        # Store patterns
        self.detected_patterns.extend(patterns)
        
        # Cross-reference related patterns
        self._identify_related_patterns(patterns)
        
        # Log analysis
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.pattern_history.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "patterns_detected": len(patterns),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            }
        })
        
        logger.info(f"Pattern analysis completed: {len(patterns)} patterns detected in {analysis_time:.2f}s")
        
        return patterns
    
    def _extract_time_series(self, data: List[Dict], value_field: str) -> List[Tuple[datetime, float]]:
        """Extract time series from data."""
        time_series = []
        
        for record in data:
            timestamp_str = record.get('timestamp')
            value = record.get(value_field, 0)
            
            if timestamp_str and isinstance(value, (int, float)):
                try:
                    timestamp = datetime.fromisoformat(timestamp_str[:19])
                    time_series.append((timestamp, float(value)))
                except ValueError:
                    continue
        
        # Sort by timestamp
        time_series.sort(key=lambda x: x[0])
        
        return time_series
    
    def _identify_related_patterns(self, patterns: List[PatternDetection]):
        """Identify relationships between detected patterns."""
        
        for i, pattern1 in enumerate(patterns):
            for j, pattern2 in enumerate(patterns[i+1:], i+1):
                
                # Check temporal overlap
                temporal_overlap = self._check_temporal_overlap(pattern1, pattern2)
                
                # Check spatial proximity
                spatial_proximity = self._check_spatial_proximity(pattern1, pattern2)
                
                # Check domain correlation
                domain_correlation = self._check_domain_correlation(pattern1, pattern2)
                
                if temporal_overlap or spatial_proximity or domain_correlation:
                    pattern1.related_patterns.append(pattern2.pattern_id)
                    pattern2.related_patterns.append(pattern1.pattern_id)
    
    def _check_temporal_overlap(self, pattern1: PatternDetection, 
                               pattern2: PatternDetection) -> bool:
        """Check if two patterns overlap in time."""
        if not (pattern1.pattern_start and pattern1.pattern_end and 
                pattern2.pattern_start and pattern2.pattern_end):
            return False
        
        # Check for any temporal overlap
        return not (pattern1.pattern_end < pattern2.pattern_start or 
                   pattern2.pattern_end < pattern1.pattern_start)
    
    def _check_spatial_proximity(self, pattern1: PatternDetection,
                                pattern2: PatternDetection,
                                max_distance_km: float = 50) -> bool:
        """Check if two patterns are spatially close."""
        if not (pattern1.location_lat and pattern1.location_lon and
                pattern2.location_lat and pattern2.location_lon):
            return False
        
        distance = SpatialPatternDetector._calculate_distance(
            pattern1.location_lat, pattern1.location_lon,
            pattern2.location_lat, pattern2.location_lon
        )
        
        return distance <= max_distance_km
    
    def _check_domain_correlation(self, pattern1: PatternDetection,
                                 pattern2: PatternDetection) -> bool:
        """Check if patterns are in related domains."""
        related_domains = [
            {"animal", "human"},
            {"human", "environmental"},
            {"animal", "environmental"}
        ]
        
        pattern_domains = {pattern1.data_domain, pattern2.data_domain}
        
        return any(pattern_domains == domain_pair for domain_pair in related_domains)
    
    def get_pattern_summary(self) -> Dict:
        """Get summary of detected patterns."""
        
        if not self.detected_patterns:
            return {"message": "No patterns detected"}
        
        # Group by pattern type
        by_type = defaultdict(list)
        by_severity = defaultdict(list)
        by_domain = defaultdict(list)
        
        for pattern in self.detected_patterns:
            by_type[pattern.pattern_type.value].append(pattern)
            by_severity[pattern.severity.value].append(pattern)
            by_domain[pattern.data_domain].append(pattern)
        
        # Recent patterns (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_patterns = [p for p in self.detected_patterns 
                          if p.detection_date >= recent_cutoff]
        
        # High priority patterns
        high_priority = [p for p in self.detected_patterns 
                        if p.severity in [PatternSeverity.HIGH, PatternSeverity.CRITICAL]]
        
        return {
            "total_patterns": len(self.detected_patterns),
            "recent_patterns_24h": len(recent_patterns),
            "high_priority_patterns": len(high_priority),
            "patterns_by_type": {ptype: len(patterns) for ptype, patterns in by_type.items()},
            "patterns_by_severity": {severity: len(patterns) for severity, patterns in by_severity.items()},
            "patterns_by_domain": {domain: len(patterns) for domain, patterns in by_domain.items()},
            "analysis_performance": {
                "total_analyses": len(self.pattern_history),
                "average_analysis_time": statistics.mean([
                    h["analysis_duration"] for h in self.pattern_history
                ]) if self.pattern_history else 0
            }
        }
    
    def get_critical_patterns(self) -> List[PatternDetection]:
        """Get all critical severity patterns."""
        return [p for p in self.detected_patterns 
                if p.severity == PatternSeverity.CRITICAL]

# Mock data generator
def generate_mock_pattern_data():
    """Generate mock data with embedded patterns for testing."""
    
    # Generate animal data with outbreak pattern
    animal_data = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Normal baseline: 1-3 cases
        baseline_cases = random.randint(1, 3)
        
        # Add outbreak spike around day 15-20
        if 15 <= i <= 20:
            outbreak_cases = baseline_cases + random.randint(8, 15)
        else:
            outbreak_cases = baseline_cases
        
        animal_data.append({
            "animal_id": f"FARM_{i:03d}",
            "timestamp": date.isoformat(),
            "location_lat": 40.7128 + random.uniform(-0.1, 0.1),
            "location_lon": -74.0060 + random.uniform(-0.1, 0.1),
            "species": "poultry",
            "mortality_count": outbreak_cases
        })
    
    # Generate human data with related pattern
    human_data = []
    for i in range(25):
        date = base_date + timedelta(days=i+2)  # Lag behind animal cases
        
        # Baseline cases
        baseline = random.randint(0, 2)
        
        # Related human cases after animal outbreak
        if 17 <= i <= 22:  # 2-day lag
            cases = baseline + random.randint(2, 6)
        else:
            cases = baseline
        
        if cases > 0:
            human_data.append({
                "case_id": f"HUM_{i:03d}",
                "timestamp": date.isoformat(),
                "location_lat": 40.7128 + random.uniform(-0.15, 0.15),
                "location_lon": -74.0060 + random.uniform(-0.15, 0.15),
                "case_classification": "confirmed",
                "case_count": cases
            })
    
    # Generate environmental data with seasonal pattern
    environmental_data = []
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Seasonal temperature pattern
        seasonal_temp = 20 + 10 * math.sin(2 * math.pi * i / 30) + random.uniform(-2, 2)
        
        environmental_data.append({
            "record_id": f"ENV_{i:03d}",
            "timestamp": date.isoformat(),
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "parameter": "temperature",
            "value": seasonal_temp
        })
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of pattern recognition system."""
    print("🔍 One Health Pattern Recognition System - Demonstration")
    print("=" * 60)
    
    # Initialize recognizer
    recognizer = OneHealthPatternRecognizer()
    
    # Generate mock data with embedded patterns
    animal_data, human_data, env_data = generate_mock_pattern_data()
    
    print(f"\n📊 Pattern Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run pattern analysis
    print(f"\n🔍 Running Comprehensive Pattern Analysis...")
    patterns = recognizer.analyze_patterns(animal_data, human_data, env_data)
    
    # Display detected patterns
    print(f"\n📈 Detected Patterns ({len(patterns)} total):")
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\n{i}. {pattern.pattern_type.value.title()} Pattern")
        print(f"   Pattern ID: {pattern.pattern_id}")
        print(f"   Domain: {pattern.data_domain}")
        print(f"   Severity: {pattern.severity.value.upper()}")
        print(f"   Confidence: {pattern.confidence_score:.2f}")
        
        if pattern.anomaly_type:
            print(f"   Anomaly Type: {pattern.anomaly_type.value}")
        
        if pattern.pattern_start and pattern.pattern_end:
            print(f"   Duration: {pattern.duration_days} days")
        
        if pattern.baseline_value and pattern.observed_value:
            print(f"   Values: {pattern.baseline_value:.1f} → {pattern.observed_value:.1f}")
        
        if pattern.deviation_score:
            print(f"   Deviation Score: {pattern.deviation_score:.2f}")
        
        if pattern.description:
            print(f"   Description: {pattern.description}")
        
        if pattern.related_patterns:
            print(f"   Related Patterns: {len(pattern.related_patterns)}")
        
        if pattern.recommended_actions:
            print(f"   Recommendations: {len(pattern.recommended_actions)}")
    
    # Pattern summary
    summary = recognizer.get_pattern_summary()
    print(f"\n📊 Pattern Summary:")
    print(f"  Total Patterns: {summary['total_patterns']}")
    print(f"  Recent (24h): {summary['recent_patterns_24h']}")
    print(f"  High Priority: {summary['high_priority_patterns']}")
    
    print(f"\n📋 By Type:")
    for ptype, count in summary['patterns_by_type'].items():
        print(f"  {ptype.replace('_', ' ').title()}: {count}")
    
    print(f"\n⚠️ By Severity:")
    for severity, count in summary['patterns_by_severity'].items():
        print(f"  {severity.upper()}: {count}")
    
    print(f"\n🏥 By Domain:")
    for domain, count in summary['patterns_by_domain'].items():
        print(f"  {domain.title()}: {count}")
    
    # Critical patterns
    critical_patterns = recognizer.get_critical_patterns()
    if critical_patterns:
        print(f"\n🚨 Critical Patterns ({len(critical_patterns)}):")
        for pattern in critical_patterns:
            print(f"  - {pattern.pattern_type.value}: {pattern.description}")
    
    print(f"\n⚡ Performance: {summary['analysis_performance']['average_analysis_time']:.3f}s average")
    
    return recognizer

if __name__ == "__main__":
    recognizer = run_demonstration()
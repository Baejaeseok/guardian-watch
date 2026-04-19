"""
Outbreak Detection System
=========================
Module 2: Essential Epidemiologic Tools

Real-time outbreak detection and early warning system for One Health surveillance,
providing automated detection, classification, and alert generation for disease outbreaks.

NIW Focus: Rapid outbreak detection enabling immediate public health response.
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

class OutbreakPhase(Enum):
    """Phases of outbreak development."""
    BASELINE = "baseline"           # Normal background levels
    EARLY_SIGNALS = "early_signals" # Pre-outbreak indicators
    EMERGENCE = "emergence"         # Initial outbreak detection
    ESCALATION = "escalation"       # Rapid growth phase
    PEAK = "peak"                  # Maximum intensity
    DECLINE = "decline"            # Decreasing phase
    RESOLUTION = "resolution"       # Return to baseline

class OutbreakType(Enum):
    """Types of outbreaks by characteristics."""
    POINT_SOURCE = "point_source"   # Single exposure source
    COMMON_SOURCE = "common_source" # Shared exposure source
    PROPAGATED = "propagated"       # Person-to-person spread
    MIXED = "mixed"                # Multiple transmission modes
    ZOONOTIC = "zoonotic"          # Animal-to-human transmission
    VECTOR_BORNE = "vector_borne"   # Vector-mediated transmission

class AlertLevel(Enum):
    """Alert levels for outbreak notifications."""
    WATCH = "watch"                # Monitoring increased activity
    ADVISORY = "advisory"          # Elevated concern
    ALERT = "alert"                # Confirmed outbreak
    WARNING = "warning"            # Severe outbreak
    EMERGENCY = "emergency"        # Public health emergency

class OutbreakSeverity(Enum):
    """Severity classification for outbreaks."""
    MILD = "mild"                  # Limited impact
    MODERATE = "moderate"          # Moderate impact
    SEVERE = "severe"              # Significant impact
    CRITICAL = "critical"          # Extreme impact

@dataclass
class OutbreakDetection:
    """Result of outbreak detection analysis."""
    
    detection_id: str
    detection_timestamp: datetime
    
    # Outbreak characteristics
    outbreak_phase: OutbreakPhase
    outbreak_type: Optional[OutbreakType] = None
    severity: OutbreakSeverity = OutbreakSeverity.MILD
    alert_level: AlertLevel = AlertLevel.WATCH
    
    # Temporal information
    outbreak_start: Optional[datetime] = None
    estimated_duration_days: Optional[int] = None
    time_to_peak_days: Optional[int] = None
    
    # Geographic information
    center_lat: Optional[float] = None
    center_lon: Optional[float] = None
    affected_radius_km: Optional[float] = None
    affected_locations: List[str] = None
    
    # Epidemiological measures
    case_count: int = 0
    attack_rate: Optional[float] = None      # % of population affected
    growth_rate: Optional[float] = None      # Daily growth rate
    doubling_time_days: Optional[float] = None
    reproduction_number: Optional[float] = None
    
    # Detection statistics
    baseline_threshold: float = 0.0
    observed_value: float = 0.0
    excess_cases: int = 0
    statistical_significance: float = 0.0    # p-value
    detection_confidence: float = 0.0        # 0-1 confidence score
    
    # Context information
    pathogen: Optional[str] = None
    affected_species: List[str] = None
    data_sources: List[str] = None
    
    # Response information
    investigation_priority: str = "routine"   # "routine", "urgent", "immediate"
    recommended_actions: List[str] = None
    notification_recipients: List[str] = None
    
    # Tracking
    related_detections: List[str] = None     # Related outbreak detection IDs
    update_frequency_hours: int = 24         # How often to update
    
    def __post_init__(self):
        """Initialize default values."""
        if self.affected_locations is None:
            self.affected_locations = []
        if self.affected_species is None:
            self.affected_species = []
        if self.data_sources is None:
            self.data_sources = []
        if self.recommended_actions is None:
            self.recommended_actions = []
        if self.notification_recipients is None:
            self.notification_recipients = []
        if self.related_detections is None:
            self.related_detections = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['detection_timestamp'] = self.detection_timestamp.isoformat()
        data['outbreak_phase'] = self.outbreak_phase.value
        data['severity'] = self.severity.value
        data['alert_level'] = self.alert_level.value
        
        if self.outbreak_type:
            data['outbreak_type'] = self.outbreak_type.value
        if self.outbreak_start:
            data['outbreak_start'] = self.outbreak_start.isoformat()
            
        return data

class StatisticalOutbreakDetector:
    """Statistical methods for outbreak detection."""
    
    @staticmethod
    def detect_aberration_cusum(time_series: List[Tuple[datetime, int]],
                               baseline_mean: float,
                               threshold_multiplier: float = 3.0) -> Optional[OutbreakDetection]:
        """Detect outbreaks using CUSUM (Cumulative Sum) method."""
        
        if len(time_series) < 5:
            return None
        
        # Calculate CUSUM statistics
        cusum_values = []
        cusum = 0
        
        for timestamp, count in time_series:
            # Expected count based on baseline
            expected = baseline_mean
            excess = count - expected
            
            # Update CUSUM (reset if negative)
            cusum = max(0, cusum + excess)
            cusum_values.append((timestamp, cusum))
        
        # Detect when CUSUM exceeds threshold
        threshold = threshold_multiplier * math.sqrt(baseline_mean)
        
        for i, (timestamp, cusum_val) in enumerate(cusum_values):
            if cusum_val > threshold:
                # Found outbreak signal
                
                # Determine outbreak start (when CUSUM started increasing)
                outbreak_start = timestamp
                for j in range(i-1, -1, -1):
                    if cusum_values[j][1] == 0:
                        break
                    outbreak_start = cusum_values[j][0]
                
                # Calculate outbreak characteristics
                outbreak_cases = sum(count for _, count in time_series[j+1:i+1])
                excess_cases = int(outbreak_cases - (baseline_mean * (i - j)))
                
                return OutbreakDetection(
                    detection_id=f"CUSUM_{timestamp.strftime('%Y%m%d_%H%M')}",
                    detection_timestamp=datetime.now(),
                    outbreak_phase=OutbreakPhase.EMERGENCE,
                    outbreak_start=outbreak_start,
                    case_count=outbreak_cases,
                    excess_cases=max(0, excess_cases),
                    baseline_threshold=threshold,
                    observed_value=cusum_val,
                    detection_confidence=min(cusum_val / (threshold * 2), 1.0),
                    alert_level=AlertLevel.ALERT,
                    severity=StatisticalOutbreakDetector._classify_severity(excess_cases),
                    recommended_actions=["Investigate outbreak source", "Enhance surveillance", "Notify authorities"]
                )
        
        return None
    
    @staticmethod
    def detect_aberration_ewma(time_series: List[Tuple[datetime, int]],
                              baseline_mean: float,
                              baseline_std: float,
                              smoothing_factor: float = 0.3) -> Optional[OutbreakDetection]:
        """Detect outbreaks using EWMA (Exponentially Weighted Moving Average)."""
        
        if len(time_series) < 3:
            return None
        
        ewma = baseline_mean
        if baseline_std == 0:
            baseline_std = 1.0  # Avoid division by zero
        threshold = baseline_mean + 3 * baseline_std
        
        for i, (timestamp, count) in enumerate(time_series):
            # Update EWMA
            ewma = smoothing_factor * count + (1 - smoothing_factor) * ewma
            
            if ewma > threshold:
                # Calculate outbreak characteristics
                recent_period = max(1, i - 7)  # Last week
                recent_cases = sum(count for _, count in time_series[recent_period:i+1])
                expected_cases = baseline_mean * (i - recent_period + 1)
                excess = recent_cases - expected_cases
                
                return OutbreakDetection(
                    detection_id=f"EWMA_{timestamp.strftime('%Y%m%d_%H%M')}",
                    detection_timestamp=datetime.now(),
                    outbreak_phase=OutbreakPhase.EMERGENCE,
                    outbreak_start=time_series[recent_period][0],
                    case_count=recent_cases,
                    excess_cases=int(max(0, excess)),
                    baseline_threshold=threshold,
                    observed_value=ewma,
                    detection_confidence=min((ewma - baseline_mean) / (3 * baseline_std), 1.0),
                    alert_level=AlertLevel.ADVISORY,
                    severity=StatisticalOutbreakDetector._classify_severity(int(excess))
                )
        
        return None
    
    @staticmethod
    def detect_serfling_method(time_series: List[Tuple[datetime, int]],
                              seasonal_baseline: Dict[int, float]) -> Optional[OutbreakDetection]:
        """Detect outbreaks using Serfling regression method (simplified)."""
        
        if len(time_series) < 4:
            return None
        
        current_timestamp, current_count = time_series[-1]
        current_week = current_timestamp.isocalendar()[1]
        
        # Get seasonal baseline for current week
        expected_count = seasonal_baseline.get(current_week, 
                                             statistics.mean(seasonal_baseline.values()))
        
        # Calculate threshold (baseline + 2 standard deviations)
        baseline_values = list(seasonal_baseline.values())
        baseline_std = statistics.stdev(baseline_values) if len(baseline_values) > 1 else 1
        threshold = expected_count + 2 * baseline_std
        
        if current_count > threshold:
            # Recent week analysis
            recent_cases = sum(count for _, count in time_series[-7:])
            expected_recent = expected_count * min(7, len(time_series))
            excess = recent_cases - expected_recent
            
            return OutbreakDetection(
                detection_id=f"SERFLING_{current_timestamp.strftime('%Y%m%d')}",
                detection_timestamp=datetime.now(),
                outbreak_phase=OutbreakPhase.EMERGENCE,
                outbreak_start=time_series[-7][0] if len(time_series) >= 7 else time_series[0][0],
                case_count=recent_cases,
                excess_cases=int(max(0, excess)),
                baseline_threshold=threshold,
                observed_value=current_count,
                detection_confidence=min((current_count - expected_count) / (2 * baseline_std), 1.0),
                alert_level=AlertLevel.ADVISORY,
                severity=StatisticalOutbreakDetector._classify_severity(int(excess))
            )
        
        return None
    
    @staticmethod
    def _classify_severity(excess_cases: int) -> OutbreakSeverity:
        """Classify outbreak severity based on excess cases."""
        if excess_cases >= 50:
            return OutbreakSeverity.CRITICAL
        elif excess_cases >= 20:
            return OutbreakSeverity.SEVERE
        elif excess_cases >= 5:
            return OutbreakSeverity.MODERATE
        else:
            return OutbreakSeverity.MILD

class SpatialOutbreakDetector:
    """Spatial methods for outbreak detection."""
    
    @staticmethod
    def detect_spatial_scan(events: List[Dict],
                          population_data: Dict[str, int],
                          max_cluster_radius_km: float = 50) -> List[OutbreakDetection]:
        """Detect spatial clusters using scan statistic approach."""
        
        if len(events) < 3:
            return []
        
        detections = []
        
        # Extract event locations
        locations = []
        for event in events:
            if event.get('location_lat') and event.get('location_lon'):
                locations.append({
                    'lat': event['location_lat'],
                    'lon': event['location_lon'],
                    'timestamp': event.get('timestamp'),
                    'cases': event.get('case_count', event.get('mortality_count', 1)),
                    'location_id': event.get('county', 'unknown')
                })
        
        if len(locations) < 3:
            return []
        
        # Test different cluster centers and radii
        for center_idx, center_location in enumerate(locations):
            for radius_km in [10, 25, 50]:
                if radius_km > max_cluster_radius_km:
                    continue
                
                # Find events within radius
                cluster_events = []
                total_cases = 0
                
                for location in locations:
                    distance = SpatialOutbreakDetector._calculate_distance(
                        center_location['lat'], center_location['lon'],
                        location['lat'], location['lon']
                    )
                    
                    if distance <= radius_km:
                        cluster_events.append(location)
                        total_cases += location['cases']
                
                if len(cluster_events) >= 3:  # Minimum cluster size
                    # Calculate expected cases based on population
                    cluster_locations = set(event['location_id'] for event in cluster_events)
                    cluster_population = sum(population_data.get(loc, 1000) for loc in cluster_locations)
                    
                    # Simple expected calculation (would use proper background rates in practice)
                    total_population = sum(population_data.values()) if population_data else len(locations) * 1000
                    expected_cases = (cluster_population / total_population) * sum(loc['cases'] for loc in locations)
                    
                    # Test for statistical significance (simplified likelihood ratio)
                    if total_cases > expected_cases * 1.5:  # 50% excess threshold
                        
                        detection = OutbreakDetection(
                            detection_id=f"SPATIAL_{center_idx}_{radius_km}km",
                            detection_timestamp=datetime.now(),
                            outbreak_phase=OutbreakPhase.EMERGENCE,
                            outbreak_type=OutbreakType.POINT_SOURCE,
                            center_lat=center_location['lat'],
                            center_lon=center_location['lon'],
                            affected_radius_km=radius_km,
                            case_count=total_cases,
                            excess_cases=int(total_cases - expected_cases),
                            observed_value=total_cases,
                            baseline_threshold=expected_cases * 1.5,
                            detection_confidence=min((total_cases / expected_cases - 1), 1.0),
                            alert_level=AlertLevel.ALERT,
                            severity=StatisticalOutbreakDetector._classify_severity(int(total_cases - expected_cases)),
                            affected_locations=list(cluster_locations),
                            recommended_actions=["Investigate common source", "Environmental assessment", "Contact tracing"]
                        )
                        
                        detections.append(detection)
        
        # Remove duplicate/overlapping detections (keep highest case count)
        unique_detections = []
        for detection in sorted(detections, key=lambda d: d.case_count, reverse=True):
            # Check for overlap with existing detections
            is_duplicate = False
            for existing in unique_detections:
                if SpatialOutbreakDetector._detections_overlap(detection, existing):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_detections.append(detection)
        
        return unique_detections
    
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
    
    @staticmethod
    def _detections_overlap(detection1: OutbreakDetection, detection2: OutbreakDetection) -> bool:
        """Check if two spatial detections overlap significantly."""
        if not (detection1.center_lat and detection1.center_lon and
                detection2.center_lat and detection2.center_lon):
            return False
        
        distance = SpatialOutbreakDetector._calculate_distance(
            detection1.center_lat, detection1.center_lon,
            detection2.center_lat, detection2.center_lon
        )
        
        # Overlap if centers are closer than combined radii
        combined_radius = (detection1.affected_radius_km or 0) + (detection2.affected_radius_km or 0)
        return distance < combined_radius * 0.7  # 70% overlap threshold

class OutbreakTracker:
    """Tracks and updates ongoing outbreak detections."""
    
    def __init__(self):
        self.active_outbreaks: Dict[str, OutbreakDetection] = {}
        self.outbreak_history: List[OutbreakDetection] = []
        
    def update_outbreak(self, outbreak_id: str, new_data: List[Dict]) -> OutbreakDetection:
        """Update an existing outbreak with new data."""
        
        if outbreak_id not in self.active_outbreaks:
            raise ValueError(f"Outbreak {outbreak_id} not found")
        
        outbreak = self.active_outbreaks[outbreak_id]
        
        # Calculate new metrics
        current_cases = sum(record.get('case_count', record.get('mortality_count', 1)) 
                           for record in new_data)
        
        # Update case count
        previous_cases = outbreak.case_count
        outbreak.case_count = current_cases
        outbreak.excess_cases = current_cases - int(outbreak.baseline_threshold)
        
        # Calculate growth rate
        if previous_cases > 0:
            days_elapsed = (datetime.now() - outbreak.detection_timestamp).days
            if days_elapsed > 0:
                outbreak.growth_rate = (current_cases / previous_cases) ** (1/days_elapsed) - 1
                
                # Calculate doubling time
                if outbreak.growth_rate > 0:
                    outbreak.doubling_time_days = math.log(2) / math.log(1 + outbreak.growth_rate)
        
        # Update severity and alert level based on current situation
        outbreak.severity = StatisticalOutbreakDetector._classify_severity(outbreak.excess_cases)
        outbreak.alert_level = self._determine_alert_level(outbreak)
        
        # Update phase
        outbreak.outbreak_phase = self._determine_outbreak_phase(outbreak, new_data)
        
        logger.info(f"Updated outbreak {outbreak_id}: {current_cases} cases, "
                   f"growth rate {outbreak.growth_rate:.3f}" if outbreak.growth_rate else "")
        
        return outbreak
    
    def resolve_outbreak(self, outbreak_id: str) -> OutbreakDetection:
        """Mark an outbreak as resolved."""
        
        if outbreak_id not in self.active_outbreaks:
            raise ValueError(f"Outbreak {outbreak_id} not found")
        
        outbreak = self.active_outbreaks.pop(outbreak_id)
        outbreak.outbreak_phase = OutbreakPhase.RESOLUTION
        outbreak.alert_level = AlertLevel.WATCH
        
        # Calculate total duration
        if outbreak.outbreak_start:
            duration = datetime.now() - outbreak.outbreak_start
            outbreak.estimated_duration_days = duration.days
        
        self.outbreak_history.append(outbreak)
        
        logger.info(f"Resolved outbreak {outbreak_id} after {outbreak.estimated_duration_days} days")
        
        return outbreak
    
    def _determine_alert_level(self, outbreak: OutbreakDetection) -> AlertLevel:
        """Determine appropriate alert level based on outbreak characteristics."""
        
        if outbreak.severity == OutbreakSeverity.CRITICAL:
            return AlertLevel.EMERGENCY
        elif outbreak.severity == OutbreakSeverity.SEVERE:
            return AlertLevel.WARNING
        elif outbreak.case_count > 20:
            return AlertLevel.ALERT
        elif outbreak.excess_cases > 5:
            return AlertLevel.ADVISORY
        else:
            return AlertLevel.WATCH
    
    def _determine_outbreak_phase(self, outbreak: OutbreakDetection, recent_data: List[Dict]) -> OutbreakPhase:
        """Determine current outbreak phase based on recent trends."""
        
        if outbreak.growth_rate is None:
            return OutbreakPhase.EMERGENCE
        
        if outbreak.growth_rate > 0.1:  # Growing > 10% per day
            return OutbreakPhase.ESCALATION
        elif outbreak.growth_rate > 0:  # Still growing slowly
            return OutbreakPhase.PEAK
        elif outbreak.growth_rate < -0.05:  # Declining > 5% per day
            return OutbreakPhase.DECLINE
        else:
            return OutbreakPhase.PEAK  # Stable at peak

class OneHealthOutbreakDetector:
    """Main outbreak detection system for One Health surveillance."""
    
    def __init__(self):
        self.outbreak_tracker = OutbreakTracker()
        self.detection_history: List[OutbreakDetection] = []
        self.baseline_data: Dict[str, Dict] = {
            "animal": {"mean": 2.0, "std": 1.5},
            "human": {"mean": 1.0, "std": 0.8},
            "environmental": {"mean": 5.0, "std": 2.0}
        }
        
        logger.info("One Health Outbreak Detection System initialized")
    
    def detect_outbreaks(self, animal_data: List[Dict],
                        human_data: List[Dict],
                        environmental_data: List[Dict]) -> List[OutbreakDetection]:
        """Comprehensive outbreak detection across all domains."""
        
        detection_start = datetime.now()
        detections = []
        
        logger.info(f"Starting outbreak detection with {len(animal_data)} animal, "
                   f"{len(human_data)} human, {len(environmental_data)} environmental records")
        
        # Time series detection for each domain
        for domain_name, data_list in [
            ("animal", animal_data),
            ("human", human_data),
            ("environmental", environmental_data)
        ]:
            if len(data_list) >= 5:
                try:
                    # Convert to time series
                    time_series = self._extract_time_series(data_list)
                    
                    if len(time_series) >= 5:
                        baseline = self.baseline_data[domain_name]
                        
                        # CUSUM detection
                        cusum_detection = StatisticalOutbreakDetector.detect_aberration_cusum(
                            time_series, baseline["mean"]
                        )
                        if cusum_detection:
                            cusum_detection.data_sources = [domain_name]
                            detections.append(cusum_detection)
                        
                        # EWMA detection
                        ewma_detection = StatisticalOutbreakDetector.detect_aberration_ewma(
                            time_series, baseline["mean"], baseline["std"]
                        )
                        if ewma_detection:
                            ewma_detection.data_sources = [domain_name]
                            detections.append(ewma_detection)
                        
                        # Seasonal detection (simplified)
                        seasonal_baseline = {week: baseline["mean"] for week in range(1, 53)}
                        seasonal_detection = StatisticalOutbreakDetector.detect_serfling_method(
                            time_series, seasonal_baseline
                        )
                        if seasonal_detection:
                            seasonal_detection.data_sources = [domain_name]
                            detections.append(seasonal_detection)
                            
                except Exception as e:
                    logger.error(f"Error in temporal detection for {domain_name}: {e}")
        
        # Spatial detection
        try:
            all_spatial_data = animal_data + human_data + environmental_data
            
            # Mock population data (would be real data in practice)
            population_data = {
                "New York": 8000000,
                "Los Angeles": 4000000,
                "Chicago": 2700000,
                "Houston": 2300000,
                "Miami": 500000
            }
            
            spatial_detections = SpatialOutbreakDetector.detect_spatial_scan(
                all_spatial_data, population_data
            )
            detections.extend(spatial_detections)
            
        except Exception as e:
            logger.error(f"Error in spatial detection: {e}")
        
        # Cross-domain analysis
        cross_domain_detections = self._detect_cross_domain_outbreaks(
            animal_data, human_data, environmental_data
        )
        detections.extend(cross_domain_detections)
        
        # Add to tracking system
        for detection in detections:
            self.outbreak_tracker.active_outbreaks[detection.detection_id] = detection
            self.detection_history.append(detection)
        
        detection_time = (datetime.now() - detection_start).total_seconds()
        
        logger.info(f"Outbreak detection completed: {len(detections)} outbreaks detected in {detection_time:.2f}s")
        
        return detections
    
    def _extract_time_series(self, data: List[Dict]) -> List[Tuple[datetime, int]]:
        """Extract time series from surveillance data."""
        time_series = []
        
        for record in data:
            timestamp_str = record.get('timestamp')
            count = record.get('case_count', 
                             record.get('mortality_count',
                                       record.get('total_collected', 1)))
            
            if timestamp_str and isinstance(count, (int, float)):
                try:
                    timestamp = datetime.fromisoformat(timestamp_str[:19])
                    time_series.append((timestamp, int(count)))
                except ValueError:
                    continue
        
        # Group by date and sum
        daily_counts = defaultdict(int)
        for timestamp, count in time_series:
            date_key = timestamp.date()
            daily_counts[date_key] += count
        
        # Convert back to sorted time series
        result = [(datetime.combine(date, datetime.min.time()), count) 
                 for date, count in sorted(daily_counts.items())]
        
        return result
    
    def _detect_cross_domain_outbreaks(self, animal_data: List[Dict],
                                      human_data: List[Dict], 
                                      environmental_data: List[Dict]) -> List[OutbreakDetection]:
        """Detect outbreaks that span multiple domains."""
        
        detections = []
        
        # Look for temporal correlation between domains
        animal_ts = self._extract_time_series(animal_data)
        human_ts = self._extract_time_series(human_data)
        
        if len(animal_ts) >= 3 and len(human_ts) >= 3:
            # Check for animal outbreaks followed by human cases
            for animal_date, animal_count in animal_ts:
                if animal_count > self.baseline_data["animal"]["mean"] * 2:  # Animal outbreak
                    
                    # Look for human cases 1-10 days later
                    for lag_days in range(1, 11):
                        target_date = animal_date + timedelta(days=lag_days)
                        
                        # Find human cases near target date
                        for human_date, human_count in human_ts:
                            time_diff = abs((human_date - target_date).days)
                            
                            if time_diff <= 2 and human_count > self.baseline_data["human"]["mean"] * 1.5:
                                # Found potential zoonotic transmission
                                
                                detection = OutbreakDetection(
                                    detection_id=f"ZOONOTIC_{animal_date.strftime('%Y%m%d')}",
                                    detection_timestamp=datetime.now(),
                                    outbreak_phase=OutbreakPhase.EMERGENCE,
                                    outbreak_type=OutbreakType.ZOONOTIC,
                                    outbreak_start=animal_date,
                                    case_count=animal_count + human_count,
                                    excess_cases=int((animal_count - self.baseline_data["animal"]["mean"]) +
                                                   (human_count - self.baseline_data["human"]["mean"])),
                                    alert_level=AlertLevel.ALERT,
                                    severity=OutbreakSeverity.SEVERE,
                                    affected_species=["animal", "human"],
                                    data_sources=["animal", "human"],
                                    investigation_priority="urgent",
                                    recommended_actions=[
                                        "Investigate animal-human transmission pathway",
                                        "Enhance cross-species surveillance",
                                        "Implement control measures at animal-human interface"
                                    ]
                                )
                                
                                detections.append(detection)
                                break
        
        return detections
    
    def get_detection_summary(self) -> Dict:
        """Get summary of outbreak detection activities."""
        
        active_outbreaks = list(self.outbreak_tracker.active_outbreaks.values())
        
        return {
            "active_outbreaks": len(active_outbreaks),
            "total_detections": len(self.detection_history),
            "recent_detections_24h": len([d for d in self.detection_history 
                                        if (datetime.now() - d.detection_timestamp).total_seconds() < 24*3600]),
            "severity_distribution": {
                severity.value: len([d for d in active_outbreaks if d.severity == severity])
                for severity in OutbreakSeverity
            },
            "alert_level_distribution": {
                level.value: len([d for d in active_outbreaks if d.alert_level == level])
                for level in AlertLevel
            },
            "outbreak_types": {
                otype.value: len([d for d in active_outbreaks 
                                if d.outbreak_type == otype])
                for otype in OutbreakType
            }
        }
    
    def get_active_outbreaks(self, severity_filter: Optional[OutbreakSeverity] = None) -> List[OutbreakDetection]:
        """Get currently active outbreaks, optionally filtered by severity."""
        
        active = list(self.outbreak_tracker.active_outbreaks.values())
        
        if severity_filter:
            active = [outbreak for outbreak in active if outbreak.severity == severity_filter]
        
        return sorted(active, key=lambda o: o.case_count, reverse=True)

# Mock data generator
def generate_mock_outbreak_data():
    """Generate mock data with embedded outbreak for testing."""
    
    # Generate animal data with clear outbreak pattern
    animal_data = []
    base_date = datetime.now() - timedelta(days=20)
    
    for i in range(20):
        date = base_date + timedelta(days=i)
        
        # Normal baseline: 1-3 cases
        baseline_cases = random.randint(1, 3)
        
        # Major outbreak spike on days 10-15
        if 10 <= i <= 15:
            outbreak_cases = baseline_cases + random.randint(15, 30)  # Large outbreak
        else:
            outbreak_cases = baseline_cases
        
        animal_data.append({
            "animal_id": f"OUTBREAK_FARM_{i:03d}",
            "timestamp": date.isoformat(),
            "location_lat": 40.7128 + random.uniform(-0.05, 0.05),
            "location_lon": -74.0060 + random.uniform(-0.05, 0.05),
            "species": "poultry",
            "mortality_count": outbreak_cases
        })
    
    # Generate human data with zoonotic transmission (2-day lag)
    human_data = []
    for i in range(18):
        date = base_date + timedelta(days=i+2)  # 2-day lag
        
        baseline = random.randint(0, 1)
        
        # Human cases following animal outbreak
        if 12 <= i <= 17:  # Following animal outbreak
            cases = baseline + random.randint(3, 8)
        else:
            cases = baseline
        
        if cases > 0:
            human_data.append({
                "case_id": f"OUTBREAK_HUM_{i:03d}",
                "timestamp": date.isoformat(),
                "location_lat": 40.7128 + random.uniform(-0.1, 0.1),
                "location_lon": -74.0060 + random.uniform(-0.1, 0.1),
                "case_classification": "confirmed",
                "case_count": cases
            })
    
    # Generate environmental data
    environmental_data = []
    for i in range(20):
        date = base_date + timedelta(days=i)
        
        # Normal environmental readings
        temp = 25 + random.uniform(-5, 5)
        
        environmental_data.append({
            "record_id": f"OUTBREAK_ENV_{i:03d}",
            "timestamp": date.isoformat(),
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "parameter": "temperature",
            "value": temp
        })
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of outbreak detection system."""
    print("🚨 One Health Outbreak Detection System - Demonstration")
    print("=" * 60)
    
    # Initialize detector
    detector = OneHealthOutbreakDetector()
    
    # Generate mock outbreak data
    animal_data, human_data, env_data = generate_mock_outbreak_data()
    
    print(f"\n📊 Outbreak Detection Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run outbreak detection
    print(f"\n🚨 Running Outbreak Detection Analysis...")
    detections = detector.detect_outbreaks(animal_data, human_data, env_data)
    
    # Display detected outbreaks
    print(f"\n📈 Detected Outbreaks ({len(detections)} total):")
    
    for i, outbreak in enumerate(detections, 1):
        print(f"\n{i}. Outbreak Detection")
        print(f"   Detection ID: {outbreak.detection_id}")
        print(f"   Phase: {outbreak.outbreak_phase.value.title()}")
        print(f"   Type: {outbreak.outbreak_type.value if outbreak.outbreak_type else 'Unknown'}")
        print(f"   Severity: {outbreak.severity.value.upper()}")
        print(f"   Alert Level: {outbreak.alert_level.value.upper()}")
        
        if outbreak.outbreak_start:
            days_ago = (datetime.now() - outbreak.outbreak_start).days
            print(f"   Started: {days_ago} days ago")
        
        print(f"   Cases: {outbreak.case_count} (excess: {outbreak.excess_cases})")
        
        if outbreak.detection_confidence:
            print(f"   Confidence: {outbreak.detection_confidence:.2f}")
        
        if outbreak.growth_rate is not None:
            print(f"   Growth Rate: {outbreak.growth_rate:.1%} per day")
        
        if outbreak.doubling_time_days:
            print(f"   Doubling Time: {outbreak.doubling_time_days:.1f} days")
        
        if outbreak.affected_radius_km:
            print(f"   Affected Area: {outbreak.affected_radius_km:.1f} km radius")
        
        if outbreak.data_sources:
            print(f"   Data Sources: {', '.join(outbreak.data_sources)}")
        
        if outbreak.investigation_priority != "routine":
            print(f"   Investigation: {outbreak.investigation_priority.upper()} priority")
        
        if outbreak.recommended_actions:
            print(f"   Actions: {len(outbreak.recommended_actions)} recommended")
    
    # Detection summary
    summary = detector.get_detection_summary()
    print(f"\n📊 Detection Summary:")
    print(f"  Active Outbreaks: {summary['active_outbreaks']}")
    print(f"  Total Detections: {summary['total_detections']}")
    print(f"  Recent (24h): {summary['recent_detections_24h']}")
    
    print(f"\n⚠️ By Severity:")
    for severity, count in summary['severity_distribution'].items():
        if count > 0:
            print(f"  {severity.upper()}: {count}")
    
    print(f"\n🚨 By Alert Level:")
    for level, count in summary['alert_level_distribution'].items():
        if count > 0:
            print(f"  {level.upper()}: {count}")
    
    # Critical outbreaks
    critical_outbreaks = detector.get_active_outbreaks(OutbreakSeverity.CRITICAL)
    if critical_outbreaks:
        print(f"\n🔴 CRITICAL Outbreaks ({len(critical_outbreaks)}):")
        for outbreak in critical_outbreaks:
            print(f"  - {outbreak.detection_id}: {outbreak.case_count} cases")
            print(f"    Alert: {outbreak.alert_level.value.upper()}")
            if outbreak.recommended_actions:
                print(f"    Actions: {outbreak.recommended_actions[0]}")
    
    # Zoonotic outbreaks
    zoonotic_outbreaks = [o for o in detections if o.outbreak_type == OutbreakType.ZOONOTIC]
    if zoonotic_outbreaks:
        print(f"\n🔬 ZOONOTIC Outbreaks ({len(zoonotic_outbreaks)}):")
        for outbreak in zoonotic_outbreaks:
            print(f"  - {outbreak.detection_id}: Animal→Human transmission detected")
            print(f"    Species: {', '.join(outbreak.affected_species)}")
    
    return detector

if __name__ == "__main__":
    detector = run_demonstration()
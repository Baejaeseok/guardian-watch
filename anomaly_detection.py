"""
Anomaly Detection and Outlier Analysis System
============================================
Module 6: Advanced Analytics

Comprehensive anomaly detection system for One Health surveillance and monitoring,
providing advanced outlier detection, pattern analysis, and early warning capabilities.

NIW Focus: Anomaly intelligence enabling early detection of unusual patterns, 
emerging threats, and system deviations across One Health domains.
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

class AnomalyType(Enum):
    """Types of anomalies to detect."""
    POINT_ANOMALY = "point_anomaly"            # Individual anomalous data points
    CONTEXTUAL_ANOMALY = "contextual_anomaly"  # Anomalous in specific context
    COLLECTIVE_ANOMALY = "collective_anomaly"  # Pattern of anomalous behavior
    SEASONAL_ANOMALY = "seasonal_anomaly"      # Deviations from seasonal patterns
    TREND_ANOMALY = "trend_anomaly"           # Unusual trend changes
    DISTRIBUTION_SHIFT = "distribution_shift"  # Changes in data distribution
    CORRELATION_BREAK = "correlation_break"    # Breakdown in expected correlations
    THRESHOLD_BREACH = "threshold_breach"      # Exceeding predefined thresholds

class DetectionMethod(Enum):
    """Anomaly detection methods."""
    STATISTICAL = "statistical"                # Statistical methods (Z-score, IQR)
    MACHINE_LEARNING = "machine_learning"      # ML-based detection
    DENSITY_BASED = "density_based"           # Density-based methods
    DISTANCE_BASED = "distance_based"         # Distance-based methods
    ISOLATION_BASED = "isolation_based"       # Isolation methods
    ENSEMBLE = "ensemble"                     # Ensemble of multiple methods
    TIME_SERIES = "time_series"               # Time series specific methods
    STREAMING = "streaming"                   # Real-time streaming detection

class AnomalySeverity(Enum):
    """Severity levels of detected anomalies."""
    LOW = "low"                              # Minor deviations
    MEDIUM = "medium"                        # Moderate anomalies
    HIGH = "high"                           # Significant anomalies
    CRITICAL = "critical"                   # Critical anomalies requiring immediate attention

class ConfidenceLevel(Enum):
    """Confidence levels for anomaly detection."""
    VERY_LOW = "very_low"                   # <50% confidence
    LOW = "low"                            # 50-70% confidence
    MEDIUM = "medium"                      # 70-85% confidence
    HIGH = "high"                          # 85-95% confidence
    VERY_HIGH = "very_high"                # >95% confidence

@dataclass
class AnomalyDetector:
    """Anomaly detection configuration."""
    
    detector_id: str
    detector_name: str
    detection_method: DetectionMethod
    anomaly_types: List[AnomalyType] = field(default_factory=list)
    
    # Detection parameters
    sensitivity: float = 0.5                  # Detection sensitivity (0-1)
    threshold_multiplier: float = 2.0         # Threshold multiplier for statistical methods
    contamination_rate: float = 0.1           # Expected proportion of anomalies
    
    # Method-specific parameters
    method_parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Feature configuration
    monitored_features: List[str] = field(default_factory=list)
    categorical_features: List[str] = field(default_factory=list)
    temporal_features: List[str] = field(default_factory=list)
    
    # Detection scope
    data_domain: str = "general"              # One Health domain
    detection_window_hours: int = 24          # Time window for detection
    minimum_data_points: int = 30             # Minimum points needed
    
    # Performance metrics
    false_positive_rate: float = 0.0         # Estimated FPR
    detection_rate: float = 0.0              # True positive rate
    precision: float = 0.0                   # Precision score
    
    # Detector status
    is_active: bool = True                   # Whether detector is active
    last_training: Optional[datetime] = None  # Last training timestamp
    last_detection: Optional[datetime] = None # Last detection run
    
    # Alert configuration
    alert_threshold: AnomalySeverity = AnomalySeverity.MEDIUM
    notification_enabled: bool = True
    escalation_rules: List[str] = field(default_factory=list)

@dataclass
class DetectedAnomaly:
    """Individual detected anomaly."""
    
    anomaly_id: str
    detector_id: str
    detection_timestamp: datetime
    
    # Anomaly characteristics
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    confidence: ConfidenceLevel
    confidence_score: float                   # Numerical confidence (0-1)
    
    # Data point information
    anomalous_features: Dict[str, Any] = field(default_factory=dict)
    anomaly_score: float = 0.0               # Numerical anomaly score
    deviation_magnitude: float = 0.0         # How much it deviates from normal
    
    # Context information
    data_timestamp: Optional[datetime] = None # Timestamp of anomalous data
    data_source: str = ""                    # Source of anomalous data
    related_features: List[str] = field(default_factory=list)
    
    # Statistical context
    baseline_statistics: Dict[str, float] = field(default_factory=dict)
    comparison_values: Dict[str, float] = field(default_factory=dict)
    
    # Health domain context
    health_domain: str = "general"           # Specific health domain
    potential_causes: List[str] = field(default_factory=list)
    health_implications: List[str] = field(default_factory=list)
    
    # Response information
    is_investigated: bool = False            # Whether anomaly has been investigated
    investigation_notes: str = ""            # Investigation findings
    is_false_positive: Optional[bool] = None # True/False/None (unknown)
    corrective_actions: List[str] = field(default_factory=list)
    
    # Follow-up tracking
    resolved: bool = False                   # Whether anomaly is resolved
    resolution_timestamp: Optional[datetime] = None
    resolution_notes: str = ""

@dataclass
class AnomalyPattern:
    """Pattern of related anomalies."""
    
    pattern_id: str
    pattern_name: str
    pattern_description: str
    
    # Pattern characteristics
    pattern_type: str = "temporal"           # "temporal", "spatial", "feature-based"
    related_anomalies: List[str] = field(default_factory=list)  # Anomaly IDs
    pattern_confidence: float = 0.0         # Confidence in pattern
    
    # Pattern timeline
    pattern_start: datetime = field(default_factory=datetime.now)
    pattern_end: Optional[datetime] = None
    pattern_duration_hours: float = 0.0
    
    # Pattern analysis
    common_features: List[str] = field(default_factory=list)
    pattern_signature: Dict[str, Any] = field(default_factory=dict)
    frequency: int = 0                       # How often this pattern occurs
    
    # Health implications
    risk_assessment: str = "unknown"         # "low", "medium", "high"
    potential_outbreak_indicator: bool = False
    recommended_actions: List[str] = field(default_factory=list)
    
    # Pattern metadata
    identified_by: str = "pattern_detection_system"
    identification_timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AnomalyReport:
    """Comprehensive anomaly detection report."""
    
    report_id: str
    report_title: str
    report_period_start: datetime
    report_period_end: datetime
    generation_timestamp: datetime
    
    # Detection summary
    total_anomalies_detected: int = 0
    anomalies_by_severity: Dict[AnomalySeverity, int] = field(default_factory=dict)
    anomalies_by_type: Dict[AnomalyType, int] = field(default_factory=dict)
    anomalies_by_domain: Dict[str, int] = field(default_factory=dict)
    
    # Detection performance
    total_detections_run: int = 0
    average_detection_time_ms: float = 0.0
    false_positive_rate: float = 0.0
    detection_accuracy: float = 0.0
    
    # Pattern analysis
    patterns_identified: int = 0
    potential_outbreaks_flagged: int = 0
    critical_anomalies_unresolved: int = 0
    
    # Top findings
    top_anomalous_features: List[Tuple[str, float]] = field(default_factory=list)
    most_affected_domains: List[str] = field(default_factory=list)
    peak_anomaly_periods: List[datetime] = field(default_factory=list)
    
    # Recommendations
    immediate_actions_required: List[str] = field(default_factory=list)
    investigation_priorities: List[str] = field(default_factory=list)
    detector_optimization_suggestions: List[str] = field(default_factory=list)
    
    # System health
    detector_performance_summary: Dict[str, float] = field(default_factory=dict)
    data_quality_issues: List[str] = field(default_factory=list)

class AnomalyDetectionEngine:
    """Comprehensive anomaly detection and analysis engine."""
    
    def __init__(self):
        self.detectors: Dict[str, AnomalyDetector] = {}
        self.detected_anomalies: List[DetectedAnomaly] = []
        self.anomaly_patterns: List[AnomalyPattern] = []
        self.anomaly_reports: List[AnomalyReport] = []
        
        # Detection capabilities
        self.method_algorithms = {
            DetectionMethod.STATISTICAL: ["z_score", "modified_z_score", "iqr", "grubbs_test"],
            DetectionMethod.MACHINE_LEARNING: ["isolation_forest", "one_class_svm", "local_outlier_factor"],
            DetectionMethod.DENSITY_BASED: ["dbscan", "local_density"],
            DetectionMethod.TIME_SERIES: ["arima_residuals", "seasonal_decomposition", "changepoint"],
            DetectionMethod.ENSEMBLE: ["voting", "stacking", "averaging"]
        }
        
        # Initialize detection framework
        self._initialize_detection_framework()
        
        logger.info("Anomaly Detection Engine initialized for One Health")
    
    def _initialize_detection_framework(self):
        """Initialize anomaly detection framework."""
        
        # Sample anomaly detectors for different One Health domains
        sample_detectors = [
            {
                "name": "Zoonotic Disease Surveillance Monitor", 
                "method": DetectionMethod.TIME_SERIES,
                "types": [AnomalyType.TREND_ANOMALY, AnomalyType.SEASONAL_ANOMALY],
                "domain": "zoonotic_surveillance", "sensitivity": 0.7
            },
            {
                "name": "Environmental Health Threshold Monitor",
                "method": DetectionMethod.STATISTICAL, 
                "types": [AnomalyType.THRESHOLD_BREACH, AnomalyType.POINT_ANOMALY],
                "domain": "environmental_health", "sensitivity": 0.8
            },
            {
                "name": "AMR Pattern Anomaly Detector",
                "method": DetectionMethod.MACHINE_LEARNING,
                "types": [AnomalyType.DISTRIBUTION_SHIFT, AnomalyType.CORRELATION_BREAK],
                "domain": "antimicrobial_resistance", "sensitivity": 0.6
            },
            {
                "name": "Food Safety Real-time Monitor",
                "method": DetectionMethod.STREAMING,
                "types": [AnomalyType.POINT_ANOMALY, AnomalyType.CONTEXTUAL_ANOMALY],
                "domain": "food_safety", "sensitivity": 0.9
            },
            {
                "name": "Multi-domain Outbreak Detector", 
                "method": DetectionMethod.ENSEMBLE,
                "types": [AnomalyType.COLLECTIVE_ANOMALY, AnomalyType.PATTERN_ANOMALY],
                "domain": "outbreak_detection", "sensitivity": 0.75
            },
            {
                "name": "Clinical Decision Support Anomaly Checker",
                "method": DetectionMethod.DENSITY_BASED,
                "types": [AnomalyType.POINT_ANOMALY, AnomalyType.CONTEXTUAL_ANOMALY],
                "domain": "clinical_systems", "sensitivity": 0.6
            }
        ]
        
        # Create anomaly detectors
        for detector_data in sample_detectors:
            detector_id = f"DETECTOR_{random.randint(100000, 999999)}"
            
            detector = AnomalyDetector(
                detector_id=detector_id,
                detector_name=detector_data["name"],
                detection_method=detector_data["method"],
                anomaly_types=detector_data["types"],
                data_domain=detector_data["domain"],
                sensitivity=detector_data["sensitivity"],
                contamination_rate=random.uniform(0.05, 0.15),
                detection_window_hours=random.randint(6, 48),
                minimum_data_points=random.randint(20, 100)
            )
            
            # Configure method-specific parameters
            if detector.detection_method == DetectionMethod.STATISTICAL:
                detector.method_parameters = {
                    "z_score_threshold": random.uniform(2.0, 3.5),
                    "iqr_multiplier": random.uniform(1.5, 3.0),
                    "window_size": random.randint(50, 200)
                }
            elif detector.detection_method == DetectionMethod.MACHINE_LEARNING:
                detector.method_parameters = {
                    "isolation_forest_estimators": random.randint(50, 200),
                    "svm_nu": random.uniform(0.01, 0.2),
                    "lof_neighbors": random.randint(10, 50)
                }
            elif detector.detection_method == DetectionMethod.TIME_SERIES:
                detector.method_parameters = {
                    "seasonal_period": random.randint(7, 365),
                    "changepoint_penalty": random.randint(1, 10),
                    "trend_threshold": random.uniform(0.1, 0.5)
                }
            
            # Configure monitored features
            detector.monitored_features = [
                "case_count", "prevalence_rate", "incidence_rate",
                "environmental_factor", "temperature", "humidity",
                "population_density", "intervention_coverage"
            ]
            
            # Set performance metrics (simulated)
            detector.false_positive_rate = random.uniform(0.01, 0.1)
            detector.detection_rate = random.uniform(0.75, 0.95)
            detector.precision = random.uniform(0.70, 0.90)
            
            # Set training and detection timestamps
            detector.last_training = datetime.now() - timedelta(days=random.randint(7, 30))
            detector.last_detection = datetime.now() - timedelta(hours=random.randint(1, 6))
            
            # Configure alerts
            detector.alert_threshold = random.choice(list(AnomalySeverity))
            detector.escalation_rules = [
                "Notify health authorities for critical anomalies",
                "Trigger automated investigation for high severity",
                "Generate daily summary for medium/low severity"
            ]
            
            self.detectors[detector_id] = detector
        
        # Generate sample detected anomalies
        self._generate_sample_anomalies()
        
        logger.info(f"Initialized {len(self.detectors)} anomaly detectors")
    
    def _generate_sample_anomalies(self):
        """Generate sample detected anomalies for demonstration."""
        
        # Anomaly scenarios for different domains
        anomaly_scenarios = [
            {
                "type": AnomalyType.TREND_ANOMALY, "severity": AnomalySeverity.HIGH,
                "domain": "zoonotic_surveillance", "description": "Unusual increase in zoonotic case reports"
            },
            {
                "type": AnomalyType.THRESHOLD_BREACH, "severity": AnomalySeverity.CRITICAL,
                "domain": "environmental_health", "description": "Air quality parameters exceeding safety limits"
            },
            {
                "type": AnomalyType.DISTRIBUTION_SHIFT, "severity": AnomalySeverity.MEDIUM,
                "domain": "antimicrobial_resistance", "description": "Shift in resistance pattern distribution"
            },
            {
                "type": AnomalyType.POINT_ANOMALY, "severity": AnomalySeverity.HIGH,
                "domain": "food_safety", "description": "Contamination spike in food processing facility"
            },
            {
                "type": AnomalyType.COLLECTIVE_ANOMALY, "severity": AnomalySeverity.CRITICAL,
                "domain": "outbreak_detection", "description": "Coordinated anomalous patterns across multiple sites"
            },
            {
                "type": AnomalyType.CONTEXTUAL_ANOMALY, "severity": AnomalySeverity.MEDIUM,
                "domain": "clinical_systems", "description": "Unusual diagnostic patterns in specific population"
            }
        ]
        
        # Create detected anomalies
        for scenario in anomaly_scenarios:
            for _ in range(random.randint(1, 3)):  # 1-3 anomalies per scenario
                anomaly_id = f"ANOMALY_{random.randint(100000, 999999)}"
                
                # Select appropriate detector
                suitable_detectors = [
                    d for d in self.detectors.values()
                    if d.data_domain == scenario["domain"] and scenario["type"] in d.anomaly_types
                ]
                detector = random.choice(suitable_detectors) if suitable_detectors else list(self.detectors.values())[0]
                
                anomaly = DetectedAnomaly(
                    anomaly_id=anomaly_id,
                    detector_id=detector.detector_id,
                    detection_timestamp=datetime.now() - timedelta(hours=random.randint(1, 72)),
                    anomaly_type=scenario["type"],
                    severity=scenario["severity"],
                    confidence=random.choice(list(ConfidenceLevel)),
                    confidence_score=random.uniform(0.6, 0.95),
                    anomaly_score=random.uniform(0.5, 1.0),
                    deviation_magnitude=random.uniform(2.0, 10.0),
                    health_domain=scenario["domain"],
                    data_timestamp=datetime.now() - timedelta(hours=random.randint(1, 48))
                )
                
                # Add anomalous features
                anomaly.anomalous_features = {
                    "primary_feature": random.uniform(50, 200),
                    "secondary_feature": random.uniform(10, 100),
                    "contextual_feature": random.choice(["high", "medium", "unusual"])
                }
                
                # Add potential causes based on domain
                if scenario["domain"] == "zoonotic_surveillance":
                    anomaly.potential_causes = [
                        "Seasonal migration patterns",
                        "Environmental factors",
                        "Surveillance system changes",
                        "Reporting behavior changes"
                    ]
                elif scenario["domain"] == "environmental_health":
                    anomaly.potential_causes = [
                        "Industrial emissions",
                        "Weather conditions",
                        "Traffic patterns",
                        "Seasonal variations"
                    ]
                elif scenario["domain"] == "food_safety":
                    anomaly.potential_causes = [
                        "Supply chain disruption",
                        "Processing equipment malfunction",
                        "Temperature control failure",
                        "Contamination event"
                    ]
                
                # Add health implications
                if scenario["severity"] in [AnomalySeverity.HIGH, AnomalySeverity.CRITICAL]:
                    anomaly.health_implications = [
                        "Potential public health threat",
                        "Increased disease transmission risk", 
                        "Population health impact",
                        "Healthcare system strain"
                    ]
                else:
                    anomaly.health_implications = [
                        "Monitor for escalation",
                        "Routine surveillance continuation",
                        "Data quality verification needed"
                    ]
                
                # Add baseline statistics
                anomaly.baseline_statistics = {
                    "mean": random.uniform(10, 50),
                    "std": random.uniform(5, 15),
                    "median": random.uniform(8, 45),
                    "percentile_95": random.uniform(40, 80)
                }
                
                # Investigation status
                anomaly.is_investigated = random.random() > 0.4  # 60% investigated
                if anomaly.is_investigated:
                    anomaly.investigation_notes = f"Investigated {scenario['description']}"
                    anomaly.is_false_positive = random.random() > 0.8  # 20% false positives
                
                self.detected_anomalies.append(anomaly)
        
        # Generate anomaly patterns
        self._identify_anomaly_patterns()
    
    def _identify_anomaly_patterns(self):
        """Identify patterns among detected anomalies."""
        
        # Group anomalies by domain and time proximity
        domain_anomalies = defaultdict(list)
        for anomaly in self.detected_anomalies:
            domain_anomalies[anomaly.health_domain].append(anomaly)
        
        # Identify patterns within domains
        for domain, anomalies in domain_anomalies.items():
            if len(anomalies) >= 2:  # Need at least 2 anomalies for a pattern
                pattern_id = f"PATTERN_{random.randint(100000, 999999)}"
                
                pattern = AnomalyPattern(
                    pattern_id=pattern_id,
                    pattern_name=f"{domain.replace('_', ' ').title()} Anomaly Cluster",
                    pattern_description=f"Cluster of {len(anomalies)} anomalies in {domain}",
                    pattern_type="temporal",
                    related_anomalies=[a.anomaly_id for a in anomalies],
                    pattern_confidence=random.uniform(0.6, 0.9)
                )
                
                # Calculate pattern timeline
                timestamps = [a.detection_timestamp for a in anomalies]
                pattern.pattern_start = min(timestamps)
                pattern.pattern_end = max(timestamps)
                pattern.pattern_duration_hours = (pattern.pattern_end - pattern.pattern_start).total_seconds() / 3600
                
                # Identify common features
                all_features = set()
                for anomaly in anomalies:
                    all_features.update(anomaly.anomalous_features.keys())
                pattern.common_features = list(all_features)
                
                # Risk assessment
                severities = [a.severity for a in anomalies]
                if AnomalySeverity.CRITICAL in severities:
                    pattern.risk_assessment = "high"
                    pattern.potential_outbreak_indicator = True
                elif AnomalySeverity.HIGH in severities:
                    pattern.risk_assessment = "medium"
                else:
                    pattern.risk_assessment = "low"
                
                # Recommended actions
                if pattern.risk_assessment == "high":
                    pattern.recommended_actions = [
                        "Immediate health authority notification",
                        "Enhanced surveillance activation",
                        "Cross-domain correlation analysis",
                        "Public health response consideration"
                    ]
                else:
                    pattern.recommended_actions = [
                        "Continue monitoring pattern evolution",
                        "Investigate common factors",
                        "Update detection thresholds if needed"
                    ]
                
                self.anomaly_patterns.append(pattern)
    
    def run_anomaly_detection(self, detector_id: str, data: Dict[str, Any]) -> List[DetectedAnomaly]:
        """Run anomaly detection on provided data."""
        
        if detector_id not in self.detectors:
            raise ValueError(f"Detector {detector_id} not found")
        
        detector = self.detectors[detector_id]
        
        # Simulate anomaly detection process
        detected_anomalies = []
        
        # Check each monitored feature
        for feature in detector.monitored_features:
            if feature in data:
                feature_value = data[feature]
                
                # Simulate detection based on method
                anomaly_detected = self._simulate_detection(detector, feature, feature_value)
                
                if anomaly_detected:
                    anomaly_id = f"ANOMALY_{random.randint(100000, 999999)}"
                    
                    anomaly = DetectedAnomaly(
                        anomaly_id=anomaly_id,
                        detector_id=detector_id,
                        detection_timestamp=datetime.now(),
                        anomaly_type=random.choice(detector.anomaly_types),
                        severity=self._calculate_severity(anomaly_detected["score"], detector),
                        confidence=self._calculate_confidence(anomaly_detected["score"]),
                        confidence_score=anomaly_detected["confidence"],
                        anomaly_score=anomaly_detected["score"],
                        deviation_magnitude=anomaly_detected["deviation"],
                        health_domain=detector.data_domain,
                        data_timestamp=datetime.now()
                    )
                    
                    # Add feature information
                    anomaly.anomalous_features = {feature: feature_value}
                    anomaly.related_features = [feature]
                    
                    # Add potential causes (domain-specific)
                    anomaly.potential_causes = self._generate_potential_causes(detector.data_domain)
                    anomaly.health_implications = self._generate_health_implications(anomaly.severity)
                    
                    detected_anomalies.append(anomaly)
                    self.detected_anomalies.append(anomaly)
        
        # Update detector last detection time
        detector.last_detection = datetime.now()
        
        logger.info(f"Anomaly detection completed: {detector_id} - {len(detected_anomalies)} anomalies detected")
        
        return detected_anomalies
    
    def _simulate_detection(self, detector: AnomalyDetector, feature: str, value: Any) -> Optional[Dict[str, float]]:
        """Simulate anomaly detection for a feature value."""
        
        # Simulate baseline statistics
        baseline_mean = random.uniform(20, 80)
        baseline_std = random.uniform(5, 20)
        
        # Convert value to numeric if possible
        if isinstance(value, (int, float)):
            numeric_value = float(value)
        else:
            # For non-numeric values, simulate a detection probability
            return {"score": random.uniform(0.3, 0.8), "confidence": random.uniform(0.6, 0.9), 
                   "deviation": random.uniform(1.0, 3.0)} if random.random() > 0.8 else None
        
        # Calculate anomaly score based on detection method
        if detector.detection_method == DetectionMethod.STATISTICAL:
            # Z-score based detection
            z_score = abs(numeric_value - baseline_mean) / baseline_std if baseline_std > 0 else 0
            threshold = detector.method_parameters.get("z_score_threshold", 2.5)
            
            if z_score > threshold:
                anomaly_score = min(z_score / threshold, 1.0)
                confidence = min(0.6 + (z_score - threshold) * 0.1, 0.95)
                return {
                    "score": anomaly_score,
                    "confidence": confidence,
                    "deviation": z_score
                }
                
        elif detector.detection_method == DetectionMethod.MACHINE_LEARNING:
            # Simulate ML-based detection
            anomaly_probability = random.uniform(0, 1)
            contamination_threshold = detector.contamination_rate
            
            if anomaly_probability > (1 - contamination_threshold):
                return {
                    "score": anomaly_probability,
                    "confidence": random.uniform(0.7, 0.95),
                    "deviation": random.uniform(1.5, 5.0)
                }
                
        elif detector.detection_method == DetectionMethod.TIME_SERIES:
            # Simulate time series anomaly detection
            seasonal_component = math.sin(2 * math.pi * datetime.now().timetuple().tm_yday / 365)
            expected_value = baseline_mean + seasonal_component * baseline_std
            
            deviation = abs(numeric_value - expected_value)
            if deviation > baseline_std * 2:
                anomaly_score = min(deviation / (baseline_std * 3), 1.0)
                return {
                    "score": anomaly_score,
                    "confidence": random.uniform(0.6, 0.9),
                    "deviation": deviation / baseline_std
                }
        
        # Apply sensitivity adjustment
        if random.random() < detector.sensitivity:
            # Sensitivity can trigger additional detections
            return {
                "score": random.uniform(0.4, 0.7),
                "confidence": random.uniform(0.5, 0.8),
                "deviation": random.uniform(1.0, 2.0)
            }
        
        return None  # No anomaly detected
    
    def _calculate_severity(self, anomaly_score: float, detector: AnomalyDetector) -> AnomalySeverity:
        """Calculate anomaly severity based on score and detector configuration."""
        
        # Adjust thresholds based on detector sensitivity
        base_thresholds = {
            AnomalySeverity.LOW: 0.3,
            AnomalySeverity.MEDIUM: 0.6,
            AnomalySeverity.HIGH: 0.8,
            AnomalySeverity.CRITICAL: 0.9
        }
        
        # Apply sensitivity multiplier
        sensitivity_factor = 1.0 + (detector.sensitivity - 0.5) * 0.2
        
        if anomaly_score >= base_thresholds[AnomalySeverity.CRITICAL] * sensitivity_factor:
            return AnomalySeverity.CRITICAL
        elif anomaly_score >= base_thresholds[AnomalySeverity.HIGH] * sensitivity_factor:
            return AnomalySeverity.HIGH
        elif anomaly_score >= base_thresholds[AnomalySeverity.MEDIUM] * sensitivity_factor:
            return AnomalySeverity.MEDIUM
        else:
            return AnomalySeverity.LOW
    
    def _calculate_confidence(self, anomaly_score: float) -> ConfidenceLevel:
        """Calculate confidence level based on anomaly score."""
        
        if anomaly_score >= 0.95:
            return ConfidenceLevel.VERY_HIGH
        elif anomaly_score >= 0.85:
            return ConfidenceLevel.HIGH
        elif anomaly_score >= 0.70:
            return ConfidenceLevel.MEDIUM
        elif anomaly_score >= 0.50:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def _generate_potential_causes(self, domain: str) -> List[str]:
        """Generate potential causes based on health domain."""
        
        domain_causes = {
            "zoonotic_surveillance": [
                "Seasonal animal migration",
                "Changes in human-animal contact",
                "Environmental factors",
                "Surveillance system modifications"
            ],
            "environmental_health": [
                "Industrial pollution events",
                "Weather pattern changes", 
                "Traffic and emissions",
                "Natural disasters"
            ],
            "antimicrobial_resistance": [
                "Antibiotic usage changes",
                "Healthcare practice modifications",
                "Agricultural antibiotic use",
                "Population demographics shifts"
            ],
            "food_safety": [
                "Supply chain contamination",
                "Processing facility issues",
                "Storage temperature problems",
                "Regulatory changes"
            ]
        }
        
        return domain_causes.get(domain, ["Unknown causes", "System changes", "Data quality issues"])
    
    def _generate_health_implications(self, severity: AnomalySeverity) -> List[str]:
        """Generate health implications based on severity."""
        
        implications = {
            AnomalySeverity.CRITICAL: [
                "Immediate public health threat",
                "Potential outbreak situation",
                "Emergency response required",
                "Healthcare system impact"
            ],
            AnomalySeverity.HIGH: [
                "Significant health risk",
                "Enhanced surveillance needed",
                "Investigation required",
                "Public health alert consideration"
            ],
            AnomalySeverity.MEDIUM: [
                "Moderate health concern",
                "Continued monitoring required",
                "Investigation recommended",
                "Trend assessment needed"
            ],
            AnomalySeverity.LOW: [
                "Minor health relevance",
                "Routine monitoring sufficient",
                "Data quality check recommended",
                "Pattern observation"
            ]
        }
        
        return implications.get(severity, ["Unknown health implications"])
    
    def investigate_anomaly(self, anomaly_id: str, investigation_notes: str, 
                          is_false_positive: bool = False) -> bool:
        """Mark anomaly as investigated with findings."""
        
        anomaly = None
        for a in self.detected_anomalies:
            if a.anomaly_id == anomaly_id:
                anomaly = a
                break
        
        if not anomaly:
            return False
        
        anomaly.is_investigated = True
        anomaly.investigation_notes = investigation_notes
        anomaly.is_false_positive = is_false_positive
        
        # Update detector false positive rate if needed
        detector = self.detectors.get(anomaly.detector_id)
        if detector and is_false_positive:
            # Simple exponential moving average update
            detector.false_positive_rate = detector.false_positive_rate * 0.9 + 0.1
        
        logger.info(f"Anomaly investigation completed: {anomaly_id}")
        
        return True
    
    def generate_anomaly_report(self, report_title: str, period_days: int = 7) -> AnomalyReport:
        """Generate comprehensive anomaly detection report."""
        
        report_id = f"ANOMALY_RPT_{random.randint(100000, 999999)}"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        report = AnomalyReport(
            report_id=report_id,
            report_title=report_title,
            report_period_start=start_date,
            report_period_end=end_date,
            generation_timestamp=datetime.now()
        )
        
        # Filter anomalies for report period
        period_anomalies = [
            a for a in self.detected_anomalies
            if start_date <= a.detection_timestamp <= end_date
        ]
        
        # Basic statistics
        report.total_anomalies_detected = len(period_anomalies)
        
        # Anomalies by severity
        severity_counts = Counter(a.severity for a in period_anomalies)
        report.anomalies_by_severity = dict(severity_counts)
        
        # Anomalies by type
        type_counts = Counter(a.anomaly_type for a in period_anomalies)
        report.anomalies_by_type = dict(type_counts)
        
        # Anomalies by domain
        domain_counts = Counter(a.health_domain for a in period_anomalies)
        report.anomalies_by_domain = dict(domain_counts)
        
        # Detection performance
        report.total_detections_run = len(self.detectors) * period_days  # Estimated
        report.average_detection_time_ms = random.uniform(100, 1000)
        
        investigated_anomalies = [a for a in period_anomalies if a.is_investigated]
        if investigated_anomalies:
            false_positives = [a for a in investigated_anomalies if a.is_false_positive]
            report.false_positive_rate = len(false_positives) / len(investigated_anomalies)
            report.detection_accuracy = 1 - report.false_positive_rate
        
        # Pattern analysis
        period_patterns = [p for p in self.anomaly_patterns 
                          if start_date <= p.identification_timestamp <= end_date]
        report.patterns_identified = len(period_patterns)
        report.potential_outbreaks_flagged = len([p for p in period_patterns if p.potential_outbreak_indicator])
        
        # Critical anomalies
        critical_anomalies = [a for a in period_anomalies if a.severity == AnomalySeverity.CRITICAL]
        unresolved_critical = [a for a in critical_anomalies if not a.resolved]
        report.critical_anomalies_unresolved = len(unresolved_critical)
        
        # Top findings
        if period_anomalies:
            # Top anomalous features
            feature_scores = defaultdict(list)
            for anomaly in period_anomalies:
                for feature, value in anomaly.anomalous_features.items():
                    if isinstance(value, (int, float)):
                        feature_scores[feature].append(anomaly.anomaly_score)
            
            feature_avg_scores = {
                feature: statistics.mean(scores) 
                for feature, scores in feature_scores.items()
            }
            
            report.top_anomalous_features = sorted(feature_avg_scores.items(), 
                                                 key=lambda x: x[1], reverse=True)[:5]
            
            # Most affected domains
            report.most_affected_domains = [domain for domain, count in domain_counts.most_common(3)]
            
            # Peak anomaly periods (simplified - by hour)
            anomaly_hours = [a.detection_timestamp.replace(minute=0, second=0, microsecond=0) 
                           for a in period_anomalies]
            hour_counts = Counter(anomaly_hours)
            report.peak_anomaly_periods = [hour for hour, count in hour_counts.most_common(3)]
        
        # Generate recommendations
        report.immediate_actions_required = []
        report.investigation_priorities = []
        report.detector_optimization_suggestions = []
        
        if report.critical_anomalies_unresolved > 0:
            report.immediate_actions_required.append(
                f"Investigate {report.critical_anomalies_unresolved} unresolved critical anomalies"
            )
        
        if report.false_positive_rate > 0.2:
            report.detector_optimization_suggestions.append(
                "High false positive rate detected - consider tuning detector sensitivity"
            )
        
        if report.patterns_identified > 0:
            report.investigation_priorities.append(
                f"Analyze {report.patterns_identified} identified anomaly patterns"
            )
        
        # Detector performance summary
        for detector_id, detector in self.detectors.items():
            detector_anomalies = [a for a in period_anomalies if a.detector_id == detector_id]
            if detector_anomalies:
                avg_confidence = statistics.mean(a.confidence_score for a in detector_anomalies)
                report.detector_performance_summary[detector.detector_name] = avg_confidence
        
        self.anomaly_reports.append(report)
        
        logger.info(f"Anomaly report generated: {report_id}")
        
        return report
    
    def get_detection_summary(self) -> Dict[str, Any]:
        """Get comprehensive anomaly detection summary."""
        
        # Detector analysis
        detectors_by_method = Counter(d.detection_method for d in self.detectors.values())
        active_detectors = len([d for d in self.detectors.values() if d.is_active])
        
        # Anomaly analysis
        if self.detected_anomalies:
            anomalies_by_severity = Counter(a.severity for a in self.detected_anomalies)
            anomalies_by_type = Counter(a.anomaly_type for a in self.detected_anomalies)
            anomalies_by_domain = Counter(a.health_domain for a in self.detected_anomalies)
            
            # Confidence analysis
            confidence_scores = [a.confidence_score for a in self.detected_anomalies]
            avg_confidence = statistics.mean(confidence_scores)
            
            # Investigation analysis
            investigated = len([a for a in self.detected_anomalies if a.is_investigated])
            investigation_rate = investigated / len(self.detected_anomalies)
        else:
            anomalies_by_severity = anomalies_by_type = anomalies_by_domain = Counter()
            avg_confidence = investigation_rate = 0
        
        return {
            "detectors": {
                "total_detectors": len(self.detectors),
                "active_detectors": active_detectors,
                "by_method": {m.value: count for m, count in detectors_by_method.items()}
            },
            "anomalies": {
                "total_detected": len(self.detected_anomalies),
                "by_severity": {s.value: count for s, count in anomalies_by_severity.items()},
                "by_type": {t.value: count for t, count in anomalies_by_type.items()},
                "by_domain": dict(anomalies_by_domain),
                "average_confidence": avg_confidence,
                "investigation_rate": investigation_rate
            },
            "patterns": {
                "total_patterns": len(self.anomaly_patterns),
                "outbreak_indicators": len([p for p in self.anomaly_patterns if p.potential_outbreak_indicator])
            },
            "reports": {
                "total_reports": len(self.anomaly_reports)
            }
        }

def run_demonstration() -> AnomalyDetectionEngine:
    """Run comprehensive anomaly detection demonstration."""
    
    print("🚨 One Health Anomaly Detection - Demonstration")
    print("=" * 70)
    
    engine = AnomalyDetectionEngine()
    
    print(f"\n🚨 Anomaly Detection Framework:")
    print(f"  Anomaly Types: {len(AnomalyType)}")
    print(f"  Detection Methods: {len(DetectionMethod)}")
    print(f"  Severity Levels: {len(AnomalySeverity)}")
    print(f"  Active Detectors: {len(engine.detectors)}")
    print(f"  Detected Anomalies: {len(engine.detected_anomalies)}")
    
    # Display detectors by method
    detectors_by_method = defaultdict(list)
    for detector in engine.detectors.values():
        detectors_by_method[detector.detection_method].append(detector.detector_name)
    
    print(f"\n🔍 Anomaly Detectors by Method:")
    for method, detectors in detectors_by_method.items():
        print(f"  {method.value.replace('_', ' ').title()}: {len(detectors)}")
        for detector in detectors[:1]:  # Show first detector
            print(f"    • {detector}")
    
    print(f"\n🚨 Running Real-time Detection...")
    
    # Simulate real-time anomaly detection
    sample_data_scenarios = [
        {
            "detector_type": "zoonotic_surveillance", 
            "data": {"case_count": 45, "prevalence_rate": 0.15, "temperature": 28.5}
        },
        {
            "detector_type": "environmental_health",
            "data": {"environmental_factor": 150, "humidity": 85, "pollution_level": 120}
        },
        {
            "detector_type": "food_safety", 
            "data": {"contamination_level": 25, "temperature": 8.5, "processing_time": 45}
        }
    ]
    
    new_detections = []
    for scenario in sample_data_scenarios:
        # Find suitable detector
        suitable_detectors = [
            d for d in engine.detectors.values() 
            if scenario["detector_type"] in d.data_domain
        ]
        
        if suitable_detectors:
            detector = suitable_detectors[0]
            detected = engine.run_anomaly_detection(detector.detector_id, scenario["data"])
            new_detections.extend(detected)
            
            print(f"  🔍 {detector.detector_name}: {len(detected)} anomalies detected")
            for anomaly in detected:
                print(f"    ⚠️ {anomaly.anomaly_type.value} - {anomaly.severity.value} severity")
    
    print(f"\n📊 Investigating Anomalies...")
    
    # Investigate some anomalies
    recent_anomalies = engine.detected_anomalies[-3:] if len(engine.detected_anomalies) >= 3 else engine.detected_anomalies
    for i, anomaly in enumerate(recent_anomalies):
        investigation_notes = f"Investigation {i+1}: {anomaly.anomaly_type.value} in {anomaly.health_domain}"
        is_false_positive = random.random() < 0.2  # 20% false positive rate
        
        engine.investigate_anomaly(anomaly.anomaly_id, investigation_notes, is_false_positive)
        
        status = "False Positive" if is_false_positive else "Confirmed"
        print(f"  📋 {anomaly.anomaly_id}: {status}")
    
    print(f"\n📋 Generating Anomaly Report...")
    
    # Generate comprehensive report
    anomaly_report = engine.generate_anomaly_report("Weekly Anomaly Detection Summary")
    
    print(f"  📋 Report Period: {anomaly_report.report_period_start.strftime('%Y-%m-%d')} to {anomaly_report.report_period_end.strftime('%Y-%m-%d')}")
    print(f"  🚨 Total Anomalies: {anomaly_report.total_anomalies_detected}")
    print(f"  📊 Detection Accuracy: {anomaly_report.detection_accuracy:.1%}")
    print(f"  🔍 Patterns Identified: {anomaly_report.patterns_identified}")
    
    return engine

def display_detection_results(engine: AnomalyDetectionEngine):
    """Display comprehensive anomaly detection results."""
    
    print(f"\n🚨 Anomaly Detection Results:")
    
    # System summary
    summary = engine.get_detection_summary()
    
    print(f"\n📊 Detection System Summary:")
    
    detectors = summary["detectors"]
    print(f"  Active Detectors: {detectors['active_detectors']}/{detectors['total_detectors']}")
    
    print(f"  Detectors by Method:")
    for method, count in detectors["by_method"].items():
        print(f"    {method.replace('_', ' ').title()}: {count}")
    
    anomalies = summary["anomalies"]
    print(f"\n  Anomaly Detection:")
    print(f"    Total Detected: {anomalies['total_detected']}")
    print(f"    Average Confidence: {anomalies['average_confidence']:.1%}")
    print(f"    Investigation Rate: {anomalies['investigation_rate']:.1%}")
    
    print(f"  Anomalies by Severity:")
    for severity, count in anomalies["by_severity"].items():
        print(f"    {severity.title()}: {count}")
    
    print(f"  Anomalies by Type:")
    for anom_type, count in anomalies["by_type"].items():
        print(f"    {anom_type.replace('_', ' ').title()}: {count}")
    
    patterns = summary["patterns"]
    print(f"\n  Pattern Analysis:")
    print(f"    Total Patterns: {patterns['total_patterns']}")
    print(f"    Outbreak Indicators: {patterns['outbreak_indicators']}")
    
    # Recent anomalies
    if engine.detected_anomalies:
        print(f"\n🚨 Recent Anomaly Detections:")
        for i, anomaly in enumerate(engine.detected_anomalies[-3:], 1):
            print(f"  {i}. {anomaly.anomaly_id}:")
            print(f"     Type: {anomaly.anomaly_type.value.replace('_', ' ').title()}")
            print(f"     Severity: {anomaly.severity.value.title()}")
            print(f"     Confidence: {anomaly.confidence_score:.1%}")
            print(f"     Domain: {anomaly.health_domain.replace('_', ' ').title()}")
            print(f"     Investigated: {'Yes' if anomaly.is_investigated else 'No'}")
    
    # Anomaly patterns
    if engine.anomaly_patterns:
        print(f"\n🔗 Identified Anomaly Patterns:")
        for i, pattern in enumerate(engine.anomaly_patterns[-2:], 1):
            print(f"  {i}. {pattern.pattern_name}:")
            print(f"     Type: {pattern.pattern_type.title()}")
            print(f"     Confidence: {pattern.pattern_confidence:.1%}")
            print(f"     Risk: {pattern.risk_assessment.title()}")
            print(f"     Anomalies: {len(pattern.related_anomalies)}")
            print(f"     Duration: {pattern.pattern_duration_hours:.1f} hours")
    
    # Latest report
    if engine.anomaly_reports:
        latest_report = engine.anomaly_reports[-1]
        print(f"\n📋 Latest Anomaly Report:")
        print(f"  Title: {latest_report.report_title}")
        print(f"  Total Anomalies: {latest_report.total_anomalies_detected}")
        print(f"  False Positive Rate: {latest_report.false_positive_rate:.1%}")
        print(f"  Critical Unresolved: {latest_report.critical_anomalies_unresolved}")
        
        if latest_report.top_anomalous_features:
            print(f"  Top Anomalous Features:")
            for feature, score in latest_report.top_anomalous_features[:3]:
                print(f"    {feature}: {score:.3f}")
    
    print(f"\n🏆 TOP PERFORMING Detectors:")
    
    # Sort detectors by performance (precision)
    top_detectors = sorted(engine.detectors.values(), key=lambda d: d.precision, reverse=True)[:3]
    
    for i, detector in enumerate(top_detectors, 1):
        print(f"  {i}. {detector.detector_name}")
        print(f"     Method: {detector.detection_method.value.replace('_', ' ').title()}")
        print(f"     Precision: {detector.precision:.1%}")
        print(f"     Detection Rate: {detector.detection_rate:.1%}")
        print(f"     FPR: {detector.false_positive_rate:.1%}")
        print(f"     Domain: {detector.data_domain.replace('_', ' ').title()}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    detection_engine = run_demonstration()
    display_detection_results(detection_engine)
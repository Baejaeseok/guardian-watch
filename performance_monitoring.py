"""
Performance Monitoring and Analytics System
==========================================
Module 5: Integration & Validation Tools

Advanced performance monitoring, analytics, and optimization for One Health platforms,
providing real-time performance insights and proactive system optimization.

NIW Focus: Performance intelligence enabling optimal One Health system operations and reliability.
"""

import json
import math
import statistics
import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable, Set
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque, Counter
import itertools
import random
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of performance metrics."""
    RESPONSE_TIME = "response_time"              # Response time metrics
    THROUGHPUT = "throughput"                    # Throughput/volume metrics
    AVAILABILITY = "availability"               # System availability metrics
    ERROR_RATE = "error_rate"                   # Error and failure rates
    RESOURCE_USAGE = "resource_usage"          # CPU, memory, disk usage
    LATENCY = "latency"                        # Network latency metrics
    CONCURRENCY = "concurrency"                # Concurrent user/process metrics
    SCALABILITY = "scalability"                # System scalability metrics

class ComponentType(Enum):
    """Types of monitored system components."""
    WEB_APPLICATION = "web_application"         # Web application components
    DATABASE = "database"                      # Database systems
    API_SERVICE = "api_service"                # API services
    INTEGRATION_SERVICE = "integration_service" # Integration services
    DATA_PROCESSOR = "data_processor"          # Data processing components
    SURVEILLANCE_ENGINE = "surveillance_engine" # Surveillance systems
    ANALYTICS_ENGINE = "analytics_engine"      # Analytics components
    REPORTING_SERVICE = "reporting_service"    # Reporting services

class AlertLevel(Enum):
    """Performance alert severity levels."""
    INFO = "info"                              # Informational
    WARNING = "warning"                        # Warning level
    CRITICAL = "critical"                      # Critical level
    EMERGENCY = "emergency"                    # Emergency level

class MetricStatus(Enum):
    """Performance metric status."""
    NORMAL = "normal"                          # Within normal range
    WARNING = "warning"                        # Approaching threshold
    CRITICAL = "critical"                      # Exceeding threshold
    UNKNOWN = "unknown"                        # Status unknown

@dataclass
class PerformanceMetric:
    """Individual performance metric measurement."""
    
    metric_id: str
    metric_name: str
    metric_type: MetricType
    component_type: ComponentType
    component_id: str
    
    # Metric values
    timestamp: datetime
    value: float
    unit: str                                  # Unit of measurement (ms, MB, %, etc.)
    
    # Context information
    measurement_method: str = "automated"      # How metric was collected
    sample_period_seconds: int = 60           # Sampling period
    tags: Dict[str, str] = field(default_factory=dict)  # Additional tags
    
    # Performance assessment
    baseline_value: Optional[float] = None     # Historical baseline
    threshold_warning: Optional[float] = None  # Warning threshold
    threshold_critical: Optional[float] = None # Critical threshold
    status: MetricStatus = MetricStatus.NORMAL
    
    # Statistical analysis
    percentile_rank: Optional[float] = None    # Percentile rank vs historical data
    z_score: Optional[float] = None           # Z-score vs baseline
    trend: str = "stable"                     # "increasing", "decreasing", "stable"

@dataclass
class PerformanceAlert:
    """Performance alert for threshold violations."""
    
    alert_id: str
    alert_level: AlertLevel
    metric_id: str
    component_id: str
    
    # Alert details
    triggered_timestamp: datetime
    alert_message: str
    threshold_value: float
    actual_value: float
    threshold_type: str                        # "warning" or "critical"
    
    # Alert resolution
    is_resolved: bool = False
    resolved_timestamp: Optional[datetime] = None
    resolution_notes: str = ""
    auto_resolved: bool = False
    
    # Impact assessment
    affected_users: int = 0                   # Estimated affected users
    business_impact: str = "low"              # "low", "medium", "high", "critical"
    estimated_downtime_seconds: float = 0.0
    
    # Response tracking
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_timestamp: Optional[datetime] = None
    response_time_seconds: float = 0.0        # Time to acknowledge

@dataclass
class SystemHealthSnapshot:
    """System health snapshot at a point in time."""
    
    snapshot_id: str
    timestamp: datetime
    
    # Overall health metrics
    overall_health_score: float = 0.0         # 0-100 scale
    availability_percentage: float = 0.0      # System availability %
    performance_score: float = 0.0           # Performance score
    
    # Component health
    healthy_components: int = 0
    warning_components: int = 0
    critical_components: int = 0
    unknown_components: int = 0
    
    # System resource utilization
    cpu_utilization_percent: float = 0.0
    memory_utilization_percent: float = 0.0
    disk_utilization_percent: float = 0.0
    network_utilization_percent: float = 0.0
    
    # Performance indicators
    average_response_time_ms: float = 0.0
    requests_per_second: float = 0.0
    error_rate_percent: float = 0.0
    active_users: int = 0
    
    # Alert summary
    active_alerts: int = 0
    warning_alerts: int = 0
    critical_alerts: int = 0
    emergency_alerts: int = 0

@dataclass
class PerformanceTrend:
    """Performance trend analysis."""
    
    trend_id: str
    metric_name: str
    component_id: str
    analysis_period_start: datetime
    analysis_period_end: datetime
    
    # Trend analysis
    trend_direction: str = "stable"            # "increasing", "decreasing", "stable"
    trend_strength: float = 0.0              # 0-1 scale (weak to strong)
    rate_of_change: float = 0.0              # Rate of change per time unit
    correlation_coefficient: float = 0.0      # Correlation with time
    
    # Statistical analysis
    data_points: int = 0
    mean_value: float = 0.0
    median_value: float = 0.0
    standard_deviation: float = 0.0
    min_value: float = 0.0
    max_value: float = 0.0
    
    # Forecasting
    predicted_value_1h: Optional[float] = None   # 1 hour forecast
    predicted_value_24h: Optional[float] = None  # 24 hour forecast
    confidence_interval: Tuple[float, float] = (0.0, 0.0)  # 95% confidence interval
    
    # Anomaly detection
    anomalies_detected: int = 0
    anomaly_timestamps: List[datetime] = field(default_factory=list)
    anomaly_severity: str = "none"           # "none", "minor", "moderate", "major"

@dataclass
class PerformanceReport:
    """Comprehensive performance report."""
    
    report_id: str
    report_title: str
    report_period_start: datetime
    report_period_end: datetime
    generation_timestamp: datetime
    
    # Report scope
    monitored_components: List[str] = field(default_factory=list)
    metrics_analyzed: int = 0
    data_points_collected: int = 0
    
    # Performance summary
    overall_system_performance: float = 0.0   # 0-100 scale
    average_availability: float = 0.0         # Average availability %
    peak_performance_period: str = ""         # Best performing time period
    worst_performance_period: str = ""        # Worst performing time period
    
    # Component performance
    best_performing_component: str = ""
    worst_performing_component: str = ""
    components_meeting_sla: int = 0
    components_below_sla: int = 0
    
    # Alert analysis
    total_alerts_generated: int = 0
    critical_incidents: int = 0
    average_resolution_time_minutes: float = 0.0
    false_positive_rate: float = 0.0
    
    # Trend analysis
    performance_trends: List[PerformanceTrend] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Resource utilization
    peak_cpu_usage: float = 0.0
    peak_memory_usage: float = 0.0
    peak_network_usage: float = 0.0
    resource_optimization_opportunities: List[str] = field(default_factory=list)

class PerformanceMonitoringManager:
    """Central performance monitoring and analytics system."""
    
    def __init__(self):
        self.performance_metrics: List[PerformanceMetric] = []
        self.performance_alerts: List[PerformanceAlert] = []
        self.health_snapshots: List[SystemHealthSnapshot] = []
        self.performance_trends: List[PerformanceTrend] = []
        self.performance_reports: List[PerformanceReport] = []
        
        # Monitoring configuration
        self.monitoring_interval_seconds = 60
        self.metric_retention_days = 30
        self.alert_thresholds: Dict[str, Dict[str, float]] = {}
        
        # Historical data for baseline calculations
        self.historical_baselines: Dict[str, List[float]] = defaultdict(list)
        
        # Initialize monitoring framework
        self._initialize_monitoring_framework()
        
        logger.info("One Health Performance Monitoring Manager initialized")
    
    def _initialize_monitoring_framework(self):
        """Initialize performance monitoring framework."""
        
        # Default alert thresholds for different metrics
        default_thresholds = {
            "response_time_ms": {"warning": 1000.0, "critical": 3000.0},
            "cpu_utilization_percent": {"warning": 75.0, "critical": 90.0},
            "memory_utilization_percent": {"warning": 80.0, "critical": 95.0},
            "disk_utilization_percent": {"warning": 85.0, "critical": 95.0},
            "error_rate_percent": {"warning": 2.0, "critical": 5.0},
            "availability_percent": {"warning": 99.0, "critical": 95.0},
            "throughput_rps": {"warning": 10.0, "critical": 5.0}  # Minimum thresholds
        }
        
        self.alert_thresholds = default_thresholds
        
        logger.info("Performance monitoring thresholds configured")
    
    def collect_metric(self, metric_name: str, metric_type: MetricType, component_type: ComponentType,
                      component_id: str, value: float, unit: str, tags: Dict[str, str] = None) -> PerformanceMetric:
        """Collect a performance metric."""
        
        metric_id = f"METRIC_{random.randint(100000, 999999)}"
        
        # Get thresholds for this metric type
        threshold_key = f"{metric_type.value}_{unit.lower()}"
        thresholds = self.alert_thresholds.get(threshold_key, {})
        
        # Create metric
        metric = PerformanceMetric(
            metric_id=metric_id,
            metric_name=metric_name,
            metric_type=metric_type,
            component_type=component_type,
            component_id=component_id,
            timestamp=datetime.now(),
            value=value,
            unit=unit,
            threshold_warning=thresholds.get("warning"),
            threshold_critical=thresholds.get("critical"),
            tags=tags or {}
        )
        
        # Calculate baseline and statistical metrics
        self._analyze_metric_performance(metric)
        
        # Determine metric status
        metric.status = self._determine_metric_status(metric)
        
        # Check for alert conditions
        if metric.status in [MetricStatus.WARNING, MetricStatus.CRITICAL]:
            self._generate_performance_alert(metric)
        
        # Store historical data for baseline calculations
        historical_key = f"{component_id}_{metric_type.value}"
        self.historical_baselines[historical_key].append(value)
        
        # Limit historical data size
        if len(self.historical_baselines[historical_key]) > 1000:
            self.historical_baselines[historical_key] = self.historical_baselines[historical_key][-1000:]
        
        self.performance_metrics.append(metric)
        
        return metric
    
    def _analyze_metric_performance(self, metric: PerformanceMetric):
        """Analyze metric performance against historical data."""
        
        historical_key = f"{metric.component_id}_{metric.metric_type.value}"
        historical_data = self.historical_baselines.get(historical_key, [])
        
        if len(historical_data) >= 10:  # Need sufficient historical data
            # Calculate baseline
            metric.baseline_value = statistics.mean(historical_data)
            
            # Calculate percentile rank
            sorted_data = sorted(historical_data + [metric.value])
            rank = sorted_data.index(metric.value) + 1
            metric.percentile_rank = (rank / len(sorted_data)) * 100
            
            # Calculate z-score
            std_dev = statistics.stdev(historical_data) if len(historical_data) > 1 else 1.0
            if std_dev > 0:
                metric.z_score = (metric.value - metric.baseline_value) / std_dev
            
            # Determine trend (simplified)
            if len(historical_data) >= 5:
                recent_avg = statistics.mean(historical_data[-5:])
                older_avg = statistics.mean(historical_data[-10:-5]) if len(historical_data) >= 10 else recent_avg
                
                if recent_avg > older_avg * 1.1:
                    metric.trend = "increasing"
                elif recent_avg < older_avg * 0.9:
                    metric.trend = "decreasing"
                else:
                    metric.trend = "stable"
    
    def _determine_metric_status(self, metric: PerformanceMetric) -> MetricStatus:
        """Determine metric status based on thresholds."""
        
        if metric.threshold_critical is not None:
            # For metrics where higher is worse (response time, error rate, etc.)
            if metric.metric_type in [MetricType.RESPONSE_TIME, MetricType.ERROR_RATE, MetricType.RESOURCE_USAGE]:
                if metric.value >= metric.threshold_critical:
                    return MetricStatus.CRITICAL
                elif metric.threshold_warning is not None and metric.value >= metric.threshold_warning:
                    return MetricStatus.WARNING
            # For metrics where lower is worse (availability, throughput, etc.)
            elif metric.metric_type in [MetricType.AVAILABILITY, MetricType.THROUGHPUT]:
                if metric.value <= metric.threshold_critical:
                    return MetricStatus.CRITICAL
                elif metric.threshold_warning is not None and metric.value <= metric.threshold_warning:
                    return MetricStatus.WARNING
        
        return MetricStatus.NORMAL
    
    def _generate_performance_alert(self, metric: PerformanceMetric):
        """Generate performance alert for threshold violations."""
        
        alert_id = f"ALERT_{random.randint(100000, 999999)}"
        
        # Determine alert level and threshold info
        if metric.status == MetricStatus.CRITICAL:
            alert_level = AlertLevel.CRITICAL
            threshold_value = metric.threshold_critical
            threshold_type = "critical"
        elif metric.status == MetricStatus.WARNING:
            alert_level = AlertLevel.WARNING
            threshold_value = metric.threshold_warning
            threshold_type = "warning"
        else:
            return  # No alert needed
        
        # Create alert message
        if metric.metric_type in [MetricType.RESPONSE_TIME, MetricType.ERROR_RATE, MetricType.RESOURCE_USAGE]:
            alert_message = f"{metric.metric_name} exceeds {threshold_type} threshold: {metric.value:.2f} {metric.unit} > {threshold_value} {metric.unit}"
        else:
            alert_message = f"{metric.metric_name} below {threshold_type} threshold: {metric.value:.2f} {metric.unit} < {threshold_value} {metric.unit}"
        
        alert = PerformanceAlert(
            alert_id=alert_id,
            alert_level=alert_level,
            metric_id=metric.metric_id,
            component_id=metric.component_id,
            triggered_timestamp=datetime.now(),
            alert_message=alert_message,
            threshold_value=threshold_value,
            actual_value=metric.value,
            threshold_type=threshold_type
        )
        
        # Estimate impact
        if alert_level == AlertLevel.CRITICAL:
            alert.business_impact = "high"
            alert.affected_users = random.randint(100, 1000)
        elif alert_level == AlertLevel.WARNING:
            alert.business_impact = "medium"
            alert.affected_users = random.randint(10, 100)
        
        self.performance_alerts.append(alert)
        
        logger.warning(f"Performance alert generated: {alert_id} - {alert_level.value}")
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str, notes: str = ""):
        """Acknowledge a performance alert."""
        
        alert = None
        for pa in self.performance_alerts:
            if pa.alert_id == alert_id:
                alert = pa
                break
        
        if not alert:
            return False
        
        alert.acknowledged = True
        alert.acknowledged_by = acknowledged_by
        alert.acknowledged_timestamp = datetime.now()
        alert.resolution_notes = notes
        alert.response_time_seconds = (datetime.now() - alert.triggered_timestamp).total_seconds()
        
        logger.info(f"Performance alert acknowledged: {alert_id}")
        
        return True
    
    def resolve_alert(self, alert_id: str, resolution_notes: str = "", auto_resolved: bool = False):
        """Resolve a performance alert."""
        
        alert = None
        for pa in self.performance_alerts:
            if pa.alert_id == alert_id:
                alert = pa
                break
        
        if not alert:
            return False
        
        alert.is_resolved = True
        alert.resolved_timestamp = datetime.now()
        alert.resolution_notes = resolution_notes
        alert.auto_resolved = auto_resolved
        
        logger.info(f"Performance alert resolved: {alert_id}")
        
        return True
    
    def capture_system_health_snapshot(self) -> SystemHealthSnapshot:
        """Capture current system health snapshot."""
        
        snapshot_id = f"SNAP_{random.randint(100000, 999999)}"
        
        snapshot = SystemHealthSnapshot(
            snapshot_id=snapshot_id,
            timestamp=datetime.now()
        )
        
        # Get recent metrics (last 5 minutes)
        recent_time = datetime.now() - timedelta(minutes=5)
        recent_metrics = [m for m in self.performance_metrics if m.timestamp >= recent_time]
        
        if recent_metrics:
            # Component health analysis
            component_statuses = Counter(m.status for m in recent_metrics)
            snapshot.healthy_components = component_statuses.get(MetricStatus.NORMAL, 0)
            snapshot.warning_components = component_statuses.get(MetricStatus.WARNING, 0)
            snapshot.critical_components = component_statuses.get(MetricStatus.CRITICAL, 0)
            snapshot.unknown_components = component_statuses.get(MetricStatus.UNKNOWN, 0)
            
            # Performance indicators
            response_time_metrics = [m for m in recent_metrics if m.metric_type == MetricType.RESPONSE_TIME]
            if response_time_metrics:
                snapshot.average_response_time_ms = statistics.mean(m.value for m in response_time_metrics)
            
            throughput_metrics = [m for m in recent_metrics if m.metric_type == MetricType.THROUGHPUT]
            if throughput_metrics:
                snapshot.requests_per_second = statistics.mean(m.value for m in throughput_metrics)
            
            error_rate_metrics = [m for m in recent_metrics if m.metric_type == MetricType.ERROR_RATE]
            if error_rate_metrics:
                snapshot.error_rate_percent = statistics.mean(m.value for m in error_rate_metrics)
            
            availability_metrics = [m for m in recent_metrics if m.metric_type == MetricType.AVAILABILITY]
            if availability_metrics:
                snapshot.availability_percentage = statistics.mean(m.value for m in availability_metrics)
        
        # System resource utilization (simulated)
        snapshot.cpu_utilization_percent = random.uniform(10, 85)
        snapshot.memory_utilization_percent = random.uniform(20, 80)
        snapshot.disk_utilization_percent = random.uniform(15, 75)
        snapshot.network_utilization_percent = random.uniform(5, 60)
        
        # Calculate overall health score
        health_factors = [
            min(100, 100 - snapshot.cpu_utilization_percent),
            min(100, 100 - snapshot.memory_utilization_percent),
            snapshot.availability_percentage,
            max(0, 100 - snapshot.error_rate_percent * 20)  # Error rate impact
        ]
        
        snapshot.overall_health_score = statistics.mean(health_factors)
        snapshot.performance_score = snapshot.overall_health_score  # Simplified
        
        # Active alerts
        active_alerts = [a for a in self.performance_alerts if not a.is_resolved]
        snapshot.active_alerts = len(active_alerts)
        snapshot.warning_alerts = len([a for a in active_alerts if a.alert_level == AlertLevel.WARNING])
        snapshot.critical_alerts = len([a for a in active_alerts if a.alert_level == AlertLevel.CRITICAL])
        snapshot.emergency_alerts = len([a for a in active_alerts if a.alert_level == AlertLevel.EMERGENCY])
        
        # Simulated active users
        snapshot.active_users = random.randint(50, 500)
        
        self.health_snapshots.append(snapshot)
        
        return snapshot
    
    def analyze_performance_trends(self, component_id: str, metric_type: MetricType,
                                 analysis_period_hours: int = 24) -> PerformanceTrend:
        """Analyze performance trends for specific component and metric."""
        
        trend_id = f"TREND_{random.randint(100000, 999999)}"
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=analysis_period_hours)
        
        # Filter relevant metrics
        relevant_metrics = [
            m for m in self.performance_metrics
            if (m.component_id == component_id and 
                m.metric_type == metric_type and
                start_time <= m.timestamp <= end_time)
        ]
        
        trend = PerformanceTrend(
            trend_id=trend_id,
            metric_name=f"{component_id}_{metric_type.value}",
            component_id=component_id,
            analysis_period_start=start_time,
            analysis_period_end=end_time
        )
        
        if len(relevant_metrics) >= 3:  # Need minimum data points
            values = [m.value for m in relevant_metrics]
            timestamps = [m.timestamp for m in relevant_metrics]
            
            # Statistical analysis
            trend.data_points = len(values)
            trend.mean_value = statistics.mean(values)
            trend.median_value = statistics.median(values)
            trend.standard_deviation = statistics.stdev(values) if len(values) > 1 else 0.0
            trend.min_value = min(values)
            trend.max_value = max(values)
            
            # Trend analysis (simplified linear trend)
            if len(values) >= 5:
                # Calculate correlation with time
                time_values = [(ts - start_time).total_seconds() for ts in timestamps]
                
                if len(set(time_values)) > 1 and trend.standard_deviation > 0:
                    # Simple correlation calculation
                    mean_time = statistics.mean(time_values)
                    mean_value = trend.mean_value
                    
                    numerator = sum((t - mean_time) * (v - mean_value) 
                                  for t, v in zip(time_values, values))
                    denominator = (sum((t - mean_time) ** 2 for t in time_values) * 
                                 sum((v - mean_value) ** 2 for v in values)) ** 0.5
                    
                    if denominator > 0:
                        trend.correlation_coefficient = numerator / denominator
                        
                        # Determine trend direction and strength
                        if abs(trend.correlation_coefficient) > 0.7:
                            trend.trend_strength = abs(trend.correlation_coefficient)
                            if trend.correlation_coefficient > 0:
                                trend.trend_direction = "increasing"
                            else:
                                trend.trend_direction = "decreasing"
                        else:
                            trend.trend_direction = "stable"
                            trend.trend_strength = 1 - abs(trend.correlation_coefficient)
                
                # Simple forecasting (linear extrapolation)
                if trend.correlation_coefficient and abs(trend.correlation_coefficient) > 0.3:
                    rate_per_hour = (values[-1] - values[0]) / analysis_period_hours
                    trend.rate_of_change = rate_per_hour
                    trend.predicted_value_1h = values[-1] + rate_per_hour
                    trend.predicted_value_24h = values[-1] + (rate_per_hour * 24)
                    
                    # Confidence interval (simplified)
                    margin = trend.standard_deviation * 1.96  # 95% confidence
                    if trend.predicted_value_24h:
                        trend.confidence_interval = (
                            trend.predicted_value_24h - margin,
                            trend.predicted_value_24h + margin
                        )
            
            # Anomaly detection (simple threshold-based)
            if trend.standard_deviation > 0:
                threshold = trend.mean_value + (2 * trend.standard_deviation)
                anomalies = [m for m in relevant_metrics if abs(m.value - trend.mean_value) > threshold]
                trend.anomalies_detected = len(anomalies)
                trend.anomaly_timestamps = [a.timestamp for a in anomalies]
                
                if trend.anomalies_detected > len(values) * 0.1:  # >10% anomalies
                    trend.anomaly_severity = "major"
                elif trend.anomalies_detected > len(values) * 0.05:  # >5% anomalies
                    trend.anomaly_severity = "moderate"
                elif trend.anomalies_detected > 0:
                    trend.anomaly_severity = "minor"
        
        self.performance_trends.append(trend)
        
        return trend
    
    def generate_performance_report(self, report_title: str, period_hours: int = 24) -> PerformanceReport:
        """Generate comprehensive performance report."""
        
        report_id = f"PERF_RPT_{random.randint(100000, 999999)}"
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=period_hours)
        
        report = PerformanceReport(
            report_id=report_id,
            report_title=report_title,
            report_period_start=start_time,
            report_period_end=end_time,
            generation_timestamp=datetime.now()
        )
        
        # Filter data for report period
        period_metrics = [m for m in self.performance_metrics if start_time <= m.timestamp <= end_time]
        period_alerts = [a for a in self.performance_alerts if start_time <= a.triggered_timestamp <= end_time]
        period_snapshots = [s for s in self.health_snapshots if start_time <= s.timestamp <= end_time]
        
        # Basic report statistics
        report.metrics_analyzed = len(period_metrics)
        report.data_points_collected = len(period_metrics)
        report.monitored_components = list(set(m.component_id for m in period_metrics))
        
        # Performance summary
        if period_metrics:
            availability_metrics = [m for m in period_metrics if m.metric_type == MetricType.AVAILABILITY]
            if availability_metrics:
                report.average_availability = statistics.mean(m.value for m in availability_metrics)
        
        if period_snapshots:
            report.overall_system_performance = statistics.mean(s.overall_health_score for s in period_snapshots)
        
        # Component performance analysis
        component_performance = {}
        for component_id in report.monitored_components:
            component_metrics = [m for m in period_metrics if m.component_id == component_id]
            if component_metrics:
                # Calculate component score based on metric status
                normal_metrics = len([m for m in component_metrics if m.status == MetricStatus.NORMAL])
                component_score = (normal_metrics / len(component_metrics)) * 100
                component_performance[component_id] = component_score
        
        if component_performance:
            report.best_performing_component = max(component_performance, key=component_performance.get)
            report.worst_performing_component = min(component_performance, key=component_performance.get)
            
            # SLA compliance (assuming 95% threshold)
            sla_threshold = 95.0
            report.components_meeting_sla = len([c for c, score in component_performance.items() 
                                               if score >= sla_threshold])
            report.components_below_sla = len(component_performance) - report.components_meeting_sla
        
        # Alert analysis
        report.total_alerts_generated = len(period_alerts)
        report.critical_incidents = len([a for a in period_alerts if a.alert_level == AlertLevel.CRITICAL])
        
        resolved_alerts = [a for a in period_alerts if a.is_resolved and a.resolved_timestamp]
        if resolved_alerts:
            resolution_times = [(a.resolved_timestamp - a.triggered_timestamp).total_seconds() / 60 
                              for a in resolved_alerts]
            report.average_resolution_time_minutes = statistics.mean(resolution_times)
        
        # Resource utilization
        if period_snapshots:
            report.peak_cpu_usage = max(s.cpu_utilization_percent for s in period_snapshots)
            report.peak_memory_usage = max(s.memory_utilization_percent for s in period_snapshots)
            report.peak_network_usage = max(s.network_utilization_percent for s in period_snapshots)
        
        # Generate insights and recommendations
        report.key_insights = self._generate_performance_insights(report, period_metrics, period_alerts)
        report.recommendations = self._generate_performance_recommendations(report)
        report.resource_optimization_opportunities = self._identify_optimization_opportunities(report)
        
        # Identify peak performance periods
        if period_snapshots:
            best_snapshot = max(period_snapshots, key=lambda s: s.overall_health_score)
            worst_snapshot = min(period_snapshots, key=lambda s: s.overall_health_score)
            
            report.peak_performance_period = best_snapshot.timestamp.strftime("%Y-%m-%d %H:%M")
            report.worst_performance_period = worst_snapshot.timestamp.strftime("%Y-%m-%d %H:%M")
        
        self.performance_reports.append(report)
        
        logger.info(f"Performance report generated: {report_id}")
        
        return report
    
    def _generate_performance_insights(self, report: PerformanceReport, metrics: List[PerformanceMetric],
                                     alerts: List[PerformanceAlert]) -> List[str]:
        """Generate key performance insights."""
        
        insights = []
        
        # System performance insights
        if report.overall_system_performance >= 95:
            insights.append("Excellent system performance with minimal issues")
        elif report.overall_system_performance >= 85:
            insights.append("Good system performance with occasional issues")
        elif report.overall_system_performance < 75:
            insights.append("System performance below acceptable levels")
        
        # Alert insights
        if report.critical_incidents > 0:
            insights.append(f"Critical incidents detected: {report.critical_incidents} requiring immediate attention")
        
        # Component insights
        if report.components_below_sla > 0:
            insights.append(f"{report.components_below_sla} components not meeting SLA requirements")
        
        # Resource utilization insights
        if report.peak_cpu_usage > 90:
            insights.append("High CPU utilization detected, consider scaling resources")
        
        if report.peak_memory_usage > 85:
            insights.append("High memory utilization may impact performance")
        
        return insights[:5]  # Limit to 5 insights
    
    def _generate_performance_recommendations(self, report: PerformanceReport) -> List[str]:
        """Generate performance improvement recommendations."""
        
        recommendations = []
        
        if report.overall_system_performance < 90:
            recommendations.append("Implement proactive monitoring and alerting for early issue detection")
        
        if report.components_below_sla > 0:
            recommendations.append("Review and optimize underperforming components")
        
        if report.average_resolution_time_minutes > 30:
            recommendations.append("Improve incident response procedures to reduce resolution time")
        
        if report.peak_cpu_usage > 80:
            recommendations.append("Consider horizontal scaling or resource optimization")
        
        if report.critical_incidents > 5:
            recommendations.append("Implement additional redundancy and failover mechanisms")
        
        if not recommendations:
            recommendations.append("Continue current monitoring practices and maintain performance levels")
        
        return recommendations[:5]
    
    def _identify_optimization_opportunities(self, report: PerformanceReport) -> List[str]:
        """Identify resource optimization opportunities."""
        
        opportunities = []
        
        if report.peak_cpu_usage < 30:
            opportunities.append("CPU resources underutilized - consider downsizing")
        
        if report.peak_memory_usage < 40:
            opportunities.append("Memory resources underutilized - optimize allocation")
        
        if report.peak_network_usage < 20:
            opportunities.append("Network capacity underutilized - review bandwidth allocation")
        
        if report.average_availability > 99.5:
            opportunities.append("High availability achieved - review if over-provisioned")
        
        return opportunities
    
    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time performance dashboard data."""
        
        # Recent metrics (last 5 minutes)
        recent_time = datetime.now() - timedelta(minutes=5)
        recent_metrics = [m for m in self.performance_metrics if m.timestamp >= recent_time]
        
        # Active alerts
        active_alerts = [a for a in self.performance_alerts if not a.is_resolved]
        
        # Latest health snapshot
        latest_snapshot = self.health_snapshots[-1] if self.health_snapshots else None
        
        dashboard = {
            "timestamp": datetime.now(),
            "system_status": "healthy",
            "total_components_monitored": len(set(m.component_id for m in recent_metrics)),
            "metrics_collected_5min": len(recent_metrics),
            "active_alerts": len(active_alerts),
            "critical_alerts": len([a for a in active_alerts if a.alert_level == AlertLevel.CRITICAL])
        }
        
        if latest_snapshot:
            dashboard.update({
                "overall_health_score": latest_snapshot.overall_health_score,
                "availability_percentage": latest_snapshot.availability_percentage,
                "average_response_time_ms": latest_snapshot.average_response_time_ms,
                "error_rate_percent": latest_snapshot.error_rate_percent,
                "cpu_utilization": latest_snapshot.cpu_utilization_percent,
                "memory_utilization": latest_snapshot.memory_utilization_percent,
                "active_users": latest_snapshot.active_users
            })
            
            # Determine system status
            if latest_snapshot.overall_health_score >= 95:
                dashboard["system_status"] = "excellent"
            elif latest_snapshot.overall_health_score >= 85:
                dashboard["system_status"] = "good"
            elif latest_snapshot.overall_health_score >= 70:
                dashboard["system_status"] = "fair"
            else:
                dashboard["system_status"] = "poor"
        
        return dashboard
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring system summary."""
        
        # Metrics summary
        total_metrics = len(self.performance_metrics)
        recent_metrics = [m for m in self.performance_metrics 
                         if (datetime.now() - m.timestamp).total_seconds() < 86400]
        
        # Alert summary
        total_alerts = len(self.performance_alerts)
        active_alerts = [a for a in self.performance_alerts if not a.is_resolved]
        
        # Component summary
        monitored_components = list(set(m.component_id for m in self.performance_metrics))
        
        return {
            "monitoring_overview": {
                "total_metrics_collected": total_metrics,
                "metrics_last_24h": len(recent_metrics),
                "monitored_components": len(monitored_components),
                "monitoring_interval_seconds": self.monitoring_interval_seconds
            },
            "alert_summary": {
                "total_alerts": total_alerts,
                "active_alerts": len(active_alerts),
                "resolved_alerts": total_alerts - len(active_alerts),
                "alerts_by_level": Counter(a.alert_level for a in active_alerts)
            },
            "health_tracking": {
                "health_snapshots": len(self.health_snapshots),
                "performance_trends": len(self.performance_trends),
                "performance_reports": len(self.performance_reports)
            },
            "system_components": {
                "component_types": Counter(m.component_type for m in self.performance_metrics),
                "metric_types": Counter(m.metric_type for m in self.performance_metrics)
            }
        }

def run_demonstration() -> PerformanceMonitoringManager:
    """Run comprehensive performance monitoring demonstration."""
    
    print("📊 One Health Performance Monitoring System - Demonstration")
    print("=" * 70)
    
    manager = PerformanceMonitoringManager()
    
    print(f"\n📊 Monitoring Framework:")
    print(f"  Metric Types: {len(MetricType)}")
    print(f"  Component Types: {len(ComponentType)}")
    print(f"  Alert Levels: {len(AlertLevel)}")
    
    print(f"\n📈 Collecting Performance Metrics...")
    
    # Simulate performance metrics collection
    metric_scenarios = [
        # Response time metrics
        {"name": "API Response Time", "type": MetricType.RESPONSE_TIME, "component": ComponentType.API_SERVICE,
         "id": "surveillance_api", "value": 450.0, "unit": "ms"},
        {"name": "Database Query Time", "type": MetricType.RESPONSE_TIME, "component": ComponentType.DATABASE,
         "id": "surveillance_db", "value": 120.0, "unit": "ms"},
        
        # Resource usage metrics
        {"name": "CPU Utilization", "type": MetricType.RESOURCE_USAGE, "component": ComponentType.WEB_APPLICATION,
         "id": "dashboard_app", "value": 65.0, "unit": "percent"},
        {"name": "Memory Usage", "type": MetricType.RESOURCE_USAGE, "component": ComponentType.DATA_PROCESSOR,
         "id": "analytics_engine", "value": 78.0, "unit": "percent"},
        
        # Throughput metrics
        {"name": "Requests per Second", "type": MetricType.THROUGHPUT, "component": ComponentType.API_SERVICE,
         "id": "surveillance_api", "value": 850.0, "unit": "rps"},
        {"name": "Data Processing Rate", "type": MetricType.THROUGHPUT, "component": ComponentType.DATA_PROCESSOR,
         "id": "analytics_engine", "value": 1250.0, "unit": "records/min"},
        
        # Availability metrics
        {"name": "System Availability", "type": MetricType.AVAILABILITY, "component": ComponentType.WEB_APPLICATION,
         "id": "dashboard_app", "value": 99.8, "unit": "percent"},
        {"name": "Database Availability", "type": MetricType.AVAILABILITY, "component": ComponentType.DATABASE,
         "id": "surveillance_db", "value": 99.9, "unit": "percent"},
        
        # Error rate metrics
        {"name": "API Error Rate", "type": MetricType.ERROR_RATE, "component": ComponentType.API_SERVICE,
         "id": "surveillance_api", "value": 0.5, "unit": "percent"},
        {"name": "Processing Error Rate", "type": MetricType.ERROR_RATE, "component": ComponentType.DATA_PROCESSOR,
         "id": "analytics_engine", "value": 1.2, "unit": "percent"}
    ]
    
    collected_metrics = []
    for scenario in metric_scenarios:
        metric = manager.collect_metric(
            scenario["name"], scenario["type"], scenario["component"],
            scenario["id"], scenario["value"], scenario["unit"]
        )
        collected_metrics.append(metric)
        
        status_icon = "✅" if metric.status == MetricStatus.NORMAL else "⚠️" if metric.status == MetricStatus.WARNING else "❌"
        print(f"  {status_icon} {metric.metric_name}: {metric.value} {metric.unit} ({metric.status.value})")
    
    print(f"\n📊 Capturing System Health Snapshots...")
    
    # Capture multiple health snapshots
    snapshots = []
    for i in range(3):
        snapshot = manager.capture_system_health_snapshot()
        snapshots.append(snapshot)
        print(f"  📊 Snapshot {i+1}: {snapshot.overall_health_score:.1f}% health score")
        time.sleep(0.1)  # Small delay between snapshots
    
    print(f"\n🔍 Analyzing Performance Trends...")
    
    # Analyze trends for key components
    trend_scenarios = [
        {"component": "surveillance_api", "metric": MetricType.RESPONSE_TIME},
        {"component": "analytics_engine", "metric": MetricType.THROUGHPUT},
        {"component": "dashboard_app", "metric": MetricType.RESOURCE_USAGE}
    ]
    
    trends_analyzed = []
    for scenario in trend_scenarios:
        trend = manager.analyze_performance_trends(scenario["component"], scenario["metric"])
        trends_analyzed.append(trend)
        print(f"  🔍 {scenario['component']} {scenario['metric'].value}: {trend.trend_direction} trend")
    
    print(f"\n📋 Generating Performance Report...")
    
    # Generate comprehensive performance report
    report = manager.generate_performance_report("System Performance Analysis Report")
    
    print(f"  📋 Report: {report.overall_system_performance:.1f}% system performance")
    print(f"  📋 Availability: {report.average_availability:.1f}%")
    print(f"  📋 Alerts: {report.total_alerts_generated} generated, {report.critical_incidents} critical")
    print(f"  📋 Components: {len(report.monitored_components)} monitored")
    
    return manager

def display_monitoring_results(manager: PerformanceMonitoringManager):
    """Display comprehensive performance monitoring results."""
    
    print(f"\n📊 Performance Monitoring Results:")
    
    # Real-time dashboard
    dashboard = manager.get_real_time_dashboard()
    
    print(f"\n🎯 Real-Time Dashboard:")
    print(f"  System Status: {dashboard['system_status'].title()}")
    print(f"  Overall Health: {dashboard.get('overall_health_score', 0):.1f}%")
    print(f"  Availability: {dashboard.get('availability_percentage', 0):.1f}%")
    print(f"  Avg Response Time: {dashboard.get('average_response_time_ms', 0):.1f}ms")
    print(f"  Error Rate: {dashboard.get('error_rate_percent', 0):.1f}%")
    print(f"  Active Users: {dashboard.get('active_users', 0)}")
    print(f"  CPU Usage: {dashboard.get('cpu_utilization', 0):.1f}%")
    print(f"  Memory Usage: {dashboard.get('memory_utilization', 0):.1f}%")
    
    # Recent metrics summary
    recent_metrics = [m for m in manager.performance_metrics
                     if (datetime.now() - m.timestamp).total_seconds() < 3600]
    
    print(f"\n📈 Performance Metrics (Last Hour: {len(recent_metrics)} metrics):")
    
    if recent_metrics:
        # Metrics by status
        status_counts = Counter(m.status for m in recent_metrics)
        for status, count in status_counts.items():
            print(f"  {status.value.title()}: {count} metrics")
        
        # Metrics by type
        type_counts = Counter(m.metric_type for m in recent_metrics)
        print(f"\n  Metrics by Type:")
        for metric_type, count in type_counts.items():
            print(f"    {metric_type.value.replace('_', ' ').title()}: {count}")
    
    # Alert analysis
    active_alerts = [a for a in manager.performance_alerts if not a.is_resolved]
    resolved_alerts = [a for a in manager.performance_alerts if a.is_resolved]
    
    print(f"\n🚨 Performance Alerts:")
    print(f"  Active Alerts: {len(active_alerts)}")
    print(f"  Resolved Alerts: {len(resolved_alerts)}")
    
    if active_alerts:
        alert_level_counts = Counter(a.alert_level for a in active_alerts)
        print(f"  Active Alerts by Level:")
        for level, count in alert_level_counts.items():
            print(f"    {level.value.title()}: {count}")
    
    # Health snapshots
    if manager.health_snapshots:
        latest_snapshot = manager.health_snapshots[-1]
        print(f"\n💗 System Health (Latest Snapshot):")
        print(f"  Overall Health: {latest_snapshot.overall_health_score:.1f}%")
        print(f"  Healthy Components: {latest_snapshot.healthy_components}")
        print(f"  Warning Components: {latest_snapshot.warning_components}")
        print(f"  Critical Components: {latest_snapshot.critical_components}")
        print(f"  Resource Utilization:")
        print(f"    CPU: {latest_snapshot.cpu_utilization_percent:.1f}%")
        print(f"    Memory: {latest_snapshot.memory_utilization_percent:.1f}%")
        print(f"    Disk: {latest_snapshot.disk_utilization_percent:.1f}%")
        print(f"    Network: {latest_snapshot.network_utilization_percent:.1f}%")
    
    # Performance trends
    if manager.performance_trends:
        print(f"\n📈 Performance Trends ({len(manager.performance_trends)} analyzed):")
        for trend in manager.performance_trends[-3:]:  # Show last 3
            print(f"  {trend.metric_name}:")
            print(f"    Trend: {trend.trend_direction.title()} (strength: {trend.trend_strength:.2f})")
            print(f"    Data Points: {trend.data_points}")
            print(f"    Mean Value: {trend.mean_value:.2f}")
            if trend.anomalies_detected > 0:
                print(f"    Anomalies: {trend.anomalies_detected} detected ({trend.anomaly_severity})")
    
    # System summary
    summary = manager.get_monitoring_summary()
    
    print(f"\n📊 Monitoring System Summary:")
    
    overview = summary["monitoring_overview"]
    print(f"  Total Metrics: {overview['total_metrics_collected']}")
    print(f"  Metrics (24h): {overview['metrics_last_24h']}")
    print(f"  Monitored Components: {overview['monitored_components']}")
    print(f"  Monitoring Interval: {overview['monitoring_interval_seconds']}s")
    
    alert_summary = summary["alert_summary"]
    print(f"  Total Alerts: {alert_summary['total_alerts']}")
    print(f"  Active Alerts: {alert_summary['active_alerts']}")
    print(f"  Resolved Alerts: {alert_summary['resolved_alerts']}")
    
    health_tracking = summary["health_tracking"]
    print(f"  Health Snapshots: {health_tracking['health_snapshots']}")
    print(f"  Performance Trends: {health_tracking['performance_trends']}")
    print(f"  Performance Reports: {health_tracking['performance_reports']}")
    
    # Latest performance report
    if manager.performance_reports:
        latest_report = manager.performance_reports[-1]
        print(f"\n📋 Latest Performance Report:")
        print(f"  Title: {latest_report.report_title}")
        print(f"  System Performance: {latest_report.overall_system_performance:.1f}%")
        print(f"  Average Availability: {latest_report.average_availability:.1f}%")
        print(f"  Components Monitored: {len(latest_report.monitored_components)}")
        print(f"  Best Performer: {latest_report.best_performing_component}")
        print(f"  Worst Performer: {latest_report.worst_performing_component}")
        
        if latest_report.key_insights:
            print(f"  Key Insights:")
            for insight in latest_report.key_insights[:3]:
                print(f"    • {insight}")
    
    print(f"\n🏆 TOP PERFORMING Components:")
    
    # Calculate component performance scores
    component_scores = {}
    for metric in recent_metrics:
        if metric.status == MetricStatus.NORMAL:
            component_scores[metric.component_id] = component_scores.get(metric.component_id, 0) + 1
    
    top_components = sorted(component_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for i, (component_id, score) in enumerate(top_components, 1):
        component_metrics = [m for m in recent_metrics if m.component_id == component_id]
        component_type = component_metrics[0].component_type.value.replace('_', ' ').title() if component_metrics else "Unknown"
        print(f"  {i}. {component_id}")
        print(f"     Type: {component_type}")
        print(f"     Normal Metrics: {score}")
        print(f"     Total Metrics: {len(component_metrics)}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    monitoring_manager = run_demonstration()
    display_monitoring_results(monitoring_manager)
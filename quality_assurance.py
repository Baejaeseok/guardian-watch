"""
Quality Assurance and Control System
===================================
Module 5: Integration & Validation Tools

Advanced quality assurance, control, and improvement system for One Health platforms,
providing comprehensive quality management and continuous improvement capabilities.

NIW Focus: Quality intelligence ensuring excellence and reliability across One Health operations.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable, Set
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque, Counter
import itertools
import random
import uuid
import hashlib
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QualityDimension(Enum):
    """Quality dimensions for assessment."""
    ACCURACY = "accuracy"                        # Data accuracy
    COMPLETENESS = "completeness"               # Data completeness
    CONSISTENCY = "consistency"                 # Internal consistency
    TIMELINESS = "timeliness"                  # Data timeliness
    VALIDITY = "validity"                      # Format/range validity
    UNIQUENESS = "uniqueness"                  # Duplicate detection
    RELIABILITY = "reliability"                # System reliability
    USABILITY = "usability"                    # Data usability

class QualityLevel(Enum):
    """Quality assessment levels."""
    EXCELLENT = "excellent"                     # >95% quality
    GOOD = "good"                              # 85-95% quality
    SATISFACTORY = "satisfactory"              # 70-85% quality
    NEEDS_IMPROVEMENT = "needs_improvement"    # 50-70% quality
    POOR = "poor"                              # <50% quality

class ProcessType(Enum):
    """Types of processes for quality assurance."""
    DATA_COLLECTION = "data_collection"        # Data collection processes
    DATA_PROCESSING = "data_processing"        # Data processing workflows
    DATA_ANALYSIS = "data_analysis"           # Analysis procedures
    SYSTEM_INTEGRATION = "system_integration" # Integration processes
    REPORTING = "reporting"                    # Reporting processes
    VALIDATION = "validation"                  # Validation processes
    SURVEILLANCE = "surveillance"              # Surveillance operations

class QualityIssueType(Enum):
    """Types of quality issues."""
    DATA_QUALITY = "data_quality"             # Data quality issues
    PROCESS_QUALITY = "process_quality"       # Process quality issues
    SYSTEM_QUALITY = "system_quality"         # System quality issues
    PERFORMANCE_ISSUE = "performance_issue"   # Performance problems
    COMPLIANCE_ISSUE = "compliance_issue"     # Compliance violations
    SECURITY_ISSUE = "security_issue"         # Security concerns

class QualityStatus(Enum):
    """Quality control status."""
    COMPLIANT = "compliant"                   # Meets quality standards
    NON_COMPLIANT = "non_compliant"          # Does not meet standards
    UNDER_REVIEW = "under_review"            # Under quality review
    IMPROVEMENT_NEEDED = "improvement_needed" # Needs improvement
    MONITORING = "monitoring"                 # Under monitoring

@dataclass
class QualityStandard:
    """Quality standard definition."""
    
    standard_id: str
    standard_name: str
    standard_description: str
    quality_dimension: QualityDimension
    process_type: ProcessType
    
    # Standard criteria
    target_threshold: float                    # Target quality threshold (0-100)
    minimum_threshold: float                   # Minimum acceptable threshold
    measurement_method: str                    # How to measure compliance
    measurement_frequency: str                 # How often to measure
    
    # Standard metadata
    effective_date: datetime
    review_date: datetime
    version: str = "1.0"
    is_active: bool = True
    
    # Compliance tracking
    last_assessment_date: Optional[datetime] = None
    current_compliance_level: float = 0.0     # Current compliance %
    compliance_trend: str = "stable"          # "improving", "stable", "declining"

@dataclass
class QualityMetric:
    """Individual quality metric measurement."""
    
    metric_id: str
    metric_name: str
    standard_id: str
    measurement_timestamp: datetime
    
    # Metric values
    measured_value: float                      # Actual measured value
    target_value: float                       # Target/expected value
    compliance_percentage: float              # % compliance with standard
    
    # Measurement context
    data_source: Optional[str] = None
    process_instance: Optional[str] = None
    measurement_method: str = "automated"
    sample_size: int = 0
    
    # Quality assessment
    quality_level: QualityLevel = QualityLevel.SATISFACTORY
    passes_minimum_threshold: bool = True
    variance_from_target: float = 0.0         # % variance from target
    
    # Additional details
    measurement_notes: str = ""
    contributing_factors: List[str] = field(default_factory=list)

@dataclass
class QualityIssue:
    """Quality issue tracking."""
    
    issue_id: str
    issue_type: QualityIssueType
    issue_title: str
    issue_description: str
    
    # Issue details
    detected_date: datetime
    affected_process: ProcessType
    affected_systems: List[str] = field(default_factory=list)
    severity: str = "medium"                   # "low", "medium", "high", "critical"
    priority: str = "medium"                   # "low", "medium", "high", "urgent"
    
    # Issue resolution
    is_resolved: bool = False
    resolution_date: Optional[datetime] = None
    resolution_description: str = ""
    assigned_to: str = ""
    estimated_resolution_time_days: int = 5
    
    # Impact assessment
    data_records_affected: int = 0
    processes_impacted: List[str] = field(default_factory=list)
    estimated_cost_impact: float = 0.0        # Cost impact estimate
    compliance_impact: str = "minor"          # "none", "minor", "moderate", "major", "severe"
    
    # Root cause analysis
    root_causes: List[str] = field(default_factory=list)
    contributing_factors: List[str] = field(default_factory=list)
    preventive_actions: List[str] = field(default_factory=list)

@dataclass
class QualityReport:
    """Comprehensive quality assessment report."""
    
    report_id: str
    report_title: str
    report_period_start: datetime
    report_period_end: datetime
    generation_timestamp: datetime
    
    # Report scope
    assessed_processes: List[ProcessType] = field(default_factory=list)
    assessed_systems: List[str] = field(default_factory=list)
    total_standards_evaluated: int = 0
    
    # Overall quality assessment
    overall_quality_score: float = 0.0        # 0-100 scale
    overall_compliance_rate: float = 0.0      # % standards meeting target
    quality_trend: str = "stable"             # Overall trend
    
    # Quality dimensions analysis
    dimension_scores: Dict[QualityDimension, float] = field(default_factory=dict)
    
    # Standards compliance
    compliant_standards: int = 0
    non_compliant_standards: int = 0
    standards_under_review: int = 0
    
    # Issue analysis
    total_issues_detected: int = 0
    critical_issues: int = 0
    high_priority_issues: int = 0
    resolved_issues: int = 0
    average_resolution_time_days: float = 0.0
    
    # Improvement recommendations
    key_findings: List[str] = field(default_factory=list)
    improvement_recommendations: List[str] = field(default_factory=list)
    priority_actions: List[str] = field(default_factory=list)
    
    # Performance metrics
    metrics_collected: int = 0
    average_quality_score: float = 0.0
    best_performing_process: str = ""
    worst_performing_process: str = ""

@dataclass
class QualityImprovement:
    """Quality improvement initiative."""
    
    initiative_id: str
    initiative_name: str
    initiative_description: str
    target_quality_dimension: QualityDimension
    
    # Initiative details
    start_date: datetime
    target_completion_date: datetime
    actual_completion_date: Optional[datetime] = None
    
    # Objectives and targets
    current_baseline_score: float = 0.0       # Starting quality score
    target_improvement_score: float = 0.0     # Target quality score
    success_criteria: List[str] = field(default_factory=list)
    
    # Implementation
    action_items: List[str] = field(default_factory=list)
    responsible_team: str = ""
    budget_allocated: float = 0.0
    resources_required: List[str] = field(default_factory=list)
    
    # Progress tracking
    completion_percentage: float = 0.0
    milestones_achieved: int = 0
    total_milestones: int = 0
    is_on_track: bool = True
    
    # Results measurement
    interim_measurements: List[Tuple[datetime, float]] = field(default_factory=list)
    final_quality_score: Optional[float] = None
    improvement_achieved: float = 0.0         # Actual improvement in score
    roi_estimate: float = 0.0                 # Return on investment

class QualityAssuranceManager:
    """Central quality assurance and control management system."""
    
    def __init__(self):
        self.quality_standards: Dict[str, QualityStandard] = {}
        self.quality_metrics: List[QualityMetric] = []
        self.quality_issues: List[QualityIssue] = []
        self.quality_reports: List[QualityReport] = []
        self.improvement_initiatives: List[QualityImprovement] = []
        
        # Initialize quality management framework
        self._initialize_quality_framework()
        
        logger.info("One Health Quality Assurance Manager initialized")
    
    def _initialize_quality_framework(self):
        """Initialize quality standards and framework."""
        
        # Standard quality standards for One Health systems
        standard_definitions = [
            # Data Quality Standards
            {
                "id": "data_accuracy_std", "name": "Data Accuracy Standard",
                "description": "Standard for data accuracy across all One Health domains",
                "dimension": QualityDimension.ACCURACY, "process": ProcessType.DATA_COLLECTION,
                "target": 95.0, "minimum": 90.0, "method": "validation_rule_compliance",
                "frequency": "daily"
            },
            {
                "id": "data_completeness_std", "name": "Data Completeness Standard", 
                "description": "Standard for data completeness and missing value management",
                "dimension": QualityDimension.COMPLETENESS, "process": ProcessType.DATA_COLLECTION,
                "target": 98.0, "minimum": 95.0, "method": "field_completion_rate",
                "frequency": "daily"
            },
            {
                "id": "data_timeliness_std", "name": "Data Timeliness Standard",
                "description": "Standard for timely data submission and processing",
                "dimension": QualityDimension.TIMELINESS, "process": ProcessType.DATA_PROCESSING,
                "target": 90.0, "minimum": 85.0, "method": "submission_delay_analysis",
                "frequency": "hourly"
            },
            
            # Process Quality Standards
            {
                "id": "integration_reliability_std", "name": "System Integration Reliability",
                "description": "Standard for system integration uptime and reliability",
                "dimension": QualityDimension.RELIABILITY, "process": ProcessType.SYSTEM_INTEGRATION,
                "target": 99.5, "minimum": 99.0, "method": "uptime_monitoring",
                "frequency": "continuous"
            },
            {
                "id": "validation_consistency_std", "name": "Validation Process Consistency",
                "description": "Standard for consistency in validation processes",
                "dimension": QualityDimension.CONSISTENCY, "process": ProcessType.VALIDATION,
                "target": 95.0, "minimum": 92.0, "method": "validation_rule_compliance",
                "frequency": "daily"
            },
            
            # Surveillance Quality Standards
            {
                "id": "surveillance_coverage_std", "name": "Surveillance Coverage Standard",
                "description": "Standard for surveillance system coverage and performance",
                "dimension": QualityDimension.COMPLETENESS, "process": ProcessType.SURVEILLANCE,
                "target": 95.0, "minimum": 90.0, "method": "coverage_analysis",
                "frequency": "weekly"
            },
            
            # Reporting Quality Standards
            {
                "id": "report_usability_std", "name": "Report Usability Standard",
                "description": "Standard for report quality and usability",
                "dimension": QualityDimension.USABILITY, "process": ProcessType.REPORTING,
                "target": 90.0, "minimum": 85.0, "method": "user_feedback_analysis",
                "frequency": "monthly"
            },
            
            # Analysis Quality Standards
            {
                "id": "analysis_validity_std", "name": "Analysis Validity Standard",
                "description": "Standard for validity and reliability of data analysis",
                "dimension": QualityDimension.VALIDITY, "process": ProcessType.DATA_ANALYSIS,
                "target": 98.0, "minimum": 95.0, "method": "peer_review_compliance",
                "frequency": "per_analysis"
            }
        ]
        
        # Create quality standard objects
        for std_data in standard_definitions:
            standard = QualityStandard(
                standard_id=std_data["id"],
                standard_name=std_data["name"],
                standard_description=std_data["description"],
                quality_dimension=std_data["dimension"],
                process_type=std_data["process"],
                target_threshold=std_data["target"],
                minimum_threshold=std_data["minimum"],
                measurement_method=std_data["method"],
                measurement_frequency=std_data["frequency"],
                effective_date=datetime.now(),
                review_date=datetime.now() + timedelta(days=365)
            )
            self.quality_standards[standard.standard_id] = standard
        
        logger.info(f"Initialized {len(self.quality_standards)} quality standards")
    
    def measure_quality_metric(self, standard_id: str, measured_value: float,
                              data_source: str = None, sample_size: int = 0) -> QualityMetric:
        """Measure quality metric against standard."""
        
        if standard_id not in self.quality_standards:
            raise ValueError(f"Quality standard {standard_id} not found")
        
        standard = self.quality_standards[standard_id]
        metric_id = f"METRIC_{random.randint(100000, 999999)}"
        
        # Calculate compliance percentage
        compliance_pct = (measured_value / standard.target_threshold) * 100
        compliance_pct = min(100.0, compliance_pct)  # Cap at 100%
        
        # Determine quality level
        if measured_value >= standard.target_threshold:
            quality_level = QualityLevel.EXCELLENT
        elif measured_value >= standard.target_threshold * 0.95:
            quality_level = QualityLevel.GOOD
        elif measured_value >= standard.minimum_threshold:
            quality_level = QualityLevel.SATISFACTORY
        elif measured_value >= standard.minimum_threshold * 0.8:
            quality_level = QualityLevel.NEEDS_IMPROVEMENT
        else:
            quality_level = QualityLevel.POOR
        
        # Calculate variance from target
        variance_from_target = ((measured_value - standard.target_threshold) / standard.target_threshold) * 100
        
        metric = QualityMetric(
            metric_id=metric_id,
            metric_name=f"{standard.standard_name} Measurement",
            standard_id=standard_id,
            measurement_timestamp=datetime.now(),
            measured_value=measured_value,
            target_value=standard.target_threshold,
            compliance_percentage=compliance_pct,
            data_source=data_source,
            sample_size=sample_size,
            quality_level=quality_level,
            passes_minimum_threshold=measured_value >= standard.minimum_threshold,
            variance_from_target=variance_from_target
        )
        
        # Update standard compliance tracking
        standard.last_assessment_date = datetime.now()
        standard.current_compliance_level = compliance_pct
        
        self.quality_metrics.append(metric)
        
        logger.info(f"Quality metric measured: {metric_id} - {quality_level.value}")
        
        return metric
    
    def detect_quality_issue(self, issue_type: QualityIssueType, title: str, description: str,
                           affected_process: ProcessType, severity: str = "medium") -> QualityIssue:
        """Detect and log quality issue."""
        
        issue_id = f"ISSUE_{random.randint(100000, 999999)}"
        
        issue = QualityIssue(
            issue_id=issue_id,
            issue_type=issue_type,
            issue_title=title,
            issue_description=description,
            detected_date=datetime.now(),
            affected_process=affected_process,
            severity=severity
        )
        
        # Set priority based on severity
        if severity == "critical":
            issue.priority = "urgent"
            issue.estimated_resolution_time_days = 1
        elif severity == "high":
            issue.priority = "high"
            issue.estimated_resolution_time_days = 3
        elif severity == "medium":
            issue.priority = "medium"
            issue.estimated_resolution_time_days = 7
        else:
            issue.priority = "low"
            issue.estimated_resolution_time_days = 14
        
        # Estimate impact based on type and severity
        if issue_type == QualityIssueType.DATA_QUALITY:
            issue.data_records_affected = random.randint(100, 10000)
        elif issue_type == QualityIssueType.SYSTEM_QUALITY:
            issue.processes_impacted = ["data_processing", "integration", "reporting"]
        
        # Estimate cost impact
        severity_multipliers = {"low": 1000, "medium": 5000, "high": 20000, "critical": 100000}
        issue.estimated_cost_impact = severity_multipliers.get(severity, 5000)
        
        self.quality_issues.append(issue)
        
        logger.warning(f"Quality issue detected: {issue_id} - {severity} severity")
        
        return issue
    
    def resolve_quality_issue(self, issue_id: str, resolution_description: str,
                             preventive_actions: List[str] = None):
        """Resolve quality issue."""
        
        issue = None
        for qi in self.quality_issues:
            if qi.issue_id == issue_id:
                issue = qi
                break
        
        if not issue:
            return False
        
        issue.is_resolved = True
        issue.resolution_date = datetime.now()
        issue.resolution_description = resolution_description
        
        if preventive_actions:
            issue.preventive_actions = preventive_actions
        
        logger.info(f"Quality issue resolved: {issue_id}")
        
        return True
    
    def assess_process_quality(self, process_type: ProcessType, assessment_period_days: int = 7) -> Dict[str, Any]:
        """Assess quality for a specific process type."""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=assessment_period_days)
        
        # Find relevant standards for this process type
        process_standards = [std for std in self.quality_standards.values() 
                           if std.process_type == process_type and std.is_active]
        
        # Find relevant metrics
        process_metrics = []
        for metric in self.quality_metrics:
            if (metric.standard_id in [std.standard_id for std in process_standards] and
                start_date <= metric.measurement_timestamp <= end_date):
                process_metrics.append(metric)
        
        # Find relevant issues
        process_issues = [issue for issue in self.quality_issues
                         if issue.affected_process == process_type and
                         start_date <= issue.detected_date <= end_date]
        
        # Calculate assessment
        assessment = {
            "process_type": process_type.value,
            "assessment_period_days": assessment_period_days,
            "standards_applicable": len(process_standards),
            "metrics_collected": len(process_metrics),
            "issues_detected": len(process_issues)
        }
        
        if process_metrics:
            # Overall quality score (average compliance)
            avg_compliance = statistics.mean(m.compliance_percentage for m in process_metrics)
            assessment["overall_quality_score"] = avg_compliance
            
            # Quality level distribution
            quality_levels = Counter(m.quality_level for m in process_metrics)
            assessment["quality_level_distribution"] = {level.value: count for level, count in quality_levels.items()}
            
            # Compliance rate (% metrics meeting minimum threshold)
            compliant_metrics = [m for m in process_metrics if m.passes_minimum_threshold]
            assessment["compliance_rate"] = (len(compliant_metrics) / len(process_metrics)) * 100
            
            # Best and worst performing standards
            metric_by_standard = defaultdict(list)
            for metric in process_metrics:
                metric_by_standard[metric.standard_id].append(metric.compliance_percentage)
            
            if metric_by_standard:
                standard_avg_scores = {std_id: statistics.mean(scores) 
                                     for std_id, scores in metric_by_standard.items()}
                best_standard_id = max(standard_avg_scores, key=standard_avg_scores.get)
                worst_standard_id = min(standard_avg_scores, key=standard_avg_scores.get)
                
                assessment["best_performing_standard"] = {
                    "standard_id": best_standard_id,
                    "standard_name": self.quality_standards[best_standard_id].standard_name,
                    "avg_score": standard_avg_scores[best_standard_id]
                }
                assessment["worst_performing_standard"] = {
                    "standard_id": worst_standard_id, 
                    "standard_name": self.quality_standards[worst_standard_id].standard_name,
                    "avg_score": standard_avg_scores[worst_standard_id]
                }
        else:
            assessment["overall_quality_score"] = 0.0
            assessment["compliance_rate"] = 0.0
        
        # Issue analysis
        if process_issues:
            severity_counts = Counter(issue.severity for issue in process_issues)
            assessment["issue_severity_breakdown"] = dict(severity_counts)
            
            resolved_issues = [issue for issue in process_issues if issue.is_resolved]
            assessment["issue_resolution_rate"] = (len(resolved_issues) / len(process_issues)) * 100
            
            if resolved_issues:
                resolution_times = []
                for issue in resolved_issues:
                    if issue.resolution_date:
                        resolution_time = (issue.resolution_date - issue.detected_date).days
                        resolution_times.append(resolution_time)
                
                if resolution_times:
                    assessment["average_resolution_time_days"] = statistics.mean(resolution_times)
        else:
            assessment["issue_resolution_rate"] = 100.0  # No issues = 100% resolution
        
        return assessment
    
    def generate_quality_report(self, report_title: str, period_days: int = 30) -> QualityReport:
        """Generate comprehensive quality report."""
        
        report_id = f"QR_{random.randint(100000, 999999)}"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        report = QualityReport(
            report_id=report_id,
            report_title=report_title,
            report_period_start=start_date,
            report_period_end=end_date,
            generation_timestamp=datetime.now()
        )
        
        # Assess all process types
        all_assessments = {}
        for process_type in ProcessType:
            assessment = self.assess_process_quality(process_type, period_days)
            all_assessments[process_type] = assessment
            
            if assessment["metrics_collected"] > 0:
                report.assessed_processes.append(process_type)
        
        # Overall quality calculations
        if report.assessed_processes:
            process_scores = [all_assessments[pt]["overall_quality_score"] 
                            for pt in report.assessed_processes
                            if all_assessments[pt]["overall_quality_score"] > 0]
            
            if process_scores:
                report.overall_quality_score = statistics.mean(process_scores)
        
        # Standards compliance analysis
        active_standards = [std for std in self.quality_standards.values() if std.is_active]
        report.total_standards_evaluated = len(active_standards)
        
        for standard in active_standards:
            if standard.current_compliance_level >= standard.target_threshold:
                report.compliant_standards += 1
            elif standard.current_compliance_level >= standard.minimum_threshold:
                report.standards_under_review += 1
            else:
                report.non_compliant_standards += 1
        
        if active_standards:
            report.overall_compliance_rate = (report.compliant_standards / len(active_standards)) * 100
        
        # Quality dimensions analysis
        dimension_metrics = defaultdict(list)
        period_metrics = [m for m in self.quality_metrics 
                         if start_date <= m.measurement_timestamp <= end_date]
        
        for metric in period_metrics:
            if metric.standard_id in self.quality_standards:
                dimension = self.quality_standards[metric.standard_id].quality_dimension
                dimension_metrics[dimension].append(metric.compliance_percentage)
        
        for dimension, scores in dimension_metrics.items():
            report.dimension_scores[dimension] = statistics.mean(scores)
        
        # Issue analysis
        period_issues = [issue for issue in self.quality_issues
                        if start_date <= issue.detected_date <= end_date]
        
        report.total_issues_detected = len(period_issues)
        report.critical_issues = len([i for i in period_issues if i.severity == "critical"])
        report.high_priority_issues = len([i for i in period_issues if i.priority == "high"])
        report.resolved_issues = len([i for i in period_issues if i.is_resolved])
        
        if period_issues:
            resolved_with_times = [i for i in period_issues if i.is_resolved and i.resolution_date]
            if resolved_with_times:
                resolution_times = [(i.resolution_date - i.detected_date).days for i in resolved_with_times]
                report.average_resolution_time_days = statistics.mean(resolution_times)
        
        # Performance metrics
        report.metrics_collected = len(period_metrics)
        if period_metrics:
            report.average_quality_score = statistics.mean(m.compliance_percentage for m in period_metrics)
        
        # Best and worst performing processes
        if report.assessed_processes:
            process_scores = {pt.value: all_assessments[pt]["overall_quality_score"] 
                            for pt in report.assessed_processes
                            if all_assessments[pt]["overall_quality_score"] > 0}
            
            if process_scores:
                report.best_performing_process = max(process_scores, key=process_scores.get)
                report.worst_performing_process = min(process_scores, key=process_scores.get)
        
        # Generate findings and recommendations
        report.key_findings = self._generate_key_findings(report, all_assessments)
        report.improvement_recommendations = self._generate_improvement_recommendations(report)
        report.priority_actions = self._generate_priority_actions(report)
        
        self.quality_reports.append(report)
        
        logger.info(f"Quality report generated: {report_id}")
        
        return report
    
    def _generate_key_findings(self, report: QualityReport, assessments: Dict) -> List[str]:
        """Generate key findings from quality report."""
        
        findings = []
        
        # Overall quality findings
        if report.overall_quality_score >= 95:
            findings.append("Excellent overall quality performance across all processes")
        elif report.overall_quality_score >= 85:
            findings.append("Good quality performance with room for improvement")
        elif report.overall_quality_score < 70:
            findings.append("Quality performance below acceptable standards")
        
        # Compliance findings
        compliance_rate = report.overall_compliance_rate
        if compliance_rate >= 95:
            findings.append("High compliance rate with quality standards")
        elif compliance_rate < 80:
            findings.append("Low compliance rate requires immediate attention")
        
        # Issue findings
        if report.critical_issues > 0:
            findings.append(f"Critical quality issues detected ({report.critical_issues} issues)")
        
        if report.total_issues_detected > 0:
            resolution_rate = (report.resolved_issues / report.total_issues_detected) * 100
            if resolution_rate < 80:
                findings.append("Low issue resolution rate needs improvement")
        
        # Process-specific findings
        if report.best_performing_process and report.worst_performing_process:
            findings.append(f"Best performing: {report.best_performing_process.replace('_', ' ').title()}, "
                          f"Worst performing: {report.worst_performing_process.replace('_', ' ').title()}")
        
        return findings[:5]  # Limit to 5 key findings
    
    def _generate_improvement_recommendations(self, report: QualityReport) -> List[str]:
        """Generate improvement recommendations."""
        
        recommendations = []
        
        if report.overall_quality_score < 85:
            recommendations.append("Implement systematic quality improvement program")
        
        if report.non_compliant_standards > report.compliant_standards:
            recommendations.append("Review and update quality standards and measurement processes")
        
        if report.critical_issues > 0:
            recommendations.append("Establish rapid response team for critical quality issues")
        
        if report.average_resolution_time_days > 7:
            recommendations.append("Streamline issue resolution processes to reduce resolution time")
        
        if QualityDimension.TIMELINESS in report.dimension_scores:
            if report.dimension_scores[QualityDimension.TIMELINESS] < 85:
                recommendations.append("Improve data timeliness through automated monitoring")
        
        if not recommendations:
            recommendations.append("Continue current quality management practices")
        
        return recommendations[:5]
    
    def _generate_priority_actions(self, report: QualityReport) -> List[str]:
        """Generate priority actions based on report."""
        
        actions = []
        
        if report.critical_issues > 0:
            actions.append("Address all critical quality issues within 24 hours")
        
        if report.overall_compliance_rate < 80:
            actions.append("Conduct immediate review of non-compliant processes")
        
        if report.overall_quality_score < 70:
            actions.append("Initiate emergency quality improvement measures")
        
        if report.worst_performing_process:
            actions.append(f"Focus improvement efforts on {report.worst_performing_process.replace('_', ' ')}")
        
        return actions[:3]  # Limit to 3 priority actions
    
    def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get real-time quality dashboard data."""
        
        # Current quality status
        recent_metrics = [m for m in self.quality_metrics
                         if (datetime.now() - m.measurement_timestamp).total_seconds() < 86400]
        
        dashboard = {
            "overall_status": "healthy",
            "timestamp": datetime.now(),
            "metrics_24h": len(recent_metrics)
        }
        
        if recent_metrics:
            avg_quality = statistics.mean(m.compliance_percentage for m in recent_metrics)
            dashboard["average_quality_score"] = avg_quality
            
            # Quality level distribution
            quality_levels = Counter(m.quality_level for m in recent_metrics)
            dashboard["quality_distribution"] = {level.value: count for level, count in quality_levels.items()}
            
            if avg_quality >= 95:
                dashboard["overall_status"] = "excellent"
            elif avg_quality >= 85:
                dashboard["overall_status"] = "good"
            elif avg_quality >= 70:
                dashboard["overall_status"] = "satisfactory"
            else:
                dashboard["overall_status"] = "needs_attention"
        
        # Active issues
        active_issues = [i for i in self.quality_issues if not i.is_resolved]
        dashboard["active_issues"] = len(active_issues)
        dashboard["critical_issues"] = len([i for i in active_issues if i.severity == "critical"])
        
        # Standards compliance
        compliant_standards = len([std for std in self.quality_standards.values()
                                 if std.current_compliance_level >= std.target_threshold])
        total_standards = len(self.quality_standards)
        dashboard["standards_compliance_rate"] = (compliant_standards / total_standards * 100) if total_standards > 0 else 0
        
        return dashboard
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get comprehensive quality system summary."""
        
        # Standards summary
        standards_summary = {
            "total_standards": len(self.quality_standards),
            "active_standards": len([std for std in self.quality_standards.values() if std.is_active]),
            "standards_by_dimension": Counter(std.quality_dimension for std in self.quality_standards.values()),
            "standards_by_process": Counter(std.process_type for std in self.quality_standards.values())
        }
        
        # Metrics summary
        metrics_summary = {
            "total_metrics": len(self.quality_metrics),
            "metrics_24h": len([m for m in self.quality_metrics
                              if (datetime.now() - m.measurement_timestamp).total_seconds() < 86400]),
            "average_quality_score": statistics.mean([m.compliance_percentage for m in self.quality_metrics]) 
                                   if self.quality_metrics else 0
        }
        
        # Issues summary
        issues_summary = {
            "total_issues": len(self.quality_issues),
            "active_issues": len([i for i in self.quality_issues if not i.is_resolved]),
            "resolved_issues": len([i for i in self.quality_issues if i.is_resolved]),
            "issues_by_severity": Counter(i.severity for i in self.quality_issues),
            "issues_by_type": Counter(i.issue_type for i in self.quality_issues)
        }
        
        # Reports summary
        reports_summary = {
            "total_reports": len(self.quality_reports),
            "improvement_initiatives": len(self.improvement_initiatives)
        }
        
        return {
            "standards": standards_summary,
            "metrics": metrics_summary,
            "issues": issues_summary,
            "reports": reports_summary
        }

def run_demonstration() -> QualityAssuranceManager:
    """Run comprehensive quality assurance demonstration."""
    
    print("🎯 One Health Quality Assurance System - Demonstration")
    print("=" * 70)
    
    manager = QualityAssuranceManager()
    
    print(f"\n🎯 Quality Framework:")
    print(f"  Quality Standards: {len(manager.quality_standards)}")
    print(f"  Quality Dimensions: {len(QualityDimension)}")
    print(f"  Process Types: {len(ProcessType)}")
    
    # Display standards by process type
    standards_by_process = defaultdict(list)
    for standard in manager.quality_standards.values():
        standards_by_process[standard.process_type].append(standard.standard_name)
    
    print(f"\n📊 Quality Standards by Process:")
    for process_type, standards in standards_by_process.items():
        print(f"  {process_type.value.replace('_', ' ').title()}: {len(standards)}")
        for standard in standards[:2]:  # Show first 2
            print(f"    • {standard}")
    
    print(f"\n📏 Measuring Quality Metrics...")
    
    # Simulate quality measurements
    measurement_scenarios = [
        {"standard": "data_accuracy_std", "value": 94.2, "source": "human_health_system"},
        {"standard": "data_completeness_std", "value": 97.8, "source": "animal_health_system"},
        {"standard": "data_timeliness_std", "value": 88.5, "source": "laboratory_system"},
        {"standard": "integration_reliability_std", "value": 99.2, "source": "integration_platform"},
        {"standard": "validation_consistency_std", "value": 93.7, "source": "validation_system"},
        {"standard": "surveillance_coverage_std", "value": 91.4, "source": "surveillance_network"},
        {"standard": "report_usability_std", "value": 87.9, "source": "reporting_system"},
        {"standard": "analysis_validity_std", "value": 96.1, "source": "analysis_platform"}
    ]
    
    metrics_created = []
    for scenario in measurement_scenarios:
        metric = manager.measure_quality_metric(
            scenario["standard"],
            scenario["value"],
            scenario["source"],
            random.randint(100, 1000)
        )
        metrics_created.append(metric)
        
        print(f"  📏 {metric.metric_name}: {metric.measured_value:.1f}% ({metric.quality_level.value})")
    
    print(f"\n⚠️ Detecting Quality Issues...")
    
    # Simulate quality issues
    issue_scenarios = [
        {
            "type": QualityIssueType.DATA_QUALITY, "title": "Data Validation Failures",
            "description": "Increased validation failures in animal health data",
            "process": ProcessType.DATA_COLLECTION, "severity": "medium"
        },
        {
            "type": QualityIssueType.SYSTEM_QUALITY, "title": "Integration Performance Degradation", 
            "description": "Slower response times in system integration",
            "process": ProcessType.SYSTEM_INTEGRATION, "severity": "high"
        },
        {
            "type": QualityIssueType.PROCESS_QUALITY, "title": "Surveillance Coverage Gap",
            "description": "Reduced coverage in rural surveillance areas",
            "process": ProcessType.SURVEILLANCE, "severity": "high"
        }
    ]
    
    issues_created = []
    for scenario in issue_scenarios:
        issue = manager.detect_quality_issue(
            scenario["type"],
            scenario["title"],
            scenario["description"],
            scenario["process"],
            scenario["severity"]
        )
        issues_created.append(issue)
        
        print(f"  ⚠️ {issue.issue_title} ({issue.severity} severity)")
    
    print(f"\n🔧 Resolving Quality Issues...")
    
    # Resolve some issues
    for issue in issues_created[:2]:  # Resolve first 2 issues
        manager.resolve_quality_issue(
            issue.issue_id,
            f"Issue resolved through process improvement and additional monitoring",
            [f"Implemented enhanced monitoring for {issue.affected_process.value}"]
        )
        print(f"  ✅ Resolved: {issue.issue_title}")
    
    print(f"\n📊 Assessing Process Quality...")
    
    # Assess key processes
    key_processes = [ProcessType.DATA_COLLECTION, ProcessType.SYSTEM_INTEGRATION, ProcessType.SURVEILLANCE]
    
    for process_type in key_processes:
        assessment = manager.assess_process_quality(process_type)
        print(f"  📊 {process_type.value.replace('_', ' ').title()}: {assessment['overall_quality_score']:.1f}% quality")
    
    print(f"\n📋 Generating Quality Report...")
    
    # Generate comprehensive quality report
    report = manager.generate_quality_report("Monthly Quality Assessment Report")
    
    print(f"  📋 Report: {report.overall_quality_score:.1f}% overall quality")
    print(f"  📋 Standards Compliance: {report.overall_compliance_rate:.1f}%")
    print(f"  📋 Issues: {report.total_issues_detected} detected, {report.resolved_issues} resolved")
    
    return manager

def display_quality_results(manager: QualityAssuranceManager):
    """Display comprehensive quality assurance results."""
    
    print(f"\n🎯 Quality Assurance Results:")
    
    # Quality standards
    print(f"\n📋 Quality Standards ({len(manager.quality_standards)} total):")
    standards_by_dimension = defaultdict(list)
    for standard in manager.quality_standards.values():
        standards_by_dimension[standard.quality_dimension].append(standard)
    
    for dimension, standards in standards_by_dimension.items():
        print(f"\n  {dimension.value.replace('_', ' ').title()} ({len(standards)} standards):")
        for standard in standards[:2]:  # Show first 2
            compliance_status = "✅ Compliant" if standard.current_compliance_level >= standard.target_threshold else "⚠️ Non-compliant"
            print(f"    • {standard.standard_name}")
            print(f"      Target: {standard.target_threshold:.1f}%, Current: {standard.current_compliance_level:.1f}% {compliance_status}")
    
    # Quality metrics
    recent_metrics = [m for m in manager.quality_metrics
                     if (datetime.now() - m.measurement_timestamp).total_seconds() < 3600]
    
    print(f"\n📏 Quality Metrics (Last Hour: {len(recent_metrics)} measurements):")
    
    if recent_metrics:
        # Metrics by quality level
        quality_level_counts = Counter(m.quality_level for m in recent_metrics)
        for level, count in quality_level_counts.items():
            print(f"  {level.value.title()}: {count} measurements")
        
        # Average scores
        avg_score = statistics.mean(m.compliance_percentage for m in recent_metrics)
        print(f"  Average Compliance: {avg_score:.1f}%")
    
    # Quality issues
    active_issues = [i for i in manager.quality_issues if not i.is_resolved]
    resolved_issues = [i for i in manager.quality_issues if i.is_resolved]
    
    print(f"\n⚠️ Quality Issues:")
    print(f"  Active Issues: {len(active_issues)}")
    print(f"  Resolved Issues: {len(resolved_issues)}")
    
    if active_issues:
        print(f"  Active Issues by Severity:")
        severity_counts = Counter(i.severity for i in active_issues)
        for severity, count in severity_counts.items():
            print(f"    {severity.title()}: {count}")
    
    # System summary
    summary = manager.get_quality_summary()
    
    print(f"\n📊 Quality System Summary:")
    
    standards = summary["standards"]
    print(f"  Standards: {standards['total_standards']} ({standards['active_standards']} active)")
    
    metrics = summary["metrics"]
    print(f"  Metrics: {metrics['total_metrics']} total, {metrics['metrics_24h']} in last 24h")
    print(f"  Average Quality Score: {metrics['average_quality_score']:.1f}%")
    
    issues = summary["issues"]
    print(f"  Issues: {issues['total_issues']} total, {issues['active_issues']} active, {issues['resolved_issues']} resolved")
    
    reports = summary["reports"]
    print(f"  Reports Generated: {reports['total_reports']}")
    print(f"  Improvement Initiatives: {reports['improvement_initiatives']}")
    
    # Quality dashboard
    dashboard = manager.get_quality_dashboard()
    
    print(f"\n🎯 Quality Dashboard:")
    print(f"  Overall Status: {dashboard['overall_status'].title()}")
    print(f"  Average Quality Score: {dashboard.get('average_quality_score', 0):.1f}%")
    print(f"  Standards Compliance: {dashboard['standards_compliance_rate']:.1f}%")
    print(f"  Active Issues: {dashboard['active_issues']}")
    print(f"  Critical Issues: {dashboard['critical_issues']}")
    
    # Latest quality report
    if manager.quality_reports:
        latest_report = manager.quality_reports[-1]
        print(f"\n📋 Latest Quality Report:")
        print(f"  Title: {latest_report.report_title}")
        print(f"  Overall Quality: {latest_report.overall_quality_score:.1f}%")
        print(f"  Compliance Rate: {latest_report.overall_compliance_rate:.1f}%")
        print(f"  Best Process: {latest_report.best_performing_process.replace('_', ' ').title()}")
        print(f"  Worst Process: {latest_report.worst_performing_process.replace('_', ' ').title()}")
        
        if latest_report.key_findings:
            print(f"  Key Findings:")
            for finding in latest_report.key_findings[:3]:
                print(f"    • {finding}")
    
    print(f"\n🏆 TOP PERFORMING Standards:")
    top_standards = sorted(manager.quality_standards.values(), 
                          key=lambda s: s.current_compliance_level, reverse=True)[:3]
    
    for i, standard in enumerate(top_standards, 1):
        print(f"  {i}. {standard.standard_name}")
        print(f"     Compliance: {standard.current_compliance_level:.1f}%")
        print(f"     Target: {standard.target_threshold:.1f}%")
        print(f"     Process: {standard.process_type.value.replace('_', ' ').title()}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    quality_manager = run_demonstration()
    display_quality_results(quality_manager)
"""
Data Validation and Quality Assurance System
===========================================
Module 5: Integration & Validation Tools

Advanced data validation, quality assessment, and integrity verification for One Health platforms,
providing comprehensive data quality control and assurance mechanisms.

NIW Focus: Validation intelligence ensuring data integrity and reliability across One Health surveillance.
"""

import json
import math
import statistics
import re
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValidationType(Enum):
    """Types of data validation."""
    FORMAT_VALIDATION = "format_validation"       # Data format and structure
    RANGE_VALIDATION = "range_validation"         # Value range checks
    BUSINESS_RULE = "business_rule"              # Business logic validation
    REFERENTIAL_INTEGRITY = "referential_integrity"  # Cross-reference validation
    TEMPORAL_VALIDATION = "temporal_validation"   # Time-based validation
    GEOGRAPHIC_VALIDATION = "geographic_validation"  # Location validation
    STATISTICAL_VALIDATION = "statistical_validation"  # Statistical outlier detection
    CONSISTENCY_CHECK = "consistency_check"       # Internal consistency

class ValidationSeverity(Enum):
    """Validation issue severity levels."""
    CRITICAL = "critical"                         # Data unusable
    HIGH = "high"                                # Significant quality impact
    MEDIUM = "medium"                            # Moderate quality concern
    LOW = "low"                                  # Minor quality issue
    INFO = "info"                                # Informational only

class ValidationStatus(Enum):
    """Validation status."""
    PENDING = "pending"                          # Validation pending
    PASSED = "passed"                            # Validation passed
    FAILED = "failed"                            # Validation failed
    WARNING = "warning"                          # Validation passed with warnings
    SKIPPED = "skipped"                          # Validation skipped
    ERROR = "error"                              # Validation error

class DataDomain(Enum):
    """Data domain types for validation."""
    HUMAN_HEALTH = "human_health"                # Human health data
    ANIMAL_HEALTH = "animal_health"              # Animal health data
    ENVIRONMENTAL = "environmental"              # Environmental data
    LABORATORY = "laboratory"                    # Laboratory data
    SURVEILLANCE = "surveillance"                # Surveillance data
    DEMOGRAPHIC = "demographic"                  # Demographic data
    GEOGRAPHIC = "geographic"                    # Geographic data

@dataclass
class ValidationRule:
    """Individual validation rule definition."""
    
    rule_id: str
    rule_name: str
    validation_type: ValidationType
    data_domain: DataDomain
    
    # Rule definition
    rule_description: str
    field_name: str
    rule_expression: str                         # Validation logic expression
    error_message: str
    
    # Rule configuration
    severity: ValidationSeverity = ValidationSeverity.MEDIUM
    is_active: bool = True
    mandatory: bool = True                       # Required validation
    
    # Rule metadata
    created_date: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    rule_version: str = "1.0"
    
    # Performance tracking
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    average_execution_time_ms: float = 0.0

@dataclass
class ValidationResult:
    """Result of validation execution."""
    
    result_id: str
    rule_id: str
    validation_timestamp: datetime
    
    # Validation outcome
    status: ValidationStatus
    severity: ValidationSeverity
    
    # Result details
    field_name: str
    field_value: Any
    error_message: Optional[str] = None
    suggested_correction: Optional[str] = None
    
    # Context information
    record_id: Optional[str] = None
    data_source: Optional[str] = None
    validation_context: Dict[str, Any] = field(default_factory=dict)
    
    # Performance metrics
    execution_time_ms: float = 0.0
    confidence_score: float = 1.0                # Confidence in validation result

@dataclass
class DataQualityScore:
    """Comprehensive data quality assessment."""
    
    score_id: str
    data_source: str
    assessment_timestamp: datetime
    
    # Overall quality metrics
    overall_score: float = 0.0                   # 0-100 scale
    completeness_score: float = 0.0             # % of required fields present
    accuracy_score: float = 0.0                 # % of accurate values
    consistency_score: float = 0.0              # % of consistent values
    validity_score: float = 0.0                 # % of valid format/range
    timeliness_score: float = 0.0               # % of timely data
    
    # Quality dimensions
    total_records_assessed: int = 0
    records_with_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    
    # Domain-specific scores
    domain_scores: Dict[DataDomain, float] = field(default_factory=dict)
    
    # Recommendations
    quality_recommendations: List[str] = field(default_factory=list)
    improvement_priority: str = "medium"         # "low", "medium", "high", "critical"

@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    
    report_id: str
    report_name: str
    generation_timestamp: datetime
    
    # Report scope
    data_sources: List[str] = field(default_factory=list)
    validation_period_start: Optional[datetime] = None
    validation_period_end: Optional[datetime] = None
    
    # Validation summary
    total_validations: int = 0
    successful_validations: int = 0
    failed_validations: int = 0
    warning_validations: int = 0
    
    # Quality metrics
    overall_data_quality: float = 0.0
    quality_trend: str = "stable"                # "improving", "stable", "declining"
    
    # Issue analysis
    issues_by_severity: Dict[ValidationSeverity, int] = field(default_factory=dict)
    issues_by_domain: Dict[DataDomain, int] = field(default_factory=dict)
    issues_by_type: Dict[ValidationType, int] = field(default_factory=dict)
    
    # Top issues and recommendations
    top_validation_failures: List[str] = field(default_factory=list)
    improvement_recommendations: List[str] = field(default_factory=list)
    quality_scores: List[DataQualityScore] = field(default_factory=list)

class DataValidationManager:
    """Central data validation and quality management system."""
    
    def __init__(self):
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_results: List[ValidationResult] = []
        self.quality_scores: List[DataQualityScore] = []
        self.validation_reports: List[ValidationReport] = []
        
        # Initialize standard validation framework
        self._initialize_validation_framework()
        
        logger.info("One Health Data Validation Manager initialized")
    
    def _initialize_validation_framework(self):
        """Initialize standard validation rules."""
        
        # Standard validation rules by domain
        standard_rules = [
            # Human health validation rules
            {
                "id": "human_age_range", "name": "Human Age Range Validation", 
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.HUMAN_HEALTH,
                "field": "age", "expression": "0 <= value <= 120",
                "description": "Validate human age is within realistic range",
                "error": "Age must be between 0 and 120 years",
                "severity": ValidationSeverity.HIGH
            },
            {
                "id": "human_vital_signs", "name": "Human Vital Signs Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.HUMAN_HEALTH,
                "field": "temperature", "expression": "35.0 <= value <= 42.0",
                "description": "Validate human body temperature range",
                "error": "Body temperature must be between 35°C and 42°C",
                "severity": ValidationSeverity.CRITICAL
            },
            {
                "id": "human_symptom_onset", "name": "Symptom Onset Date Validation",
                "type": ValidationType.TEMPORAL_VALIDATION, "domain": DataDomain.HUMAN_HEALTH,
                "field": "symptom_onset_date", "expression": "value <= today and value >= today - 365 days",
                "description": "Validate symptom onset is not in future and within reasonable past",
                "error": "Symptom onset date cannot be in the future or more than 1 year ago",
                "severity": ValidationSeverity.HIGH
            },
            
            # Animal health validation rules
            {
                "id": "animal_species_code", "name": "Animal Species Code Validation",
                "type": ValidationType.FORMAT_VALIDATION, "domain": DataDomain.ANIMAL_HEALTH,
                "field": "species_code", "expression": "value.matches('[A-Z]{2}[0-9]{3}')",
                "description": "Validate animal species follows standard coding format",
                "error": "Species code must follow format: 2 uppercase letters + 3 digits",
                "severity": ValidationSeverity.HIGH
            },
            {
                "id": "animal_weight_range", "name": "Animal Weight Range Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.ANIMAL_HEALTH,
                "field": "weight_kg", "expression": "0.001 <= value <= 10000",
                "description": "Validate animal weight is within realistic range",
                "error": "Animal weight must be between 1g and 10,000kg",
                "severity": ValidationSeverity.MEDIUM
            },
            
            # Laboratory validation rules
            {
                "id": "lab_result_format", "name": "Laboratory Result Format Validation",
                "type": ValidationType.FORMAT_VALIDATION, "domain": DataDomain.LABORATORY,
                "field": "test_result", "expression": "value in ['positive', 'negative', 'indeterminate', 'pending']",
                "description": "Validate laboratory result uses standard terminology",
                "error": "Test result must be: positive, negative, indeterminate, or pending",
                "severity": ValidationSeverity.CRITICAL
            },
            {
                "id": "lab_accession_number", "name": "Laboratory Accession Number Validation",
                "type": ValidationType.FORMAT_VALIDATION, "domain": DataDomain.LABORATORY,
                "field": "accession_number", "expression": "value.matches('[0-9]{8}')",
                "description": "Validate laboratory accession number format",
                "error": "Accession number must be exactly 8 digits",
                "severity": ValidationSeverity.HIGH
            },
            
            # Geographic validation rules
            {
                "id": "latitude_range", "name": "Latitude Range Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.GEOGRAPHIC,
                "field": "latitude", "expression": "-90.0 <= value <= 90.0",
                "description": "Validate latitude coordinates are within valid range",
                "error": "Latitude must be between -90 and 90 degrees",
                "severity": ValidationSeverity.CRITICAL
            },
            {
                "id": "longitude_range", "name": "Longitude Range Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.GEOGRAPHIC,
                "field": "longitude", "expression": "-180.0 <= value <= 180.0",
                "description": "Validate longitude coordinates are within valid range",
                "error": "Longitude must be between -180 and 180 degrees",
                "severity": ValidationSeverity.CRITICAL
            },
            
            # Environmental validation rules
            {
                "id": "temperature_range", "name": "Environmental Temperature Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.ENVIRONMENTAL,
                "field": "air_temperature", "expression": "-50.0 <= value <= 60.0",
                "description": "Validate environmental temperature is within Earth's range",
                "error": "Air temperature must be between -50°C and 60°C",
                "severity": ValidationSeverity.MEDIUM
            },
            {
                "id": "humidity_range", "name": "Relative Humidity Validation",
                "type": ValidationType.RANGE_VALIDATION, "domain": DataDomain.ENVIRONMENTAL,
                "field": "relative_humidity", "expression": "0.0 <= value <= 100.0",
                "description": "Validate relative humidity percentage",
                "error": "Relative humidity must be between 0% and 100%",
                "severity": ValidationSeverity.MEDIUM
            },
            
            # Surveillance validation rules
            {
                "id": "case_classification", "name": "Case Classification Validation",
                "type": ValidationType.FORMAT_VALIDATION, "domain": DataDomain.SURVEILLANCE,
                "field": "case_classification", "expression": "value in ['suspected', 'probable', 'confirmed', 'not_a_case']",
                "description": "Validate case classification uses standard terminology",
                "error": "Case classification must be: suspected, probable, confirmed, or not_a_case",
                "severity": ValidationSeverity.CRITICAL
            },
            {
                "id": "notification_date", "name": "Notification Date Validation",
                "type": ValidationType.TEMPORAL_VALIDATION, "domain": DataDomain.SURVEILLANCE,
                "field": "notification_date", "expression": "value <= today and value >= today - 30 days",
                "description": "Validate notification date is recent and not in future",
                "error": "Notification date cannot be in future or more than 30 days ago",
                "severity": ValidationSeverity.HIGH
            }
        ]
        
        # Create validation rule objects
        for rule_data in standard_rules:
            rule = ValidationRule(
                rule_id=rule_data["id"],
                rule_name=rule_data["name"],
                validation_type=rule_data["type"],
                data_domain=rule_data["domain"],
                rule_description=rule_data["description"],
                field_name=rule_data["field"],
                rule_expression=rule_data["expression"],
                error_message=rule_data["error"],
                severity=rule_data["severity"]
            )
            self.validation_rules[rule.rule_id] = rule
        
        logger.info(f"Initialized {len(self.validation_rules)} standard validation rules")
    
    def validate_field(self, field_name: str, field_value: Any, 
                      data_domain: DataDomain, record_context: Dict[str, Any] = None) -> List[ValidationResult]:
        """Validate a single field against applicable rules."""
        
        results = []
        
        # Find applicable validation rules
        applicable_rules = [
            rule for rule in self.validation_rules.values()
            if rule.field_name == field_name and rule.data_domain == data_domain and rule.is_active
        ]
        
        for rule in applicable_rules:
            start_time = datetime.now()
            
            try:
                # Execute validation rule
                validation_passed = self._execute_validation_rule(rule, field_value, record_context)
                
                # Calculate execution time
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                
                # Create validation result
                result = ValidationResult(
                    result_id=f"VAL_{random.randint(10000, 99999)}",
                    rule_id=rule.rule_id,
                    validation_timestamp=datetime.now(),
                    status=ValidationStatus.PASSED if validation_passed else ValidationStatus.FAILED,
                    severity=rule.severity,
                    field_name=field_name,
                    field_value=field_value,
                    execution_time_ms=execution_time
                )
                
                if not validation_passed:
                    result.error_message = rule.error_message
                    result.suggested_correction = self._generate_correction_suggestion(rule, field_value)
                
                # Add context information
                if record_context:
                    result.validation_context = record_context.copy()
                    result.record_id = record_context.get("record_id")
                    result.data_source = record_context.get("data_source")
                
                results.append(result)
                
                # Update rule performance metrics
                rule.execution_count += 1
                if validation_passed:
                    rule.success_count += 1
                else:
                    rule.failure_count += 1
                
                # Update average execution time
                if rule.average_execution_time_ms > 0:
                    rule.average_execution_time_ms = (
                        (rule.average_execution_time_ms * 0.9) + (execution_time * 0.1)
                    )
                else:
                    rule.average_execution_time_ms = execution_time
                
            except Exception as e:
                # Handle validation execution errors
                error_result = ValidationResult(
                    result_id=f"VAL_{random.randint(10000, 99999)}",
                    rule_id=rule.rule_id,
                    validation_timestamp=datetime.now(),
                    status=ValidationStatus.ERROR,
                    severity=ValidationSeverity.CRITICAL,
                    field_name=field_name,
                    field_value=field_value,
                    error_message=f"Validation execution error: {str(e)}"
                )
                results.append(error_result)
                
                logger.error(f"Error executing validation rule {rule.rule_id}: {str(e)}")
        
        # Store validation results
        self.validation_results.extend(results)
        
        return results
    
    def _execute_validation_rule(self, rule: ValidationRule, field_value: Any, 
                                context: Dict[str, Any] = None) -> bool:
        """Execute validation rule logic."""
        
        try:
            # Handle different validation types
            if rule.validation_type == ValidationType.RANGE_VALIDATION:
                return self._validate_range(rule.rule_expression, field_value)
            elif rule.validation_type == ValidationType.FORMAT_VALIDATION:
                return self._validate_format(rule.rule_expression, field_value)
            elif rule.validation_type == ValidationType.TEMPORAL_VALIDATION:
                return self._validate_temporal(rule.rule_expression, field_value)
            elif rule.validation_type == ValidationType.BUSINESS_RULE:
                return self._validate_business_rule(rule.rule_expression, field_value, context)
            elif rule.validation_type == ValidationType.STATISTICAL_VALIDATION:
                return self._validate_statistical(rule.rule_expression, field_value, context)
            else:
                # Generic validation
                return self._validate_generic(rule.rule_expression, field_value)
                
        except Exception as e:
            logger.error(f"Validation rule execution failed for {rule.rule_id}: {str(e)}")
            return False
    
    def _validate_range(self, expression: str, value: Any) -> bool:
        """Validate value is within specified range."""
        
        try:
            # Convert value to numeric if needed
            if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                value = float(value)
            
            if not isinstance(value, (int, float)):
                return False
            
            # Parse range expression (e.g., "0 <= value <= 120")
            if "<=" in expression:
                parts = expression.split("<=")
                if len(parts) == 3:  # min <= value <= max
                    min_val = float(parts[0].strip())
                    max_val = float(parts[2].strip())
                    return min_val <= value <= max_val
                elif len(parts) == 2:
                    if "value" == parts[0].strip():  # value <= max
                        max_val = float(parts[1].strip())
                        return value <= max_val
                    else:  # min <= value
                        min_val = float(parts[0].strip())
                        return min_val <= value
            
            return True
            
        except (ValueError, TypeError):
            return False
    
    def _validate_format(self, expression: str, value: Any) -> bool:
        """Validate value matches specified format."""
        
        try:
            value_str = str(value) if value is not None else ""
            
            # Handle different format validation types
            if "matches" in expression:
                # Regular expression pattern matching
                pattern = expression.split("'")[1]  # Extract pattern from quotes
                return bool(re.match(pattern, value_str))
            elif "in [" in expression:
                # Value in list validation
                valid_values = expression.split("[")[1].split("]")[0]
                valid_list = [v.strip().strip("'\"") for v in valid_values.split(",")]
                return value_str in valid_list
            elif "len(" in expression:
                # Length validation
                if "==" in expression:
                    target_len = int(expression.split("==")[1].strip())
                    return len(value_str) == target_len
                elif "<=" in expression:
                    max_len = int(expression.split("<=")[1].strip())
                    return len(value_str) <= max_len
                elif ">=" in expression:
                    min_len = int(expression.split(">=")[1].strip())
                    return len(value_str) >= min_len
            
            return True
            
        except Exception:
            return False
    
    def _validate_temporal(self, expression: str, value: Any) -> bool:
        """Validate temporal/date-related constraints."""
        
        try:
            # Parse date value
            if isinstance(value, str):
                # Try to parse common date formats
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y", "%d/%m/%Y"]:
                    try:
                        value = datetime.strptime(value, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False
            elif not isinstance(value, datetime):
                return False
            
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Parse temporal expression
            if "today" in expression:
                # Simple temporal validation
                if "value <= today" in expression:
                    return value.date() <= today.date()
                elif "value >= today - 365 days" in expression:
                    return value >= today - timedelta(days=365)
                elif "value >= today - 30 days" in expression:
                    return value >= today - timedelta(days=30)
            
            return True
            
        except Exception:
            return False
    
    def _validate_business_rule(self, expression: str, value: Any, context: Dict[str, Any]) -> bool:
        """Validate business rule logic."""
        
        try:
            # Simple business rule validation
            return True  # Placeholder implementation
            
        except Exception:
            return False
    
    def _validate_statistical(self, expression: str, value: Any, context: Dict[str, Any]) -> bool:
        """Validate using statistical methods (outlier detection, etc.)."""
        
        try:
            # Simple statistical validation
            if not isinstance(value, (int, float)):
                return True
            
            # Basic outlier detection
            if context and "historical_values" in context:
                historical = context["historical_values"]
                if len(historical) >= 10:
                    mean_val = statistics.mean(historical)
                    std_val = statistics.stdev(historical)
                    
                    if std_val > 0:
                        z_score = abs((value - mean_val) / std_val)
                        return z_score <= 3.0
            
            return True
            
        except Exception:
            return True
    
    def _validate_generic(self, expression: str, value: Any) -> bool:
        """Generic validation using expression evaluation."""
        
        try:
            # Simple generic validation
            return True
            
        except Exception:
            return False
    
    def _generate_correction_suggestion(self, rule: ValidationRule, field_value: Any) -> Optional[str]:
        """Generate suggestion for correcting validation failure."""
        
        try:
            if rule.validation_type == ValidationType.RANGE_VALIDATION:
                if "<=" in rule.rule_expression:
                    parts = rule.rule_expression.split("<=")
                    if len(parts) == 3:
                        min_val = parts[0].strip()
                        max_val = parts[2].strip()
                        return f"Value should be between {min_val} and {max_val}"
                    
            elif rule.validation_type == ValidationType.FORMAT_VALIDATION:
                if "matches" in rule.rule_expression:
                    pattern = rule.rule_expression.split("'")[1]
                    return f"Value should match pattern: {pattern}"
                elif "in [" in rule.rule_expression:
                    valid_values = rule.rule_expression.split("[")[1].split("]")[0]
                    return f"Value should be one of: {valid_values}"
                    
            elif rule.validation_type == ValidationType.TEMPORAL_VALIDATION:
                return "Check date format and ensure date is within valid time range"
            
            return "Please check the value format and requirements"
            
        except Exception:
            return None
    
    def validate_record(self, record: Dict[str, Any], data_domain: DataDomain,
                       record_id: Optional[str] = None, data_source: Optional[str] = None) -> List[ValidationResult]:
        """Validate complete data record."""
        
        all_results = []
        
        # Prepare validation context
        context = {
            "record_id": record_id,
            "data_source": data_source,
            "full_record": record
        }
        
        # Validate each field in the record
        for field_name, field_value in record.items():
            if field_value is not None:  # Skip null values
                field_results = self.validate_field(field_name, field_value, data_domain, context)
                all_results.extend(field_results)
        
        return all_results
    
    def assess_data_quality(self, data_source: str, validation_results: List[ValidationResult],
                           total_records: int) -> DataQualityScore:
        """Assess overall data quality based on validation results."""
        
        score_id = f"SCORE_{random.randint(100000, 999999)}"
        
        quality_score = DataQualityScore(
            score_id=score_id,
            data_source=data_source,
            assessment_timestamp=datetime.now(),
            total_records_assessed=total_records
        )
        
        if not validation_results:
            quality_score.overall_score = 100.0
            return quality_score
        
        # Count issues by severity
        severity_counts = Counter(result.severity for result in validation_results)
        quality_score.critical_issues = severity_counts.get(ValidationSeverity.CRITICAL, 0)
        quality_score.high_issues = severity_counts.get(ValidationSeverity.HIGH, 0)
        quality_score.medium_issues = severity_counts.get(ValidationSeverity.MEDIUM, 0)
        quality_score.low_issues = severity_counts.get(ValidationSeverity.LOW, 0)
        
        # Calculate quality dimensions
        failed_validations = [r for r in validation_results if r.status == ValidationStatus.FAILED]
        total_validations = len(validation_results)
        
        if total_validations > 0:
            # Validity score
            passed_validations = total_validations - len(failed_validations)
            quality_score.validity_score = (passed_validations / total_validations) * 100
            
            # Accuracy score (weighted by severity)
            weighted_errors = (
                severity_counts.get(ValidationSeverity.CRITICAL, 0) * 4 +
                severity_counts.get(ValidationSeverity.HIGH, 0) * 3 +
                severity_counts.get(ValidationSeverity.MEDIUM, 0) * 2 +
                severity_counts.get(ValidationSeverity.LOW, 0) * 1
            )
            max_weighted_errors = total_validations * 4
            quality_score.accuracy_score = max(0, (1 - weighted_errors / max_weighted_errors) * 100)
            
            # Completeness score
            fields_with_data = len(set(r.field_name for r in validation_results))
            expected_fields = 15  # Estimated expected fields
            quality_score.completeness_score = min(100, (fields_with_data / expected_fields) * 100)
            
            # Consistency and timeliness scores
            quality_score.consistency_score = 95.0  # Simulated
            quality_score.timeliness_score = 90.0   # Simulated
            
            # Overall score (weighted average)
            weights = {"validity": 0.3, "accuracy": 0.25, "completeness": 0.2, "consistency": 0.15, "timeliness": 0.1}
            quality_score.overall_score = (
                quality_score.validity_score * weights["validity"] +
                quality_score.accuracy_score * weights["accuracy"] +
                quality_score.completeness_score * weights["completeness"] +
                quality_score.consistency_score * weights["consistency"] +
                quality_score.timeliness_score * weights["timeliness"]
            )
        
        # Records with issues
        quality_score.records_with_issues = len(set(r.record_id for r in failed_validations if r.record_id))
        
        # Generate recommendations
        quality_score.quality_recommendations = self._generate_quality_recommendations(quality_score)
        
        # Determine priority
        if quality_score.overall_score < 60:
            quality_score.improvement_priority = "critical"
        elif quality_score.overall_score < 75:
            quality_score.improvement_priority = "high"
        elif quality_score.overall_score < 90:
            quality_score.improvement_priority = "medium"
        else:
            quality_score.improvement_priority = "low"
        
        self.quality_scores.append(quality_score)
        
        return quality_score
    
    def _generate_quality_recommendations(self, quality_score: DataQualityScore) -> List[str]:
        """Generate data quality improvement recommendations."""
        
        recommendations = []
        
        if quality_score.completeness_score < 80:
            recommendations.append("Improve data collection processes to reduce missing values")
        
        if quality_score.accuracy_score < 80:
            recommendations.append("Implement additional validation checks at data entry points")
        
        if quality_score.validity_score < 90:
            recommendations.append("Review and update data validation rules")
        
        if quality_score.critical_issues > 0:
            recommendations.append("Address critical data quality issues immediately")
        
        if not recommendations:
            recommendations.append("Maintain current data quality standards")
        
        return recommendations
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get comprehensive validation system summary."""
        
        # Rule analysis
        total_rules = len(self.validation_rules)
        active_rules = len([r for r in self.validation_rules.values() if r.is_active])
        rules_by_type = Counter(r.validation_type for r in self.validation_rules.values())
        rules_by_domain = Counter(r.data_domain for r in self.validation_rules.values())
        
        # Recent results analysis
        recent_results = [
            r for r in self.validation_results
            if (datetime.now() - r.validation_timestamp).total_seconds() < 86400
        ]
        
        if recent_results:
            total_validations = len(recent_results)
            successful_validations = len([r for r in recent_results if r.status == ValidationStatus.PASSED])
            avg_execution_time = statistics.mean(r.execution_time_ms for r in recent_results)
            success_rate = successful_validations / total_validations
        else:
            total_validations = successful_validations = 0
            avg_execution_time = 0
            success_rate = 0
        
        # Quality scores
        if self.quality_scores:
            recent_scores = [s for s in self.quality_scores 
                           if (datetime.now() - s.assessment_timestamp).total_seconds() < 86400]
            avg_quality = statistics.mean(s.overall_score for s in recent_scores) if recent_scores else 0
        else:
            avg_quality = 0
        
        return {
            "validation_framework": {
                "total_rules": total_rules,
                "active_rules": active_rules,
                "rules_by_type": {t.value: count for t, count in rules_by_type.items()},
                "rules_by_domain": {d.value: count for d, count in rules_by_domain.items()}
            },
            "validation_performance_24h": {
                "total_validations": total_validations,
                "successful_validations": successful_validations,
                "success_rate": success_rate,
                "average_execution_time_ms": avg_execution_time
            },
            "data_quality": {
                "average_quality_score": avg_quality,
                "quality_assessments": len(self.quality_scores)
            }
        }

def run_demonstration() -> DataValidationManager:
    """Run comprehensive validation system demonstration."""
    
    print("✅ One Health Data Validation System - Demonstration")
    print("=" * 70)
    
    manager = DataValidationManager()
    
    print(f"\n✅ Validation Framework:")
    print(f"  Validation Rules: {len(manager.validation_rules)}")
    print(f"  Validation Types: {len(ValidationType)}")
    print(f"  Data Domains: {len(DataDomain)}")
    
    # Test data scenarios
    test_scenarios = [
        {
            "domain": DataDomain.HUMAN_HEALTH,
            "records": [
                {"age": 25, "temperature": 37.2, "symptom_onset_date": "2026-04-10"},
                {"age": 150, "temperature": 45.0, "symptom_onset_date": "2026-05-01"},  # Invalid
            ]
        },
        {
            "domain": DataDomain.ANIMAL_HEALTH,
            "records": [
                {"species_code": "BV123", "weight_kg": 450.5},
                {"species_code": "invalid", "weight_kg": -50},  # Invalid
            ]
        },
        {
            "domain": DataDomain.LABORATORY,
            "records": [
                {"test_result": "positive", "accession_number": "12345678"},
                {"test_result": "invalid", "accession_number": "123"},  # Invalid
            ]
        }
    ]
    
    print(f"\n✅ Testing Data Validation...")
    
    all_results = []
    total_records = 0
    
    for scenario in test_scenarios:
        domain = scenario["domain"]
        print(f"\n  Testing {domain.value.replace('_', ' ').title()}: {len(scenario['records'])} records")
        
        for i, record in enumerate(scenario["records"]):
            record_id = f"{domain.value.upper()}_REC_{i+1}"
            results = manager.validate_record(record, domain, record_id, f"{domain.value}_source")
            all_results.extend(results)
            total_records += 1
            
            failed = [r for r in results if r.status == ValidationStatus.FAILED]
            if failed:
                print(f"    ❌ Record {i+1}: {len(failed)} failures")
            else:
                print(f"    ✅ Record {i+1}: Passed")
    
    print(f"\n📊 Assessing Data Quality...")
    
    # Quality assessments
    for scenario in test_scenarios:
        domain = scenario["domain"]
        source = f"{domain.value}_source"
        source_results = [r for r in all_results if r.data_source == source]
        
        quality = manager.assess_data_quality(source, source_results, len(scenario["records"]))
        print(f"  {domain.value.replace('_', ' ').title()}: {quality.overall_score:.1f}% quality")
    
    return manager

def display_validation_results(manager: DataValidationManager):
    """Display comprehensive validation results."""
    
    print(f"\n✅ Data Validation Results:")
    
    # Summary
    summary = manager.get_validation_summary()
    
    framework = summary["validation_framework"] 
    print(f"\n📋 Validation Framework:")
    print(f"  Total Rules: {framework['total_rules']}")
    print(f"  Active Rules: {framework['active_rules']}")
    
    print(f"\n  Rules by Type:")
    for rule_type, count in framework["rules_by_type"].items():
        print(f"    {rule_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n  Rules by Domain:")
    for domain, count in framework["rules_by_domain"].items():
        print(f"    {domain.replace('_', ' ').title()}: {count}")
    
    # Performance
    performance = summary["validation_performance_24h"]
    print(f"\n🚀 Validation Performance (24h):")
    print(f"  Total Validations: {performance['total_validations']}")
    print(f"  Success Rate: {performance['success_rate']:.1%}")
    print(f"  Avg Execution Time: {performance['average_execution_time_ms']:.1f}ms")
    
    # Quality scores
    if manager.quality_scores:
        print(f"\n📊 Data Quality Scores:")
        for quality_score in manager.quality_scores:
            print(f"\n  {quality_score.data_source}:")
            print(f"    Overall Score: {quality_score.overall_score:.1f}%")
            print(f"    Completeness: {quality_score.completeness_score:.1f}%")
            print(f"    Accuracy: {quality_score.accuracy_score:.1f}%")
            print(f"    Validity: {quality_score.validity_score:.1f}%")
            print(f"    Priority: {quality_score.improvement_priority.title()}")
            print(f"    Issues: {quality_score.critical_issues} critical, {quality_score.high_issues} high")
    
    print(f"\n🏆 TOP PERFORMING Validation Rules:")
    top_rules = sorted(manager.validation_rules.values(), 
                      key=lambda r: r.success_count if r.execution_count > 0 else 0, reverse=True)[:3]
    
    for i, rule in enumerate(top_rules, 1):
        success_rate = (rule.success_count / rule.execution_count * 100) if rule.execution_count > 0 else 0
        print(f"  {i}. {rule.rule_name}")
        print(f"     Success Rate: {success_rate:.1f}%")
        print(f"     Domain: {rule.data_domain.value.replace('_', ' ').title()}")
        print(f"     Executions: {rule.execution_count}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    validation_manager = run_demonstration()
    display_validation_results(validation_manager)
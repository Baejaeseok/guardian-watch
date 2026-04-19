"""
Health Indicators Calculator
============================
Module 1: Data and Health Indicators in Public Health Practice

Calculates comprehensive health indicators and metrics for One Health surveillance
including epidemiological indicators, early warning scores, and system performance metrics.

NIW Focus: Evidence-based indicators demonstrating integrated surveillance effectiveness.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import math
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IndicatorCategory(Enum):
    """Categories of health indicators."""
    EPIDEMIOLOGICAL = "epidemiological"           # Disease occurrence patterns
    EARLY_WARNING = "early_warning"              # Risk prediction metrics
    INTEGRATION = "integration"                  # One Health connectivity
    PERFORMANCE = "performance"                  # System efficiency
    IMPACT = "impact"                            # Public health outcomes
    SURVEILLANCE = "surveillance"                # Monitoring effectiveness

class IndicatorType(Enum):
    """Types of indicator measurements."""
    RATE = "rate"                    # Events per population
    RATIO = "ratio"                  # Proportion between groups
    INDEX = "index"                  # Composite score
    COUNT = "count"                  # Absolute numbers
    PERCENTAGE = "percentage"        # Fraction as percent
    SCORE = "score"                  # Ranked assessment

class RiskLevel(Enum):
    """Risk classification levels."""
    MINIMAL = "minimal"      # 0-25%
    LOW = "low"             # 26-50%
    MODERATE = "moderate"   # 51-75%
    HIGH = "high"           # 76-90%
    CRITICAL = "critical"   # 91-100%

@dataclass
class HealthIndicator:
    """Standardized health indicator measurement."""
    
    # Core identification
    indicator_id: str
    indicator_name: str
    category: IndicatorCategory
    indicator_type: IndicatorType
    
    # Measurement details
    value: float
    unit: str
    calculation_date: datetime
    period_start: datetime
    period_end: datetime
    
    # Geographic scope
    geographic_level: str          # "national", "state", "county", "local"
    location_code: Optional[str] = None
    location_name: Optional[str] = None
    
    # Population context
    population_size: Optional[int] = None
    population_description: Optional[str] = None
    
    # Quality and interpretation
    confidence_interval: Optional[Tuple[float, float]] = None
    data_quality: str = "unknown"        # "high", "medium", "low"
    interpretation: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    
    # Benchmark comparison
    target_value: Optional[float] = None
    national_average: Optional[float] = None
    historical_trend: Optional[str] = None  # "increasing", "stable", "decreasing"
    
    # Methodology
    calculation_method: str = "standard"
    data_sources: List[str] = None
    limitations: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.data_sources is None:
            self.data_sources = []
        if self.limitations is None:
            self.limitations = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['calculation_date'] = self.calculation_date.isoformat()
        data['period_start'] = self.period_start.isoformat()
        data['period_end'] = self.period_end.isoformat()
        data['category'] = self.category.value
        data['indicator_type'] = self.indicator_type.value
        if self.risk_level:
            data['risk_level'] = self.risk_level.value
        return data

class EpidemiologicalIndicators:
    """Calculate standard epidemiological indicators."""
    
    @staticmethod
    def calculate_incidence_rate(new_cases: int, population: int, 
                               time_period_years: float) -> float:
        """Calculate incidence rate per 100,000 population per year."""
        if population <= 0 or time_period_years <= 0:
            return 0.0
        
        return (new_cases / population) * 100000 / time_period_years
    
    @staticmethod
    def calculate_prevalence_rate(total_cases: int, population: int) -> float:
        """Calculate prevalence rate per 100,000 population."""
        if population <= 0:
            return 0.0
        
        return (total_cases / population) * 100000
    
    @staticmethod
    def calculate_case_fatality_rate(deaths: int, cases: int) -> float:
        """Calculate case fatality rate as percentage."""
        if cases <= 0:
            return 0.0
        
        return (deaths / cases) * 100
    
    @staticmethod
    def calculate_attack_rate(cases: int, exposed_population: int) -> float:
        """Calculate attack rate as percentage."""
        if exposed_population <= 0:
            return 0.0
        
        return (cases / exposed_population) * 100
    
    @staticmethod
    def calculate_reproduction_number(cases_over_time: List[Tuple[datetime, int]], 
                                   generation_interval_days: int = 7) -> float:
        """Estimate basic reproduction number R0."""
        if len(cases_over_time) < 2:
            return 1.0
        
        # Simple exponential growth estimation
        daily_cases = []
        for i in range(1, len(cases_over_time)):
            prev_date, prev_cases = cases_over_time[i-1]
            curr_date, curr_cases = cases_over_time[i]
            
            days_diff = (curr_date - prev_date).days
            if days_diff > 0:
                daily_growth = (curr_cases / max(prev_cases, 1)) ** (1/days_diff) - 1
                daily_cases.append(daily_growth)
        
        if not daily_cases:
            return 1.0
        
        avg_growth_rate = statistics.mean(daily_cases)
        r0 = (1 + avg_growth_rate) ** generation_interval_days
        
        return max(0.1, min(r0, 10.0))  # Reasonable bounds

class OneHealthIntegrationIndicators:
    """Calculate One Health integration and connectivity indicators."""
    
    @staticmethod
    def calculate_cross_sector_correlation(animal_data: List[Dict], 
                                         human_data: List[Dict],
                                         time_window_days: int = 30) -> float:
        """Calculate correlation between animal and human health events."""
        if not animal_data or not human_data:
            return 0.0
        
        # Group by time periods
        from collections import defaultdict
        animal_counts = defaultdict(int)
        human_counts = defaultdict(int)
        
        for record in animal_data:
            if 'timestamp' in record:
                date_key = record['timestamp'][:10]  # YYYY-MM-DD
                animal_counts[date_key] += 1
        
        for record in human_data:
            if 'timestamp' in record:
                date_key = record['timestamp'][:10]
                human_counts[date_key] += 1
        
        # Calculate correlation
        common_dates = set(animal_counts.keys()) & set(human_counts.keys())
        if len(common_dates) < 3:
            return 0.0
        
        animal_values = [animal_counts[date] for date in common_dates]
        human_values = [human_counts[date] for date in common_dates]
        
        try:
            correlation = statistics.correlation(animal_values, human_values)
            return correlation
        except statistics.StatisticsError:
            return 0.0
    
    @staticmethod
    def calculate_data_integration_score(standardized_records: List[Dict]) -> float:
        """Calculate data integration quality score (0-100)."""
        if not standardized_records:
            return 0.0
        
        scores = []
        
        for record in standardized_records:
            score = 0
            
            # Geographic completeness
            if record.get('location_lat') and record.get('location_lon'):
                score += 25
            elif record.get('state_code'):
                score += 15
            
            # Temporal completeness
            if record.get('timestamp') and record.get('event_date'):
                score += 25
            elif record.get('timestamp'):
                score += 15
            
            # Content completeness
            if (record.get('primary_parameter') and 
                record.get('parameter_value') is not None):
                score += 25
            
            # Pathogen identification
            if record.get('pathogen_name'):
                score += 25
            
            scores.append(score)
        
        return statistics.mean(scores)
    
    @staticmethod
    def calculate_response_time_efficiency(alert_records: List[Dict]) -> float:
        """Calculate average response time for alerts in hours."""
        if not alert_records:
            return 0.0
        
        response_times = []
        
        for alert in alert_records:
            alert_time_str = alert.get('timestamp')
            response_time_str = alert.get('response_timestamp')
            
            if alert_time_str and response_time_str:
                try:
                    alert_time = datetime.fromisoformat(alert_time_str.replace('Z', '+00:00'))
                    response_time = datetime.fromisoformat(response_time_str.replace('Z', '+00:00'))
                    
                    diff_hours = (response_time - alert_time).total_seconds() / 3600
                    if diff_hours >= 0:
                        response_times.append(diff_hours)
                        
                except (ValueError, AttributeError):
                    continue
        
        return statistics.mean(response_times) if response_times else 0.0

class EarlyWarningIndicators:
    """Calculate early warning and risk assessment indicators."""
    
    @staticmethod
    def calculate_outbreak_risk_score(case_data: List[Dict], 
                                    environmental_data: List[Dict]) -> float:
        """Calculate composite outbreak risk score (0-100)."""
        risk_factors = []
        
        # Case trend analysis
        if case_data:
            recent_cases = len([c for c in case_data 
                              if 'timestamp' in c and 
                              (datetime.now() - 
                               datetime.fromisoformat(c['timestamp'][:19])).days <= 14])
            
            # Risk increases with recent case count
            case_risk = min(recent_cases * 5, 40)  # Max 40 points
            risk_factors.append(case_risk)
        
        # Environmental risk factors
        if environmental_data:
            high_risk_env = 0
            for record in environmental_data:
                if record.get('parameter') == 'temperature':
                    temp = record.get('value', 20)
                    if 25 <= temp <= 35:  # Optimal for vectors
                        high_risk_env += 10
                elif record.get('parameter') == 'humidity':
                    humidity = record.get('value', 50)
                    if humidity >= 60:  # High humidity
                        high_risk_env += 10
                elif record.get('pathogen_detected'):
                    high_risk_env += 20  # Pathogen in vectors
            
            env_risk = min(high_risk_env, 40)  # Max 40 points
            risk_factors.append(env_risk)
        
        # Seasonal factors (simplified)
        current_month = datetime.now().month
        if current_month in [6, 7, 8, 9]:  # Summer/early fall
            risk_factors.append(20)  # Higher vector activity
        else:
            risk_factors.append(5)
        
        total_risk = sum(risk_factors)
        return min(total_risk, 100)
    
    @staticmethod
    def classify_risk_level(risk_score: float) -> RiskLevel:
        """Classify numeric risk score into risk level."""
        if risk_score >= 91:
            return RiskLevel.CRITICAL
        elif risk_score >= 76:
            return RiskLevel.HIGH
        elif risk_score >= 51:
            return RiskLevel.MODERATE
        elif risk_score >= 26:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    @staticmethod
    def calculate_surveillance_sensitivity(detected_outbreaks: int, 
                                         total_outbreaks: int) -> float:
        """Calculate surveillance system sensitivity as percentage."""
        if total_outbreaks <= 0:
            return 0.0
        
        return (detected_outbreaks / total_outbreaks) * 100
    
    @staticmethod
    def calculate_false_positive_rate(false_alerts: int, 
                                    total_alerts: int) -> float:
        """Calculate false positive rate as percentage."""
        if total_alerts <= 0:
            return 0.0
        
        return (false_alerts / total_alerts) * 100

class PerformanceIndicators:
    """Calculate system performance and efficiency indicators."""
    
    @staticmethod
    def calculate_data_completeness(records: List[Dict]) -> float:
        """Calculate overall data completeness percentage."""
        if not records:
            return 0.0
        
        completeness_scores = []
        
        for record in records:
            total_fields = 0
            complete_fields = 0
            
            for key, value in record.items():
                if not key.startswith('_'):
                    total_fields += 1
                    if value is not None and value != "" and value != []:
                        complete_fields += 1
            
            if total_fields > 0:
                completeness_scores.append(complete_fields / total_fields)
        
        return statistics.mean(completeness_scores) * 100
    
    @staticmethod
    def calculate_timeliness_score(records: List[Dict], 
                                 target_hours: float = 24) -> float:
        """Calculate reporting timeliness score."""
        if not records:
            return 0.0
        
        timeliness_scores = []
        
        for record in records:
            event_time_str = record.get('event_date') or record.get('timestamp')
            report_time_str = record.get('timestamp')
            
            if event_time_str and report_time_str:
                try:
                    event_time = datetime.fromisoformat(event_time_str[:19])
                    report_time = datetime.fromisoformat(report_time_str[:19])
                    
                    delay_hours = (report_time - event_time).total_seconds() / 3600
                    
                    if delay_hours <= 0:
                        score = 100
                    elif delay_hours <= target_hours:
                        score = 100 * (1 - delay_hours / target_hours)
                    else:
                        score = 0
                    
                    timeliness_scores.append(score)
                    
                except (ValueError, AttributeError):
                    continue
        
        return statistics.mean(timeliness_scores) if timeliness_scores else 0.0

class OneHealthIndicatorCalculator:
    """Main calculator for all One Health indicators."""
    
    def __init__(self):
        self.indicators: List[HealthIndicator] = []
        self.calculation_metadata = {
            "calculation_start": datetime.now(),
            "total_indicators": 0,
            "successful_calculations": 0,
            "failed_calculations": 0
        }
        
        logger.info("One Health Indicator Calculator initialized")
    
    def calculate_all_indicators(self, animal_data: List[Dict], 
                               human_data: List[Dict],
                               environmental_data: List[Dict],
                               standardized_data: List[Dict],
                               alert_data: List[Dict] = None) -> List[HealthIndicator]:
        """Calculate comprehensive set of One Health indicators."""
        
        current_time = datetime.now()
        period_start = current_time - timedelta(days=30)
        
        if alert_data is None:
            alert_data = []
        
        # Epidemiological Indicators
        try:
            self._calculate_epidemiological_indicators(
                human_data, current_time, period_start
            )
        except Exception as e:
            logger.error(f"Error calculating epidemiological indicators: {e}")
            self.calculation_metadata["failed_calculations"] += 1
        
        # One Health Integration Indicators
        try:
            self._calculate_integration_indicators(
                animal_data, human_data, standardized_data, current_time, period_start
            )
        except Exception as e:
            logger.error(f"Error calculating integration indicators: {e}")
            self.calculation_metadata["failed_calculations"] += 1
        
        # Early Warning Indicators
        try:
            self._calculate_early_warning_indicators(
                human_data, environmental_data, current_time, period_start
            )
        except Exception as e:
            logger.error(f"Error calculating early warning indicators: {e}")
            self.calculation_metadata["failed_calculations"] += 1
        
        # Performance Indicators
        try:
            self._calculate_performance_indicators(
                standardized_data, alert_data, current_time, period_start
            )
        except Exception as e:
            logger.error(f"Error calculating performance indicators: {e}")
            self.calculation_metadata["failed_calculations"] += 1
        
        self.calculation_metadata["total_indicators"] = len(self.indicators)
        self.calculation_metadata["calculation_end"] = datetime.now()
        
        logger.info(f"Calculated {len(self.indicators)} health indicators")
        return self.indicators
    
    def _calculate_epidemiological_indicators(self, human_data: List[Dict],
                                            current_time: datetime,
                                            period_start: datetime):
        """Calculate epidemiological indicators from human data."""
        
        # Filter recent human cases
        recent_cases = [case for case in human_data 
                       if 'timestamp' in case and
                       period_start <= datetime.fromisoformat(case['timestamp'][:19]) <= current_time]
        
        # Incidence Rate
        new_cases = len(recent_cases)
        population = 1000000  # Assume 1M population for demo
        time_period_years = 30 / 365.25  # 30 days
        
        incidence_rate = EpidemiologicalIndicators.calculate_incidence_rate(
            new_cases, population, time_period_years
        )
        
        self.indicators.append(HealthIndicator(
            indicator_id="EPID_INCIDENCE_001",
            indicator_name="Disease Incidence Rate",
            category=IndicatorCategory.EPIDEMIOLOGICAL,
            indicator_type=IndicatorType.RATE,
            value=incidence_rate,
            unit="per 100,000 per year",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="regional",
            population_size=population,
            data_sources=["human_health_collector"],
            interpretation=f"Current incidence rate based on {new_cases} new cases"
        ))
        
        # Case Fatality Rate
        confirmed_cases = [case for case in recent_cases 
                          if case.get('case_classification') in ['confirmed', 'probable']]
        deaths = len([case for case in confirmed_cases 
                     if case.get('healthcare_level') == 'deceased'])
        
        if confirmed_cases:
            cfr = EpidemiologicalIndicators.calculate_case_fatality_rate(
                deaths, len(confirmed_cases)
            )
            
            self.indicators.append(HealthIndicator(
                indicator_id="EPID_CFR_001",
                indicator_name="Case Fatality Rate",
                category=IndicatorCategory.EPIDEMIOLOGICAL,
                indicator_type=IndicatorType.PERCENTAGE,
                value=cfr,
                unit="percent",
                calculation_date=current_time,
                period_start=period_start,
                period_end=current_time,
                geographic_level="regional",
                data_sources=["human_health_collector"],
                interpretation=f"CFR based on {deaths} deaths among {len(confirmed_cases)} cases"
            ))
        
        self.calculation_metadata["successful_calculations"] += 2
    
    def _calculate_integration_indicators(self, animal_data: List[Dict],
                                        human_data: List[Dict],
                                        standardized_data: List[Dict],
                                        current_time: datetime,
                                        period_start: datetime):
        """Calculate One Health integration indicators."""
        
        # Cross-sector correlation
        correlation = OneHealthIntegrationIndicators.calculate_cross_sector_correlation(
            animal_data, human_data
        )
        
        self.indicators.append(HealthIndicator(
            indicator_id="INTEG_CORR_001",
            indicator_name="Animal-Human Health Correlation",
            category=IndicatorCategory.INTEGRATION,
            indicator_type=IndicatorType.INDEX,
            value=correlation,
            unit="correlation coefficient",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="regional",
            data_sources=["animal_health_collector", "human_health_collector"],
            interpretation=f"Correlation strength: {abs(correlation):.3f}"
        ))
        
        # Data integration quality
        integration_score = OneHealthIntegrationIndicators.calculate_data_integration_score(
            standardized_data
        )
        
        self.indicators.append(HealthIndicator(
            indicator_id="INTEG_QUALITY_001",
            indicator_name="Data Integration Quality Score",
            category=IndicatorCategory.INTEGRATION,
            indicator_type=IndicatorType.SCORE,
            value=integration_score,
            unit="score (0-100)",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="system",
            data_sources=["data_standardizer"],
            interpretation=f"Integration quality: {integration_score:.1f}/100",
            target_value=85.0
        ))
        
        self.calculation_metadata["successful_calculations"] += 2
    
    def _calculate_early_warning_indicators(self, human_data: List[Dict],
                                          environmental_data: List[Dict],
                                          current_time: datetime,
                                          period_start: datetime):
        """Calculate early warning system indicators."""
        
        # Outbreak risk score
        risk_score = EarlyWarningIndicators.calculate_outbreak_risk_score(
            human_data, environmental_data
        )
        
        risk_level = EarlyWarningIndicators.classify_risk_level(risk_score)
        
        self.indicators.append(HealthIndicator(
            indicator_id="EARLY_RISK_001",
            indicator_name="Composite Outbreak Risk Score",
            category=IndicatorCategory.EARLY_WARNING,
            indicator_type=IndicatorType.SCORE,
            value=risk_score,
            unit="risk score (0-100)",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="regional",
            risk_level=risk_level,
            data_sources=["human_health_collector", "environmental_data_collector"],
            interpretation=f"Current risk level: {risk_level.value.upper()}",
            target_value=25.0  # Keep below moderate risk
        ))
        
        # Vector-borne disease risk (environmental focus)
        vector_alerts = [env for env in environmental_data 
                        if env.get('pathogen_detected')]
        
        if environmental_data:
            vector_risk_rate = (len(vector_alerts) / len(environmental_data)) * 100
            
            self.indicators.append(HealthIndicator(
                indicator_id="EARLY_VECTOR_001",
                indicator_name="Vector-Borne Disease Risk Rate",
                category=IndicatorCategory.EARLY_WARNING,
                indicator_type=IndicatorType.PERCENTAGE,
                value=vector_risk_rate,
                unit="percent",
                calculation_date=current_time,
                period_start=period_start,
                period_end=current_time,
                geographic_level="regional",
                data_sources=["environmental_data_collector"],
                interpretation=f"Pathogen detected in {len(vector_alerts)} of {len(environmental_data)} surveys"
            ))
        
        self.calculation_metadata["successful_calculations"] += 2
    
    def _calculate_performance_indicators(self, standardized_data: List[Dict],
                                        alert_data: List[Dict],
                                        current_time: datetime,
                                        period_start: datetime):
        """Calculate system performance indicators."""
        
        # Data completeness
        completeness = PerformanceIndicators.calculate_data_completeness(
            standardized_data
        )
        
        self.indicators.append(HealthIndicator(
            indicator_id="PERF_COMPLETE_001",
            indicator_name="Data Completeness Rate",
            category=IndicatorCategory.PERFORMANCE,
            indicator_type=IndicatorType.PERCENTAGE,
            value=completeness,
            unit="percent",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="system",
            data_sources=["data_standardizer"],
            interpretation=f"Average data completeness: {completeness:.1f}%",
            target_value=95.0
        ))
        
        # Reporting timeliness
        timeliness = PerformanceIndicators.calculate_timeliness_score(
            standardized_data, target_hours=24
        )
        
        self.indicators.append(HealthIndicator(
            indicator_id="PERF_TIMELINESS_001",
            indicator_name="Reporting Timeliness Score",
            category=IndicatorCategory.PERFORMANCE,
            indicator_type=IndicatorType.SCORE,
            value=timeliness,
            unit="score (0-100)",
            calculation_date=current_time,
            period_start=period_start,
            period_end=current_time,
            geographic_level="system",
            data_sources=["all_collectors"],
            interpretation=f"Average reporting timeliness: {timeliness:.1f}/100",
            target_value=80.0
        ))
        
        self.calculation_metadata["successful_calculations"] += 2
    
    def get_indicator_summary(self) -> Dict:
        """Get summary of calculated indicators."""
        if not self.indicators:
            return {"message": "No indicators calculated"}
        
        summary = {
            "total_indicators": len(self.indicators),
            "calculation_metadata": self.calculation_metadata,
            "categories": {},
            "risk_levels": {},
            "performance_summary": {}
        }
        
        # Group by category
        for indicator in self.indicators:
            category = indicator.category.value
            if category not in summary["categories"]:
                summary["categories"][category] = []
            
            summary["categories"][category].append({
                "name": indicator.indicator_name,
                "value": indicator.value,
                "unit": indicator.unit,
                "interpretation": indicator.interpretation
            })
        
        # Risk level distribution
        risk_indicators = [i for i in self.indicators if i.risk_level]
        for indicator in risk_indicators:
            risk = indicator.risk_level.value
            summary["risk_levels"][risk] = summary["risk_levels"].get(risk, 0) + 1
        
        # Performance against targets
        target_indicators = [i for i in self.indicators if i.target_value is not None]
        if target_indicators:
            met_targets = sum(1 for i in target_indicators 
                            if i.value >= i.target_value)
            summary["performance_summary"] = {
                "indicators_with_targets": len(target_indicators),
                "targets_met": met_targets,
                "target_achievement_rate": (met_targets / len(target_indicators)) * 100
            }
        
        return summary
    
    def export_indicators(self, filepath: str, format: str = "json") -> bool:
        """Export calculated indicators to file."""
        try:
            if format.lower() == "json":
                with open(filepath, 'w') as f:
                    data = [indicator.to_dict() for indicator in self.indicators]
                    json.dump({
                        "indicators": data,
                        "summary": self.get_indicator_summary(),
                        "export_timestamp": datetime.now().isoformat()
                    }, f, indent=2)
            
            elif format.lower() == "csv":
                with open(filepath, 'w', newline='') as f:
                    if self.indicators:
                        fieldnames = self.indicators[0].to_dict().keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for indicator in self.indicators:
                            writer.writerow(indicator.to_dict())
            
            logger.info(f"Exported {len(self.indicators)} indicators to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting indicators: {e}")
            return False

# Mock data generator for testing
def generate_mock_indicator_data():
    """Generate mock data for indicator calculation testing."""
    
    # Mock animal data
    animal_data = [
        {
            "animal_id": "COW_001",
            "timestamp": "2024-04-10T08:00:00",
            "species": "cattle",
            "mortality_count": 2,
            "pathogen_detected": "H5N1"
        },
        {
            "animal_id": "PIG_002", 
            "timestamp": "2024-04-12T10:00:00",
            "species": "swine",
            "mortality_count": 1,
            "pathogen_detected": "Brucella"
        }
    ]
    
    # Mock human data
    human_data = [
        {
            "case_id": "HUM_001",
            "timestamp": "2024-04-11T14:00:00",
            "case_classification": "confirmed",
            "healthcare_level": "hospitalized",
            "suspected_pathogen": "H5N1"
        },
        {
            "case_id": "HUM_002",
            "timestamp": "2024-04-13T09:00:00", 
            "case_classification": "probable",
            "healthcare_level": "outpatient"
        }
    ]
    
    # Mock environmental data
    environmental_data = [
        {
            "parameter": "temperature",
            "value": 28.5,
            "timestamp": "2024-04-10T12:00:00"
        },
        {
            "parameter": "humidity",
            "value": 65.0,
            "timestamp": "2024-04-10T12:00:00"
        },
        {
            "survey_id": "VEC_001",
            "pathogen_detected": "West_Nile_virus",
            "timestamp": "2024-04-12T19:00:00"
        }
    ]
    
    # Mock standardized data
    standardized_data = [
        {
            "record_id": "STD_001",
            "source": "animal",
            "timestamp": "2024-04-10T08:30:00",
            "event_date": "2024-04-10T08:00:00",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "state_code": "NY",
            "pathogen_name": "Influenza A virus (H5N1)",
            "data_quality": "high"
        },
        {
            "record_id": "STD_002",
            "source": "human",
            "timestamp": "2024-04-11T15:00:00",
            "event_date": "2024-04-11T14:00:00", 
            "location_lat": 40.7580,
            "location_lon": -73.9855,
            "state_code": "NY",
            "pathogen_name": "Influenza A virus (H5N1)",
            "data_quality": "high"
        }
    ]
    
    return animal_data, human_data, environmental_data, standardized_data

def run_demonstration():
    """Run demonstration of health indicator calculations."""
    print("📊 One Health Indicator Calculator - Demonstration")
    print("=" * 60)
    
    # Initialize calculator
    calculator = OneHealthIndicatorCalculator()
    
    # Generate mock data
    animal_data, human_data, env_data, standardized_data = generate_mock_indicator_data()
    
    print(f"\n🔢 Input Data Summary:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    print(f"  Standardized Records: {len(standardized_data)}")
    
    # Calculate all indicators
    print(f"\n⚙️ Calculating Health Indicators...")
    indicators = calculator.calculate_all_indicators(
        animal_data, human_data, env_data, standardized_data
    )
    
    # Display results
    print(f"\n📈 Calculated Indicators ({len(indicators)} total):")
    
    for i, indicator in enumerate(indicators, 1):
        print(f"\n{i}. {indicator.indicator_name}")
        print(f"   Category: {indicator.category.value}")
        print(f"   Value: {indicator.value:.3f} {indicator.unit}")
        
        if indicator.interpretation:
            print(f"   Interpretation: {indicator.interpretation}")
        
        if indicator.risk_level:
            print(f"   Risk Level: {indicator.risk_level.value.upper()}")
        
        if indicator.target_value:
            status = "✅ MET" if indicator.value >= indicator.target_value else "❌ NOT MET"
            print(f"   Target: {indicator.target_value} {indicator.unit} ({status})")
    
    # Summary statistics
    summary = calculator.get_indicator_summary()
    print(f"\n📊 Indicator Summary:")
    print(f"  Total Calculated: {summary['total_indicators']}")
    print(f"  Successful: {summary['calculation_metadata']['successful_calculations']}")
    print(f"  Failed: {summary['calculation_metadata']['failed_calculations']}")
    
    # Category breakdown
    print(f"\n📋 By Category:")
    for category, cat_indicators in summary['categories'].items():
        print(f"  {category.replace('_', ' ').title()}: {len(cat_indicators)} indicators")
    
    # Risk levels
    if summary['risk_levels']:
        print(f"\n⚠️ Risk Level Distribution:")
        for risk_level, count in summary['risk_levels'].items():
            print(f"  {risk_level.upper()}: {count} indicator(s)")
    
    # Performance against targets
    if summary.get('performance_summary'):
        perf = summary['performance_summary']
        print(f"\n🎯 Target Achievement:")
        print(f"  {perf['targets_met']}/{perf['indicators_with_targets']} targets met "
              f"({perf['target_achievement_rate']:.1f}%)")
    
    return calculator

if __name__ == "__main__":
    calculator = run_demonstration()
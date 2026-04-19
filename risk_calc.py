"""
Risk Calculator
===============
Module 2: Essential Epidemiologic Tools

Comprehensive risk assessment and calculation engine for One Health surveillance
combining animal, human, and environmental risk factors for integrated threat evaluation.

NIW Focus: Advanced risk stratification enabling proactive public health responses.
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RiskCategory(Enum):
    """Risk assessment categories."""
    ZOONOTIC_TRANSMISSION = "zoonotic_transmission"
    OUTBREAK_POTENTIAL = "outbreak_potential"
    ENVIRONMENTAL_EXPOSURE = "environmental_exposure"
    VECTOR_BORNE = "vector_borne"
    FOODBORNE = "foodborne"
    OCCUPATIONAL = "occupational"
    COMMUNITY_SPREAD = "community_spread"

class RiskLevel(Enum):
    """Standardized risk levels."""
    MINIMAL = "minimal"      # 0-20%
    LOW = "low"             # 21-40%
    MODERATE = "moderate"   # 41-60%
    HIGH = "high"           # 61-80%
    CRITICAL = "critical"   # 81-100%

class ConfidenceLevel(Enum):
    """Confidence in risk assessment."""
    LOW = "low"           # Limited data
    MEDIUM = "medium"     # Adequate data
    HIGH = "high"         # Comprehensive data

@dataclass
class RiskFactor:
    """Individual risk factor component."""
    factor_id: str
    factor_name: str
    category: RiskCategory
    weight: float          # 0.0 to 1.0 importance weight
    value: float          # 0.0 to 100.0 risk score
    confidence: ConfidenceLevel
    data_source: str
    last_updated: datetime
    description: Optional[str] = None
    
    def weighted_score(self) -> float:
        """Calculate weighted risk score."""
        confidence_multiplier = {
            ConfidenceLevel.LOW: 0.7,
            ConfidenceLevel.MEDIUM: 0.85,
            ConfidenceLevel.HIGH: 1.0
        }
        
        return self.value * self.weight * confidence_multiplier[self.confidence]

@dataclass
class RiskAssessment:
    """Comprehensive risk assessment result."""
    assessment_id: str
    assessment_date: datetime
    location_lat: float
    location_lon: float
    geographic_scope: str      # "local", "county", "state", "regional"
    
    # Risk scores
    overall_risk_score: float  # 0-100 composite score
    risk_level: RiskLevel
    confidence_level: ConfidenceLevel
    
    # Component scores by category
    category_scores: Dict[str, float]
    risk_factors: List[RiskFactor]
    
    # Temporal context
    risk_trend: str           # "increasing", "stable", "decreasing"
    forecast_days: int        # Risk projection period
    
    # Recommendations
    recommended_actions: List[str]
    monitoring_priorities: List[str]
    
    # Validation
    expert_review: Optional[bool] = None
    peer_validation: Optional[bool] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['assessment_date'] = self.assessment_date.isoformat()
        data['risk_level'] = self.risk_level.value
        data['confidence_level'] = self.confidence_level.value
        
        # Convert risk factors
        data['risk_factors'] = [factor.to_dict() for factor in self.risk_factors]
        
        return data

class ZoonoticRiskCalculator:
    """Calculates zoonotic disease transmission risk."""
    
    @staticmethod
    def calculate_animal_contact_risk(animal_data: List[Dict]) -> RiskFactor:
        """Calculate risk from animal contact exposure."""
        if not animal_data:
            return RiskFactor(
                factor_id="ZOONOTIC_001",
                factor_name="Animal Contact Risk",
                category=RiskCategory.ZOONOTIC_TRANSMISSION,
                weight=0.3,
                value=0.0,
                confidence=ConfidenceLevel.LOW,
                data_source="animal_collector",
                last_updated=datetime.now()
            )
        
        # Analyze animal health data
        high_risk_species = ["poultry", "swine", "cattle", "wildlife"]
        risk_score = 0
        
        for record in animal_data:
            species = record.get('species', '').lower()
            if species in high_risk_species:
                risk_score += 15
                
            # Mortality/morbidity indicators
            mortality = record.get('mortality_count', 0)
            morbidity = record.get('morbidity_count', 0)
            
            if mortality > 5:
                risk_score += 20
            elif mortality > 2:
                risk_score += 10
                
            if morbidity > 10:
                risk_score += 15
            elif morbidity > 5:
                risk_score += 8
            
            # Pathogen detection
            if record.get('pathogen_detected'):
                pathogen = record.get('pathogen_detected').lower()
                high_risk_pathogens = ['h5n1', 'h1n1', 'brucella', 'salmonella']
                
                if any(hrp in pathogen for hrp in high_risk_pathogens):
                    risk_score += 25
                else:
                    risk_score += 10
        
        # Normalize to 0-100 scale
        final_score = min(risk_score, 100)
        
        return RiskFactor(
            factor_id="ZOONOTIC_001",
            factor_name="Animal Contact Risk",
            category=RiskCategory.ZOONOTIC_TRANSMISSION,
            weight=0.3,
            value=final_score,
            confidence=ConfidenceLevel.HIGH if len(animal_data) >= 5 else ConfidenceLevel.MEDIUM,
            data_source="animal_collector",
            last_updated=datetime.now(),
            description=f"Risk based on {len(animal_data)} animal health records"
        )
    
    @staticmethod
    def calculate_human_susceptibility(human_data: List[Dict]) -> RiskFactor:
        """Calculate human population susceptibility risk."""
        if not human_data:
            return RiskFactor(
                factor_id="ZOONOTIC_002",
                factor_name="Human Susceptibility Risk",
                category=RiskCategory.ZOONOTIC_TRANSMISSION,
                weight=0.25,
                value=30.0,  # Baseline population susceptibility
                confidence=ConfidenceLevel.LOW,
                data_source="human_collector",
                last_updated=datetime.now()
            )
        
        risk_score = 30  # Baseline
        
        # Analyze case severity and outcomes
        severe_cases = 0
        total_cases = len(human_data)
        high_risk_occupations = 0
        
        for record in human_data:
            # Severity indicators
            severity = record.get('severity', '').lower()
            healthcare_level = record.get('healthcare_level', '').lower()
            
            if severity in ['severe', 'critical']:
                severe_cases += 1
                risk_score += 8
                
            if healthcare_level in ['icu', 'deceased']:
                risk_score += 12
            elif healthcare_level == 'hospitalized':
                risk_score += 6
            
            # High-risk occupation exposure
            occupation = record.get('occupation', '').lower()
            high_risk_jobs = ['veterinarian', 'farm_worker', 'healthcare_worker']
            
            if any(job in occupation for job in high_risk_jobs):
                high_risk_occupations += 1
                risk_score += 5
            
            # Age vulnerability
            age_group = record.get('age_group', '').lower()
            if age_group in ['elderly', 'very_elderly', 'infant']:
                risk_score += 3
        
        # Population-level indicators
        if total_cases > 0:
            severe_rate = (severe_cases / total_cases) * 100
            if severe_rate > 20:
                risk_score += 15
            elif severe_rate > 10:
                risk_score += 8
        
        final_score = min(risk_score, 100)
        
        return RiskFactor(
            factor_id="ZOONOTIC_002",
            factor_name="Human Susceptibility Risk", 
            category=RiskCategory.ZOONOTIC_TRANSMISSION,
            weight=0.25,
            value=final_score,
            confidence=ConfidenceLevel.HIGH if total_cases >= 10 else ConfidenceLevel.MEDIUM,
            data_source="human_collector",
            last_updated=datetime.now(),
            description=f"Risk based on {total_cases} human cases, {severe_cases} severe"
        )

class EnvironmentalRiskCalculator:
    """Calculates environmental and vector-borne risk."""
    
    @staticmethod
    def calculate_vector_risk(environmental_data: List[Dict]) -> RiskFactor:
        """Calculate vector-borne disease transmission risk."""
        if not environmental_data:
            return RiskFactor(
                factor_id="VECTOR_001",
                factor_name="Vector-Borne Transmission Risk",
                category=RiskCategory.VECTOR_BORNE,
                weight=0.35,
                value=20.0,  # Baseline seasonal risk
                confidence=ConfidenceLevel.LOW,
                data_source="environmental_collector",
                last_updated=datetime.now()
            )
        
        risk_score = 20  # Baseline seasonal risk
        
        # Analyze climate conditions
        optimal_temp_count = 0
        optimal_humidity_count = 0
        pathogen_detections = 0
        high_vector_populations = 0
        
        for record in environmental_data:
            parameter = record.get('parameter', '').lower()
            value = record.get('value', 0)
            
            # Temperature analysis
            if parameter == 'temperature':
                if 20 <= value <= 35:  # Optimal for most vectors
                    optimal_temp_count += 1
                    risk_score += 5
                elif value > 40:  # Extreme heat may reduce vectors
                    risk_score -= 2
            
            # Humidity analysis  
            elif parameter == 'humidity':
                if value >= 60:  # High humidity favors vectors
                    optimal_humidity_count += 1
                    risk_score += 4
            
            # Precipitation (breeding sites)
            elif parameter == 'precipitation':
                if value > 15:  # Heavy rainfall creates breeding sites
                    risk_score += 6
                elif 5 <= value <= 15:  # Moderate rainfall
                    risk_score += 3
            
            # Vector population data
            elif parameter == 'vector_count' or 'vector' in record.get('survey_id', ''):
                vector_count = record.get('total_collected', value)
                if vector_count > 20:  # High vector density
                    high_vector_populations += 1
                    risk_score += 10
                elif vector_count > 10:
                    risk_score += 5
            
            # Pathogen in vectors
            if record.get('pathogen_detected'):
                pathogen_detections += 1
                pathogen = record.get('pathogen_detected').lower()
                
                critical_pathogens = ['west_nile_virus', 'dengue', 'zika', 'chikungunya']
                if any(cp in pathogen for cp in critical_pathogens):
                    risk_score += 20
                else:
                    risk_score += 12
        
        # Environmental favorability bonus
        if optimal_temp_count >= 2 and optimal_humidity_count >= 1:
            risk_score += 10  # Very favorable conditions
        
        final_score = min(risk_score, 100)
        
        return RiskFactor(
            factor_id="VECTOR_001", 
            factor_name="Vector-Borne Transmission Risk",
            category=RiskCategory.VECTOR_BORNE,
            weight=0.35,
            value=final_score,
            confidence=ConfidenceLevel.HIGH if len(environmental_data) >= 10 else ConfidenceLevel.MEDIUM,
            data_source="environmental_collector",
            last_updated=datetime.now(),
            description=f"Risk based on {len(environmental_data)} environmental records, {pathogen_detections} pathogen detections"
        )
    
    @staticmethod
    def calculate_climate_risk(environmental_data: List[Dict]) -> RiskFactor:
        """Calculate climate-related disease risk."""
        risk_score = 25  # Baseline climate risk
        
        extreme_events = 0
        
        for record in environmental_data:
            parameter = record.get('parameter', '').lower()
            value = record.get('value', 0)
            
            # Extreme weather events
            if parameter == 'temperature':
                if value > 40 or value < -10:  # Extreme temperatures
                    extreme_events += 1
                    risk_score += 8
            elif parameter == 'precipitation':
                if value > 50:  # Heavy rainfall/flooding
                    extreme_events += 1  
                    risk_score += 10
            elif parameter == 'wind_speed':
                if value > 100:  # Hurricane-force winds
                    extreme_events += 1
                    risk_score += 6
        
        # Climate change amplification
        current_month = datetime.now().month
        if current_month in [6, 7, 8, 9]:  # Peak season
            risk_score += 5
        
        final_score = min(risk_score, 100)
        
        return RiskFactor(
            factor_id="CLIMATE_001",
            factor_name="Climate-Related Disease Risk",
            category=RiskCategory.ENVIRONMENTAL_EXPOSURE, 
            weight=0.2,
            value=final_score,
            confidence=ConfidenceLevel.MEDIUM,
            data_source="environmental_collector",
            last_updated=datetime.now(),
            description=f"Climate risk with {extreme_events} extreme weather events"
        )

class OutbreakRiskCalculator:
    """Calculates outbreak potential and spread risk."""
    
    @staticmethod
    def calculate_transmission_potential(human_data: List[Dict], 
                                       population_density: int = 1000) -> RiskFactor:
        """Calculate disease transmission and outbreak potential."""
        if not human_data:
            return RiskFactor(
                factor_id="OUTBREAK_001",
                factor_name="Transmission Potential",
                category=RiskCategory.OUTBREAK_POTENTIAL,
                weight=0.4,
                value=15.0,
                confidence=ConfidenceLevel.LOW,
                data_source="human_collector",
                last_updated=datetime.now()
            )
        
        risk_score = 15  # Baseline transmission risk
        
        # Temporal clustering analysis
        recent_cases = []
        confirmed_cases = []
        
        cutoff_date = datetime.now() - timedelta(days=14)
        
        for record in human_data:
            timestamp_str = record.get('timestamp', '')
            case_class = record.get('case_classification', '').lower()
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str[:19])
                if timestamp >= cutoff_date:
                    recent_cases.append(record)
                
                if case_class in ['confirmed', 'probable']:
                    confirmed_cases.append(record)
                    
            except (ValueError, TypeError):
                continue
        
        # Recent case surge
        recent_count = len(recent_cases)
        if recent_count >= 10:
            risk_score += 25
        elif recent_count >= 5:
            risk_score += 15
        elif recent_count >= 3:
            risk_score += 8
        
        # Case confirmation rate
        total_cases = len(human_data)
        if total_cases > 0:
            confirmation_rate = len(confirmed_cases) / total_cases
            if confirmation_rate > 0.7:  # High confirmation suggests real outbreak
                risk_score += 15
            elif confirmation_rate > 0.5:
                risk_score += 10
        
        # Population density factor
        if population_density > 5000:  # High density areas
            risk_score += 10
        elif population_density > 2000:
            risk_score += 5
        
        # Person-to-person transmission indicators
        household_clusters = 0
        for record in human_data:
            household_size = record.get('household_size', 1)
            if household_size > 4:  # Large household risk
                risk_score += 2
                
            exposure_types = record.get('exposure_types', [])
            if isinstance(exposure_types, list) and 'person_to_person' in exposure_types:
                household_clusters += 1
                risk_score += 12
        
        final_score = min(risk_score, 100)
        
        return RiskFactor(
            factor_id="OUTBREAK_001",
            factor_name="Transmission Potential",
            category=RiskCategory.OUTBREAK_POTENTIAL,
            weight=0.4,
            value=final_score,
            confidence=ConfidenceLevel.HIGH if total_cases >= 8 else ConfidenceLevel.MEDIUM,
            data_source="human_collector",
            last_updated=datetime.now(),
            description=f"Outbreak risk based on {recent_count} recent cases, {len(confirmed_cases)} confirmed"
        )

class IntegratedRiskCalculator:
    """Main integrated risk assessment calculator."""
    
    def __init__(self):
        self.assessments: List[RiskAssessment] = []
        self.calculation_log: List[Dict] = []
        
        logger.info("Integrated Risk Calculator initialized")
    
    def calculate_comprehensive_risk(self, animal_data: List[Dict],
                                   human_data: List[Dict], 
                                   environmental_data: List[Dict],
                                   location_lat: float = 40.7128,
                                   location_lon: float = -74.0060,
                                   geographic_scope: str = "county") -> RiskAssessment:
        """Calculate comprehensive One Health risk assessment."""
        
        assessment_start = datetime.now()
        
        # Calculate individual risk factors
        risk_factors = []
        
        try:
            # Zoonotic transmission risks
            animal_contact_risk = ZoonoticRiskCalculator.calculate_animal_contact_risk(animal_data)
            risk_factors.append(animal_contact_risk)
            
            human_susceptibility = ZoonoticRiskCalculator.calculate_human_susceptibility(human_data)
            risk_factors.append(human_susceptibility)
            
            # Environmental risks
            vector_risk = EnvironmentalRiskCalculator.calculate_vector_risk(environmental_data)
            risk_factors.append(vector_risk)
            
            climate_risk = EnvironmentalRiskCalculator.calculate_climate_risk(environmental_data)
            risk_factors.append(climate_risk)
            
            # Outbreak potential
            transmission_risk = OutbreakRiskCalculator.calculate_transmission_potential(
                human_data, population_density=2500
            )
            risk_factors.append(transmission_risk)
            
            logger.info(f"Calculated {len(risk_factors)} risk factors")
            
        except Exception as e:
            logger.error(f"Error calculating risk factors: {e}")
            risk_factors = []
        
        # Calculate overall risk score
        if risk_factors:
            overall_score = self._calculate_weighted_risk_score(risk_factors)
        else:
            overall_score = 25.0  # Default moderate-low risk
        
        # Determine risk level and confidence
        risk_level = self._classify_risk_level(overall_score)
        confidence_level = self._assess_confidence_level(risk_factors)
        
        # Calculate category scores
        category_scores = self._calculate_category_scores(risk_factors)
        
        # Determine trend (simplified)
        risk_trend = self._analyze_risk_trend(human_data, environmental_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, category_scores, risk_factors)
        monitoring_priorities = self._identify_monitoring_priorities(risk_factors)
        
        # Create assessment
        assessment = RiskAssessment(
            assessment_id=f"RISK_ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            assessment_date=assessment_start,
            location_lat=location_lat,
            location_lon=location_lon,
            geographic_scope=geographic_scope,
            overall_risk_score=overall_score,
            risk_level=risk_level,
            confidence_level=confidence_level,
            category_scores=category_scores,
            risk_factors=risk_factors,
            risk_trend=risk_trend,
            forecast_days=14,
            recommended_actions=recommendations,
            monitoring_priorities=monitoring_priorities
        )
        
        self.assessments.append(assessment)
        
        # Log calculation
        self.calculation_log.append({
            "assessment_id": assessment.assessment_id,
            "calculation_time": (datetime.now() - assessment_start).total_seconds(),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            },
            "risk_factors_calculated": len(risk_factors),
            "overall_risk_score": overall_score,
            "risk_level": risk_level.value
        })
        
        logger.info(f"Completed risk assessment: {risk_level.value} risk ({overall_score:.1f}/100)")
        
        return assessment
    
    def _calculate_weighted_risk_score(self, risk_factors: List[RiskFactor]) -> float:
        """Calculate weighted composite risk score."""
        if not risk_factors:
            return 0.0
        
        total_weighted_score = 0
        total_weight = 0
        
        for factor in risk_factors:
            weighted_score = factor.weighted_score()
            total_weighted_score += weighted_score
            total_weight += factor.weight
        
        if total_weight == 0:
            return 0.0
        
        # Normalize to 0-100 scale
        normalized_score = (total_weighted_score / total_weight)
        return min(max(normalized_score, 0), 100)
    
    def _classify_risk_level(self, risk_score: float) -> RiskLevel:
        """Classify numeric risk score into risk level."""
        if risk_score >= 81:
            return RiskLevel.CRITICAL
        elif risk_score >= 61:
            return RiskLevel.HIGH
        elif risk_score >= 41:
            return RiskLevel.MODERATE
        elif risk_score >= 21:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _assess_confidence_level(self, risk_factors: List[RiskFactor]) -> ConfidenceLevel:
        """Assess overall confidence in risk assessment."""
        if not risk_factors:
            return ConfidenceLevel.LOW
        
        confidence_scores = []
        for factor in risk_factors:
            if factor.confidence == ConfidenceLevel.HIGH:
                confidence_scores.append(3)
            elif factor.confidence == ConfidenceLevel.MEDIUM:
                confidence_scores.append(2)
            else:
                confidence_scores.append(1)
        
        avg_confidence = statistics.mean(confidence_scores)
        
        if avg_confidence >= 2.5:
            return ConfidenceLevel.HIGH
        elif avg_confidence >= 1.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _calculate_category_scores(self, risk_factors: List[RiskFactor]) -> Dict[str, float]:
        """Calculate risk scores by category."""
        category_scores = {}
        
        for factor in risk_factors:
            category = factor.category.value
            weighted_score = factor.weighted_score()
            
            if category not in category_scores:
                category_scores[category] = weighted_score
            else:
                # Average multiple factors in same category
                category_scores[category] = (category_scores[category] + weighted_score) / 2
        
        return category_scores
    
    def _analyze_risk_trend(self, human_data: List[Dict], 
                          environmental_data: List[Dict]) -> str:
        """Analyze risk trend direction."""
        
        # Simple trend analysis based on recent vs. older data
        recent_cutoff = datetime.now() - timedelta(days=7)
        older_cutoff = datetime.now() - timedelta(days=14)
        
        recent_human_cases = 0
        older_human_cases = 0
        
        for record in human_data:
            timestamp_str = record.get('timestamp', '')
            try:
                timestamp = datetime.fromisoformat(timestamp_str[:19])
                if timestamp >= recent_cutoff:
                    recent_human_cases += 1
                elif timestamp >= older_cutoff:
                    older_human_cases += 1
            except (ValueError, TypeError):
                continue
        
        # Environmental pathogen trend
        recent_env_pathogens = 0
        older_env_pathogens = 0
        
        for record in environmental_data:
            if record.get('pathogen_detected'):
                timestamp_str = record.get('timestamp', '')
                try:
                    timestamp = datetime.fromisoformat(timestamp_str[:19])
                    if timestamp >= recent_cutoff:
                        recent_env_pathogens += 1
                    elif timestamp >= older_cutoff:
                        older_env_pathogens += 1
                except (ValueError, TypeError):
                    continue
        
        # Determine trend
        human_trend = recent_human_cases - older_human_cases
        env_trend = recent_env_pathogens - older_env_pathogens
        
        if human_trend > 1 or env_trend > 0:
            return "increasing"
        elif human_trend < -1 or env_trend < 0:
            return "decreasing" 
        else:
            return "stable"
    
    def _generate_recommendations(self, risk_level: RiskLevel,
                                category_scores: Dict[str, float],
                                risk_factors: List[RiskFactor]) -> List[str]:
        """Generate risk-appropriate recommendations."""
        recommendations = []
        
        # General recommendations by risk level
        if risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "Activate emergency response protocols",
                "Implement immediate containment measures",
                "Alert public health authorities",
                "Enhance active surveillance"
            ])
        elif risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Increase surveillance frequency",
                "Prepare response resources",
                "Issue health advisories",
                "Coordinate cross-sector response"
            ])
        elif risk_level == RiskLevel.MODERATE:
            recommendations.extend([
                "Maintain enhanced monitoring",
                "Review preparedness plans",
                "Educate high-risk populations"
            ])
        else:
            recommendations.extend([
                "Continue routine surveillance", 
                "Monitor for changes"
            ])
        
        # Category-specific recommendations
        for category, score in category_scores.items():
            if score > 60:
                if category == "zoonotic_transmission":
                    recommendations.append("Strengthen animal-human interface surveillance")
                elif category == "vector_borne":
                    recommendations.append("Implement vector control measures")
                elif category == "outbreak_potential":
                    recommendations.append("Prepare outbreak investigation resources")
                elif category == "environmental_exposure":
                    recommendations.append("Monitor environmental conditions closely")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _identify_monitoring_priorities(self, risk_factors: List[RiskFactor]) -> List[str]:
        """Identify monitoring priorities based on risk factors."""
        priorities = []
        
        # Sort risk factors by weighted score
        sorted_factors = sorted(risk_factors, 
                              key=lambda f: f.weighted_score(), 
                              reverse=True)
        
        for factor in sorted_factors[:3]:  # Top 3 priorities
            if factor.weighted_score() > 30:
                category = factor.category.value.replace('_', ' ').title()
                priorities.append(f"Monitor {category}")
        
        # Add data quality priorities
        low_confidence_factors = [f for f in risk_factors 
                                if f.confidence == ConfidenceLevel.LOW]
        
        if low_confidence_factors:
            priorities.append("Improve data collection quality")
        
        return priorities
    
    def get_assessment_summary(self) -> Dict:
        """Get summary of all risk assessments."""
        if not self.assessments:
            return {"message": "No risk assessments completed"}
        
        latest = self.assessments[-1]
        
        return {
            "total_assessments": len(self.assessments),
            "latest_assessment": {
                "assessment_id": latest.assessment_id,
                "overall_risk_score": latest.overall_risk_score,
                "risk_level": latest.risk_level.value,
                "confidence_level": latest.confidence_level.value,
                "risk_trend": latest.risk_trend,
                "category_scores": latest.category_scores,
                "recommendations_count": len(latest.recommended_actions)
            },
            "calculation_performance": {
                "average_calculation_time": statistics.mean([
                    log['calculation_time'] for log in self.calculation_log
                ]) if self.calculation_log else 0,
                "total_risk_factors_calculated": sum([
                    log['risk_factors_calculated'] for log in self.calculation_log
                ])
            }
        }

# Mock data generator for testing
def generate_mock_risk_data():
    """Generate mock data for risk calculation testing."""
    
    # Mock animal data with higher risk scenario
    animal_data = [
        {
            "species": "poultry",
            "mortality_count": 12,
            "morbidity_count": 25,
            "pathogen_detected": "H5N1",
            "timestamp": "2024-04-13T08:00:00"
        },
        {
            "species": "cattle",
            "mortality_count": 3,
            "morbidity_count": 8,
            "pathogen_detected": "Brucella",
            "timestamp": "2024-04-12T14:00:00"
        },
        {
            "species": "swine",
            "mortality_count": 1,
            "morbidity_count": 4,
            "timestamp": "2024-04-14T10:00:00"
        }
    ]
    
    # Mock human data with outbreak indicators
    human_data = [
        {
            "case_classification": "confirmed",
            "severity": "severe",
            "healthcare_level": "hospitalized",
            "occupation": "farm_worker",
            "age_group": "adult",
            "household_size": 6,
            "exposure_types": ["direct_animal_contact"],
            "timestamp": "2024-04-13T15:00:00"
        },
        {
            "case_classification": "probable", 
            "severity": "moderate",
            "healthcare_level": "emergency_department",
            "occupation": "veterinarian",
            "age_group": "adult",
            "household_size": 4,
            "exposure_types": ["direct_animal_contact", "occupational"],
            "timestamp": "2024-04-14T09:00:00"
        },
        {
            "case_classification": "confirmed",
            "severity": "critical", 
            "healthcare_level": "icu",
            "age_group": "elderly",
            "household_size": 2,
            "exposure_types": ["person_to_person"],
            "timestamp": "2024-04-14T12:00:00"
        }
    ]
    
    # Mock environmental data with vector risk
    environmental_data = [
        {
            "parameter": "temperature",
            "value": 28.5,
            "timestamp": "2024-04-14T12:00:00"
        },
        {
            "parameter": "humidity", 
            "value": 68.0,
            "timestamp": "2024-04-14T12:00:00"
        },
        {
            "parameter": "precipitation",
            "value": 18.5,
            "timestamp": "2024-04-13T00:00:00"
        },
        {
            "survey_id": "VEC_001",
            "parameter": "vector_count",
            "total_collected": 35,
            "pathogen_detected": "West_Nile_virus",
            "timestamp": "2024-04-13T20:00:00"
        },
        {
            "parameter": "wind_speed",
            "value": 45.0,
            "timestamp": "2024-04-14T06:00:00"
        }
    ]
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of integrated risk calculation."""
    print("🎯 Integrated Risk Calculator - Demonstration")
    print("=" * 60)
    
    # Initialize calculator
    calculator = IntegratedRiskCalculator()
    
    # Generate mock data
    animal_data, human_data, env_data = generate_mock_risk_data()
    
    print(f"\n📊 Input Data Summary:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")  
    print(f"  Environmental Records: {len(env_data)}")
    
    # Calculate comprehensive risk
    print(f"\n⚙️ Calculating Integrated Risk Assessment...")
    assessment = calculator.calculate_comprehensive_risk(
        animal_data=animal_data,
        human_data=human_data,
        environmental_data=env_data,
        location_lat=40.7128,
        location_lon=-74.0060,
        geographic_scope="county"
    )
    
    # Display results
    print(f"\n📈 Risk Assessment Results:")
    print(f"  Assessment ID: {assessment.assessment_id}")
    print(f"  Overall Risk Score: {assessment.overall_risk_score:.1f}/100")
    print(f"  Risk Level: {assessment.risk_level.value.upper()}")
    print(f"  Confidence: {assessment.confidence_level.value.upper()}")
    print(f"  Risk Trend: {assessment.risk_trend.upper()}")
    
    # Category breakdown
    print(f"\n📋 Risk by Category:")
    for category, score in assessment.category_scores.items():
        category_display = category.replace('_', ' ').title()
        print(f"  {category_display}: {score:.1f}/100")
    
    # Individual risk factors
    print(f"\n🔍 Risk Factor Details:")
    for i, factor in enumerate(assessment.risk_factors, 1):
        weighted_score = factor.weighted_score()
        print(f"  {i}. {factor.factor_name}")
        print(f"     Score: {factor.value:.1f} (weighted: {weighted_score:.1f})")
        print(f"     Weight: {factor.weight:.2f}, Confidence: {factor.confidence.value}")
    
    # Recommendations
    print(f"\n💡 Recommended Actions ({len(assessment.recommended_actions)}):")
    for i, action in enumerate(assessment.recommended_actions, 1):
        print(f"  {i}. {action}")
    
    # Monitoring priorities
    print(f"\n🎯 Monitoring Priorities ({len(assessment.monitoring_priorities)}):")
    for i, priority in enumerate(assessment.monitoring_priorities, 1):
        print(f"  {i}. {priority}")
    
    # Summary statistics
    summary = calculator.get_assessment_summary()
    print(f"\n📊 Calculator Performance:")
    print(f"  Calculation Time: {summary['calculation_performance']['average_calculation_time']:.3f} seconds")
    print(f"  Risk Factors Calculated: {summary['calculation_performance']['total_risk_factors_calculated']}")
    
    return calculator

if __name__ == "__main__":
    calculator = run_demonstration()
"""
Human Health Data Collector
===========================
Module 1: Data and Health Indicators in Public Health Practice

Collects and standardizes human health surveillance data for zoonotic disease monitoring
following epidemiological principles and case definitions.

NIW Focus: Integration of human surveillance with animal health for early zoonotic detection.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import random
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgeGroup(Enum):
    """Standardized age group classification for epidemiological analysis."""
    INFANT = "0-2"           # 0-2 years
    TODDLER = "3-5"          # 3-5 years
    CHILD = "6-12"           # 6-12 years
    ADOLESCENT = "13-17"     # 13-17 years
    YOUNG_ADULT = "18-30"    # 18-30 years
    ADULT = "31-50"          # 31-50 years
    MIDDLE_AGED = "51-65"    # 51-65 years
    ELDERLY = "66-80"        # 66-80 years
    VERY_ELDERLY = "81+"     # 81+ years

class CaseClassification(Enum):
    """Standard case classification based on CDC definitions."""
    SUSPECTED = "suspected"
    PROBABLE = "probable"
    CONFIRMED = "confirmed"
    NOT_CASE = "not_case"
    UNDER_INVESTIGATION = "under_investigation"

class ExposureType(Enum):
    """Types of potential zoonotic exposure."""
    DIRECT_ANIMAL_CONTACT = "direct_animal_contact"
    INDIRECT_ANIMAL_CONTACT = "indirect_animal_contact" 
    VECTOR_BITE = "vector_bite"
    ENVIRONMENTAL = "environmental"
    FOODBORNE = "foodborne"
    WATERBORNE = "waterborne"
    PERSON_TO_PERSON = "person_to_person"
    LABORATORY = "laboratory"
    OCCUPATIONAL = "occupational"
    UNKNOWN = "unknown"

class SymptomSeverity(Enum):
    """Symptom severity classification."""
    ASYMPTOMATIC = "asymptomatic"
    MILD = "mild"
    MODERATE = "moderate" 
    SEVERE = "severe"
    CRITICAL = "critical"

class HealthcareLevel(Enum):
    """Level of healthcare interaction."""
    NONE = "none"
    OUTPATIENT = "outpatient"
    EMERGENCY_DEPT = "emergency_department"
    HOSPITALIZED = "hospitalized"
    ICU = "intensive_care"
    DECEASED = "deceased"

@dataclass
class HumanHealthRecord:
    """Standardized human health surveillance record for zoonotic diseases."""
    case_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    county: str
    state: str
    age_group: AgeGroup
    sex: str  # "M", "F", "U" (unknown)
    symptoms: List[str]
    onset_date: datetime
    case_classification: CaseClassification
    severity: SymptomSeverity
    healthcare_level: HealthcareLevel
    exposure_types: List[ExposureType]
    animal_exposure_details: Optional[Dict]
    suspected_pathogen: Optional[str]
    confirmed_pathogen: Optional[str]
    diagnostic_tests: List[str]
    occupation: Optional[str]
    travel_history: Optional[List[Dict]]
    household_size: int
    reporting_facility: str
    reporter_type: str  # "physician", "laboratory", "hospital", "public_health"
    follow_up_needed: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['onset_date'] = self.onset_date.isoformat()
        data['age_group'] = self.age_group.value
        data['case_classification'] = self.case_classification.value
        data['severity'] = self.severity.value
        data['healthcare_level'] = self.healthcare_level.value
        data['exposure_types'] = [exp.value for exp in self.exposure_types]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HumanHealthRecord':
        """Create from dictionary."""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['onset_date'] = datetime.fromisoformat(data['onset_date'])
        data['age_group'] = AgeGroup(data['age_group'])
        data['case_classification'] = CaseClassification(data['case_classification'])
        data['severity'] = SymptomSeverity(data['severity'])
        data['healthcare_level'] = HealthcareLevel(data['healthcare_level'])
        data['exposure_types'] = [ExposureType(exp) for exp in data['exposure_types']]
        return cls(**data)

class ZoonoticSyndromes:
    """Standardized syndromic surveillance definitions for zoonotic diseases."""
    
    RESPIRATORY_SYNDROME = [
        "fever", "cough", "dyspnea", "chest_pain", "sore_throat", 
        "pneumonia", "acute_respiratory_distress"
    ]
    
    FEBRILE_SYNDROME = [
        "fever", "chills", "sweats", "headache", "myalgia", 
        "fatigue", "malaise"
    ]
    
    GASTROINTESTINAL_SYNDROME = [
        "nausea", "vomiting", "diarrhea", "abdominal_pain", 
        "bloody_stools", "cramping"
    ]
    
    NEUROLOGICAL_SYNDROME = [
        "confusion", "seizures", "encephalitis", "meningitis", 
        "paralysis", "weakness", "altered_mental_status"
    ]
    
    HEMORRHAGIC_SYNDROME = [
        "bleeding", "petechiae", "bruising", "nosebleeds", 
        "blood_vomit", "bloody_urine"
    ]
    
    CUTANEOUS_SYNDROME = [
        "rash", "skin_lesions", "ulcers", "lymphadenopathy",
        "eschar", "cellulitis"
    ]
    
    @classmethod
    def classify_syndrome(cls, symptoms: List[str]) -> List[str]:
        """Classify symptoms into syndromic categories."""
        syndromes = []
        
        if any(s in cls.RESPIRATORY_SYNDROME for s in symptoms):
            syndromes.append("RESPIRATORY")
        if any(s in cls.FEBRILE_SYNDROME for s in symptoms):
            syndromes.append("FEBRILE")
        if any(s in cls.GASTROINTESTINAL_SYNDROME for s in symptoms):
            syndromes.append("GASTROINTESTINAL")
        if any(s in cls.NEUROLOGICAL_SYNDROME for s in symptoms):
            syndromes.append("NEUROLOGICAL")
        if any(s in cls.HEMORRHAGIC_SYNDROME for s in symptoms):
            syndromes.append("HEMORRHAGIC")
        if any(s in cls.CUTANEOUS_SYNDROME for s in symptoms):
            syndromes.append("CUTANEOUS")
        
        return syndromes if syndromes else ["UNDIFFERENTIATED"]

class HighRiskOccupations:
    """High risk occupations for zoonotic disease exposure."""
    
    TIER_1_HIGHEST = [
        "veterinarian", "animal_technician", "farm_worker", 
        "slaughterhouse_worker", "wildlife_biologist", "zoo_keeper"
    ]
    
    TIER_2_HIGH = [
        "laboratory_worker", "healthcare_worker", "public_health_worker",
        "agricultural_inspector", "animal_control_officer"
    ]
    
    TIER_3_MODERATE = [
        "outdoor_worker", "hunter", "fisher", "park_ranger",
        "landscaper", "construction_worker", "postal_worker"
    ]
    
    @classmethod
    def get_risk_level(cls, occupation: str) -> str:
        """Get occupational risk level."""
        if occupation and occupation.lower() in [occ.lower() for occ in cls.TIER_1_HIGHEST]:
            return "HIGHEST"
        elif occupation and occupation.lower() in [occ.lower() for occ in cls.TIER_2_HIGH]:
            return "HIGH"
        elif occupation and occupation.lower() in [occ.lower() for occ in cls.TIER_3_MODERATE]:
            return "MODERATE"
        else:
            return "LOW"

class OutbreakThresholds:
    """Epidemiological thresholds for outbreak detection."""
    
    # Cases per 100,000 population that trigger investigation
    INVESTIGATION_THRESHOLDS = {
        "H5N1": 1,                    # Any case triggers investigation
        "SARS-CoV": 1,               # Any case triggers investigation
        "MERS-CoV": 1,               # Any case triggers investigation
        "Brucellosis": 5,            # 5 cases per 100k
        "Q_fever": 10,               # 10 cases per 100k
        "West_Nile_virus": 15,       # 15 cases per 100k
        "Lyme_disease": 25,          # 25 cases per 100k
    }
    
    # Time window for clustering (days)
    CLUSTER_TIME_WINDOW = 14  # 2 weeks
    
    # Geographic distance for clustering (km)
    CLUSTER_DISTANCE_KM = 25  # 25 km radius
    
    @classmethod
    def exceeds_threshold(cls, pathogen: str, case_count: int, 
                         population: int = 100000) -> bool:
        """Check if case count exceeds investigation threshold."""
        if pathogen not in cls.INVESTIGATION_THRESHOLDS:
            return case_count >= 5  # Default threshold
        
        threshold = cls.INVESTIGATION_THRESHOLDS[pathogen]
        rate_per_100k = (case_count / population) * 100000
        return rate_per_100k >= threshold

class HumanHealthDataCollector:
    """Main collector for human health surveillance data."""
    
    def __init__(self, storage_path: str = "./human_health_data"):
        self.storage_path = storage_path
        self.records: List[HumanHealthRecord] = []
        self.alert_triggers: List[Dict] = []
        self.clusters: List[Dict] = []
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        logger.info(f"Human Health Data Collector initialized")
        logger.info(f"Storage path: {storage_path}")
    
    def add_record(self, record: HumanHealthRecord) -> bool:
        """Add new human health record with validation and analysis."""
        try:
            # Validate record
            if not self._validate_record(record):
                logger.error(f"Invalid record: {record.case_id}")
                return False
            
            # Add to collection
            self.records.append(record)
            logger.info(f"Added record: {record.case_id} - {record.case_classification.value} "
                       f"case in {record.county}, {record.state}")
            
            # Check for outbreak thresholds
            self._check_outbreak_thresholds(record)
            
            # Check for high-risk exposures
            self._check_high_risk_exposures(record)
            
            # Check for syndromic patterns
            self._analyze_syndromic_patterns(record)
            
            # Check for spatial-temporal clusters
            self._check_clusters(record)
            
            # Auto-save
            self._save_record(record)
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding record {record.case_id}: {e}")
            return False
    
    def _validate_record(self, record: HumanHealthRecord) -> bool:
        """Validate human health record."""
        
        # Required fields
        if not record.case_id or not record.timestamp:
            return False
        
        # Geographic validation
        if not (-90 <= record.location_lat <= 90):
            return False
        if not (-180 <= record.location_lon <= 180):
            return False
        
        # Temporal validation
        if record.onset_date > record.timestamp:
            return False
        
        # Age and sex validation
        if record.sex not in ["M", "F", "U"]:
            return False
        
        return True
    
    def _check_outbreak_thresholds(self, record: HumanHealthRecord):
        """Check if cases exceed outbreak investigation thresholds."""
        
        # Only check confirmed/probable cases
        if record.case_classification not in [CaseClassification.CONFIRMED, 
                                             CaseClassification.PROBABLE]:
            return
        
        # Check each pathogen
        pathogens_to_check = []
        if record.confirmed_pathogen:
            pathogens_to_check.append(record.confirmed_pathogen)
        if record.suspected_pathogen:
            pathogens_to_check.append(record.suspected_pathogen)
        
        for pathogen in pathogens_to_check:
            # Count recent cases in same state
            recent_cases = self._count_recent_cases(
                pathogen, record.state, days=30
            )
            
            # Assume 1M population for calculation (would be actual in real system)
            if OutbreakThresholds.exceeds_threshold(pathogen, recent_cases, 1000000):
                alert = {
                    "alert_type": "OUTBREAK_THRESHOLD",
                    "case_id": record.case_id,
                    "timestamp": datetime.now().isoformat(),
                    "pathogen": pathogen,
                    "location": f"{record.county}, {record.state}",
                    "case_count_30_days": recent_cases,
                    "threshold_exceeded": True,
                    "priority": "HIGH"
                }
                self.alert_triggers.append(alert)
                logger.warning(f"OUTBREAK THRESHOLD EXCEEDED: {alert}")
    
    def _check_high_risk_exposures(self, record: HumanHealthRecord):
        """Check for high-risk occupational or exposure patterns."""
        
        # High-risk occupation
        if record.occupation:
            risk_level = HighRiskOccupations.get_risk_level(record.occupation)
            
            if risk_level in ["HIGHEST", "HIGH"]:
                alert = {
                    "alert_type": "HIGH_RISK_OCCUPATION",
                    "case_id": record.case_id,
                    "timestamp": datetime.now().isoformat(),
                    "occupation": record.occupation,
                    "risk_level": risk_level,
                    "location": f"{record.county}, {record.state}",
                    "priority": "MODERATE"
                }
                self.alert_triggers.append(alert)
                logger.info(f"HIGH-RISK OCCUPATION EXPOSURE: {alert}")
        
        # Direct animal contact with severe illness
        if (ExposureType.DIRECT_ANIMAL_CONTACT in record.exposure_types and
            record.severity in [SymptomSeverity.SEVERE, SymptomSeverity.CRITICAL]):
            
            alert = {
                "alert_type": "HIGH_RISK_ANIMAL_EXPOSURE",
                "case_id": record.case_id,
                "timestamp": datetime.now().isoformat(),
                "exposure_details": record.animal_exposure_details,
                "severity": record.severity.value,
                "location": f"{record.county}, {record.state}",
                "priority": "HIGH"
            }
            self.alert_triggers.append(alert)
            logger.warning(f"HIGH-RISK ANIMAL EXPOSURE: {alert}")
    
    def _analyze_syndromic_patterns(self, record: HumanHealthRecord):
        """Analyze syndromic surveillance patterns."""
        
        syndromes = ZoonoticSyndromes.classify_syndrome(record.symptoms)
        
        # Check for unusual syndrome combinations
        if len(syndromes) >= 3:  # Multiple syndrome involvement
            alert = {
                "alert_type": "MULTI_SYSTEM_SYNDROME",
                "case_id": record.case_id,
                "timestamp": datetime.now().isoformat(),
                "syndromes": syndromes,
                "symptoms": record.symptoms,
                "location": f"{record.county}, {record.state}",
                "priority": "MODERATE"
            }
            self.alert_triggers.append(alert)
            logger.info(f"MULTI-SYSTEM SYNDROME: {alert}")
        
        # Check for hemorrhagic syndrome (high concern)
        if "HEMORRHAGIC" in syndromes:
            alert = {
                "alert_type": "HEMORRHAGIC_SYNDROME",
                "case_id": record.case_id,
                "timestamp": datetime.now().isoformat(),
                "symptoms": record.symptoms,
                "location": f"{record.county}, {record.state}",
                "priority": "HIGH"
            }
            self.alert_triggers.append(alert)
            logger.warning(f"HEMORRHAGIC SYNDROME DETECTED: {alert}")
    
    def _check_clusters(self, record: HumanHealthRecord):
        """Check for spatial-temporal clustering of cases."""
        
        # Only check confirmed/probable cases
        if record.case_classification not in [CaseClassification.CONFIRMED, 
                                             CaseClassification.PROBABLE]:
            return
        
        # Find nearby cases in time window
        cutoff_date = record.timestamp - timedelta(days=OutbreakThresholds.CLUSTER_TIME_WINDOW)
        nearby_cases = []
        
        for existing_record in self.records:
            if (existing_record.case_id == record.case_id or 
                existing_record.timestamp < cutoff_date):
                continue
            
            # Calculate distance (simple approximation)
            distance = self._calculate_distance(
                record.location_lat, record.location_lon,
                existing_record.location_lat, existing_record.location_lon
            )
            
            if distance <= OutbreakThresholds.CLUSTER_DISTANCE_KM:
                nearby_cases.append(existing_record)
        
        # Check for cluster (3+ cases in space-time window)
        if len(nearby_cases) >= 2:  # Plus current case = 3 total
            cluster_id = f"CLUSTER_{record.state}_{record.timestamp.strftime('%Y%m%d')}"
            
            cluster = {
                "cluster_id": cluster_id,
                "timestamp": datetime.now().isoformat(),
                "center_lat": record.location_lat,
                "center_lon": record.location_lon,
                "location": f"{record.county}, {record.state}",
                "case_count": len(nearby_cases) + 1,
                "cases": [record.case_id] + [c.case_id for c in nearby_cases],
                "time_window_days": OutbreakThresholds.CLUSTER_TIME_WINDOW,
                "distance_km": OutbreakThresholds.CLUSTER_DISTANCE_KM
            }
            
            self.clusters.append(cluster)
            
            alert = {
                "alert_type": "SPATIAL_TEMPORAL_CLUSTER",
                "case_id": record.case_id,
                "timestamp": datetime.now().isoformat(),
                "cluster_info": cluster,
                "priority": "HIGH"
            }
            self.alert_triggers.append(alert)
            logger.warning(f"CLUSTER DETECTED: {alert}")
    
    def _calculate_distance(self, lat1: float, lon1: float, 
                          lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers."""
        import math
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = (math.sin(dlat/2)**2 + math.cos(lat1_rad) * 
             math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in km
        return c * 6371
    
    def _count_recent_cases(self, pathogen: str, state: str, days: int = 30) -> int:
        """Count recent cases of specific pathogen in state."""
        cutoff = datetime.now() - timedelta(days=days)
        
        count = 0
        for record in self.records:
            if (record.timestamp >= cutoff and
                record.state == state and
                record.case_classification in [CaseClassification.CONFIRMED, 
                                             CaseClassification.PROBABLE]):
                
                if (record.confirmed_pathogen == pathogen or 
                    record.suspected_pathogen == pathogen):
                    count += 1
        
        return count
    
    def _save_record(self, record: HumanHealthRecord):
        """Save record to persistent storage."""
        try:
            filename = f"{record.case_id}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.storage_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(record.to_dict(), f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving record {record.case_id}: {e}")
    
    def get_records_by_syndrome(self, syndrome: str) -> List[HumanHealthRecord]:
        """Get records matching specific syndrome."""
        matching_records = []
        
        for record in self.records:
            syndromes = ZoonoticSyndromes.classify_syndrome(record.symptoms)
            if syndrome.upper() in syndromes:
                matching_records.append(record)
        
        return matching_records
    
    def get_high_risk_cases(self, days: int = 7) -> List[HumanHealthRecord]:
        """Get high-risk cases from last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        
        high_risk = []
        for record in self.records:
            if record.timestamp >= cutoff:
                # High-risk criteria
                is_high_risk = (
                    record.severity in [SymptomSeverity.SEVERE, SymptomSeverity.CRITICAL] or
                    record.healthcare_level in [HealthcareLevel.ICU, HealthcareLevel.DECEASED] or
                    HighRiskOccupations.get_risk_level(record.occupation or "") in ["HIGHEST", "HIGH"] or
                    ExposureType.DIRECT_ANIMAL_CONTACT in record.exposure_types
                )
                
                if is_high_risk:
                    high_risk.append(record)
        
        return high_risk
    
    def generate_epi_summary(self, days: int = 7) -> Dict:
        """Generate epidemiological summary for last N days."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        recent_records = [r for r in self.records if r.timestamp >= start_time]
        
        # Case classification breakdown
        classifications = {}
        for record in recent_records:
            cls = record.case_classification.value
            classifications[cls] = classifications.get(cls, 0) + 1
        
        # Age group distribution
        age_groups = {}
        for record in recent_records:
            age = record.age_group.value
            age_groups[age] = age_groups.get(age, 0) + 1
        
        # Syndrome patterns
        all_syndromes = []
        for record in recent_records:
            syndromes = ZoonoticSyndromes.classify_syndrome(record.symptoms)
            all_syndromes.extend(syndromes)
        
        syndrome_counts = {}
        for syndrome in all_syndromes:
            syndrome_counts[syndrome] = syndrome_counts.get(syndrome, 0) + 1
        
        # Recent alerts
        recent_alerts = [alert for alert in self.alert_triggers
                        if datetime.fromisoformat(alert['timestamp']) >= start_time]
        
        return {
            "period": f"{days} days",
            "start_date": start_time.isoformat(),
            "end_date": end_time.isoformat(),
            "total_cases": len(recent_records),
            "case_classifications": classifications,
            "age_distribution": age_groups,
            "syndrome_patterns": syndrome_counts,
            "clusters_detected": len([c for c in self.clusters 
                                    if datetime.fromisoformat(c['timestamp']) >= start_time]),
            "total_alerts": len(recent_alerts),
            "high_priority_alerts": len([a for a in recent_alerts 
                                       if a.get('priority') == 'HIGH'])
        }

# Mock data generator
class MockHumanDataGenerator:
    """Generate realistic mock human health data."""
    
    COMMON_SYMPTOMS = [
        "fever", "headache", "fatigue", "cough", "myalgia", 
        "nausea", "diarrhea", "rash", "joint_pain"
    ]
    
    SEVERE_SYMPTOMS = [
        "dyspnea", "chest_pain", "confusion", "seizures", 
        "bleeding", "pneumonia", "encephalitis"
    ]
    
    OCCUPATIONS = [
        "veterinarian", "farm_worker", "healthcare_worker", "teacher",
        "office_worker", "construction_worker", "retail_worker", 
        "retired", "unemployed", "student"
    ]
    
    @classmethod
    def generate_random_case(cls) -> HumanHealthRecord:
        """Generate a random human health case."""
        
        # Random location (US)
        lat = random.uniform(25.0, 48.0)
        lon = random.uniform(-125.0, -65.0)
        
        states = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC"]
        state = random.choice(states)
        county = f"County_{random.randint(1, 5)}"
        
        # Random onset (last 30 days)
        onset = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 23)
        )
        report = onset + timedelta(days=random.randint(0, 7))
        
        # Symptoms based on severity
        severity = random.choice(list(SymptomSeverity))
        if severity in [SymptomSeverity.SEVERE, SymptomSeverity.CRITICAL]:
            symptoms = random.sample(cls.COMMON_SYMPTOMS, random.randint(2, 4))
            symptoms.extend(random.sample(cls.SEVERE_SYMPTOMS, random.randint(1, 2)))
        else:
            symptoms = random.sample(cls.COMMON_SYMPTOMS, random.randint(1, 3))
        
        # Healthcare level based on severity
        if severity == SymptomSeverity.CRITICAL:
            healthcare = random.choice([HealthcareLevel.ICU, HealthcareLevel.HOSPITALIZED])
        elif severity == SymptomSeverity.SEVERE:
            healthcare = random.choice([HealthcareLevel.HOSPITALIZED, HealthcareLevel.EMERGENCY_DEPT])
        else:
            healthcare = random.choice([HealthcareLevel.OUTPATIENT, HealthcareLevel.NONE])
        
        return HumanHealthRecord(
            case_id=f"HUM_{random.randint(100000, 999999)}",
            timestamp=report,
            location_lat=lat,
            location_lon=lon,
            county=county,
            state=state,
            age_group=random.choice(list(AgeGroup)),
            sex=random.choice(["M", "F"]),
            symptoms=symptoms,
            onset_date=onset,
            case_classification=random.choice(list(CaseClassification)),
            severity=severity,
            healthcare_level=healthcare,
            exposure_types=[random.choice(list(ExposureType))],
            animal_exposure_details={"animal_type": "poultry", "contact_type": "direct"} 
                                   if random.random() > 0.7 else None,
            suspected_pathogen=random.choice(["H5N1", "West_Nile_virus", "Brucella_spp", None, None]),
            confirmed_pathogen=None,
            diagnostic_tests=random.sample(["PCR", "Serology", "Culture", "Antigen"], 
                                         random.randint(0, 2)),
            occupation=random.choice(cls.OCCUPATIONS),
            travel_history=None,
            household_size=random.randint(1, 6),
            reporting_facility=f"Hospital_{random.randint(1, 10)}",
            reporter_type=random.choice(["physician", "laboratory", "hospital"])
        )

def run_demonstration():
    """Run demonstration of human health data collection."""
    print("👥 Human Health Data Collector - Demonstration")
    print("=" * 60)
    
    # Initialize collector
    collector = HumanHealthDataCollector()
    
    # Generate sample cases
    print("\n📊 Generating sample human health cases...")
    for i in range(20):
        case = MockHumanDataGenerator.generate_random_case()
        collector.add_record(case)
    
    # Show summary
    print(f"\n📈 Data Collection Summary:")
    print(f"  Total Cases: {len(collector.records)}")
    print(f"  Alert Triggers: {len(collector.alert_triggers)}")
    print(f"  Clusters Detected: {len(collector.clusters)}")
    
    # Show high-risk cases
    high_risk = collector.get_high_risk_cases(7)
    print(f"\n⚠️ High-Risk Cases (7 days): {len(high_risk)}")
    
    for case in high_risk[:3]:  # Show first 3
        print(f"  - {case.case_id}: {case.severity.value} - {case.occupation or 'N/A'} "
              f"in {case.county}, {case.state}")
    
    # Show recent alerts
    recent_alerts = [a for a in collector.alert_triggers 
                    if datetime.fromisoformat(a['timestamp']) >= 
                    datetime.now() - timedelta(hours=24)]
    
    print(f"\n🚨 Recent Alerts (24h): {len(recent_alerts)}")
    for alert in recent_alerts[:3]:
        print(f"  - {alert['alert_type']}: {alert.get('priority', 'N/A')} priority")
    
    # Epidemiological summary
    epi_summary = collector.generate_epi_summary(7)
    print(f"\n📊 7-Day Epidemiological Summary:")
    print(f"  Total Cases: {epi_summary['total_cases']}")
    print(f"  Confirmed: {epi_summary['case_classifications'].get('confirmed', 0)}")
    print(f"  Probable: {epi_summary['case_classifications'].get('probable', 0)}")
    print(f"  Clusters: {epi_summary['clusters_detected']}")
    print(f"  High Priority Alerts: {epi_summary['high_priority_alerts']}")
    
    return collector

if __name__ == "__main__":
    collector = run_demonstration()
"""
Animal Health Data Collector
============================
Module 1: Data and Health Indicators in Public Health Practice

Collects and standardizes animal health surveillance data from multiple sources
following epidemiological principles for zoonotic disease monitoring.

NIW Focus: Practical data integration for early zoonotic disease detection.
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

class AnimalSpecies(Enum):
    """Standardized animal species classification for surveillance."""
    POULTRY_CHICKEN = "poultry_chicken"
    POULTRY_TURKEY = "poultry_turkey" 
    POULTRY_DUCK = "poultry_duck"
    POULTRY_GOOSE = "poultry_goose"
    CATTLE = "cattle"
    SWINE = "swine"
    SHEEP = "sheep"
    GOATS = "goats"
    HORSES = "horses"
    WILD_BIRDS = "wild_birds"
    WILD_MAMMALS = "wild_mammals"
    COMPANION_ANIMALS = "companion_animals"

class HealthStatus(Enum):
    """Animal health status classification."""
    HEALTHY = "healthy"
    SICK = "sick" 
    DEAD = "dead"
    RECOVERED = "recovered"
    UNDER_OBSERVATION = "under_observation"
    QUARANTINED = "quarantined"

class ReportSource(Enum):
    """Data source classification."""
    USDA_APHIS = "usda_aphis"
    STATE_VET = "state_veterinarian"
    PRIVATE_VET = "private_veterinarian"
    FARM_OWNER = "farm_owner"
    WILDLIFE_AGENCY = "wildlife_agency"
    LAB_REPORT = "laboratory"
    UNIVERSITY = "university_extension"

@dataclass
class AnimalHealthRecord:
    """Standardized animal health surveillance record."""
    record_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    county: str
    state: str
    species: AnimalSpecies
    health_status: HealthStatus
    population_size: int
    affected_count: int
    clinical_signs: List[str]
    suspected_pathogen: Optional[str]
    confirmed_pathogen: Optional[str]
    diagnostic_method: Optional[str]
    source: ReportSource
    farm_type: Optional[str]  # "commercial", "backyard", "wild", "zoo"
    premises_id: Optional[str]
    reporter_contact: Optional[str]
    follow_up_needed: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['species'] = self.species.value
        data['health_status'] = self.health_status.value
        data['source'] = self.source.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AnimalHealthRecord':
        """Create from dictionary."""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['species'] = AnimalSpecies(data['species'])
        data['health_status'] = HealthStatus(data['health_status'])
        data['source'] = ReportSource(data['source'])
        return cls(**data)

class SurveillanceThresholds:
    """Epidemiological thresholds for triggering enhanced surveillance."""
    
    # Mortality thresholds by species (% of population)
    MORTALITY_THRESHOLDS = {
        AnimalSpecies.POULTRY_CHICKEN: 0.05,  # 5% mortality
        AnimalSpecies.POULTRY_TURKEY: 0.05,
        AnimalSpecies.POULTRY_DUCK: 0.10,
        AnimalSpecies.CATTLE: 0.02,            # 2% mortality
        AnimalSpecies.SWINE: 0.03,             # 3% mortality
        AnimalSpecies.WILD_BIRDS: 0.15,        # 15% mortality for wild birds
    }
    
    # Morbidity thresholds by species (% of population)
    MORBIDITY_THRESHOLDS = {
        AnimalSpecies.POULTRY_CHICKEN: 0.10,   # 10% morbidity
        AnimalSpecies.POULTRY_TURKEY: 0.10,
        AnimalSpecies.CATTLE: 0.05,            # 5% morbidity
        AnimalSpecies.SWINE: 0.08,             # 8% morbidity
    }
    
    @classmethod
    def exceeds_mortality_threshold(cls, species: AnimalSpecies, 
                                   population: int, deaths: int) -> bool:
        """Check if mortality exceeds surveillance threshold."""
        if species not in cls.MORTALITY_THRESHOLDS:
            return deaths > 0  # Any death in unlisted species triggers alert
        
        threshold = cls.MORTALITY_THRESHOLDS[species]
        mortality_rate = deaths / population if population > 0 else 0
        return mortality_rate >= threshold
    
    @classmethod
    def exceeds_morbidity_threshold(cls, species: AnimalSpecies,
                                   population: int, sick: int) -> bool:
        """Check if morbidity exceeds surveillance threshold."""
        if species not in cls.MORBIDITY_THRESHOLDS:
            return sick >= 5  # 5+ sick animals in unlisted species
        
        threshold = cls.MORBIDITY_THRESHOLDS[species]
        morbidity_rate = sick / population if population > 0 else 0
        return morbidity_rate >= threshold

class HighPriorityPathogens:
    """High priority pathogens for zoonotic disease surveillance."""
    
    TIER_1_CRITICAL = [
        "H5N1",
        "H7N9", 
        "SARS-CoV",
        "MERS-CoV",
        "Nipah_virus",
        "Ebola_virus",
        "Marburg_virus"
    ]
    
    TIER_2_HIGH = [
        "Brucella_spp",
        "Bacillus_anthracis",
        "Yersinia_pestis",
        "Francisella_tularensis",
        "Coxiella_burnetii",
        "West_Nile_virus",
        "Eastern_equine_encephalitis"
    ]
    
    TIER_3_MODERATE = [
        "Salmonella_spp",
        "Campylobacter_spp", 
        "E_coli_O157",
        "Listeria_monocytogenes",
        "Leptospira_spp",
        "Borrelia_burgdorferi",
        "Rickettsia_rickettsii"
    ]
    
    @classmethod
    def get_priority_level(cls, pathogen: str) -> str:
        """Get priority level for pathogen."""
        if pathogen in cls.TIER_1_CRITICAL:
            return "CRITICAL"
        elif pathogen in cls.TIER_2_HIGH:
            return "HIGH"
        elif pathogen in cls.TIER_3_MODERATE:
            return "MODERATE"
        else:
            return "ROUTINE"

class AnimalHealthDataCollector:
    """Main collector for animal health surveillance data."""
    
    def __init__(self, storage_path: str = "./animal_health_data"):
        self.storage_path = storage_path
        self.records: List[AnimalHealthRecord] = []
        self.alert_triggers: List[Dict] = []
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
        
        logger.info(f"Animal Health Data Collector initialized")
        logger.info(f"Storage path: {storage_path}")
    
    def add_record(self, record: AnimalHealthRecord) -> bool:
        """Add new animal health record with validation."""
        try:
            # Validate record
            if not self._validate_record(record):
                logger.error(f"Invalid record: {record.record_id}")
                return False
            
            # Add to collection
            self.records.append(record)
            logger.info(f"Added record: {record.record_id} - {record.species.value} "
                       f"in {record.county}, {record.state}")
            
            # Check for surveillance thresholds
            self._check_surveillance_thresholds(record)
            
            # Check for high priority pathogens
            self._check_priority_pathogens(record)
            
            # Auto-save
            self._save_record(record)
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding record {record.record_id}: {e}")
            return False
    
    def _validate_record(self, record: AnimalHealthRecord) -> bool:
        """Validate animal health record for epidemiological standards."""
        
        # Required fields validation
        if not record.record_id or not record.timestamp:
            return False
        
        # Geographic validation
        if not (-90 <= record.location_lat <= 90):
            return False
        if not (-180 <= record.location_lon <= 180):
            return False
        
        # Population validation
        if record.population_size < 0 or record.affected_count < 0:
            return False
        if record.affected_count > record.population_size:
            return False
        
        # Species validation
        if not isinstance(record.species, AnimalSpecies):
            return False
        
        return True
    
    def _check_surveillance_thresholds(self, record: AnimalHealthRecord):
        """Check if record exceeds surveillance thresholds."""
        
        deaths = record.affected_count if record.health_status == HealthStatus.DEAD else 0
        sick = record.affected_count if record.health_status == HealthStatus.SICK else 0
        
        # Check mortality threshold
        if SurveillanceThresholds.exceeds_mortality_threshold(
            record.species, record.population_size, deaths):
            
            alert = {
                "alert_type": "MORTALITY_THRESHOLD",
                "record_id": record.record_id,
                "timestamp": datetime.now().isoformat(),
                "species": record.species.value,
                "location": f"{record.county}, {record.state}",
                "mortality_rate": (deaths / record.population_size * 100) if record.population_size > 0 else 0,
                "threshold_exceeded": True,
                "priority": "HIGH"
            }
            self.alert_triggers.append(alert)
            logger.warning(f"MORTALITY THRESHOLD EXCEEDED: {alert}")
        
        # Check morbidity threshold
        if SurveillanceThresholds.exceeds_morbidity_threshold(
            record.species, record.population_size, sick):
            
            alert = {
                "alert_type": "MORBIDITY_THRESHOLD", 
                "record_id": record.record_id,
                "timestamp": datetime.now().isoformat(),
                "species": record.species.value,
                "location": f"{record.county}, {record.state}",
                "morbidity_rate": (sick / record.population_size * 100) if record.population_size > 0 else 0,
                "threshold_exceeded": True,
                "priority": "MODERATE"
            }
            self.alert_triggers.append(alert)
            logger.warning(f"MORBIDITY THRESHOLD EXCEEDED: {alert}")
    
    def _check_priority_pathogens(self, record: AnimalHealthRecord):
        """Check for high priority zoonotic pathogens."""
        
        pathogens_to_check = []
        if record.confirmed_pathogen:
            pathogens_to_check.append(record.confirmed_pathogen)
        if record.suspected_pathogen:
            pathogens_to_check.append(record.suspected_pathogen)
        
        for pathogen in pathogens_to_check:
            priority = HighPriorityPathogens.get_priority_level(pathogen)
            
            if priority in ["CRITICAL", "HIGH"]:
                alert = {
                    "alert_type": "HIGH_PRIORITY_PATHOGEN",
                    "record_id": record.record_id,
                    "timestamp": datetime.now().isoformat(),
                    "pathogen": pathogen,
                    "priority_level": priority,
                    "species": record.species.value,
                    "location": f"{record.county}, {record.state}",
                    "status": "confirmed" if record.confirmed_pathogen == pathogen else "suspected"
                }
                self.alert_triggers.append(alert)
                logger.critical(f"HIGH PRIORITY PATHOGEN DETECTED: {alert}")
    
    def _save_record(self, record: AnimalHealthRecord):
        """Save record to persistent storage."""
        try:
            # Save individual record
            filename = f"{record.record_id}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.storage_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(record.to_dict(), f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving record {record.record_id}: {e}")
    
    def get_records_by_timeframe(self, start_time: datetime, 
                                end_time: datetime) -> List[AnimalHealthRecord]:
        """Get records within specified timeframe."""
        return [r for r in self.records if start_time <= r.timestamp <= end_time]
    
    def get_records_by_species(self, species: AnimalSpecies) -> List[AnimalHealthRecord]:
        """Get records for specific animal species."""
        return [r for r in self.records if r.species == species]
    
    def get_records_by_location(self, state: str, 
                               county: Optional[str] = None) -> List[AnimalHealthRecord]:
        """Get records by geographic location."""
        records = [r for r in self.records if r.state.upper() == state.upper()]
        if county:
            records = [r for r in records if r.county.upper() == county.upper()]
        return records
    
    def get_high_priority_alerts(self, hours: int = 24) -> List[Dict]:
        """Get high priority alerts from last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alert_triggers 
                if datetime.fromisoformat(alert['timestamp']) >= cutoff
                and alert.get('priority') in ['CRITICAL', 'HIGH']]
    
    def generate_surveillance_summary(self, days: int = 7) -> Dict:
        """Generate surveillance summary for last N days."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        recent_records = self.get_records_by_timeframe(start_time, end_time)
        
        # Count by species
        species_counts = {}
        for record in recent_records:
            species = record.species.value
            if species not in species_counts:
                species_counts[species] = {"total": 0, "sick": 0, "dead": 0}
            
            species_counts[species]["total"] += 1
            if record.health_status == HealthStatus.SICK:
                species_counts[species]["sick"] += 1
            elif record.health_status == HealthStatus.DEAD:
                species_counts[species]["dead"] += 1
        
        # Count by state
        state_counts = {}
        for record in recent_records:
            state = record.state
            state_counts[state] = state_counts.get(state, 0) + 1
        
        # Recent alerts
        recent_alerts = [alert for alert in self.alert_triggers
                        if datetime.fromisoformat(alert['timestamp']) >= start_time]
        
        return {
            "period": f"{days} days",
            "start_date": start_time.isoformat(),
            "end_date": end_time.isoformat(),
            "total_records": len(recent_records),
            "species_breakdown": species_counts,
            "state_breakdown": state_counts,
            "total_alerts": len(recent_alerts),
            "high_priority_alerts": len([a for a in recent_alerts 
                                       if a.get('priority') in ['CRITICAL', 'HIGH']])
        }
    
    def export_csv(self, filepath: str, days: Optional[int] = None):
        """Export records to CSV format for external analysis."""
        records_to_export = self.records
        
        if days:
            start_time = datetime.now() - timedelta(days=days)
            records_to_export = [r for r in self.records if r.timestamp >= start_time]
        
        try:
            with open(filepath, 'w', newline='') as csvfile:
                fieldnames = [
                    'record_id', 'timestamp', 'location_lat', 'location_lon',
                    'county', 'state', 'species', 'health_status', 'population_size',
                    'affected_count', 'clinical_signs', 'suspected_pathogen',
                    'confirmed_pathogen', 'diagnostic_method', 'source', 'farm_type'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for record in records_to_export:
                    row = record.to_dict()
                    row['clinical_signs'] = '; '.join(row['clinical_signs'])
                    writer.writerow(row)
                    
            logger.info(f"Exported {len(records_to_export)} records to {filepath}")
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")

# Mock data generators for demonstration
class MockDataGenerator:
    """Generate realistic mock data for demonstration purposes."""
    
    US_STATES = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"]
    
    COUNTIES_BY_STATE = {
        "CA": ["Los Angeles", "San Diego", "Orange", "Riverside", "San Bernardino"],
        "TX": ["Harris", "Dallas", "Tarrant", "Travis", "Collin"],
        "FL": ["Miami-Dade", "Broward", "Palm Beach", "Hillsborough", "Orange"],
        "NY": ["Kings", "Queens", "New York", "Suffolk", "Bronx"]
    }
    
    CLINICAL_SIGNS = {
        AnimalSpecies.POULTRY_CHICKEN: [
            "respiratory_distress", "decreased_egg_production", "sudden_death",
            "diarrhea", "lethargy", "swollen_head", "coughing", "sneezing"
        ],
        AnimalSpecies.CATTLE: [
            "fever", "lameness", "decreased_milk_production", "abortion",
            "respiratory_distress", "diarrhea", "neurological_signs"
        ],
        AnimalSpecies.SWINE: [
            "fever", "respiratory_distress", "diarrhea", "skin_lesions",
            "lameness", "decreased_feed_intake", "coughing"
        ]
    }
    
    @classmethod
    def generate_random_record(cls) -> AnimalHealthRecord:
        """Generate a single random animal health record."""
        
        state = random.choice(cls.US_STATES)
        counties = cls.COUNTIES_BY_STATE.get(state, [f"County_{i}" for i in range(1, 6)])
        county = random.choice(counties)
        
        # Random coordinates (roughly within US)
        lat = random.uniform(25.0, 48.0)
        lon = random.uniform(-125.0, -65.0)
        
        species = random.choice(list(AnimalSpecies))
        health_status = random.choice(list(HealthStatus))
        
        # Population size based on species
        if "poultry" in species.value:
            population = random.randint(100, 50000)
        elif species == AnimalSpecies.CATTLE:
            population = random.randint(50, 5000)
        else:
            population = random.randint(10, 1000)
        
        # Affected count
        if health_status == HealthStatus.HEALTHY:
            affected = 0
        else:
            affected = random.randint(1, min(100, population // 10))
        
        # Clinical signs
        signs = cls.CLINICAL_SIGNS.get(species, ["unknown_symptoms"])
        num_signs = min(random.randint(1, 3), len(signs))
        clinical_signs = random.sample(signs, num_signs)
        
        # Random pathogen (sometimes)
        pathogens = ["H5N1", "Brucella_spp", "Salmonella_spp", "West_Nile_virus", None]
        suspected_pathogen = random.choice(pathogens + [None] * 5)  # Mostly None
        
        return AnimalHealthRecord(
            record_id=f"ANI_{random.randint(100000, 999999)}",
            timestamp=datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            ),
            location_lat=lat,
            location_lon=lon,
            county=county,
            state=state,
            species=species,
            health_status=health_status,
            population_size=population,
            affected_count=affected,
            clinical_signs=clinical_signs,
            suspected_pathogen=suspected_pathogen,
            confirmed_pathogen=None,
            diagnostic_method=random.choice(["PCR", "Culture", "Serology", "Clinical", None]),
            source=random.choice(list(ReportSource)),
            farm_type=random.choice(["commercial", "backyard", "wild", "zoo"]),
            premises_id=f"PREM_{random.randint(10000, 99999)}",
            reporter_contact=f"contact_{random.randint(1000, 9999)}@email.com"
        )
    
    @classmethod
    def generate_outbreak_scenario(cls, species: AnimalSpecies, 
                                  state: str, pathogen: str, 
                                  num_records: int = 10) -> List[AnimalHealthRecord]:
        """Generate realistic outbreak scenario for testing."""
        
        records = []
        base_lat = random.uniform(35.0, 40.0)
        base_lon = random.uniform(-120.0, -80.0)
        
        counties = cls.COUNTIES_BY_STATE.get(state, [f"County_{i}" for i in range(1, 4)])
        
        for i in range(num_records):
            # Cluster around base location (within ~50 km)
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)
            
            record = AnimalHealthRecord(
                record_id=f"OUTBREAK_{state}_{i:03d}",
                timestamp=datetime.now() - timedelta(
                    days=random.randint(0, 14),  # Within 2 weeks
                    hours=random.randint(0, 23)
                ),
                location_lat=base_lat + lat_offset,
                location_lon=base_lon + lon_offset,
                county=random.choice(counties),
                state=state,
                species=species,
                health_status=random.choice([HealthStatus.SICK, HealthStatus.DEAD]),
                population_size=random.randint(500, 10000),
                affected_count=random.randint(50, 500),
                clinical_signs=cls.CLINICAL_SIGNS.get(species, ["respiratory_distress"]),
                suspected_pathogen=pathogen,
                confirmed_pathogen=pathogen if random.random() > 0.3 else None,
                diagnostic_method="PCR",
                source=ReportSource.USDA_APHIS,
                farm_type="commercial",
                premises_id=f"PREM_{state}_{i:03d}",
                reporter_contact=f"outbreak_reporter_{i}@usda.gov"
            )
            records.append(record)
        
        return records

def run_demonstration():
    """Run demonstration of animal health data collection."""
    print("🐄 Animal Health Data Collector - Demonstration")
    print("=" * 60)
    
    # Initialize collector
    collector = AnimalHealthDataCollector()
    
    # Generate some random records
    print("\n📊 Generating sample animal health records...")
    for i in range(15):
        record = MockDataGenerator.generate_random_record()
        collector.add_record(record)
    
    # Generate H5N1 outbreak scenario
    print("\n🦠 Simulating H5N1 outbreak in California...")
    outbreak_records = MockDataGenerator.generate_outbreak_scenario(
        AnimalSpecies.POULTRY_CHICKEN, "CA", "H5N1", 8
    )
    
    for record in outbreak_records:
        collector.add_record(record)
    
    # Show summary
    print(f"\n📈 Data Collection Summary:")
    print(f"  Total Records: {len(collector.records)}")
    print(f"  Alert Triggers: {len(collector.alert_triggers)}")
    
    # Show alerts
    alerts = collector.get_high_priority_alerts(24)
    print(f"\n🚨 High Priority Alerts (24h): {len(alerts)}")
    
    for alert in alerts[:3]:  # Show first 3
        print(f"  - {alert['alert_type']}: {alert.get('pathogen', 'N/A')} "
              f"in {alert['location']} (Priority: {alert['priority']})")
    
    # Surveillance summary
    summary = collector.generate_surveillance_summary(7)
    print(f"\n📊 7-Day Surveillance Summary:")
    print(f"  Total Records: {summary['total_records']}")
    print(f"  High Priority Alerts: {summary['high_priority_alerts']}")
    print(f"  States Reporting: {len(summary['state_breakdown'])}")
    
    # Export data
    try:
        csv_path = os.path.join(collector.storage_path, "surveillance_export.csv") 
        collector.export_csv(csv_path, 7)
        print(f"\n💾 Data exported to: {csv_path}")
    except Exception as e:
        print(f"Export error: {e}")
    
    return collector

if __name__ == "__main__":
    collector = run_demonstration()
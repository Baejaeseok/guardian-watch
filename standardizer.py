"""
Data Standardizer
=================
Module 1: Data and Health Indicators in Public Health Practice

Standardizes data formats and structures across animal, human, and environmental
surveillance systems for integrated One Health analysis.

NIW Focus: Seamless data integration enabling cross-domain correlation analysis.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import re
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataSource(Enum):
    """Types of data sources in the One Health system."""
    ANIMAL = "animal"
    HUMAN = "human"
    ENVIRONMENTAL = "environmental"
    LABORATORY = "laboratory"
    EXTERNAL = "external"

class StandardizedDataTypes(Enum):
    """Standardized data type classifications."""
    CASE_REPORT = "case_report"
    SURVEILLANCE_RECORD = "surveillance_record"
    LABORATORY_RESULT = "laboratory_result"
    ENVIRONMENTAL_MEASUREMENT = "environmental_measurement"
    OUTBREAK_ALERT = "outbreak_alert"
    RISK_ASSESSMENT = "risk_assessment"

class GeographicLevel(Enum):
    """Geographic resolution levels."""
    COORDINATE = "coordinate"      # Exact lat/lon
    ADDRESS = "address"           # Street address
    ZIP_CODE = "zip_code"         # Postal code
    COUNTY = "county"             # County level
    STATE = "state"               # State/province
    NATIONAL = "national"         # Country level

class TemporalResolution(Enum):
    """Temporal data resolution."""
    REAL_TIME = "real_time"       # < 1 hour
    HOURLY = "hourly"             # Hour precision
    DAILY = "daily"               # Day precision
    WEEKLY = "weekly"             # Week precision
    MONTHLY = "monthly"           # Month precision

@dataclass
class StandardizedRecord:
    """Universal standardized record format for One Health integration."""
    
    # Core identification
    record_id: str                    # Unique identifier
    source: DataSource                # Origin system
    data_type: StandardizedDataTypes  # Type classification
    timestamp: datetime               # When recorded
    
    # Geographic standardization
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    geographic_level: Optional[GeographicLevel] = None
    county_code: Optional[str] = None  # FIPS code
    state_code: Optional[str] = None   # ISO state code
    country_code: str = "US"           # ISO country code
    
    # Temporal standardization
    event_date: Optional[datetime] = None  # When event occurred
    temporal_resolution: Optional[TemporalResolution] = None
    
    # Subject standardization
    subject_type: Optional[str] = None     # "human", "animal", "environment"
    subject_id: Optional[str] = None       # Individual/location identifier
    
    # Content standardization
    primary_parameter: Optional[str] = None    # Main measurement/observation
    parameter_value: Optional[Union[float, str]] = None
    parameter_unit: Optional[str] = None
    
    # Pathogen standardization
    pathogen_name: Optional[str] = None        # Standardized pathogen name
    pathogen_code: Optional[str] = None        # Standard code (SNOMED, ICD)
    
    # Quality metadata
    data_quality: str = "unknown"             # "high", "medium", "low", "unknown"
    validation_status: str = "unvalidated"    # "validated", "pending", "failed"
    completeness_score: float = 0.0           # 0.0 to 1.0
    
    # Integration metadata
    source_system: str = "unknown"            # Original system name
    processing_timestamp: datetime = None     # When standardized
    cross_references: List[str] = None        # Related record IDs
    
    # Original data preservation
    original_data: Dict[str, Any] = None      # Source data backup
    transformation_log: List[str] = None      # Processing steps
    
    def __post_init__(self):
        """Initialize default values."""
        if self.processing_timestamp is None:
            self.processing_timestamp = datetime.now()
        if self.cross_references is None:
            self.cross_references = []
        if self.original_data is None:
            self.original_data = {}
        if self.transformation_log is None:
            self.transformation_log = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        
        # Convert datetime fields
        if self.timestamp:
            data['timestamp'] = self.timestamp.isoformat()
        if self.event_date:
            data['event_date'] = self.event_date.isoformat()
        if self.processing_timestamp:
            data['processing_timestamp'] = self.processing_timestamp.isoformat()
        
        # Convert enum fields
        data['source'] = self.source.value
        data['data_type'] = self.data_type.value
        if self.geographic_level:
            data['geographic_level'] = self.geographic_level.value
        if self.temporal_resolution:
            data['temporal_resolution'] = self.temporal_resolution.value
        
        return data

class PathogenStandardizer:
    """Standardizes pathogen names and codes across systems."""
    
    # Standard pathogen mappings
    PATHOGEN_MAPPINGS = {
        # Influenza variants
        "h5n1": "Influenza A virus (H5N1)",
        "h1n1": "Influenza A virus (H1N1)",
        "h7n9": "Influenza A virus (H7N9)",
        "avian_influenza": "Influenza A virus (H5N1)",
        "bird_flu": "Influenza A virus (H5N1)",
        
        # Bacterial pathogens
        "brucella": "Brucella species",
        "brucella_spp": "Brucella species",
        "brucellosis": "Brucella species",
        "salmonella": "Salmonella species",
        "e_coli": "Escherichia coli",
        "campylobacter": "Campylobacter jejuni",
        
        # Vector-borne
        "west_nile": "West Nile virus",
        "west_nile_virus": "West Nile virus",
        "wnv": "West Nile virus",
        "lyme": "Borrelia burgdorferi",
        "lyme_disease": "Borrelia burgdorferi",
        "rocky_mountain_spotted_fever": "Rickettsia rickettsii",
        "rmfs": "Rickettsia rickettsii",
        
        # Zoonotic viruses
        "rabies": "Rabies virus",
        "rabv": "Rabies virus",
        "hantavirus": "Hantavirus",
        "ebola": "Ebola virus",
        "marburg": "Marburg virus",
        
        # Parasitic
        "malaria": "Plasmodium species",
        "giardia": "Giardia lamblia",
        "toxoplasma": "Toxoplasma gondii",
    }
    
    # SNOMED CT codes (simplified)
    SNOMED_CODES = {
        "Influenza A virus (H5N1)": "442438000",
        "Brucella species": "36855009",
        "West Nile virus": "398102009",
        "Borrelia burgdorferi": "36415000",
        "Rabies virus": "59881000",
        "Salmonella species": "27268008",
    }
    
    @classmethod
    def standardize_pathogen_name(cls, pathogen_input: str) -> Optional[str]:
        """Convert various pathogen name formats to standard name."""
        if not pathogen_input:
            return None
        
        # Normalize input
        normalized = pathogen_input.lower().strip().replace(" ", "_")
        normalized = re.sub(r'[^a-zA-Z0-9_]', '', normalized)
        
        # Direct mapping
        if normalized in cls.PATHOGEN_MAPPINGS:
            return cls.PATHOGEN_MAPPINGS[normalized]
        
        # Partial matching
        for key, standard_name in cls.PATHOGEN_MAPPINGS.items():
            if key in normalized or normalized in key:
                return standard_name
        
        # If no match found, return cleaned original
        return pathogen_input.strip()
    
    @classmethod
    def get_pathogen_code(cls, standard_name: str) -> Optional[str]:
        """Get SNOMED CT code for standardized pathogen name."""
        return cls.SNOMED_CODES.get(standard_name)

class GeographicStandardizer:
    """Standardizes geographic information across systems."""
    
    # US State mappings
    STATE_MAPPINGS = {
        "california": "CA", "ca": "CA", "calif": "CA",
        "texas": "TX", "tx": "TX", "tex": "TX",
        "florida": "FL", "fl": "FL", "fla": "FL",
        "new_york": "NY", "ny": "NY", "newyork": "NY",
        "illinois": "IL", "il": "IL", "ill": "IL",
        "pennsylvania": "PA", "pa": "PA", "penn": "PA",
    }
    
    # Sample county FIPS codes
    COUNTY_FIPS = {
        ("CA", "los_angeles"): "06037",
        ("TX", "harris"): "48201", 
        ("FL", "miami_dade"): "12086",
        ("NY", "new_york"): "36061",
        ("IL", "cook"): "17031",
    }
    
    @classmethod
    def standardize_state(cls, state_input: str) -> Optional[str]:
        """Convert state name/abbreviation to standard 2-letter code."""
        if not state_input:
            return None
        
        normalized = state_input.lower().strip().replace(" ", "_")
        
        # Check if already valid 2-letter code
        if len(state_input) == 2 and state_input.upper() in ["CA", "TX", "FL", "NY", "IL", "PA"]:
            return state_input.upper()
        
        return cls.STATE_MAPPINGS.get(normalized)
    
    @classmethod
    def get_county_fips(cls, state_code: str, county_name: str) -> Optional[str]:
        """Get FIPS code for county."""
        if not state_code or not county_name:
            return None
        
        normalized_county = county_name.lower().replace(" ", "_").replace("county", "").strip("_")
        return cls.COUNTY_FIPS.get((state_code, normalized_county))
    
    @classmethod
    def validate_coordinates(cls, lat: float, lon: float) -> bool:
        """Validate lat/lon coordinates."""
        if lat is None or lon is None:
            return False
        
        return (-90 <= lat <= 90) and (-180 <= lon <= 180)
    
    @classmethod
    def determine_geographic_level(cls, lat: Optional[float], lon: Optional[float], 
                                  county: Optional[str], state: Optional[str]) -> GeographicLevel:
        """Determine the most precise geographic level available."""
        if lat is not None and lon is not None and cls.validate_coordinates(lat, lon):
            return GeographicLevel.COORDINATE
        elif county and state:
            return GeographicLevel.COUNTY
        elif state:
            return GeographicLevel.STATE
        else:
            return GeographicLevel.NATIONAL

class TemporalStandardizer:
    """Standardizes temporal data across systems."""
    
    @classmethod
    def parse_datetime(cls, date_input: Union[str, datetime]) -> Optional[datetime]:
        """Parse various date formats to standard datetime."""
        if isinstance(date_input, datetime):
            return date_input
        
        if not date_input or not isinstance(date_input, str):
            return None
        
        # Common date format patterns
        patterns = [
            "%Y-%m-%d %H:%M:%S",      # 2024-01-15 14:30:00
            "%Y-%m-%dT%H:%M:%S",      # 2024-01-15T14:30:00
            "%Y-%m-%d",               # 2024-01-15
            "%m/%d/%Y",               # 01/15/2024
            "%d/%m/%Y",               # 15/01/2024
            "%Y%m%d",                 # 20240115
        ]
        
        for pattern in patterns:
            try:
                return datetime.strptime(date_input.strip(), pattern)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_input}")
        return None
    
    @classmethod
    def determine_temporal_resolution(cls, timestamp: datetime, 
                                    event_date: Optional[datetime]) -> TemporalResolution:
        """Determine temporal resolution based on available data."""
        if not timestamp:
            return TemporalResolution.MONTHLY
        
        # If we have both timestamp and event date
        if event_date:
            diff = abs((timestamp - event_date).total_seconds())
            if diff < 3600:  # Less than 1 hour
                return TemporalResolution.REAL_TIME
            elif diff < 86400:  # Less than 24 hours
                return TemporalResolution.HOURLY
            else:
                return TemporalResolution.DAILY
        
        # Check if timestamp has time component
        if timestamp.time() != datetime.min.time():
            return TemporalResolution.HOURLY
        else:
            return TemporalResolution.DAILY

class DataQualityAssessor:
    """Assesses and scores data quality."""
    
    @classmethod
    def calculate_completeness(cls, record_data: Dict) -> float:
        """Calculate completeness score (0.0 to 1.0)."""
        total_fields = 0
        populated_fields = 0
        
        for key, value in record_data.items():
            if key.startswith('_'):  # Skip private fields
                continue
            
            total_fields += 1
            
            if value is not None and value != "" and value != []:
                populated_fields += 1
        
        return populated_fields / total_fields if total_fields > 0 else 0.0
    
    @classmethod
    def assess_quality(cls, record: StandardizedRecord) -> str:
        """Assess overall data quality level."""
        score = 0
        
        # Geographic quality
        if record.location_lat and record.location_lon:
            if GeographicStandardizer.validate_coordinates(record.location_lat, record.location_lon):
                score += 25
        elif record.county_code and record.state_code:
            score += 15
        elif record.state_code:
            score += 10
        
        # Temporal quality
        if record.timestamp and record.event_date:
            score += 25
        elif record.timestamp:
            score += 15
        
        # Content quality
        if record.primary_parameter and record.parameter_value:
            score += 25
        elif record.primary_parameter:
            score += 15
        
        # Pathogen quality
        if record.pathogen_name and record.pathogen_code:
            score += 25
        elif record.pathogen_name:
            score += 15
        
        # Determine quality level
        if score >= 75:
            return "high"
        elif score >= 50:
            return "medium"
        elif score >= 25:
            return "low"
        else:
            return "poor"

class OneHealthDataStandardizer:
    """Main standardization engine for One Health integration."""
    
    def __init__(self):
        self.standardized_records: List[StandardizedRecord] = []
        self.processing_stats: Dict[str, int] = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "warnings": 0
        }
        
        logger.info("One Health Data Standardizer initialized")
    
    def standardize_animal_data(self, animal_record: Dict) -> StandardizedRecord:
        """Standardize animal health surveillance data."""
        try:
            # Create base record
            record = StandardizedRecord(
                record_id=self._generate_standard_id("ANIMAL", animal_record),
                source=DataSource.ANIMAL,
                data_type=StandardizedDataTypes.SURVEILLANCE_RECORD,
                timestamp=TemporalStandardizer.parse_datetime(animal_record.get('timestamp')),
                source_system="animal_health_collector",
                original_data=animal_record.copy()
            )
            
            # Geographic standardization
            record.location_lat = animal_record.get('location_lat')
            record.location_lon = animal_record.get('location_lon')
            record.state_code = GeographicStandardizer.standardize_state(
                animal_record.get('state')
            )
            record.county_code = GeographicStandardizer.get_county_fips(
                record.state_code, animal_record.get('county')
            )
            record.geographic_level = GeographicStandardizer.determine_geographic_level(
                record.location_lat, record.location_lon, 
                animal_record.get('county'), animal_record.get('state')
            )
            
            # Subject standardization
            record.subject_type = "animal"
            record.subject_id = animal_record.get('animal_id')
            
            # Content standardization
            if animal_record.get('mortality_count'):
                record.primary_parameter = "mortality_count"
                record.parameter_value = animal_record.get('mortality_count')
                record.parameter_unit = "count"
            elif animal_record.get('morbidity_count'):
                record.primary_parameter = "morbidity_count" 
                record.parameter_value = animal_record.get('morbidity_count')
                record.parameter_unit = "count"
            
            # Pathogen standardization
            if animal_record.get('pathogen_detected'):
                record.pathogen_name = PathogenStandardizer.standardize_pathogen_name(
                    animal_record.get('pathogen_detected')
                )
                record.pathogen_code = PathogenStandardizer.get_pathogen_code(
                    record.pathogen_name
                )
            
            # Temporal standardization
            record.event_date = TemporalStandardizer.parse_datetime(
                animal_record.get('observation_date', animal_record.get('timestamp'))
            )
            record.temporal_resolution = TemporalStandardizer.determine_temporal_resolution(
                record.timestamp, record.event_date
            )
            
            # Quality assessment
            record.completeness_score = DataQualityAssessor.calculate_completeness(
                animal_record
            )
            record.data_quality = DataQualityAssessor.assess_quality(record)
            record.validation_status = "validated"
            
            # Processing log
            record.transformation_log.append("Animal data standardized")
            
            return record
            
        except Exception as e:
            logger.error(f"Error standardizing animal data: {e}")
            raise
    
    def standardize_human_data(self, human_record: Dict) -> StandardizedRecord:
        """Standardize human health surveillance data."""
        try:
            # Create base record
            record = StandardizedRecord(
                record_id=self._generate_standard_id("HUMAN", human_record),
                source=DataSource.HUMAN,
                data_type=StandardizedDataTypes.CASE_REPORT,
                timestamp=TemporalStandardizer.parse_datetime(human_record.get('timestamp')),
                source_system="human_health_collector",
                original_data=human_record.copy()
            )
            
            # Geographic standardization
            record.location_lat = human_record.get('location_lat')
            record.location_lon = human_record.get('location_lon')
            record.state_code = GeographicStandardizer.standardize_state(
                human_record.get('state')
            )
            record.county_code = GeographicStandardizer.get_county_fips(
                record.state_code, human_record.get('county')
            )
            record.geographic_level = GeographicStandardizer.determine_geographic_level(
                record.location_lat, record.location_lon,
                human_record.get('county'), human_record.get('state')
            )
            
            # Subject standardization
            record.subject_type = "human"
            record.subject_id = human_record.get('case_id')
            
            # Content standardization
            if human_record.get('case_classification'):
                record.primary_parameter = "case_classification"
                record.parameter_value = human_record.get('case_classification')
            
            # Pathogen standardization
            pathogen_source = (human_record.get('confirmed_pathogen') or 
                             human_record.get('suspected_pathogen'))
            if pathogen_source:
                record.pathogen_name = PathogenStandardizer.standardize_pathogen_name(
                    pathogen_source
                )
                record.pathogen_code = PathogenStandardizer.get_pathogen_code(
                    record.pathogen_name
                )
            
            # Temporal standardization
            record.event_date = TemporalStandardizer.parse_datetime(
                human_record.get('onset_date', human_record.get('timestamp'))
            )
            record.temporal_resolution = TemporalStandardizer.determine_temporal_resolution(
                record.timestamp, record.event_date
            )
            
            # Quality assessment
            record.completeness_score = DataQualityAssessor.calculate_completeness(
                human_record
            )
            record.data_quality = DataQualityAssessor.assess_quality(record)
            record.validation_status = "validated"
            
            # Processing log
            record.transformation_log.append("Human data standardized")
            
            return record
            
        except Exception as e:
            logger.error(f"Error standardizing human data: {e}")
            raise
    
    def standardize_environmental_data(self, env_record: Dict) -> StandardizedRecord:
        """Standardize environmental surveillance data."""
        try:
            # Create base record
            record = StandardizedRecord(
                record_id=self._generate_standard_id("ENV", env_record),
                source=DataSource.ENVIRONMENTAL,
                data_type=StandardizedDataTypes.ENVIRONMENTAL_MEASUREMENT,
                timestamp=TemporalStandardizer.parse_datetime(env_record.get('timestamp')),
                source_system="environmental_data_collector",
                original_data=env_record.copy()
            )
            
            # Geographic standardization
            record.location_lat = env_record.get('location_lat')
            record.location_lon = env_record.get('location_lon')
            record.state_code = GeographicStandardizer.standardize_state(
                env_record.get('state')
            )
            record.county_code = GeographicStandardizer.get_county_fips(
                record.state_code, env_record.get('county')
            )
            record.geographic_level = GeographicStandardizer.determine_geographic_level(
                record.location_lat, record.location_lon,
                env_record.get('county'), env_record.get('state')
            )
            
            # Subject standardization
            record.subject_type = "environment"
            record.subject_id = env_record.get('station_id', env_record.get('survey_id'))
            
            # Content standardization
            record.primary_parameter = env_record.get('parameter')
            record.parameter_value = env_record.get('value')
            record.parameter_unit = env_record.get('unit')
            
            # For vector surveys, check for pathogen
            if env_record.get('pathogen_detected'):
                record.pathogen_name = PathogenStandardizer.standardize_pathogen_name(
                    env_record.get('pathogen_detected')
                )
                record.pathogen_code = PathogenStandardizer.get_pathogen_code(
                    record.pathogen_name
                )
            
            # Temporal standardization
            record.event_date = record.timestamp  # Same for environmental
            record.temporal_resolution = TemporalStandardizer.determine_temporal_resolution(
                record.timestamp, record.event_date
            )
            
            # Quality assessment
            record.completeness_score = DataQualityAssessor.calculate_completeness(
                env_record
            )
            record.data_quality = DataQualityAssessor.assess_quality(record)
            record.validation_status = "validated"
            
            # Processing log
            record.transformation_log.append("Environmental data standardized")
            
            return record
            
        except Exception as e:
            logger.error(f"Error standardizing environmental data: {e}")
            raise
    
    def batch_standardize(self, data_records: List[Dict], 
                         source_type: str) -> List[StandardizedRecord]:
        """Standardize multiple records from specified source."""
        standardized = []
        
        for record in data_records:
            try:
                if source_type.lower() == "animal":
                    std_record = self.standardize_animal_data(record)
                elif source_type.lower() == "human":
                    std_record = self.standardize_human_data(record)
                elif source_type.lower() == "environmental":
                    std_record = self.standardize_environmental_data(record)
                else:
                    logger.warning(f"Unknown source type: {source_type}")
                    self.processing_stats["warnings"] += 1
                    continue
                
                standardized.append(std_record)
                self.standardized_records.append(std_record)
                
                self.processing_stats["processed"] += 1
                self.processing_stats["successful"] += 1
                
                logger.info(f"Standardized {source_type} record: {std_record.record_id}")
                
            except Exception as e:
                logger.error(f"Failed to standardize {source_type} record: {e}")
                self.processing_stats["processed"] += 1
                self.processing_stats["failed"] += 1
        
        return standardized
    
    def _generate_standard_id(self, prefix: str, record_data: Dict) -> str:
        """Generate standardized unique identifier."""
        # Create hash from key record elements
        hash_input = (
            str(record_data.get('timestamp', '')) +
            str(record_data.get('location_lat', '')) +
            str(record_data.get('location_lon', '')) +
            str(record_data.get('county', '')) +
            str(record_data.get('state', ''))
        )
        
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        timestamp_str = datetime.now().strftime("%Y%m%d")
        
        return f"STD_{prefix}_{timestamp_str}_{hash_value}"
    
    def get_quality_summary(self) -> Dict:
        """Get data quality summary across all standardized records."""
        if not self.standardized_records:
            return {"message": "No records to analyze"}
        
        quality_counts = {"high": 0, "medium": 0, "low": 0, "poor": 0}
        completeness_scores = []
        source_counts = {}
        
        for record in self.standardized_records:
            quality_counts[record.data_quality] += 1
            completeness_scores.append(record.completeness_score)
            
            source = record.source.value
            source_counts[source] = source_counts.get(source, 0) + 1
        
        avg_completeness = sum(completeness_scores) / len(completeness_scores)
        
        return {
            "total_records": len(self.standardized_records),
            "quality_distribution": quality_counts,
            "average_completeness": round(avg_completeness, 3),
            "source_distribution": source_counts,
            "processing_stats": self.processing_stats
        }
    
    def export_standardized_data(self, filepath: str, format: str = "json") -> bool:
        """Export standardized data to file."""
        try:
            if format.lower() == "json":
                with open(filepath, 'w') as f:
                    data = [record.to_dict() for record in self.standardized_records]
                    json.dump(data, f, indent=2)
            
            elif format.lower() == "csv":
                if not self.standardized_records:
                    return False
                
                with open(filepath, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.standardized_records[0].to_dict().keys())
                    writer.writeheader()
                    
                    for record in self.standardized_records:
                        writer.writerow(record.to_dict())
            
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
            
            logger.info(f"Exported {len(self.standardized_records)} records to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False

# Mock data for testing
def generate_mock_integration_data():
    """Generate mock data from different sources for integration testing."""
    
    # Mock animal data
    animal_data = [
        {
            "animal_id": "FARM_001_COW_123",
            "timestamp": "2024-04-14T08:30:00",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "county": "New York County",
            "state": "NY",
            "species": "cattle",
            "mortality_count": 3,
            "morbidity_count": 7,
            "pathogen_detected": "h5n1",
            "observation_date": "2024-04-14T06:00:00"
        },
        {
            "animal_id": "FARM_002_PIG_456",
            "timestamp": "2024-04-14T09:15:00",
            "location_lat": 34.0522,
            "location_lon": -118.2437,
            "county": "Los Angeles",
            "state": "California",
            "species": "swine",
            "mortality_count": 1,
            "morbidity_count": 4,
            "pathogen_detected": "brucella_spp"
        }
    ]
    
    # Mock human data
    human_data = [
        {
            "case_id": "HUM_789012",
            "timestamp": "2024-04-14T10:00:00",
            "location_lat": 40.7580,
            "location_lon": -73.9855,
            "county": "New York",
            "state": "NY",
            "case_classification": "confirmed",
            "suspected_pathogen": "influenza_h5n1",
            "onset_date": "2024-04-12T00:00:00"
        },
        {
            "case_id": "HUM_345678",
            "timestamp": "2024-04-14T11:30:00",
            "location_lat": 34.1083,
            "location_lon": -118.2437,
            "county": "Los Angeles",
            "state": "CA",
            "case_classification": "probable",
            "confirmed_pathogen": "west_nile_virus"
        }
    ]
    
    # Mock environmental data
    environmental_data = [
        {
            "record_id": "ENV_123456",
            "timestamp": "2024-04-14T07:00:00",
            "location_lat": 40.7489,
            "location_lon": -73.9680,
            "county": "New York",
            "state": "NY",
            "parameter": "temperature",
            "value": 24.5,
            "unit": "celsius",
            "station_id": "WS_NYC_001"
        },
        {
            "survey_id": "VEC_987654",
            "timestamp": "2024-04-14T19:00:00", 
            "location_lat": 34.0522,
            "location_lon": -118.2437,
            "county": "Los Angeles",
            "state": "CA",
            "parameter": "vector_count",
            "value": 45,
            "unit": "count",
            "pathogen_detected": "wnv"
        }
    ]
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of data standardization."""
    print("🔧 One Health Data Standardizer - Demonstration")
    print("=" * 60)
    
    # Initialize standardizer
    standardizer = OneHealthDataStandardizer()
    
    # Generate mock data
    animal_data, human_data, env_data = generate_mock_integration_data()
    
    # Standardize each data source
    print("\n📊 Standardizing Animal Health Data...")
    animal_standardized = standardizer.batch_standardize(animal_data, "animal")
    print(f"  Processed: {len(animal_standardized)} animal records")
    
    print("\n👥 Standardizing Human Health Data...")
    human_standardized = standardizer.batch_standardize(human_data, "human") 
    print(f"  Processed: {len(human_standardized)} human records")
    
    print("\n🌍 Standardizing Environmental Data...")
    env_standardized = standardizer.batch_standardize(env_data, "environmental")
    print(f"  Processed: {len(env_standardized)} environmental records")
    
    # Show sample standardized records
    print(f"\n📋 Sample Standardized Records:")
    for i, record in enumerate(standardizer.standardized_records[:3]):
        print(f"  {i+1}. {record.record_id} ({record.source.value})")
        print(f"     Location: {record.state_code}, Level: {record.geographic_level.value if record.geographic_level else 'N/A'}")
        print(f"     Quality: {record.data_quality}, Completeness: {record.completeness_score:.2f}")
        if record.pathogen_name:
            print(f"     Pathogen: {record.pathogen_name}")
    
    # Quality summary
    quality_summary = standardizer.get_quality_summary()
    print(f"\n📈 Data Quality Summary:")
    print(f"  Total Standardized: {quality_summary['total_records']}")
    print(f"  Average Completeness: {quality_summary['average_completeness']}")
    print(f"  Quality Distribution: {quality_summary['quality_distribution']}")
    print(f"  Processing Stats: {quality_summary['processing_stats']}")
    
    # Cross-reference analysis
    print(f"\n🔗 Cross-Reference Opportunities:")
    ny_records = [r for r in standardizer.standardized_records if r.state_code == "NY"]
    ca_records = [r for r in standardizer.standardized_records if r.state_code == "CA"]
    
    print(f"  New York records: {len(ny_records)} (potential correlation)")
    print(f"  California records: {len(ca_records)} (potential correlation)")
    
    # Pathogen standardization examples
    print(f"\n🦠 Pathogen Standardization Examples:")
    for record in standardizer.standardized_records:
        if record.pathogen_name:
            orig_pathogen = record.original_data.get('pathogen_detected') or \
                           record.original_data.get('suspected_pathogen') or \
                           record.original_data.get('confirmed_pathogen')
            print(f"  '{orig_pathogen}' → '{record.pathogen_name}'")
    
    return standardizer

if __name__ == "__main__":
    standardizer = run_demonstration()
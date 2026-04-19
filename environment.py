"""
Environmental Data Collector
============================
Module 1: Data and Health Indicators in Public Health Practice

Collects environmental and ecological data relevant to zoonotic disease transmission
including climate factors, vector populations, and ecosystem changes.

NIW Focus: Environmental intelligence for predictive zoonotic disease surveillance.
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
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnvironmentalDataType(Enum):
    """Types of environmental data for zoonotic surveillance."""
    CLIMATE = "climate"
    VECTOR = "vector"
    WATER_QUALITY = "water_quality"
    WILDLIFE_MIGRATION = "wildlife_migration"
    LAND_USE = "land_use"
    VEGETATION = "vegetation"
    ATMOSPHERIC = "atmospheric"

class ClimateParameter(Enum):
    """Climate parameters affecting disease transmission."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRECIPITATION = "precipitation"
    WIND_SPEED = "wind_speed"
    WIND_DIRECTION = "wind_direction"
    BAROMETRIC_PRESSURE = "barometric_pressure"
    UV_INDEX = "uv_index"

class VectorSpecies(Enum):
    """Vector species for disease transmission."""
    AEDES_AEGYPTI = "aedes_aegypti"       # Yellow fever mosquito
    AEDES_ALBOPICTUS = "aedes_albopictus" # Asian tiger mosquito
    ANOPHELES = "anopheles"               # Malaria mosquito
    CULEX = "culex"                       # West Nile virus vector
    IXODES_TICK = "ixodes_tick"          # Lyme disease tick
    DERMACENTOR_TICK = "dermacentor_tick" # Rocky Mountain spotted fever
    FLEAS = "fleas"                       # Plague vector
    MITES = "mites"                       # Various diseases

class WaterQualityParameter(Enum):
    """Water quality parameters affecting zoonotic diseases."""
    PH_LEVEL = "ph_level"
    DISSOLVED_OXYGEN = "dissolved_oxygen"
    TURBIDITY = "turbidity"
    COLIFORM_COUNT = "coliform_count"
    TEMPERATURE = "water_temperature"
    NITRATES = "nitrates"
    PHOSPHATES = "phosphates"

@dataclass
class EnvironmentalRecord:
    """Standardized environmental monitoring record."""
    record_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    county: str
    state: str
    data_type: EnvironmentalDataType
    parameter: str  # Specific parameter being measured
    value: float
    unit: str
    source: str  # "weather_station", "satellite", "field_survey", "laboratory"
    quality_flag: str  # "good", "questionable", "poor", "estimated"
    collection_method: str
    station_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['data_type'] = self.data_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EnvironmentalRecord':
        """Create from dictionary."""
        data = data.copy()
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['data_type'] = EnvironmentalDataType(data['data_type'])
        return cls(**data)

@dataclass
class VectorSurveyRecord:
    """Vector population surveillance record."""
    survey_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    county: str
    state: str
    vector_species: VectorSpecies
    collection_method: str  # "light_trap", "gravid_trap", "larvae_survey"
    trap_nights: int
    total_collected: int
    female_count: int
    male_count: int
    infection_rate: Optional[float]  # % infected with pathogens
    pathogen_detected: Optional[str]
    environmental_conditions: Dict  # Temperature, humidity during collection
    surveyor: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['vector_species'] = self.vector_species.value
        return data

class EnvironmentalThresholds:
    """Environmental thresholds for zoonotic disease risk."""
    
    # Temperature ranges optimal for vector breeding (Celsius)
    VECTOR_BREEDING_TEMPS = {
        VectorSpecies.AEDES_AEGYPTI: (20, 35),
        VectorSpecies.AEDES_ALBOPICTUS: (15, 30),
        VectorSpecies.CULEX: (14, 32),
        VectorSpecies.IXODES_TICK: (0, 25),
    }
    
    # Humidity thresholds for vector activity (%)
    VECTOR_HUMIDITY_THRESHOLDS = {
        VectorSpecies.AEDES_AEGYPTI: 60,
        VectorSpecies.AEDES_ALBOPICTUS: 50,
        VectorSpecies.CULEX: 40,
    }
    
    # Precipitation thresholds for breeding site creation (mm/week)
    BREEDING_PRECIPITATION = 10.0  # 10mm per week minimum
    
    @classmethod
    def is_favorable_for_vectors(cls, temperature: float, humidity: float, 
                                precipitation: float, species: VectorSpecies) -> bool:
        """Check if conditions favor vector breeding."""
        
        # Temperature check
        if species in cls.VECTOR_BREEDING_TEMPS:
            temp_min, temp_max = cls.VECTOR_BREEDING_TEMPS[species]
            if not (temp_min <= temperature <= temp_max):
                return False
        
        # Humidity check
        if species in cls.VECTOR_HUMIDITY_THRESHOLDS:
            if humidity < cls.VECTOR_HUMIDITY_THRESHOLDS[species]:
                return False
        
        # Precipitation check (for breeding sites)
        if precipitation < cls.BREEDING_PRECIPITATION:
            return False
        
        return True

class ClimateRiskCalculator:
    """Calculate climate-based disease transmission risk."""
    
    @staticmethod
    def calculate_heat_index(temperature: float, humidity: float) -> float:
        """Calculate heat index from temperature (Celsius) and humidity (%)."""
        # Convert to Fahrenheit for heat index calculation
        temp_f = (temperature * 9/5) + 32
        
        if temp_f < 80:
            return temp_f
        
        # Heat index formula
        hi = (0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094)))
        
        if hi > 79:
            # More complex calculation for higher temperatures
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = [
                -42.379, 2.04901523, 10.14333127, -0.22475541, -0.00683783,
                -0.05481717, 0.00122874, 0.00085282, -0.00000199
            ]
            
            hi = (c1 + (c2 * temp_f) + (c3 * humidity) + (c4 * temp_f * humidity) + 
                  (c5 * temp_f * temp_f) + (c6 * humidity * humidity) + 
                  (c7 * temp_f * temp_f * humidity) + (c8 * temp_f * humidity * humidity) + 
                  (c9 * temp_f * temp_f * humidity * humidity))
        
        # Convert back to Celsius
        return (hi - 32) * 5/9
    
    @staticmethod
    def calculate_vector_development_rate(temperature: float, species: VectorSpecies) -> float:
        """Calculate vector development rate based on temperature."""
        # Simplified degree-day model
        base_temps = {
            VectorSpecies.AEDES_AEGYPTI: 12.4,
            VectorSpecies.CULEX: 11.3,
            VectorSpecies.IXODES_TICK: 0.0,
        }
        
        base_temp = base_temps.get(species, 10.0)
        
        if temperature <= base_temp:
            return 0.0
        
        # Development rate increases linearly with temperature above base
        return max(0, temperature - base_temp) / 100  # Normalized rate

class EnvironmentalDataCollector:
    """Main collector for environmental surveillance data."""
    
    def __init__(self, storage_path: str = "./environmental_data"):
        self.storage_path = storage_path
        self.climate_records: List[EnvironmentalRecord] = []
        self.vector_records: List[VectorSurveyRecord] = []
        self.risk_assessments: List[Dict] = []
        self.alerts: List[Dict] = []
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        logger.info(f"Environmental Data Collector initialized")
        logger.info(f"Storage path: {storage_path}")
    
    def add_climate_record(self, record: EnvironmentalRecord) -> bool:
        """Add climate monitoring record."""
        try:
            if not self._validate_climate_record(record):
                logger.error(f"Invalid climate record: {record.record_id}")
                return False
            
            self.climate_records.append(record)
            logger.info(f"Added climate record: {record.parameter} = {record.value} {record.unit} "
                       f"at {record.county}, {record.state}")
            
            # Check for extreme conditions
            self._check_extreme_conditions(record)
            
            # Calculate vector risk
            self._assess_vector_risk(record)
            
            self._save_climate_record(record)
            return True
            
        except Exception as e:
            logger.error(f"Error adding climate record {record.record_id}: {e}")
            return False
    
    def add_vector_survey(self, record: VectorSurveyRecord) -> bool:
        """Add vector surveillance record."""
        try:
            if not self._validate_vector_record(record):
                logger.error(f"Invalid vector record: {record.survey_id}")
                return False
            
            self.vector_records.append(record)
            logger.info(f"Added vector survey: {record.vector_species.value} - "
                       f"{record.total_collected} collected in {record.county}, {record.state}")
            
            # Check for high vector populations
            self._check_vector_thresholds(record)
            
            # Check for pathogen detection
            if record.pathogen_detected:
                self._alert_pathogen_in_vector(record)
            
            self._save_vector_record(record)
            return True
            
        except Exception as e:
            logger.error(f"Error adding vector record {record.survey_id}: {e}")
            return False
    
    def _validate_climate_record(self, record: EnvironmentalRecord) -> bool:
        """Validate climate record."""
        # Geographic bounds
        if not (-90 <= record.location_lat <= 90):
            return False
        if not (-180 <= record.location_lon <= 180):
            return False
        
        # Parameter-specific validation
        if record.parameter == "temperature":
            if not (-50 <= record.value <= 60):  # Celsius
                return False
        elif record.parameter == "humidity":
            if not (0 <= record.value <= 100):  # Percentage
                return False
        elif record.parameter == "precipitation":
            if record.value < 0:
                return False
        
        return True
    
    def _validate_vector_record(self, record: VectorSurveyRecord) -> bool:
        """Validate vector surveillance record."""
        if record.total_collected < 0:
            return False
        if record.female_count + record.male_count > record.total_collected:
            return False
        if record.infection_rate and not (0 <= record.infection_rate <= 100):
            return False
        
        return True
    
    def _check_extreme_conditions(self, record: EnvironmentalRecord):
        """Check for extreme weather conditions."""
        alerts = []
        
        if record.parameter == "temperature":
            if record.value > 40:  # Extreme heat
                alerts.append("EXTREME_HEAT")
            elif record.value < -20:  # Extreme cold
                alerts.append("EXTREME_COLD")
        
        elif record.parameter == "precipitation":
            if record.value > 50:  # Heavy rainfall (mm/day)
                alerts.append("HEAVY_RAINFALL")
        
        elif record.parameter == "wind_speed":
            if record.value > 120:  # Hurricane force (km/h)
                alerts.append("EXTREME_WIND")
        
        for alert_type in alerts:
            alert = {
                "alert_type": alert_type,
                "record_id": record.record_id,
                "timestamp": datetime.now().isoformat(),
                "location": f"{record.county}, {record.state}",
                "parameter": record.parameter,
                "value": record.value,
                "unit": record.unit,
                "priority": "HIGH"
            }
            self.alerts.append(alert)
            logger.warning(f"EXTREME CONDITION: {alert}")
    
    def _assess_vector_risk(self, record: EnvironmentalRecord):
        """Assess vector-borne disease risk based on climate."""
        
        # Get recent climate data for this location
        location_data = self._get_recent_location_data(
            record.location_lat, record.location_lon, days=7
        )
        
        # Calculate average conditions
        avg_temp = self._get_avg_parameter(location_data, "temperature")
        avg_humidity = self._get_avg_parameter(location_data, "humidity")
        total_precip = self._get_sum_parameter(location_data, "precipitation")
        
        if avg_temp is None or avg_humidity is None:
            return
        
        # Check conditions for each vector species
        for species in VectorSpecies:
            if EnvironmentalThresholds.is_favorable_for_vectors(
                avg_temp, avg_humidity, total_precip, species):
                
                risk_assessment = {
                    "assessment_id": f"RISK_{record.location_lat}_{record.location_lon}_{datetime.now().strftime('%Y%m%d')}",
                    "timestamp": datetime.now().isoformat(),
                    "location_lat": record.location_lat,
                    "location_lon": record.location_lon,
                    "location": f"{record.county}, {record.state}",
                    "vector_species": species.value,
                    "risk_level": "HIGH",
                    "avg_temperature": avg_temp,
                    "avg_humidity": avg_humidity,
                    "total_precipitation": total_precip,
                    "favorable_conditions": True
                }
                
                self.risk_assessments.append(risk_assessment)
                
                alert = {
                    "alert_type": "FAVORABLE_VECTOR_CONDITIONS",
                    "timestamp": datetime.now().isoformat(),
                    "vector_species": species.value,
                    "location": f"{record.county}, {record.state}",
                    "risk_assessment": risk_assessment,
                    "priority": "MODERATE"
                }
                self.alerts.append(alert)
                logger.info(f"FAVORABLE VECTOR CONDITIONS: {alert}")
    
    def _check_vector_thresholds(self, record: VectorSurveyRecord):
        """Check if vector populations exceed alert thresholds."""
        
        # Population density thresholds (per trap night)
        thresholds = {
            VectorSpecies.AEDES_AEGYPTI: 10,
            VectorSpecies.AEDES_ALBOPICTUS: 15,
            VectorSpecies.CULEX: 20,
            VectorSpecies.IXODES_TICK: 5,
        }
        
        density = record.total_collected / max(record.trap_nights, 1)
        threshold = thresholds.get(record.vector_species, 10)
        
        if density > threshold:
            alert = {
                "alert_type": "HIGH_VECTOR_POPULATION",
                "survey_id": record.survey_id,
                "timestamp": datetime.now().isoformat(),
                "vector_species": record.vector_species.value,
                "location": f"{record.county}, {record.state}",
                "density": density,
                "threshold": threshold,
                "total_collected": record.total_collected,
                "priority": "HIGH"
            }
            self.alerts.append(alert)
            logger.warning(f"HIGH VECTOR POPULATION: {alert}")
    
    def _alert_pathogen_in_vector(self, record: VectorSurveyRecord):
        """Alert when pathogen detected in vectors."""
        alert = {
            "alert_type": "PATHOGEN_IN_VECTOR",
            "survey_id": record.survey_id,
            "timestamp": datetime.now().isoformat(),
            "vector_species": record.vector_species.value,
            "pathogen": record.pathogen_detected,
            "infection_rate": record.infection_rate,
            "location": f"{record.county}, {record.state}",
            "priority": "CRITICAL"
        }
        self.alerts.append(alert)
        logger.critical(f"PATHOGEN IN VECTOR: {alert}")
    
    def _get_recent_location_data(self, lat: float, lon: float, 
                                 days: int = 7) -> List[EnvironmentalRecord]:
        """Get recent climate data for specific location."""
        cutoff = datetime.now() - timedelta(days=days)
        
        nearby_records = []
        for record in self.climate_records:
            if (record.timestamp >= cutoff and
                abs(record.location_lat - lat) < 0.1 and  # ~11km
                abs(record.location_lon - lon) < 0.1):
                nearby_records.append(record)
        
        return nearby_records
    
    def _get_avg_parameter(self, records: List[EnvironmentalRecord], parameter: str) -> Optional[float]:
        """Calculate average value for parameter."""
        values = [r.value for r in records if r.parameter == parameter]
        return sum(values) / len(values) if values else None
    
    def _get_sum_parameter(self, records: List[EnvironmentalRecord], parameter: str) -> float:
        """Calculate sum for parameter (e.g., precipitation)."""
        values = [r.value for r in records if r.parameter == parameter]
        return sum(values)
    
    def _save_climate_record(self, record: EnvironmentalRecord):
        """Save climate record to storage."""
        try:
            filename = f"climate_{record.record_id}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.storage_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(record.to_dict(), f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving climate record {record.record_id}: {e}")
    
    def _save_vector_record(self, record: VectorSurveyRecord):
        """Save vector record to storage."""
        try:
            filename = f"vector_{record.survey_id}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.storage_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(record.to_dict(), f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving vector record {record.survey_id}: {e}")
    
    def get_current_conditions(self, lat: float, lon: float) -> Dict:
        """Get current environmental conditions for location."""
        recent_data = self._get_recent_location_data(lat, lon, days=1)
        
        conditions = {}
        for param in ["temperature", "humidity", "precipitation", "wind_speed"]:
            avg = self._get_avg_parameter(recent_data, param)
            if avg is not None:
                conditions[param] = avg
        
        return conditions
    
    def get_vector_risk_forecast(self, lat: float, lon: float, days: int = 14) -> Dict:
        """Generate vector-borne disease risk forecast."""
        
        conditions = self.get_current_conditions(lat, lon)
        
        if not conditions:
            return {"risk_level": "UNKNOWN", "reason": "Insufficient data"}
        
        high_risk_species = []
        moderate_risk_species = []
        
        temp = conditions.get("temperature", 20)
        humidity = conditions.get("humidity", 50)
        precip = conditions.get("precipitation", 0) * 7  # Weekly total
        
        for species in VectorSpecies:
            if EnvironmentalThresholds.is_favorable_for_vectors(temp, humidity, precip, species):
                # Calculate development rate
                dev_rate = ClimateRiskCalculator.calculate_vector_development_rate(temp, species)
                
                if dev_rate > 0.3:
                    high_risk_species.append(species.value)
                elif dev_rate > 0.1:
                    moderate_risk_species.append(species.value)
        
        # Determine overall risk
        if high_risk_species:
            risk_level = "HIGH"
        elif moderate_risk_species:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
        
        return {
            "risk_level": risk_level,
            "forecast_days": days,
            "current_conditions": conditions,
            "high_risk_vectors": high_risk_species,
            "moderate_risk_vectors": moderate_risk_species,
            "heat_index": ClimateRiskCalculator.calculate_heat_index(temp, humidity),
            "recommendations": self._generate_risk_recommendations(risk_level, high_risk_species)
        }
    
    def _generate_risk_recommendations(self, risk_level: str, high_risk_vectors: List[str]) -> List[str]:
        """Generate recommendations based on risk level."""
        recommendations = []
        
        if risk_level == "HIGH":
            recommendations.extend([
                "Increase vector surveillance activities",
                "Implement enhanced mosquito control measures",
                "Issue public health advisories for vector-borne diseases",
                "Monitor for increased vector-borne disease cases"
            ])
        
        if "aedes_aegypti" in high_risk_vectors:
            recommendations.append("Monitor for yellow fever and dengue transmission")
        
        if "culex" in high_risk_vectors:
            recommendations.append("Increase West Nile virus surveillance")
        
        if "ixodes_tick" in high_risk_vectors:
            recommendations.append("Enhance tick-borne disease surveillance")
        
        return recommendations
    
    def generate_environmental_summary(self, days: int = 7) -> Dict:
        """Generate environmental surveillance summary."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        recent_climate = [r for r in self.climate_records if r.timestamp >= start_time]
        recent_vectors = [r for r in self.vector_records if r.timestamp >= start_time]
        recent_alerts = [a for a in self.alerts 
                        if datetime.fromisoformat(a['timestamp']) >= start_time]
        
        # Parameter summaries
        temp_records = [r for r in recent_climate if r.parameter == "temperature"]
        humid_records = [r for r in recent_climate if r.parameter == "humidity"]
        precip_records = [r for r in recent_climate if r.parameter == "precipitation"]
        
        return {
            "period": f"{days} days",
            "start_date": start_time.isoformat(),
            "end_date": end_time.isoformat(),
            "climate_records": len(recent_climate),
            "vector_surveys": len(recent_vectors),
            "total_alerts": len(recent_alerts),
            "high_priority_alerts": len([a for a in recent_alerts if a.get('priority') == 'HIGH']),
            "temperature_range": {
                "min": min([r.value for r in temp_records]) if temp_records else None,
                "max": max([r.value for r in temp_records]) if temp_records else None,
                "avg": sum([r.value for r in temp_records]) / len(temp_records) if temp_records else None
            },
            "total_vectors_collected": sum([r.total_collected for r in recent_vectors]),
            "pathogen_positive_surveys": len([r for r in recent_vectors if r.pathogen_detected])
        }

# Mock data generators
class MockEnvironmentalDataGenerator:
    """Generate realistic mock environmental data."""
    
    US_LOCATIONS = [
        (40.7128, -74.0060, "New York", "NY"),
        (34.0522, -118.2437, "Los Angeles", "CA"),
        (41.8781, -87.6298, "Chicago", "IL"),
        (29.7604, -95.3698, "Houston", "TX"),
        (25.7617, -80.1918, "Miami", "FL"),
    ]
    
    @classmethod
    def generate_climate_record(cls, location_idx: int = None) -> EnvironmentalRecord:
        """Generate realistic climate record."""
        if location_idx is None:
            location_idx = random.randint(0, len(cls.US_LOCATIONS) - 1)
        
        lat, lon, county, state = cls.US_LOCATIONS[location_idx]
        
        # Add some random variation to location
        lat += random.uniform(-0.1, 0.1)
        lon += random.uniform(-0.1, 0.1)
        
        # Generate realistic climate data
        parameter = random.choice(["temperature", "humidity", "precipitation", "wind_speed"])
        
        if parameter == "temperature":
            value = random.uniform(10, 35)  # Celsius
            unit = "celsius"
        elif parameter == "humidity":
            value = random.uniform(30, 90)  # Percentage
            unit = "percent"
        elif parameter == "precipitation":
            value = random.uniform(0, 25)  # mm/day
            unit = "mm"
        else:  # wind_speed
            value = random.uniform(5, 40)  # km/h
            unit = "kmh"
        
        return EnvironmentalRecord(
            record_id=f"ENV_{random.randint(100000, 999999)}",
            timestamp=datetime.now() - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23)
            ),
            location_lat=lat,
            location_lon=lon,
            county=county,
            state=state,
            data_type=EnvironmentalDataType.CLIMATE,
            parameter=parameter,
            value=value,
            unit=unit,
            source="weather_station",
            quality_flag="good",
            collection_method="automated",
            station_id=f"WS_{random.randint(1000, 9999)}"
        )
    
    @classmethod
    def generate_vector_survey(cls, location_idx: int = None) -> VectorSurveyRecord:
        """Generate realistic vector surveillance record."""
        if location_idx is None:
            location_idx = random.randint(0, len(cls.US_LOCATIONS) - 1)
        
        lat, lon, county, state = cls.US_LOCATIONS[location_idx]
        lat += random.uniform(-0.1, 0.1)
        lon += random.uniform(-0.1, 0.1)
        
        species = random.choice(list(VectorSpecies))
        total = random.randint(0, 50)
        female = random.randint(0, total)
        male = total - female
        
        return VectorSurveyRecord(
            survey_id=f"VEC_{random.randint(100000, 999999)}",
            timestamp=datetime.now() - timedelta(
                days=random.randint(0, 14),
                hours=random.randint(0, 23)
            ),
            location_lat=lat,
            location_lon=lon,
            county=county,
            state=state,
            vector_species=species,
            collection_method="light_trap",
            trap_nights=random.randint(1, 3),
            total_collected=total,
            female_count=female,
            male_count=male,
            infection_rate=random.uniform(0, 5) if random.random() > 0.8 else None,
            pathogen_detected="West_Nile_virus" if random.random() > 0.95 else None,
            environmental_conditions={
                "temperature": random.uniform(20, 30),
                "humidity": random.uniform(50, 80)
            },
            surveyor=f"Surveyor_{random.randint(1, 10)}"
        )

def run_demonstration():
    """Run demonstration of environmental data collection."""
    print("🌍 Environmental Data Collector - Demonstration")
    print("=" * 60)
    
    # Initialize collector
    collector = EnvironmentalDataCollector()
    
    # Generate climate data
    print("\n🌡️ Generating climate monitoring data...")
    for i in range(25):
        record = MockEnvironmentalDataGenerator.generate_climate_record()
        collector.add_climate_record(record)
    
    # Generate vector surveillance data
    print("\n🦟 Generating vector surveillance data...")
    for i in range(15):
        survey = MockEnvironmentalDataGenerator.generate_vector_survey()
        collector.add_vector_survey(survey)
    
    # Show summary
    print(f"\n📊 Environmental Data Summary:")
    print(f"  Climate Records: {len(collector.climate_records)}")
    print(f"  Vector Surveys: {len(collector.vector_records)}")
    print(f"  Risk Assessments: {len(collector.risk_assessments)}")
    print(f"  Total Alerts: {len(collector.alerts)}")
    
    # Show recent alerts
    high_priority_alerts = [a for a in collector.alerts if a.get('priority') in ['HIGH', 'CRITICAL']]
    print(f"\n🚨 High Priority Alerts: {len(high_priority_alerts)}")
    
    for alert in high_priority_alerts[:3]:
        print(f"  - {alert['alert_type']}: {alert.get('priority', 'N/A')} - {alert.get('location', 'N/A')}")
    
    # Generate risk forecast
    ny_lat, ny_lon = 40.7128, -74.0060
    forecast = collector.get_vector_risk_forecast(ny_lat, ny_lon)
    print(f"\n🎯 Vector Risk Forecast (New York):")
    print(f"  Risk Level: {forecast['risk_level']}")
    print(f"  High Risk Vectors: {forecast.get('high_risk_vectors', [])}")
    heat_index = forecast.get('heat_index', 'N/A')
    if isinstance(heat_index, (int, float)):
        print(f"  Heat Index: {heat_index:.1f}°C")
    else:
        print(f"  Heat Index: {heat_index}")
    
    
    # Environmental summary
    env_summary = collector.generate_environmental_summary(7)
    print(f"\n📈 7-Day Environmental Summary:")
    print(f"  Climate Records: {env_summary['climate_records']}")
    print(f"  Vector Surveys: {env_summary['vector_surveys']}")
    print(f"  High Priority Alerts: {env_summary['high_priority_alerts']}")
    print(f"  Vectors Collected: {env_summary['total_vectors_collected']}")
    print(f"  Pathogen Positive: {env_summary['pathogen_positive_surveys']}")
    
    if env_summary['temperature_range']['avg']:
        print(f"  Avg Temperature: {env_summary['temperature_range']['avg']:.1f}°C")
    
    return collector

if __name__ == "__main__":
    collector = run_demonstration()
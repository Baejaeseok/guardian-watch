"""
Animal-Human Health Data Bridge
===============================
Core integration module for One Health surveillance system.
Connects animal and human health data streams for early zoonotic disease detection.

NIW Focus: Practical demonstration of cross-species disease surveillance integration.
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth using Haversine formula.
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

@dataclass
class AnimalHealthEvent:
    """Standardized animal health event structure."""
    event_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    animal_type: str  # 'poultry', 'cattle', 'swine', 'wildlife'
    disease_suspect: str
    severity: str  # 'low', 'medium', 'high'
    affected_count: int
    farm_id: Optional[str] = None
    reported_by: Optional[str] = None
    
@dataclass
class HumanHealthEvent:
    """Standardized human health event structure."""
    event_id: str
    timestamp: datetime
    location_lat: float
    location_lon: float
    symptoms: List[str]
    age_group: str
    severity: str  # 'mild', 'moderate', 'severe'
    occupation: Optional[str] = None
    animal_exposure: bool = False
    healthcare_facility: Optional[str] = None

@dataclass
class CrossSpeciesAlert:
    """Alert when animal and human events are correlated."""
    alert_id: str
    timestamp: datetime
    animal_event: AnimalHealthEvent
    human_event: HumanHealthEvent
    correlation_score: float
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    geographic_distance_km: float
    temporal_distance_hours: float
    recommended_actions: List[str]

class ZoonoticPathogenMapper:
    """Maps pathogens to their animal hosts and human symptoms."""
    
    PATHOGEN_PROFILES = {
        'H5N1': {
            'animal_hosts': ['poultry', 'waterfowl', 'wild_birds'],
            'animal_symptoms': ['sudden_death', 'respiratory_distress', 'decreased_egg_production'],
            'human_symptoms': ['fever', 'cough', 'dyspnea', 'conjunctivitis'],
            'high_risk_occupations': ['farmer', 'veterinarian', 'poultry_worker'],
            'transmission_routes': ['direct_contact', 'respiratory_droplets', 'contaminated_surfaces']
        },
        'brucellosis': {
            'animal_hosts': ['cattle', 'swine', 'goats', 'sheep'],
            'animal_symptoms': ['abortion', 'infertility', 'arthritis', 'mastitis'],
            'human_symptoms': ['fever', 'sweats', 'joint_pain', 'fatigue'],
            'high_risk_occupations': ['farmer', 'veterinarian', 'slaughterhouse_worker'],
            'transmission_routes': ['direct_contact', 'ingestion', 'inhalation']
        },
        'west_nile_virus': {
            'animal_hosts': ['birds', 'horses', 'mammals'],
            'animal_symptoms': ['neurological_signs', 'weakness', 'death'],
            'human_symptoms': ['fever', 'headache', 'muscle_weakness', 'neurological_symptoms'],
            'high_risk_occupations': ['outdoor_worker', 'veterinarian'],
            'transmission_routes': ['mosquito_bite', 'laboratory_exposure']
        },
        'lyme_disease': {
            'animal_hosts': ['deer', 'rodents', 'dogs'],
            'animal_symptoms': ['lameness', 'fever', 'lethargy'],
            'human_symptoms': ['erythema_migrans', 'fever', 'joint_pain', 'neurological_symptoms'],
            'high_risk_occupations': ['forestry_worker', 'hunter', 'outdoor_recreationist'],
            'transmission_routes': ['tick_bite']
        }
    }
    
    @classmethod
    def identify_likely_pathogen(cls, animal_event: AnimalHealthEvent, human_symptoms: List[str]) -> List[Tuple[str, float]]:
        """Identify likely pathogens based on animal and human data."""
        matches = []
        
        for pathogen, profile in cls.PATHOGEN_PROFILES.items():
            score = 0.0
            
            # Check animal host match
            if animal_event.animal_type in profile['animal_hosts']:
                score += 0.4
            
            # Check symptom overlap
            symptom_matches = len(set(human_symptoms) & set(profile['human_symptoms']))
            if symptom_matches > 0:
                score += (symptom_matches / len(profile['human_symptoms'])) * 0.6
            
            if score > 0.3:  # Minimum threshold
                matches.append((pathogen, score))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

class SpatioTemporalCorrelator:
    """Analyzes spatial and temporal relationships between events."""
    
    def __init__(self, max_distance_km: float = 50, max_time_hours: float = 168):  # 1 week
        self.max_distance_km = max_distance_km
        self.max_time_hours = max_time_hours
    
    def calculate_correlation_score(self, animal_event: AnimalHealthEvent, human_event: HumanHealthEvent) -> Tuple[float, Dict]:
        """Calculate correlation score between animal and human events."""
        
        # Calculate geographic distance
        distance_km = calculate_distance_km(
            animal_event.location_lat, animal_event.location_lon,
            human_event.location_lat, human_event.location_lon
        )
        
        # Calculate temporal distance
        time_diff = abs((human_event.timestamp - animal_event.timestamp).total_seconds() / 3600)
        
        # Initialize correlation factors
        correlation_factors = {}
        total_score = 0.0
        
        # Geographic proximity score (closer = higher score)
        if distance_km <= self.max_distance_km:
            geo_score = 1.0 - (distance_km / self.max_distance_km)
            correlation_factors['geographic'] = geo_score
            total_score += geo_score * 0.3
        else:
            correlation_factors['geographic'] = 0.0
        
        # Temporal proximity score (closer in time = higher score)
        if time_diff <= self.max_time_hours:
            temporal_score = 1.0 - (time_diff / self.max_time_hours)
            correlation_factors['temporal'] = temporal_score
            total_score += temporal_score * 0.2
        else:
            correlation_factors['temporal'] = 0.0
        
        # Pathogen likelihood score
        human_symptoms = getattr(human_event, 'symptoms', [])
        pathogen_matches = ZoonoticPathogenMapper.identify_likely_pathogen(animal_event, human_symptoms)
        
        if pathogen_matches:
            pathogen_score = pathogen_matches[0][1]  # Highest scoring pathogen
            correlation_factors['pathogen'] = pathogen_score
            correlation_factors['likely_pathogen'] = pathogen_matches[0][0]
            total_score += pathogen_score * 0.4
        else:
            correlation_factors['pathogen'] = 0.0
            correlation_factors['likely_pathogen'] = None
        
        # Occupational risk factor
        if hasattr(human_event, 'occupation') and human_event.occupation:
            if pathogen_matches:
                likely_pathogen = pathogen_matches[0][0]
                high_risk_occupations = ZoonoticPathogenMapper.PATHOGEN_PROFILES[likely_pathogen].get('high_risk_occupations', [])
                if human_event.occupation in high_risk_occupations:
                    correlation_factors['occupational_risk'] = 1.0
                    total_score += 0.1
                else:
                    correlation_factors['occupational_risk'] = 0.0
        
        correlation_factors['total_score'] = min(total_score, 1.0)
        correlation_factors['distance_km'] = distance_km
        correlation_factors['time_diff_hours'] = time_diff
        
        return correlation_factors['total_score'], correlation_factors

class AnimalHumanBridge:
    """Main bridge class connecting animal and human health surveillance."""
    
    def __init__(self):
        self.animal_events: List[AnimalHealthEvent] = []
        self.human_events: List[HumanHealthEvent] = []
        self.alerts: List[CrossSpeciesAlert] = []
        self.correlator = SpatioTemporalCorrelator()
        
        logger.info("Animal-Human Health Bridge initialized")
    
    def add_animal_event(self, event: AnimalHealthEvent):
        """Add new animal health event and check for correlations."""
        self.animal_events.append(event)
        logger.info(f"Added animal event: {event.disease_suspect} in {event.animal_type}")
        
        # Check correlations with recent human events
        self._check_correlations_for_animal_event(event)
    
    def add_human_event(self, event: HumanHealthEvent):
        """Add new human health event and check for correlations."""
        self.human_events.append(event)
        logger.info(f"Added human event: {event.symptoms} - age group {event.age_group}")
        
        # Check correlations with recent animal events
        self._check_correlations_for_human_event(event)
    
    def _check_correlations_for_animal_event(self, animal_event: AnimalHealthEvent):
        """Check new animal event against recent human events."""
        
        # Look at human events from the last 30 days
        cutoff_date = animal_event.timestamp - timedelta(days=30)
        recent_human_events = [he for he in self.human_events if he.timestamp >= cutoff_date]
        
        for human_event in recent_human_events:
            score, factors = self.correlator.calculate_correlation_score(animal_event, human_event)
            
            if score > 0.5:  # Significant correlation threshold
                alert = self._create_alert(animal_event, human_event, score, factors)
                self.alerts.append(alert)
                logger.warning(f"CORRELATION ALERT: {alert.alert_id} - Score: {score:.3f}")
    
    def _check_correlations_for_human_event(self, human_event: HumanHealthEvent):
        """Check new human event against recent animal events."""
        
        # Look at animal events from the last 30 days
        cutoff_date = human_event.timestamp - timedelta(days=30)
        recent_animal_events = [ae for ae in self.animal_events if ae.timestamp >= cutoff_date]
        
        for animal_event in recent_animal_events:
            score, factors = self.correlator.calculate_correlation_score(animal_event, human_event)
            
            if score > 0.5:  # Significant correlation threshold
                alert = self._create_alert(animal_event, human_event, score, factors)
                self.alerts.append(alert)
                logger.warning(f"CORRELATION ALERT: {alert.alert_id} - Score: {score:.3f}")
    
    def _create_alert(self, animal_event: AnimalHealthEvent, human_event: HumanHealthEvent, 
                     score: float, factors: Dict) -> CrossSpeciesAlert:
        """Create a cross-species alert."""
        
        # Determine risk level based on score
        if score >= 0.8:
            risk_level = 'critical'
        elif score >= 0.7:
            risk_level = 'high'
        elif score >= 0.6:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Generate recommended actions
        actions = self._generate_recommended_actions(risk_level, factors.get('likely_pathogen'))
        
        alert = CrossSpeciesAlert(
            alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{animal_event.event_id}_{human_event.event_id}",
            timestamp=datetime.now(),
            animal_event=animal_event,
            human_event=human_event,
            correlation_score=score,
            risk_level=risk_level,
            geographic_distance_km=factors.get('distance_km', 0),
            temporal_distance_hours=factors.get('time_diff_hours', 0),
            recommended_actions=actions
        )
        
        return alert
    
    def _generate_recommended_actions(self, risk_level: str, likely_pathogen: Optional[str]) -> List[str]:
        """Generate context-specific recommended actions."""
        
        base_actions = [
            "Notify local health department",
            "Enhance surveillance in affected area",
            "Review laboratory testing protocols"
        ]
        
        if risk_level in ['high', 'critical']:
            base_actions.extend([
                "Activate rapid response team",
                "Implement movement restrictions if warranted",
                "Increase environmental sampling",
                "Coordinate with veterinary authorities"
            ])
        
        if likely_pathogen:
            pathogen_specific = {
                'H5N1': ["Implement poultry quarantine", "Use enhanced PPE", "Monitor poultry workers"],
                'brucellosis': ["Test livestock herd", "Implement milk pasteurization", "Screen farm workers"],
                'west_nile_virus': ["Enhance mosquito control", "Monitor dead bird reports", "Issue public advisories"],
                'lyme_disease': ["Increase tick surveillance", "Issue prevention guidance", "Monitor pet health"]
            }
            base_actions.extend(pathogen_specific.get(likely_pathogen, []))
        
        return base_actions
    
    def get_recent_alerts(self, hours: int = 24) -> List[CrossSpeciesAlert]:
        """Get alerts from the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alerts if alert.timestamp >= cutoff]
    
    def get_high_risk_areas(self, days: int = 7) -> List[Dict]:
        """Identify geographic areas with multiple correlations."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_alerts = [alert for alert in self.alerts if alert.timestamp >= cutoff]
        
        # Group alerts by geographic proximity
        risk_areas = []
        processed_alerts = set()
        
        for alert in recent_alerts:
            if alert.alert_id in processed_alerts:
                continue
                
            # Find nearby alerts (within 25km)
            nearby_alerts = []
            alert_lat = alert.animal_event.location_lat
            alert_lon = alert.animal_event.location_lon
            
            for other_alert in recent_alerts:
                if other_alert.alert_id in processed_alerts:
                    continue
                    
                distance = calculate_distance_km(
                    alert_lat, alert_lon,
                    other_alert.animal_event.location_lat, other_alert.animal_event.location_lon
                )
                
                if distance <= 25:  # 25km radius
                    nearby_alerts.append(other_alert)
                    processed_alerts.add(other_alert.alert_id)
            
            if len(nearby_alerts) >= 2:  # Multiple alerts in area
                lats = [a.animal_event.location_lat for a in nearby_alerts]
                lons = [a.animal_event.location_lon for a in nearby_alerts]
                avg_lat = sum(lats) / len(lats)
                avg_lon = sum(lons) / len(lons)
                max_risk = max([a.correlation_score for a in nearby_alerts])
                
                risk_areas.append({
                    'center_lat': avg_lat,
                    'center_lon': avg_lon,
                    'alert_count': len(nearby_alerts),
                    'max_correlation_score': max_risk,
                    'alerts': [a.alert_id for a in nearby_alerts]
                })
        
        return sorted(risk_areas, key=lambda x: x['max_correlation_score'], reverse=True)
    
    def export_data_for_analysis(self) -> Dict:
        """Export all data for external analysis tools."""
        return {
            'animal_events': [
                {
                    'event_id': ae.event_id,
                    'timestamp': ae.timestamp.isoformat(),
                    'location_lat': ae.location_lat,
                    'location_lon': ae.location_lon,
                    'animal_type': ae.animal_type,
                    'disease_suspect': ae.disease_suspect,
                    'severity': ae.severity,
                    'affected_count': ae.affected_count
                } for ae in self.animal_events
            ],
            'human_events': [
                {
                    'event_id': he.event_id,
                    'timestamp': he.timestamp.isoformat(),
                    'location_lat': he.location_lat,
                    'location_lon': he.location_lon,
                    'symptoms': he.symptoms,
                    'age_group': he.age_group,
                    'occupation': he.occupation,
                    'animal_exposure': he.animal_exposure,
                    'severity': he.severity
                } for he in self.human_events
            ],
            'alerts': [
                {
                    'alert_id': alert.alert_id,
                    'timestamp': alert.timestamp.isoformat(),
                    'correlation_score': alert.correlation_score,
                    'risk_level': alert.risk_level,
                    'geographic_distance_km': alert.geographic_distance_km,
                    'temporal_distance_hours': alert.temporal_distance_hours,
                    'recommended_actions': alert.recommended_actions
                } for alert in self.alerts
            ]
        }

# Demo and testing functions
def create_sample_animal_event() -> AnimalHealthEvent:
    """Create a sample animal health event for testing."""
    return AnimalHealthEvent(
        event_id="ANIMAL_001",
        timestamp=datetime.now() - timedelta(hours=12),
        location_lat=40.7128,
        location_lon=-74.0060,
        animal_type="poultry",
        disease_suspect="H5N1",
        severity="high",
        affected_count=150,
        farm_id="FARM_NY_001",
        reported_by="Dr. Smith, DVM"
    )

def create_sample_human_event() -> HumanHealthEvent:
    """Create a sample human health event for testing."""
    return HumanHealthEvent(
        event_id="HUMAN_001",
        timestamp=datetime.now() - timedelta(hours=6),
        location_lat=40.7580,
        location_lon=-73.9855,
        symptoms=["fever", "cough", "dyspnea"],
        age_group="40-60",
        occupation="farmer",
        animal_exposure=True,
        severity="moderate",
        healthcare_facility="NYC General Hospital"
    )

def run_demonstration():
    """Run a demonstration of the bridge system."""
    print("🦠 Animal-Human Health Data Bridge - Demonstration")
    print("=" * 60)
    
    # Initialize bridge
    bridge = AnimalHumanBridge()
    
    # Add sample events
    print("\n📊 Adding sample animal health event...")
    animal_event = create_sample_animal_event()
    bridge.add_animal_event(animal_event)
    
    print("\n👥 Adding sample human health event...")
    human_event = create_sample_human_event()
    bridge.add_human_event(human_event)
    
    # Check for alerts
    recent_alerts = bridge.get_recent_alerts(24)
    print(f"\n🚨 Generated {len(recent_alerts)} correlation alerts")
    
    for alert in recent_alerts:
        print(f"\nAlert ID: {alert.alert_id}")
        print(f"Risk Level: {alert.risk_level}")
        print(f"Correlation Score: {alert.correlation_score:.3f}")
        print(f"Distance: {alert.geographic_distance_km:.1f} km")
        print(f"Time Difference: {alert.temporal_distance_hours:.1f} hours")
        print("Recommended Actions:")
        for action in alert.recommended_actions[:3]:  # Show first 3
            print(f"  - {action}")
    
    # Show risk areas
    risk_areas = bridge.get_high_risk_areas(7)
    print(f"\n🗺️ Identified {len(risk_areas)} high-risk areas")
    
    print(f"\n📈 System Status:")
    print(f"  Animal Events: {len(bridge.animal_events)}")
    print(f"  Human Events: {len(bridge.human_events)}")
    print(f"  Total Alerts: {len(bridge.alerts)}")
    
    return bridge

if __name__ == "__main__":
    bridge = run_demonstration()
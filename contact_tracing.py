"""
Contact Tracing System
======================
Module 4: Response & Control Systems

Advanced contact tracing and transmission pathway analysis system for One Health responses,
providing comprehensive contact identification, tracking, and risk assessment.

NIW Focus: Contact intelligence enabling rapid transmission chain interruption and exposure management.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
import itertools
import random
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContactType(Enum):
    """Types of contact exposure."""
    HOUSEHOLD = "household"                    # Household members
    CLOSE_CONTACT = "close_contact"           # <2m for >15 minutes
    CASUAL_CONTACT = "casual_contact"         # Brief/distant interaction
    WORKPLACE = "workplace"                   # Work-related exposure
    HEALTHCARE = "healthcare"                 # Healthcare setting
    COMMUNITY = "community"                   # Community gathering
    TRAVEL = "travel"                         # Travel-related
    UNKNOWN = "unknown"                       # Unknown exposure

class ExposureRisk(Enum):
    """Risk level of exposure."""
    HIGH_RISK = "high_risk"                   # High transmission risk
    MEDIUM_RISK = "medium_risk"               # Moderate transmission risk
    LOW_RISK = "low_risk"                     # Low transmission risk
    MINIMAL_RISK = "minimal_risk"             # Minimal transmission risk
    NO_RISK = "no_risk"                       # No significant risk

class ContactStatus(Enum):
    """Contact monitoring status."""
    IDENTIFIED = "identified"                 # Contact identified
    NOTIFIED = "notified"                     # Contact notified
    MONITORING = "monitoring"                 # Under monitoring
    QUARANTINED = "quarantined"               # In quarantine
    TESTED = "tested"                         # Tested for pathogen
    CLEARED = "cleared"                       # Monitoring complete
    LOST_TO_FOLLOWUP = "lost_to_followup"     # Lost contact
    BECAME_CASE = "became_case"               # Developed illness

class TracingMethod(Enum):
    """Contact tracing methods."""
    INTERVIEW = "interview"                   # Direct interview
    DIGITAL_TRACKING = "digital_tracking"     # Digital contact tracing
    GEOLOCATION = "geolocation"               # Location-based tracing
    SOCIAL_NETWORK = "social_network"         # Social network analysis
    ENVIRONMENTAL = "environmental"           # Environmental tracking
    VETERINARY = "veterinary"                 # Animal contact tracing

@dataclass
class ExposureEvent:
    """Single exposure event between case and contact."""
    
    event_id: str
    case_id: str
    contact_id: str
    exposure_date: datetime
    exposure_location: str
    
    # Exposure characteristics
    contact_type: ContactType
    exposure_duration_minutes: int
    distance_meters: float
    setting_type: str  # "indoor", "outdoor", "vehicle", "aircraft"
    ventilation_quality: str  # "poor", "moderate", "good", "excellent"
    protective_measures_used: List[str] = field(default_factory=list)
    
    # Risk assessment
    exposure_risk: ExposureRisk = ExposureRisk.MEDIUM_RISK
    transmission_probability: float = 0.0     # Calculated transmission probability
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    
    # Additional details
    activity_description: str = ""
    symptoms_in_case: bool = True
    infectious_period: bool = True
    notes: str = ""

@dataclass
class ContactRecord:
    """Comprehensive contact record for tracing."""
    
    contact_id: str
    case_id: str  # Source case
    identification_date: datetime
    
    # Contact demographics
    first_name: str
    last_name: str
    age: Optional[int] = None
    gender: str = "unknown"
    phone_numbers: List[str] = field(default_factory=list)
    email_addresses: List[str] = field(default_factory=list)
    addresses: List[str] = field(default_factory=list)
    
    # Exposure information
    exposure_events: List[ExposureEvent] = field(default_factory=list)
    highest_risk_exposure: ExposureRisk = ExposureRisk.LOW_RISK
    total_exposure_time_minutes: int = 0
    first_exposure_date: Optional[datetime] = None
    last_exposure_date: Optional[datetime] = None
    
    # Contact status and monitoring
    contact_status: ContactStatus = ContactStatus.IDENTIFIED
    notification_date: Optional[datetime] = None
    monitoring_start_date: Optional[datetime] = None
    monitoring_end_date: Optional[datetime] = None
    quarantine_start_date: Optional[datetime] = None
    quarantine_end_date: Optional[datetime] = None
    
    # Health monitoring
    symptom_onset_date: Optional[datetime] = None
    symptoms_reported: List[str] = field(default_factory=list)
    temperature_readings: List[Tuple[datetime, float]] = field(default_factory=list)
    test_results: List[Dict[str, Any]] = field(default_factory=list)
    became_case: bool = False
    case_conversion_date: Optional[datetime] = None
    
    # Compliance and follow-up
    compliance_score: float = 1.0             # 0-1 compliance with monitoring
    missed_check_ins: int = 0
    successful_check_ins: int = 0
    follow_up_notes: List[str] = field(default_factory=list)
    
    # Secondary contacts
    secondary_contacts_identified: int = 0
    secondary_contacts_traced: int = 0

@dataclass
class TransmissionChain:
    """Transmission chain linking related cases."""
    
    chain_id: str
    index_case_id: str
    chain_start_date: datetime
    
    # Chain composition
    total_cases: int = 1
    confirmed_cases: List[str] = field(default_factory=list)
    probable_cases: List[str] = field(default_factory=list)
    generation_levels: Dict[str, int] = field(default_factory=dict)  # case_id -> generation
    
    # Chain characteristics
    attack_rate: float = 0.0                  # % contacts who became cases
    serial_interval_days: float = 0.0         # Average time between generations
    doubling_time_days: float = 0.0           # Time for cases to double
    reproduction_number: float = 1.0          # R number for this chain
    
    # Geographic and demographic patterns
    locations_involved: List[str] = field(default_factory=list)
    age_groups_affected: List[str] = field(default_factory=list)
    settings_involved: List[str] = field(default_factory=list)
    
    # Chain status
    is_active: bool = True
    control_measures_applied: List[str] = field(default_factory=list)
    chain_end_date: Optional[datetime] = None
    interruption_method: str = ""
    
    # Analysis insights
    super_spreader_events: List[str] = field(default_factory=list)
    transmission_patterns: List[str] = field(default_factory=list)
    intervention_effectiveness: float = 0.0

class ContactTracer:
    """Individual contact tracer performance tracking."""
    
    def __init__(self, tracer_id: str, tracer_name: str):
        self.tracer_id = tracer_id
        self.tracer_name = tracer_name
        self.contacts_assigned = 0
        self.contacts_successfully_reached = 0
        self.contacts_completed = 0
        self.average_completion_time_hours = 24.0
        self.quality_score = 0.8
        self.active_caseload = 0
        self.performance_metrics = {}

class ContactTracingManager:
    """Central contact tracing management system."""
    
    def __init__(self):
        self.contact_records: Dict[str, ContactRecord] = {}
        self.transmission_chains: Dict[str, TransmissionChain] = {}
        self.contact_tracers: Dict[str, ContactTracer] = {}
        self.exposure_events: List[ExposureEvent] = []
        self.tracing_metrics: Dict[str, Any] = {}
        
        # Initialize default contact tracers
        self._initialize_contact_tracers()
        
        logger.info("One Health Contact Tracing Manager initialized")
    
    def _initialize_contact_tracers(self):
        """Initialize contact tracer team."""
        tracer_names = [
            "Dr. Sarah Chen", "Mike Rodriguez", "Jennifer Park", 
            "David Thompson", "Lisa Wang", "Carlos Martinez",
            "Emily Johnson", "Robert Kim", "Maria Garcia"
        ]
        
        for i, name in enumerate(tracer_names):
            tracer_id = f"TRACER_{i+1:03d}"
            tracer = ContactTracer(tracer_id, name)
            tracer.quality_score = random.uniform(0.7, 0.95)
            tracer.average_completion_time_hours = random.uniform(12, 48)
            self.contact_tracers[tracer_id] = tracer
    
    def create_contact_record(self, case_id: str, contact_info: Dict[str, Any],
                            exposure_details: Dict[str, Any]) -> ContactRecord:
        """Create new contact record from case investigation."""
        
        contact_id = f"CONTACT_{random.randint(100000, 999999)}"
        
        contact = ContactRecord(
            contact_id=contact_id,
            case_id=case_id,
            identification_date=datetime.now(),
            first_name=contact_info.get("first_name", "Unknown"),
            last_name=contact_info.get("last_name", ""),
            age=contact_info.get("age"),
            gender=contact_info.get("gender", "unknown"),
            phone_numbers=contact_info.get("phone_numbers", []),
            email_addresses=contact_info.get("email_addresses", []),
            addresses=contact_info.get("addresses", [])
        )
        
        # Create exposure event
        exposure_event = self._create_exposure_event(case_id, contact_id, exposure_details)
        contact.exposure_events.append(exposure_event)
        
        # Set risk assessment
        contact.highest_risk_exposure = exposure_event.exposure_risk
        contact.total_exposure_time_minutes = exposure_event.exposure_duration_minutes
        contact.first_exposure_date = exposure_event.exposure_date
        contact.last_exposure_date = exposure_event.exposure_date
        
        # Assign to contact tracer
        assigned_tracer = self._assign_contact_tracer()
        if assigned_tracer:
            assigned_tracer.contacts_assigned += 1
            assigned_tracer.active_caseload += 1
        
        self.contact_records[contact_id] = contact
        self.exposure_events.append(exposure_event)
        
        logger.info(f"Contact record created: {contact_id}")
        
        return contact
    
    def _create_exposure_event(self, case_id: str, contact_id: str, 
                              exposure_details: Dict[str, Any]) -> ExposureEvent:
        """Create exposure event from details."""
        
        event_id = f"EXPOSURE_{random.randint(100000, 999999)}"
        
        # Parse exposure details
        exposure_date = exposure_details.get("exposure_date", datetime.now() - timedelta(days=3))
        location = exposure_details.get("location", "Unknown location")
        contact_type_str = exposure_details.get("contact_type", "close_contact")
        duration = exposure_details.get("duration_minutes", 60)
        distance = exposure_details.get("distance_meters", 1.5)
        setting = exposure_details.get("setting", "indoor")
        
        # Determine contact type
        try:
            contact_type = ContactType(contact_type_str)
        except ValueError:
            contact_type = ContactType.CLOSE_CONTACT
        
        event = ExposureEvent(
            event_id=event_id,
            case_id=case_id,
            contact_id=contact_id,
            exposure_date=exposure_date,
            exposure_location=location,
            contact_type=contact_type,
            exposure_duration_minutes=duration,
            distance_meters=distance,
            setting_type=setting,
            ventilation_quality=exposure_details.get("ventilation", "moderate"),
            protective_measures_used=exposure_details.get("protective_measures", []),
            activity_description=exposure_details.get("activity", "")
        )
        
        # Calculate risk assessment
        event.exposure_risk = self._assess_exposure_risk(event)
        event.transmission_probability = self._calculate_transmission_probability(event)
        event.risk_factors = self._identify_risk_factors(event)
        event.protective_factors = self._identify_protective_factors(event)
        
        return event
    
    def _assess_exposure_risk(self, event: ExposureEvent) -> ExposureRisk:
        """Assess exposure risk based on event characteristics."""
        
        risk_score = 0.5  # Base risk
        
        # Duration factor
        if event.exposure_duration_minutes >= 60:
            risk_score += 0.3
        elif event.exposure_duration_minutes >= 15:
            risk_score += 0.2
        
        # Distance factor
        if event.distance_meters < 1.0:
            risk_score += 0.3
        elif event.distance_meters < 2.0:
            risk_score += 0.2
        
        # Setting factor
        if event.setting_type == "indoor":
            risk_score += 0.2
        elif event.setting_type == "vehicle":
            risk_score += 0.25
        
        # Ventilation factor
        if event.ventilation_quality == "poor":
            risk_score += 0.2
        elif event.ventilation_quality == "good":
            risk_score -= 0.1
        elif event.ventilation_quality == "excellent":
            risk_score -= 0.2
        
        # Contact type factor
        if event.contact_type == ContactType.HOUSEHOLD:
            risk_score += 0.3
        elif event.contact_type == ContactType.HEALTHCARE:
            risk_score += 0.2
        
        # Protective measures factor
        if "mask_wearing" in event.protective_measures_used:
            risk_score -= 0.15
        if "physical_distancing" in event.protective_measures_used:
            risk_score -= 0.1
        
        # Classify risk
        risk_score = max(0.0, min(1.0, risk_score))
        
        if risk_score >= 0.8:
            return ExposureRisk.HIGH_RISK
        elif risk_score >= 0.6:
            return ExposureRisk.MEDIUM_RISK
        elif risk_score >= 0.3:
            return ExposureRisk.LOW_RISK
        else:
            return ExposureRisk.MINIMAL_RISK
    
    def _calculate_transmission_probability(self, event: ExposureEvent) -> float:
        """Calculate transmission probability based on exposure characteristics."""
        
        base_probability = 0.1  # 10% base transmission probability
        
        # Adjust by contact type
        contact_multipliers = {
            ContactType.HOUSEHOLD: 3.0,
            ContactType.CLOSE_CONTACT: 2.0,
            ContactType.WORKPLACE: 1.5,
            ContactType.HEALTHCARE: 1.8,
            ContactType.CASUAL_CONTACT: 0.5,
            ContactType.COMMUNITY: 0.8,
            ContactType.TRAVEL: 1.2
        }
        
        probability = base_probability * contact_multipliers.get(event.contact_type, 1.0)
        
        # Adjust by duration
        if event.exposure_duration_minutes >= 240:  # 4+ hours
            probability *= 2.5
        elif event.exposure_duration_minutes >= 60:  # 1+ hours
            probability *= 1.8
        elif event.exposure_duration_minutes >= 15:  # 15+ minutes
            probability *= 1.3
        
        # Adjust by distance
        if event.distance_meters < 0.5:
            probability *= 2.0
        elif event.distance_meters < 1.0:
            probability *= 1.5
        elif event.distance_meters < 2.0:
            probability *= 1.2
        
        # Adjust by setting and ventilation
        if event.setting_type == "indoor" and event.ventilation_quality == "poor":
            probability *= 2.0
        elif event.setting_type == "outdoor":
            probability *= 0.2
        
        # Adjust by protective measures
        protection_factor = 1.0
        if "mask_wearing" in event.protective_measures_used:
            protection_factor *= 0.2
        if "physical_distancing" in event.protective_measures_used:
            protection_factor *= 0.5
        if "vaccination" in event.protective_measures_used:
            protection_factor *= 0.3
        
        probability *= protection_factor
        
        return min(1.0, probability)
    
    def _identify_risk_factors(self, event: ExposureEvent) -> List[str]:
        """Identify risk factors for transmission."""
        
        factors = []
        
        if event.exposure_duration_minutes >= 60:
            factors.append("Prolonged exposure duration")
        
        if event.distance_meters < 1.0:
            factors.append("Close physical proximity")
        
        if event.setting_type == "indoor" and event.ventilation_quality in ["poor", "moderate"]:
            factors.append("Indoor setting with poor ventilation")
        
        if event.contact_type == ContactType.HOUSEHOLD:
            factors.append("Household contact")
        
        if "coughing" in event.activity_description.lower():
            factors.append("Symptomatic case during exposure")
        
        if not event.protective_measures_used:
            factors.append("No protective measures used")
        
        return factors
    
    def _identify_protective_factors(self, event: ExposureEvent) -> List[str]:
        """Identify protective factors against transmission."""
        
        factors = []
        
        if event.setting_type == "outdoor":
            factors.append("Outdoor setting")
        
        if event.ventilation_quality in ["good", "excellent"]:
            factors.append("Good ventilation")
        
        if event.distance_meters >= 2.0:
            factors.append("Physical distancing maintained")
        
        if "mask_wearing" in event.protective_measures_used:
            factors.append("Mask wearing")
        
        if "vaccination" in event.protective_measures_used:
            factors.append("Vaccination protection")
        
        if event.exposure_duration_minutes < 15:
            factors.append("Brief exposure duration")
        
        return factors
    
    def _assign_contact_tracer(self) -> Optional[ContactTracer]:
        """Assign contact to available tracer with lowest caseload."""
        
        if not self.contact_tracers:
            return None
        
        # Find tracer with lowest active caseload
        available_tracers = [(tracer.active_caseload, tracer) for tracer in self.contact_tracers.values()]
        available_tracers.sort(key=lambda x: x[0])
        
        return available_tracers[0][1] if available_tracers else None
    
    def update_contact_status(self, contact_id: str, new_status: ContactStatus,
                            status_details: Dict[str, Any] = None):
        """Update contact monitoring status."""
        
        if contact_id not in self.contact_records:
            return False
        
        contact = self.contact_records[contact_id]
        old_status = contact.contact_status
        contact.contact_status = new_status
        
        # Update status-specific fields
        now = datetime.now()
        
        if new_status == ContactStatus.NOTIFIED and old_status == ContactStatus.IDENTIFIED:
            contact.notification_date = now
        elif new_status == ContactStatus.MONITORING:
            contact.monitoring_start_date = now
            # Set monitoring end date (14 days from last exposure)
            if contact.last_exposure_date:
                contact.monitoring_end_date = contact.last_exposure_date + timedelta(days=14)
        elif new_status == ContactStatus.QUARANTINED:
            contact.quarantine_start_date = now
            # Set quarantine end date
            if contact.last_exposure_date:
                contact.quarantine_end_date = contact.last_exposure_date + timedelta(days=14)
        elif new_status == ContactStatus.BECAME_CASE:
            contact.became_case = True
            contact.case_conversion_date = now
            if status_details and "symptom_onset" in status_details:
                contact.symptom_onset_date = status_details["symptom_onset"]
        
        # Update tracer metrics
        if new_status == ContactStatus.CLEARED or new_status == ContactStatus.BECAME_CASE:
            # Find assigned tracer and update metrics
            for tracer in self.contact_tracers.values():
                if tracer.active_caseload > 0:
                    tracer.active_caseload -= 1
                    tracer.contacts_completed += 1
                    break
        
        logger.info(f"Contact status updated: {contact_id} -> {new_status.value}")
        
        return True
    
    def add_symptom_monitoring(self, contact_id: str, symptoms: List[str], 
                             temperature: float = None):
        """Add symptom monitoring data for contact."""
        
        if contact_id not in self.contact_records:
            return False
        
        contact = self.contact_records[contact_id]
        
        # Add symptoms
        if symptoms:
            contact.symptoms_reported.extend(symptoms)
            if not contact.symptom_onset_date:
                contact.symptom_onset_date = datetime.now()
        
        # Add temperature reading
        if temperature:
            contact.temperature_readings.append((datetime.now(), temperature))
        
        # Update compliance tracking
        contact.successful_check_ins += 1
        
        return True
    
    def create_transmission_chain(self, index_case_id: str) -> TransmissionChain:
        """Create new transmission chain starting from index case."""
        
        chain_id = f"CHAIN_{random.randint(100000, 999999)}"
        
        chain = TransmissionChain(
            chain_id=chain_id,
            index_case_id=index_case_id,
            chain_start_date=datetime.now()
        )
        
        chain.confirmed_cases.append(index_case_id)
        chain.generation_levels[index_case_id] = 0  # Index case is generation 0
        
        self.transmission_chains[chain_id] = chain
        
        logger.info(f"Transmission chain created: {chain_id}")
        
        return chain
    
    def analyze_transmission_chain(self, chain_id: str) -> Dict[str, Any]:
        """Analyze transmission chain characteristics."""
        
        if chain_id not in self.transmission_chains:
            return {}
        
        chain = self.transmission_chains[chain_id]
        
        # Find related contacts who became cases
        related_contacts = []
        for contact in self.contact_records.values():
            if contact.case_id in chain.confirmed_cases and contact.became_case:
                related_contacts.append(contact)
                if contact.contact_id not in chain.confirmed_cases:
                    chain.confirmed_cases.append(contact.contact_id)
                    chain.total_cases += 1
                    # Set generation level (one higher than source case)
                    source_generation = chain.generation_levels.get(contact.case_id, 0)
                    chain.generation_levels[contact.contact_id] = source_generation + 1
        
        # Calculate chain metrics
        total_contacts = len([c for c in self.contact_records.values() 
                            if c.case_id in chain.confirmed_cases])
        
        if total_contacts > 0:
            chain.attack_rate = len(related_contacts) / total_contacts
        
        # Calculate serial interval (time between generations)
        if len(related_contacts) > 0:
            serial_intervals = []
            for contact in related_contacts:
                if (contact.symptom_onset_date and contact.first_exposure_date):
                    interval = (contact.symptom_onset_date - contact.first_exposure_date).days
                    if interval > 0:
                        serial_intervals.append(interval)
            
            if serial_intervals:
                chain.serial_interval_days = statistics.mean(serial_intervals)
        
        # Identify locations and settings
        locations = set()
        settings = set()
        for event in self.exposure_events:
            if event.case_id in chain.confirmed_cases:
                locations.add(event.exposure_location)
                settings.add(event.setting_type)
        
        chain.locations_involved = list(locations)
        chain.settings_involved = list(settings)
        
        # Calculate reproduction number for this chain
        generations = list(chain.generation_levels.values())
        if len(set(generations)) > 1:  # Multiple generations exist
            gen_counts = defaultdict(int)
            for gen in generations:
                gen_counts[gen] += 1
            
            # Simple R calculation: average cases per generation
            if len(gen_counts) > 1:
                reproductive_events = []
                for gen in sorted(gen_counts.keys())[:-1]:  # Exclude final generation
                    if gen_counts[gen] > 0:
                        reproductive_events.append(gen_counts[gen + 1] / gen_counts[gen])
                
                if reproductive_events:
                    chain.reproduction_number = statistics.mean(reproductive_events)
        
        # Identify super-spreader events
        case_contact_counts = defaultdict(int)
        for contact in self.contact_records.values():
            if contact.case_id in chain.confirmed_cases:
                case_contact_counts[contact.case_id] += 1
        
        # Cases with >5 contacts might be super-spreaders
        for case_id, contact_count in case_contact_counts.items():
            if contact_count >= 5:
                chain.super_spreader_events.append(f"Case {case_id}: {contact_count} contacts")
        
        return {
            "chain_id": chain_id,
            "total_cases": chain.total_cases,
            "attack_rate": chain.attack_rate,
            "serial_interval": chain.serial_interval_days,
            "reproduction_number": chain.reproduction_number,
            "generations": max(chain.generation_levels.values()) + 1 if chain.generation_levels else 1,
            "locations_involved": len(chain.locations_involved),
            "super_spreader_events": len(chain.super_spreader_events),
            "analysis_date": datetime.now()
        }
    
    def get_contact_tracing_summary(self) -> Dict[str, Any]:
        """Get comprehensive contact tracing summary."""
        
        # Contact statistics
        contact_stats = {
            "total_contacts": len(self.contact_records),
            "contacts_by_status": defaultdict(int),
            "contacts_by_risk": defaultdict(int)
        }
        
        for contact in self.contact_records.values():
            contact_stats["contacts_by_status"][contact.contact_status.value] += 1
            contact_stats["contacts_by_risk"][contact.highest_risk_exposure.value] += 1
        
        # Conversion and follow-up statistics
        converted_contacts = [c for c in self.contact_records.values() if c.became_case]
        monitoring_contacts = [c for c in self.contact_records.values() 
                             if c.contact_status == ContactStatus.MONITORING]
        
        conversion_stats = {
            "contacts_became_cases": len(converted_contacts),
            "conversion_rate": len(converted_contacts) / len(self.contact_records) if self.contact_records else 0,
            "contacts_under_monitoring": len(monitoring_contacts)
        }
        
        # Exposure analysis
        if self.exposure_events:
            avg_transmission_prob = statistics.mean(e.transmission_probability for e in self.exposure_events)
            high_risk_exposures = len([e for e in self.exposure_events 
                                     if e.exposure_risk == ExposureRisk.HIGH_RISK])
        else:
            avg_transmission_prob = 0.0
            high_risk_exposures = 0
        
        exposure_stats = {
            "total_exposure_events": len(self.exposure_events),
            "average_transmission_probability": avg_transmission_prob,
            "high_risk_exposures": high_risk_exposures,
            "exposure_settings": list(set(e.setting_type for e in self.exposure_events))
        }
        
        # Transmission chain analysis
        chain_stats = {
            "total_chains": len(self.transmission_chains),
            "active_chains": len([c for c in self.transmission_chains.values() if c.is_active]),
            "average_chain_size": statistics.mean([c.total_cases for c in self.transmission_chains.values()]) 
                                 if self.transmission_chains else 0
        }
        
        # Tracer performance
        tracer_performance = {
            "total_tracers": len(self.contact_tracers),
            "average_caseload": statistics.mean([t.active_caseload for t in self.contact_tracers.values()]) 
                               if self.contact_tracers else 0,
            "total_contacts_assigned": sum(t.contacts_assigned for t in self.contact_tracers.values()),
            "average_completion_time": statistics.mean([t.average_completion_time_hours 
                                                      for t in self.contact_tracers.values()]) 
                                      if self.contact_tracers else 0,
            "average_quality_score": statistics.mean([t.quality_score for t in self.contact_tracers.values()]) 
                                    if self.contact_tracers else 0
        }
        
        return {
            "contact_statistics": dict(contact_stats),
            "conversion_statistics": conversion_stats,
            "exposure_analysis": exposure_stats,
            "transmission_chains": chain_stats,
            "tracer_performance": tracer_performance
        }

def run_demonstration() -> ContactTracingManager:
    """Run comprehensive contact tracing demonstration."""
    
    print("🔍 One Health Contact Tracing System - Demonstration")
    print("=" * 70)
    
    manager = ContactTracingManager()
    
    # Simulate outbreak scenario with multiple cases and contacts
    case_scenarios = [
        {
            "case_id": "CASE_001",
            "case_name": "Index Case - Healthcare Worker",
            "contacts": [
                {
                    "info": {"first_name": "John", "last_name": "Smith", "age": 45, "phone_numbers": ["555-1234"]},
                    "exposure": {"contact_type": "workplace", "duration_minutes": 120, "distance_meters": 1.0, 
                               "setting": "indoor", "ventilation": "moderate", "protective_measures": ["mask_wearing"]}
                },
                {
                    "info": {"first_name": "Maria", "last_name": "Garcia", "age": 32, "phone_numbers": ["555-5678"]},
                    "exposure": {"contact_type": "household", "duration_minutes": 480, "distance_meters": 0.5,
                               "setting": "indoor", "ventilation": "poor", "protective_measures": []}
                },
                {
                    "info": {"first_name": "David", "last_name": "Lee", "age": 28, "phone_numbers": ["555-9012"]},
                    "exposure": {"contact_type": "close_contact", "duration_minutes": 45, "distance_meters": 1.5,
                               "setting": "indoor", "ventilation": "good", "protective_measures": ["mask_wearing", "physical_distancing"]}
                }
            ]
        },
        {
            "case_id": "CASE_002", 
            "case_name": "Secondary Case - Community Member",
            "contacts": [
                {
                    "info": {"first_name": "Sarah", "last_name": "Johnson", "age": 35, "phone_numbers": ["555-3456"]},
                    "exposure": {"contact_type": "community", "duration_minutes": 90, "distance_meters": 1.8,
                               "setting": "indoor", "ventilation": "poor", "protective_measures": []}
                },
                {
                    "info": {"first_name": "Mike", "last_name": "Chen", "age": 42, "phone_numbers": ["555-7890"]},
                    "exposure": {"contact_type": "travel", "duration_minutes": 180, "distance_meters": 1.0,
                               "setting": "vehicle", "ventilation": "poor", "protective_measures": []}
                }
            ]
        }
    ]
    
    print(f"\n🔍 Contact Tracing Scenarios:")
    for scenario in case_scenarios:
        print(f"  {scenario['case_id']}: {scenario['case_name']}")
        print(f"    Contacts to trace: {len(scenario['contacts'])}")
    
    print(f"\n🔍 Creating Contact Records...")
    
    # Create contact records
    all_contacts = []
    for scenario in case_scenarios:
        for contact_data in scenario["contacts"]:
            contact = manager.create_contact_record(
                case_id=scenario["case_id"],
                contact_info=contact_data["info"],
                exposure_details=contact_data["exposure"]
            )
            all_contacts.append(contact)
            risk_level = contact.highest_risk_exposure.value.replace("_", " ").title()
            transmission_prob = max(contact.exposure_events[0].transmission_probability * 100 if contact.exposure_events else 0, 0)
            print(f"  ✅ {contact.first_name} {contact.last_name}: {risk_level} Risk ({transmission_prob:.1f}% transmission probability)")
    
    print(f"\n📞 Simulating Contact Notification and Monitoring...")
    
    # Simulate contact tracing process
    for contact in all_contacts:
        # Notification
        manager.update_contact_status(contact.contact_id, ContactStatus.NOTIFIED)
        
        # Begin monitoring
        manager.update_contact_status(contact.contact_id, ContactStatus.MONITORING)
        
        # Simulate daily monitoring for high-risk contacts
        if contact.highest_risk_exposure in [ExposureRisk.HIGH_RISK, ExposureRisk.MEDIUM_RISK]:
            # Simulate 5-10 days of monitoring
            monitoring_days = random.randint(5, 10)
            for day in range(monitoring_days):
                # Random symptoms
                symptoms = []
                if random.random() < 0.1:  # 10% chance of symptoms each day
                    possible_symptoms = ["fever", "cough", "fatigue", "headache", "sore throat"]
                    symptoms = random.sample(possible_symptoms, random.randint(1, 3))
                
                # Random temperature
                temperature = random.uniform(97.5, 99.8)  # Normal range, occasionally elevated
                if symptoms:
                    temperature += random.uniform(1.0, 3.0)  # Fever if symptomatic
                
                manager.add_symptom_monitoring(contact.contact_id, symptoms, temperature)
        
        # Simulate outcome - some contacts may become cases
        if contact.highest_risk_exposure == ExposureRisk.HIGH_RISK:
            if random.random() < 0.15:  # 15% conversion rate for high-risk
                manager.update_contact_status(contact.contact_id, ContactStatus.BECAME_CASE, 
                                            {"symptom_onset": datetime.now() - timedelta(days=random.randint(1, 3))})
            else:
                manager.update_contact_status(contact.contact_id, ContactStatus.CLEARED)
        elif contact.highest_risk_exposure == ExposureRisk.MEDIUM_RISK:
            if random.random() < 0.08:  # 8% conversion rate for medium-risk
                manager.update_contact_status(contact.contact_id, ContactStatus.BECAME_CASE,
                                            {"symptom_onset": datetime.now() - timedelta(days=random.randint(1, 3))})
            else:
                manager.update_contact_status(contact.contact_id, ContactStatus.CLEARED)
        else:
            manager.update_contact_status(contact.contact_id, ContactStatus.CLEARED)
    
    print(f"\n🔗 Creating and Analyzing Transmission Chains...")
    
    # Create transmission chains
    chains = []
    for scenario in case_scenarios:
        chain = manager.create_transmission_chain(scenario["case_id"])
        analysis = manager.analyze_transmission_chain(chain.chain_id)
        chains.append((chain, analysis))
        
        print(f"  🔗 Chain {chain.chain_id}: {analysis['total_cases']} cases, "
              f"{analysis['attack_rate']:.1%} attack rate, "
              f"R = {analysis['reproduction_number']:.2f}")
    
    return manager

def display_contact_tracing_results(manager: ContactTracingManager):
    """Display comprehensive contact tracing results."""
    
    contacts = list(manager.contact_records.values())
    
    print(f"\n🔍 Contact Tracing Results ({len(contacts)} contacts):")
    
    for i, contact in enumerate(contacts, 1):
        print(f"\n{i}. {contact.first_name} {contact.last_name}")
        print(f"   Source Case: {contact.case_id}")
        print(f"   Risk Level: {contact.highest_risk_exposure.value.replace('_', ' ').title()}")
        print(f"   Status: {contact.contact_status.value.replace('_', ' ').title()}")
        print(f"   Total Exposure Time: {contact.total_exposure_time_minutes} minutes")
        
        if contact.exposure_events:
            event = contact.exposure_events[0]  # First/primary exposure
            print(f"   Transmission Probability: {event.transmission_probability:.1%}")
            print(f"   Exposure Setting: {event.setting_type.title()}")
            print(f"   Contact Type: {event.contact_type.value.replace('_', ' ').title()}")
        
        if contact.became_case:
            print(f"   ⚠️ BECAME CASE on {contact.case_conversion_date.strftime('%Y-%m-%d') if contact.case_conversion_date else 'Unknown'}")
        
        if contact.symptoms_reported:
            print(f"   Symptoms: {', '.join(contact.symptoms_reported[:3])}")
        
        print(f"   Check-ins: {contact.successful_check_ins} successful")
    
    # Summary statistics
    summary = manager.get_contact_tracing_summary()
    
    print(f"\n📊 Contact Tracing Summary:")
    print(f"  Total Contacts: {summary['contact_statistics']['total_contacts']}")
    
    print(f"\n📈 Contact Status Distribution:")
    for status, count in summary["contact_statistics"]["contacts_by_status"].items():
        print(f"  {status.replace('_', ' ').title()}: {count}")
    
    print(f"\n⚠️ Risk Level Distribution:")
    for risk, count in summary["contact_statistics"]["contacts_by_risk"].items():
        print(f"  {risk.replace('_', ' ').title()}: {count}")
    
    print(f"\n📈 Conversion Statistics:")
    conv = summary["conversion_statistics"]
    print(f"  Contacts Became Cases: {conv['contacts_became_cases']}")
    print(f"  Conversion Rate: {conv['conversion_rate']:.1%}")
    print(f"  Under Monitoring: {conv['contacts_under_monitoring']}")
    
    print(f"\n🔬 Exposure Analysis:")
    exp = summary["exposure_analysis"]
    print(f"  Total Exposure Events: {exp['total_exposure_events']}")
    print(f"  Average Transmission Probability: {exp['average_transmission_probability']:.1%}")
    print(f"  High-Risk Exposures: {exp['high_risk_exposures']}")
    print(f"  Exposure Settings: {', '.join(exp['exposure_settings'])}")
    
    print(f"\n🔗 Transmission Chains:")
    chains = summary["transmission_chains"]
    print(f"  Total Chains: {chains['total_chains']}")
    print(f"  Active Chains: {chains['active_chains']}")
    print(f"  Average Chain Size: {chains['average_chain_size']:.1f} cases")
    
    print(f"\n👥 Contact Tracer Performance:")
    tracer = summary["tracer_performance"]
    print(f"  Total Tracers: {tracer['total_tracers']}")
    print(f"  Average Caseload: {tracer['average_caseload']:.1f}")
    print(f"  Total Contacts Assigned: {tracer['total_contacts_assigned']}")
    print(f"  Average Completion Time: {tracer['average_completion_time']:.1f} hours")
    print(f"  Average Quality Score: {tracer['average_quality_score']:.1%}")
    
    # Show transmission chains details
    print(f"\n🔗 Transmission Chain Details:")
    for chain_id, chain in manager.transmission_chains.items():
        analysis = manager.analyze_transmission_chain(chain_id)
        print(f"  {chain_id}:")
        print(f"    Cases: {analysis['total_cases']}")
        print(f"    Attack Rate: {analysis['attack_rate']:.1%}")
        print(f"    Generations: {analysis['generations']}")
        print(f"    R Number: {analysis['reproduction_number']:.2f}")
        if analysis['super_spreader_events'] > 0:
            print(f"    Super-spreader Events: {analysis['super_spreader_events']}")
    
    print(f"\n🏆 TOP PERFORMING Tracers:")
    top_tracers = sorted(manager.contact_tracers.values(), 
                        key=lambda t: t.quality_score, reverse=True)[:3]
    for i, tracer in enumerate(top_tracers, 1):
        print(f"  {i}. {tracer.tracer_name}")
        print(f"     Quality Score: {tracer.quality_score:.1%}")
        print(f"     Contacts Assigned: {tracer.contacts_assigned}")
        print(f"     Completion Time: {tracer.average_completion_time_hours:.1f} hours")

if __name__ == "__main__":
    # Run comprehensive demonstration
    contact_tracing_manager = run_demonstration()
    display_contact_tracing_results(contact_tracing_manager)
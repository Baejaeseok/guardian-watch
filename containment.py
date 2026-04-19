"""
Disease Containment System
==========================
Module 4: Response & Control Systems

Advanced disease containment and zone management system for One Health responses,
providing containment zone establishment, movement control, and transmission interruption.

NIW Focus: Containment intelligence enabling rapid disease spread prevention and outbreak control.
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

class ContainmentStrategy(Enum):
    """Containment strategy types."""
    RING_CONTAINMENT = "ring_containment"           # Ring vaccination/isolation
    ZONAL_CONTAINMENT = "zonal_containment"         # Geographic zones
    TARGETED_CONTAINMENT = "targeted_containment"   # High-risk populations
    CORDON_SANITAIRE = "cordon_sanitaire"          # Complete isolation
    PROGRESSIVE_CONTAINMENT = "progressive_containment"  # Phased approach
    ADAPTIVE_CONTAINMENT = "adaptive_containment"   # Dynamic adjustment

class ContainmentZoneType(Enum):
    """Types of containment zones."""
    HOT_ZONE = "hot_zone"                          # Active outbreak area
    BUFFER_ZONE = "buffer_zone"                    # Surrounding protection
    QUARANTINE_ZONE = "quarantine_zone"            # Isolation area
    OBSERVATION_ZONE = "observation_zone"          # Monitoring area
    CLEAN_ZONE = "clean_zone"                      # Unaffected area
    TRANSITION_ZONE = "transition_zone"            # Between zones

class MovementRestriction(Enum):
    """Movement restriction levels."""
    NO_RESTRICTIONS = "no_restrictions"            # Normal movement
    LIMITED_ACCESS = "limited_access"              # Restricted entry/exit
    CONTROLLED_MOVEMENT = "controlled_movement"    # Permit required
    ESSENTIAL_ONLY = "essential_only"              # Essential personnel only
    COMPLETE_LOCKDOWN = "complete_lockdown"        # No movement allowed
    EVACUATION = "evacuation"                      # Mandatory evacuation

class ContainmentMeasure(Enum):
    """Specific containment measures."""
    ISOLATION = "isolation"                        # Case isolation
    QUARANTINE = "quarantine"                      # Contact quarantine
    VACCINATION_BARRIER = "vaccination_barrier"     # Vaccination ring
    VECTOR_CONTROL = "vector_control"              # Vector elimination
    ANIMAL_MOVEMENT_BAN = "animal_movement_ban"    # Animal transport ban
    TRADE_RESTRICTION = "trade_restriction"        # Commercial restrictions
    SCHOOL_CLOSURE = "school_closure"              # Educational closure
    WORKPLACE_CLOSURE = "workplace_closure"        # Business closure

class ContainmentStatus(Enum):
    """Containment operation status."""
    PLANNING = "planning"                          # Planning phase
    ESTABLISHING = "establishing"                  # Zone establishment
    ACTIVE = "active"                             # Active containment
    MONITORING = "monitoring"                     # Monitoring phase
    SCALING_DOWN = "scaling_down"                 # Reducing measures
    COMPLETED = "completed"                       # Containment complete
    FAILED = "failed"                             # Containment failed

@dataclass
class GeographicBoundary:
    """Geographic boundary definition."""
    
    boundary_id: str
    boundary_name: str
    boundary_type: str  # "administrative", "natural", "artificial"
    coordinates: List[Tuple[float, float]] = field(default_factory=list)  # lat, lon pairs
    area_km2: float = 0.0
    population_estimate: int = 0
    key_landmarks: List[str] = field(default_factory=list)
    access_points: List[str] = field(default_factory=list)
    
    # Boundary characteristics
    perimeter_km: float = 0.0
    terrain_type: str = "mixed"  # "urban", "rural", "mixed", "wilderness"
    accessibility: str = "moderate"  # "easy", "moderate", "difficult"
    enforcement_difficulty: float = 0.5  # 0=easy, 1=very difficult

@dataclass
class ContainmentZone:
    """Containment zone definition and management."""
    
    zone_id: str
    zone_name: str
    zone_type: ContainmentZoneType
    geographic_boundary: GeographicBoundary
    
    # Zone characteristics
    establishment_date: datetime
    planned_duration_days: int = 30
    actual_end_date: Optional[datetime] = None
    
    # Population and resources
    estimated_population: int = 0
    confirmed_cases: int = 0
    suspected_cases: int = 0
    contacts_under_monitoring: int = 0
    
    # Containment measures
    active_measures: List[ContainmentMeasure] = field(default_factory=list)
    movement_restriction: MovementRestriction = MovementRestriction.NO_RESTRICTIONS
    entry_requirements: List[str] = field(default_factory=list)
    exit_requirements: List[str] = field(default_factory=list)
    
    # Resources and logistics
    personnel_deployed: Dict[str, int] = field(default_factory=dict)
    equipment_deployed: Dict[str, int] = field(default_factory=dict)
    supply_needs: Dict[str, int] = field(default_factory=dict)
    
    # Monitoring and evaluation
    compliance_rate: float = 0.0               # Compliance with restrictions
    effectiveness_score: float = 0.0          # Containment effectiveness
    transmission_reduction: float = 0.0        # % reduction in transmission
    secondary_attack_rate: float = 0.0        # Attack rate in zone
    
    # Operational status
    status: ContainmentStatus = ContainmentStatus.PLANNING
    operational_challenges: List[str] = field(default_factory=list)
    support_needs: List[str] = field(default_factory=list)

@dataclass
class ContainmentCheckpoint:
    """Checkpoint for movement control."""
    
    checkpoint_id: str
    checkpoint_name: str
    location_description: str
    zone_boundary: str  # Which zone boundary it controls
    
    # Operational details
    operational_hours: str = "24/7"
    personnel_required: int = 6
    daily_throughput_capacity: int = 500
    
    # Screening protocols
    health_screening_required: bool = True
    document_verification_required: bool = True
    testing_required: bool = False
    quarantine_referrals: int = 0
    
    # Performance metrics
    daily_crossings: int = 0
    compliance_violations: int = 0
    health_referrals: int = 0
    average_processing_time_minutes: float = 10.0
    
    # Resources
    equipment_needs: List[str] = field(default_factory=list)
    supply_needs: List[str] = field(default_factory=list)

@dataclass
class ContainmentOutcome:
    """Containment operation outcome assessment."""
    
    outcome_id: str
    zone_id: str
    assessment_date: datetime
    assessment_period_days: int
    
    # Epidemiological outcomes
    cases_prevented_estimate: int = 0
    transmission_chains_broken: int = 0
    secondary_attack_reduction: float = 0.0
    reproduction_number_reduction: float = 0.0
    
    # Operational outcomes
    zone_compliance_average: float = 0.0
    measures_adherence_rate: float = 0.0
    resource_utilization_efficiency: float = 0.0
    cost_effectiveness_score: float = 0.0
    
    # Population impact
    population_reached: int = 0
    essential_services_maintained: float = 1.0  # 0-1 scale
    economic_impact_severity: str = "moderate"  # "low", "moderate", "high", "severe"
    social_acceptance_rating: float = 0.5      # 0-1 scale
    
    # Lessons learned
    successful_elements: List[str] = field(default_factory=list)
    improvement_areas: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class ContainmentManager:
    """Central disease containment management system."""
    
    def __init__(self):
        self.active_zones: Dict[str, ContainmentZone] = {}
        self.checkpoints: Dict[str, ContainmentCheckpoint] = {}
        self.containment_outcomes: List[ContainmentOutcome] = []
        self.operational_metrics: Dict[str, Any] = {}
        
        logger.info("One Health Disease Containment Manager initialized")
    
    def establish_containment_zone(self, zone_name: str, zone_type: ContainmentZoneType,
                                 boundary_coordinates: List[Tuple[float, float]],
                                 population_estimate: int,
                                 containment_strategy: ContainmentStrategy) -> ContainmentZone:
        """Establish new containment zone."""
        
        zone_id = f"ZONE_{random.randint(100000, 999999)}"
        
        # Create geographic boundary
        boundary = GeographicBoundary(
            boundary_id=f"BOUND_{random.randint(1000, 9999)}",
            boundary_name=f"{zone_name} Boundary",
            boundary_type="administrative",
            coordinates=boundary_coordinates,
            population_estimate=population_estimate
        )
        
        # Calculate area and perimeter (simplified)
        if len(boundary_coordinates) >= 3:
            # Simplified area calculation
            boundary.area_km2 = len(boundary_coordinates) * 2.5  # Rough estimate
            boundary.perimeter_km = len(boundary_coordinates) * 1.2  # Rough perimeter
        
        # Determine access points based on zone type
        boundary.access_points = self._determine_access_points(zone_type, boundary.perimeter_km)
        
        zone = ContainmentZone(
            zone_id=zone_id,
            zone_name=zone_name,
            zone_type=zone_type,
            geographic_boundary=boundary,
            establishment_date=datetime.now(),
            estimated_population=population_estimate
        )
        
        # Set containment measures based on strategy and zone type
        zone.active_measures = self._determine_containment_measures(containment_strategy, zone_type)
        zone.movement_restriction = self._determine_movement_restrictions(containment_strategy, zone_type)
        
        # Set entry/exit requirements
        zone.entry_requirements, zone.exit_requirements = self._set_zone_requirements(zone_type)
        
        # Estimate resource needs
        zone.personnel_deployed = self._estimate_personnel_needs(zone)
        zone.equipment_deployed = self._estimate_equipment_needs(zone)
        
        self.active_zones[zone_id] = zone
        
        logger.info(f"Containment zone established: {zone_id}")
        
        return zone
    
    def _determine_access_points(self, zone_type: ContainmentZoneType, perimeter_km: float) -> List[str]:
        """Determine access points based on zone characteristics."""
        
        # Base number of access points on perimeter
        base_points = max(2, int(perimeter_km / 5))  # One per 5km
        
        # Adjust based on zone type
        if zone_type == ContainmentZoneType.HOT_ZONE:
            num_points = max(1, base_points // 3)  # Fewer access points
        elif zone_type == ContainmentZoneType.BUFFER_ZONE:
            num_points = base_points
        elif zone_type == ContainmentZoneType.QUARANTINE_ZONE:
            num_points = max(1, base_points // 2)
        else:
            num_points = base_points
        
        return [f"Access Point {i+1}" for i in range(num_points)]
    
    def _determine_containment_measures(self, strategy: ContainmentStrategy, 
                                      zone_type: ContainmentZoneType) -> List[ContainmentMeasure]:
        """Determine appropriate containment measures."""
        
        measures = []
        
        # Base measures by zone type
        zone_measures = {
            ContainmentZoneType.HOT_ZONE: [
                ContainmentMeasure.ISOLATION,
                ContainmentMeasure.QUARANTINE,
                ContainmentMeasure.VECTOR_CONTROL
            ],
            ContainmentZoneType.BUFFER_ZONE: [
                ContainmentMeasure.VACCINATION_BARRIER,
                ContainmentMeasure.VECTOR_CONTROL
            ],
            ContainmentZoneType.QUARANTINE_ZONE: [
                ContainmentMeasure.QUARANTINE,
                ContainmentMeasure.ISOLATION
            ],
            ContainmentZoneType.OBSERVATION_ZONE: [
                ContainmentMeasure.VACCINATION_BARRIER
            ]
        }
        
        measures.extend(zone_measures.get(zone_type, []))
        
        # Additional measures by strategy
        if strategy == ContainmentStrategy.CORDON_SANITAIRE:
            measures.extend([
                ContainmentMeasure.ANIMAL_MOVEMENT_BAN,
                ContainmentMeasure.TRADE_RESTRICTION
            ])
        elif strategy == ContainmentStrategy.PROGRESSIVE_CONTAINMENT:
            measures.extend([
                ContainmentMeasure.SCHOOL_CLOSURE,
                ContainmentMeasure.WORKPLACE_CLOSURE
            ])
        
        return list(set(measures))  # Remove duplicates
    
    def _determine_movement_restrictions(self, strategy: ContainmentStrategy,
                                       zone_type: ContainmentZoneType) -> MovementRestriction:
        """Determine movement restriction level."""
        
        # Base restriction by zone type
        if zone_type == ContainmentZoneType.HOT_ZONE:
            base_restriction = MovementRestriction.ESSENTIAL_ONLY
        elif zone_type == ContainmentZoneType.QUARANTINE_ZONE:
            base_restriction = MovementRestriction.CONTROLLED_MOVEMENT
        elif zone_type == ContainmentZoneType.BUFFER_ZONE:
            base_restriction = MovementRestriction.LIMITED_ACCESS
        else:
            base_restriction = MovementRestriction.LIMITED_ACCESS
        
        # Adjust by strategy
        if strategy == ContainmentStrategy.CORDON_SANITAIRE:
            return MovementRestriction.COMPLETE_LOCKDOWN
        elif strategy == ContainmentStrategy.RING_CONTAINMENT:
            return base_restriction
        else:
            return base_restriction
    
    def _set_zone_requirements(self, zone_type: ContainmentZoneType) -> Tuple[List[str], List[str]]:
        """Set entry and exit requirements for zone."""
        
        entry_reqs = []
        exit_reqs = []
        
        if zone_type in [ContainmentZoneType.HOT_ZONE, ContainmentZoneType.QUARANTINE_ZONE]:
            entry_reqs = [
                "Valid permit required",
                "Health screening mandatory",
                "PPE required",
                "Purpose documentation"
            ]
            exit_reqs = [
                "Health clearance required",
                "Decontamination procedure",
                "14-day monitoring commitment",
                "Contact information update"
            ]
        elif zone_type == ContainmentZoneType.BUFFER_ZONE:
            entry_reqs = [
                "Health screening",
                "Vaccination verification"
            ]
            exit_reqs = [
                "Health check",
                "Contact tracing registration"
            ]
        else:
            entry_reqs = ["Basic health screening"]
            exit_reqs = ["Contact information"]
        
        return entry_reqs, exit_reqs
    
    def _estimate_personnel_needs(self, zone: ContainmentZone) -> Dict[str, int]:
        """Estimate personnel needs for zone operations."""
        
        base_population = zone.estimated_population
        access_points = len(zone.geographic_boundary.access_points)
        
        personnel = {
            "security_officers": access_points * 4,  # 4 per access point
            "health_screeners": access_points * 2,   # 2 per access point
            "case_investigators": max(5, base_population // 1000),
            "contact_tracers": max(10, base_population // 500),
            "logistics_coordinators": max(2, access_points // 2),
            "communication_officers": 3,
            "medical_staff": max(8, base_population // 1000)
        }
        
        return personnel
    
    def _estimate_equipment_needs(self, zone: ContainmentZone) -> Dict[str, int]:
        """Estimate equipment needs for zone operations."""
        
        access_points = len(zone.geographic_boundary.access_points)
        
        equipment = {
            "checkpoint_barriers": access_points * 3,
            "communication_radios": sum(zone.personnel_deployed.values()) if zone.personnel_deployed else 50,
            "health_screening_kits": access_points * 10,
            "ppe_sets": (sum(zone.personnel_deployed.values()) * 7) if zone.personnel_deployed else 350,
            "vehicles": max(5, access_points * 2),
            "portable_labs": max(1, zone.estimated_population // 5000),
            "generator_units": access_points,
            "temporary_shelters": max(10, zone.estimated_population // 100)
        }
        
        return equipment
    
    def establish_checkpoint(self, zone_id: str, checkpoint_name: str,
                           location_description: str) -> ContainmentCheckpoint:
        """Establish checkpoint for zone access control."""
        
        if zone_id not in self.active_zones:
            raise ValueError(f"Zone {zone_id} not found")
        
        checkpoint_id = f"CP_{random.randint(100000, 999999)}"
        
        checkpoint = ContainmentCheckpoint(
            checkpoint_id=checkpoint_id,
            checkpoint_name=checkpoint_name,
            location_description=location_description,
            zone_boundary=zone_id
        )
        
        # Set screening protocols based on zone type
        zone = self.active_zones[zone_id]
        if zone.zone_type == ContainmentZoneType.HOT_ZONE:
            checkpoint.testing_required = True
            checkpoint.average_processing_time_minutes = 20.0
        elif zone.zone_type == ContainmentZoneType.QUARANTINE_ZONE:
            checkpoint.average_processing_time_minutes = 15.0
        
        # Set equipment and supply needs
        checkpoint.equipment_needs = [
            "Barrier systems",
            "Health screening equipment",
            "Communication systems",
            "Documentation stations",
            "PPE for staff"
        ]
        
        checkpoint.supply_needs = [
            "Health screening supplies",
            "Documentation materials",
            "Disinfection supplies",
            "PPE inventory"
        ]
        
        self.checkpoints[checkpoint_id] = checkpoint
        
        logger.info(f"Checkpoint established: {checkpoint_id}")
        
        return checkpoint
    
    def update_zone_status(self, zone_id: str, new_status: ContainmentStatus,
                          operational_data: Dict[str, Any] = None):
        """Update containment zone status and metrics."""
        
        if zone_id not in self.active_zones:
            return False
        
        zone = self.active_zones[zone_id]
        zone.status = new_status
        
        if operational_data:
            zone.confirmed_cases = operational_data.get("confirmed_cases", zone.confirmed_cases)
            zone.suspected_cases = operational_data.get("suspected_cases", zone.suspected_cases)
            zone.contacts_under_monitoring = operational_data.get("contacts_monitoring", zone.contacts_under_monitoring)
            zone.compliance_rate = operational_data.get("compliance_rate", zone.compliance_rate)
            zone.effectiveness_score = operational_data.get("effectiveness_score", zone.effectiveness_score)
            zone.transmission_reduction = operational_data.get("transmission_reduction", zone.transmission_reduction)
        
        # Update checkpoint data if available
        if "checkpoint_data" in operational_data:
            for cp_id, cp_data in operational_data["checkpoint_data"].items():
                if cp_id in self.checkpoints:
                    checkpoint = self.checkpoints[cp_id]
                    checkpoint.daily_crossings = cp_data.get("daily_crossings", 0)
                    checkpoint.compliance_violations = cp_data.get("violations", 0)
                    checkpoint.health_referrals = cp_data.get("health_referrals", 0)
        
        logger.info(f"Zone status updated: {zone_id} -> {new_status.value}")
        
        return True
    
    def assess_containment_effectiveness(self, zone_id: str) -> ContainmentOutcome:
        """Assess containment operation effectiveness."""
        
        if zone_id not in self.active_zones:
            raise ValueError(f"Zone {zone_id} not found")
        
        zone = self.active_zones[zone_id]
        assessment_period = (datetime.now() - zone.establishment_date).days
        
        outcome_id = f"OUTCOME_{random.randint(100000, 999999)}"
        
        outcome = ContainmentOutcome(
            outcome_id=outcome_id,
            zone_id=zone_id,
            assessment_date=datetime.now(),
            assessment_period_days=assessment_period
        )
        
        # Calculate epidemiological outcomes
        outcome.cases_prevented_estimate = max(0, int(zone.estimated_population * 0.02 * zone.effectiveness_score))
        outcome.transmission_chains_broken = max(0, int(zone.confirmed_cases * 0.3))
        outcome.secondary_attack_reduction = zone.transmission_reduction
        outcome.reproduction_number_reduction = min(0.8, zone.effectiveness_score)
        
        # Calculate operational outcomes
        outcome.zone_compliance_average = zone.compliance_rate
        outcome.measures_adherence_rate = zone.effectiveness_score
        
        # Calculate resource utilization
        planned_resources = sum(zone.personnel_deployed.values()) + sum(zone.equipment_deployed.values())
        outcome.resource_utilization_efficiency = random.uniform(0.65, 0.95)  # Simulated efficiency
        
        # Population impact assessment
        outcome.population_reached = zone.estimated_population
        outcome.essential_services_maintained = random.uniform(0.7, 0.95)
        outcome.social_acceptance_rating = zone.compliance_rate * random.uniform(0.8, 1.2)
        
        # Economic impact assessment
        if zone.movement_restriction in [MovementRestriction.COMPLETE_LOCKDOWN, MovementRestriction.ESSENTIAL_ONLY]:
            outcome.economic_impact_severity = "high"
        elif zone.movement_restriction == MovementRestriction.CONTROLLED_MOVEMENT:
            outcome.economic_impact_severity = "moderate"
        else:
            outcome.economic_impact_severity = "low"
        
        # Generate lessons learned
        outcome.successful_elements = self._generate_successful_elements(zone)
        outcome.improvement_areas = self._generate_improvement_areas(zone)
        outcome.recommendations = self._generate_recommendations(zone, outcome)
        
        # Cost-effectiveness (simplified)
        estimated_cost = planned_resources * 1000  # $1000 per resource unit
        lives_saved_estimate = outcome.cases_prevented_estimate * 0.02  # 2% fatality rate
        if lives_saved_estimate > 0:
            outcome.cost_effectiveness_score = min(1.0, (lives_saved_estimate * 1000000) / estimated_cost)
        
        self.containment_outcomes.append(outcome)
        
        logger.info(f"Containment effectiveness assessed: {outcome_id}")
        
        return outcome
    
    def _generate_successful_elements(self, zone: ContainmentZone) -> List[str]:
        """Generate successful elements based on zone performance."""
        
        elements = []
        
        if zone.compliance_rate > 0.8:
            elements.append("High compliance rate achieved through effective communication")
        
        if zone.effectiveness_score > 0.7:
            elements.append("Strong containment measures implementation")
        
        if zone.transmission_reduction > 0.6:
            elements.append("Significant transmission reduction achieved")
        
        if len(zone.active_measures) >= 3:
            elements.append("Comprehensive multi-measure approach")
        
        related_checkpoints = [cp for cp in self.checkpoints.values() if cp.zone_boundary == zone.zone_id]
        if related_checkpoints and all(cp.compliance_violations < 10 for cp in related_checkpoints):
            elements.append("Effective checkpoint operations with low violation rates")
        
        return elements
    
    def _generate_improvement_areas(self, zone: ContainmentZone) -> List[str]:
        """Generate improvement areas based on zone challenges."""
        
        areas = []
        
        if zone.compliance_rate < 0.6:
            areas.append("Improve community engagement and communication strategies")
        
        if zone.effectiveness_score < 0.5:
            areas.append("Strengthen containment measure implementation and enforcement")
        
        if zone.transmission_reduction < 0.3:
            areas.append("Review and adjust containment strategy for better transmission control")
        
        if zone.operational_challenges:
            areas.append("Address operational challenges through improved planning and resources")
        
        related_checkpoints = [cp for cp in self.checkpoints.values() if cp.zone_boundary == zone.zone_id]
        if related_checkpoints and any(cp.compliance_violations > 20 for cp in related_checkpoints):
            areas.append("Enhance checkpoint security and violation management")
        
        return areas
    
    def _generate_recommendations(self, zone: ContainmentZone, outcome: ContainmentOutcome) -> List[str]:
        """Generate recommendations based on assessment."""
        
        recommendations = []
        
        if outcome.cost_effectiveness_score < 0.5:
            recommendations.append("Optimize resource allocation for improved cost-effectiveness")
        
        if outcome.social_acceptance_rating < 0.6:
            recommendations.append("Implement enhanced community engagement and support programs")
        
        if outcome.essential_services_maintained < 0.8:
            recommendations.append("Strengthen essential services continuity planning")
        
        if zone.status == ContainmentStatus.ACTIVE and outcome.assessment_period_days > 30:
            recommendations.append("Consider transition to monitoring phase with scaled-down measures")
        
        if outcome.reproduction_number_reduction > 0.7:
            recommendations.append("Document successful practices for future containment operations")
        
        return recommendations
    
    def get_containment_summary(self) -> Dict[str, Any]:
        """Get comprehensive containment operations summary."""
        
        # Zone statistics
        zone_stats = {
            "total_zones": len(self.active_zones),
            "zones_by_type": defaultdict(int),
            "zones_by_status": defaultdict(int)
        }
        
        for zone in self.active_zones.values():
            zone_stats["zones_by_type"][zone.zone_type.value] += 1
            zone_stats["zones_by_status"][zone.status.value] += 1
        
        # Population and impact
        total_population = sum(z.estimated_population for z in self.active_zones.values())
        total_cases = sum(z.confirmed_cases + z.suspected_cases for z in self.active_zones.values())
        total_contacts = sum(z.contacts_under_monitoring for z in self.active_zones.values())
        
        # Checkpoint statistics
        checkpoint_stats = {
            "total_checkpoints": len(self.checkpoints),
            "daily_crossings": sum(cp.daily_crossings for cp in self.checkpoints.values()),
            "total_violations": sum(cp.compliance_violations for cp in self.checkpoints.values()),
            "health_referrals": sum(cp.health_referrals for cp in self.checkpoints.values())
        }
        
        # Performance metrics
        if self.active_zones:
            avg_compliance = statistics.mean(z.compliance_rate for z in self.active_zones.values())
            avg_effectiveness = statistics.mean(z.effectiveness_score for z in self.active_zones.values())
            avg_transmission_reduction = statistics.mean(z.transmission_reduction for z in self.active_zones.values())
        else:
            avg_compliance = avg_effectiveness = avg_transmission_reduction = 0.0
        
        # Outcome analysis
        if self.containment_outcomes:
            total_cases_prevented = sum(o.cases_prevented_estimate for o in self.containment_outcomes)
            avg_cost_effectiveness = statistics.mean(o.cost_effectiveness_score for o in self.containment_outcomes)
            avg_social_acceptance = statistics.mean(o.social_acceptance_rating for o in self.containment_outcomes)
        else:
            total_cases_prevented = 0
            avg_cost_effectiveness = avg_social_acceptance = 0.0
        
        return {
            "zone_statistics": dict(zone_stats),
            "population_impact": {
                "total_population_in_zones": total_population,
                "total_cases_managed": total_cases,
                "total_contacts_monitored": total_contacts
            },
            "checkpoint_operations": checkpoint_stats,
            "performance_metrics": {
                "average_compliance_rate": avg_compliance,
                "average_effectiveness_score": avg_effectiveness,
                "average_transmission_reduction": avg_transmission_reduction
            },
            "outcome_analysis": {
                "total_cases_prevented": total_cases_prevented,
                "average_cost_effectiveness": avg_cost_effectiveness,
                "average_social_acceptance": avg_social_acceptance,
                "assessments_completed": len(self.containment_outcomes)
            }
        }

def run_demonstration() -> ContainmentManager:
    """Run comprehensive containment management demonstration."""
    
    print("🚧 One Health Disease Containment System - Demonstration")
    print("=" * 75)
    
    manager = ContainmentManager()
    
    # Define containment scenarios
    containment_scenarios = [
        {
            "zone_name": "H5N1 Outbreak Core",
            "zone_type": ContainmentZoneType.HOT_ZONE,
            "strategy": ContainmentStrategy.RING_CONTAINMENT,
            "coordinates": [(40.7589, -73.9851), (40.7614, -73.9776), (40.7505, -73.9776), (40.7489, -73.9851)],
            "population": 15000
        },
        {
            "zone_name": "Protective Buffer Zone",
            "zone_type": ContainmentZoneType.BUFFER_ZONE,
            "strategy": ContainmentStrategy.ZONAL_CONTAINMENT,
            "coordinates": [(40.7700, -73.9900), (40.7650, -73.9700), (40.7400, -73.9700), (40.7350, -73.9900)],
            "population": 45000
        },
        {
            "zone_name": "Contact Quarantine Area",
            "zone_type": ContainmentZoneType.QUARANTINE_ZONE,
            "strategy": ContainmentStrategy.TARGETED_CONTAINMENT,
            "coordinates": [(40.7800, -73.9600), (40.7850, -73.9500), (40.7750, -73.9500)],
            "population": 8000
        },
        {
            "zone_name": "Border Monitoring Zone",
            "zone_type": ContainmentZoneType.OBSERVATION_ZONE,
            "strategy": ContainmentStrategy.PROGRESSIVE_CONTAINMENT,
            "coordinates": [(40.7900, -73.9400), (40.7950, -73.9300), (40.7850, -73.9300), (40.7800, -73.9400)],
            "population": 25000
        }
    ]
    
    print(f"\n🚧 Containment Scenarios:")
    for i, scenario in enumerate(containment_scenarios, 1):
        print(f"  Scenario {i}: {scenario['zone_name']}")
        print(f"    Type: {scenario['zone_type'].value.replace('_', ' ').title()}")
        print(f"    Strategy: {scenario['strategy'].value.replace('_', ' ').title()}")
        print(f"    Population: {scenario['population']:,}")
    
    print(f"\n🚧 Establishing Containment Zones...")
    
    # Establish containment zones
    zones = []
    for scenario in containment_scenarios:
        zone = manager.establish_containment_zone(
            zone_name=scenario["zone_name"],
            zone_type=scenario["zone_type"],
            boundary_coordinates=scenario["coordinates"],
            population_estimate=scenario["population"],
            containment_strategy=scenario["strategy"]
        )
        zones.append(zone)
        print(f"✅ Established: {zone.zone_name} ({zone.zone_id})")
    
    print(f"\n🛡️ Setting Up Checkpoints...")
    
    # Establish checkpoints
    checkpoint_configs = [
        {"zone_idx": 0, "name": "Main Entry Checkpoint", "location": "Highway 1 Intersection"},
        {"zone_idx": 0, "name": "Emergency Access Point", "location": "Hospital Route"},
        {"zone_idx": 1, "name": "Buffer Zone North Gate", "location": "Northern District Border"},
        {"zone_idx": 1, "name": "Buffer Zone South Gate", "location": "Southern District Border"},
        {"zone_idx": 2, "name": "Quarantine Facility Gate", "location": "Isolation Complex Entrance"},
        {"zone_idx": 3, "name": "Border Monitoring Station", "location": "State Boundary Crossing"}
    ]
    
    checkpoints = []
    for config in checkpoint_configs:
        zone = zones[config["zone_idx"]]
        checkpoint = manager.establish_checkpoint(
            zone_id=zone.zone_id,
            checkpoint_name=config["name"],
            location_description=config["location"]
        )
        checkpoints.append(checkpoint)
        print(f"🛡️ Checkpoint: {checkpoint.checkpoint_name} -> {zone.zone_name}")
    
    print(f"\n📊 Simulating Containment Operations...")
    
    # Simulate containment operations
    for i, zone in enumerate(zones):
        # Simulate operational data
        operational_data = {
            "confirmed_cases": random.randint(5, 50),
            "suspected_cases": random.randint(10, 100),
            "contacts_monitoring": random.randint(50, 500),
            "compliance_rate": random.uniform(0.6, 0.95),
            "effectiveness_score": random.uniform(0.5, 0.9),
            "transmission_reduction": random.uniform(0.3, 0.8),
            "checkpoint_data": {}
        }
        
        # Add checkpoint data
        related_checkpoints = [cp for cp in checkpoints if cp.zone_boundary == zone.zone_id]
        for cp in related_checkpoints:
            operational_data["checkpoint_data"][cp.checkpoint_id] = {
                "daily_crossings": random.randint(50, 500),
                "violations": random.randint(0, 25),
                "health_referrals": random.randint(0, 15)
            }
        
        # Update zone status
        manager.update_zone_status(zone.zone_id, ContainmentStatus.ACTIVE, operational_data)
        
        print(f"  📊 {zone.zone_name}: {zone.compliance_rate:.1%} compliance, {zone.effectiveness_score:.1%} effective")
    
    print(f"\n📈 Conducting Effectiveness Assessments...")
    
    # Assess containment effectiveness
    for zone in zones:
        outcome = manager.assess_containment_effectiveness(zone.zone_id)
        print(f"  📈 {zone.zone_name}: {outcome.cases_prevented_estimate} cases prevented, {outcome.cost_effectiveness_score:.2f} cost-effectiveness")
    
    return manager

def display_containment_results(manager: ContainmentManager):
    """Display comprehensive containment results."""
    
    zones = list(manager.active_zones.values())
    
    print(f"\n🚧 Disease Containment Results ({len(zones)} zones):")
    
    for i, zone in enumerate(zones, 1):
        print(f"\n{i}. {zone.zone_name}")
        print(f"   Type: {zone.zone_type.value.replace('_', ' ').title()}")
        print(f"   Status: {zone.status.value.replace('_', ' ').title()}")
        print(f"   Population: {zone.estimated_population:,}")
        print(f"   Area: {zone.geographic_boundary.area_km2:.1f} km²")
        print(f"   Cases: {zone.confirmed_cases} confirmed, {zone.suspected_cases} suspected")
        print(f"   Contacts Monitored: {zone.contacts_under_monitoring}")
        print(f"   Compliance Rate: {zone.compliance_rate:.1%}")
        print(f"   Effectiveness: {zone.effectiveness_score:.1%}")
        print(f"   Transmission Reduction: {zone.transmission_reduction:.1%}")
        print(f"   Movement Restriction: {zone.movement_restriction.value.replace('_', ' ').title()}")
        
        if zone.active_measures:
            print(f"   Active Measures ({len(zone.active_measures)}):")
            for measure in zone.active_measures[:3]:  # Show first 3
                print(f"     • {measure.value.replace('_', ' ').title()}")
        
        # Access points
        print(f"   Access Points: {len(zone.geographic_boundary.access_points)}")
        
        # Personnel deployment
        if zone.personnel_deployed:
            total_personnel = sum(zone.personnel_deployed.values())
            print(f"   Personnel Deployed: {total_personnel}")
    
    # Checkpoint summary
    checkpoints = list(manager.checkpoints.values())
    print(f"\n🛡️ Checkpoint Operations ({len(checkpoints)} checkpoints):")
    
    for checkpoint in checkpoints:
        print(f"  {checkpoint.checkpoint_name}:")
        print(f"    Daily Crossings: {checkpoint.daily_crossings}")
        print(f"    Compliance Violations: {checkpoint.compliance_violations}")
        print(f"    Health Referrals: {checkpoint.health_referrals}")
        print(f"    Processing Time: {checkpoint.average_processing_time_minutes:.1f} minutes")
    
    # Summary statistics
    summary = manager.get_containment_summary()
    
    print(f"\n📊 Containment Operations Summary:")
    print(f"  Total Zones: {summary['zone_statistics']['total_zones']}")
    print(f"  Total Population in Zones: {summary['population_impact']['total_population_in_zones']:,}")
    print(f"  Total Cases Managed: {summary['population_impact']['total_cases_managed']}")
    print(f"  Total Contacts Monitored: {summary['population_impact']['total_contacts_monitored']}")
    
    print(f"\n📈 Performance Metrics:")
    perf = summary["performance_metrics"]
    print(f"  Average Compliance Rate: {perf['average_compliance_rate']:.1%}")
    print(f"  Average Effectiveness Score: {perf['average_effectiveness_score']:.1%}")
    print(f"  Average Transmission Reduction: {perf['average_transmission_reduction']:.1%}")
    
    print(f"\n🛡️ Checkpoint Statistics:")
    cp_stats = summary["checkpoint_operations"]
    print(f"  Total Checkpoints: {cp_stats['total_checkpoints']}")
    print(f"  Daily Crossings: {cp_stats['daily_crossings']}")
    print(f"  Total Violations: {cp_stats['total_violations']}")
    print(f"  Health Referrals: {cp_stats['health_referrals']}")
    
    print(f"\n📈 Outcome Analysis:")
    outcome = summary["outcome_analysis"]
    print(f"  Cases Prevented: {outcome['total_cases_prevented']}")
    print(f"  Average Cost-Effectiveness: {outcome['average_cost_effectiveness']:.2f}")
    print(f"  Average Social Acceptance: {outcome['average_social_acceptance']:.1%}")
    print(f"  Assessments Completed: {outcome['assessments_completed']}")
    
    print(f"\n🏆 Zone Type Distribution:")
    for zone_type, count in summary["zone_statistics"]["zones_by_type"].items():
        print(f"  {zone_type.replace('_', ' ').title()}: {count}")
    
    print(f"\n🏆 TOP PERFORMING Zones:")
    top_zones = sorted(zones, key=lambda z: z.effectiveness_score, reverse=True)[:3]
    for i, zone in enumerate(top_zones, 1):
        print(f"  {i}. {zone.zone_name}")
        print(f"     Effectiveness: {zone.effectiveness_score:.1%}")
        print(f"     Compliance: {zone.compliance_rate:.1%}")
        print(f"     Transmission Reduction: {zone.transmission_reduction:.1%}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    containment_manager = run_demonstration()
    display_containment_results(containment_manager)
"""
Response Coordination System
============================
Module 4: Response & Control Systems

Advanced outbreak response coordination and intervention management system for One Health,
providing real-time response orchestration, resource deployment, and intervention tracking.

NIW Focus: Response intelligence enabling rapid, coordinated, and effective outbreak interventions.
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

class ResponseType(Enum):
    """Types of outbreak responses."""
    INVESTIGATION = "investigation"           # Outbreak investigation
    CONTAINMENT = "containment"              # Disease containment
    MITIGATION = "mitigation"                # Impact mitigation
    PREVENTION = "prevention"                # Preventive measures
    RECOVERY = "recovery"                    # Recovery operations
    SURVEILLANCE_ENHANCEMENT = "surveillance_enhancement"  # Enhanced surveillance

class InterventionType(Enum):
    """Types of interventions."""
    QUARANTINE = "quarantine"                # Isolation/quarantine
    VACCINATION = "vaccination"              # Vaccination programs
    TREATMENT = "treatment"                  # Medical treatment
    VECTOR_CONTROL = "vector_control"        # Vector management
    ENVIRONMENTAL = "environmental"          # Environmental controls
    COMMUNICATION = "communication"          # Public communication
    LABORATORY = "laboratory"                # Lab diagnostics
    SURVEILLANCE = "surveillance"            # Active surveillance

class ResponsePriority(Enum):
    """Response priority levels."""
    CRITICAL = "critical"                    # Immediate action required
    HIGH = "high"                           # Urgent action needed
    MEDIUM = "medium"                       # Moderate priority
    LOW = "low"                             # Low priority
    MONITORING = "monitoring"               # Monitoring only

class ResponseStatus(Enum):
    """Response status."""
    PLANNED = "planned"                     # Response planned
    ACTIVE = "active"                       # Response active
    COMPLETED = "completed"                 # Response completed
    CANCELLED = "cancelled"                 # Response cancelled
    SUSPENDED = "suspended"                 # Response suspended

class ResourceType(Enum):
    """Types of response resources."""
    PERSONNEL = "personnel"                 # Human resources
    EQUIPMENT = "equipment"                # Equipment/supplies
    LABORATORY = "laboratory"              # Lab resources
    TRANSPORTATION = "transportation"       # Transport resources
    COMMUNICATION = "communication"        # Communication tools
    FINANCIAL = "financial"                # Financial resources

@dataclass
class ResponseResource:
    """Response resource definition."""
    
    resource_id: str
    resource_type: ResourceType
    resource_name: str
    quantity_available: float
    quantity_required: float = 0.0
    quantity_allocated: float = 0.0
    unit: str = "units"
    cost_per_unit: float = 0.0
    location: Optional[str] = None
    availability_start: Optional[datetime] = None
    availability_end: Optional[datetime] = None
    is_allocated: bool = False

@dataclass
class Intervention:
    """Single intervention definition."""
    
    intervention_id: str
    intervention_type: InterventionType
    intervention_name: str
    target_population: str
    target_area: str
    
    # Timing
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    
    # Resources
    required_resources: List[ResponseResource] = field(default_factory=list)
    allocated_resources: List[ResponseResource] = field(default_factory=list)
    
    # Performance metrics
    target_coverage: float = 1.0              # Target coverage (0-1)
    actual_coverage: float = 0.0              # Actual coverage achieved
    effectiveness_score: float = 0.0          # Effectiveness (0-1)
    cost_estimate: float = 0.0                # Cost estimate
    actual_cost: float = 0.0                  # Actual cost
    
    # Status tracking
    status: ResponseStatus = ResponseStatus.PLANNED
    progress_percentage: float = 0.0           # Progress (0-100)
    
    # Key metrics
    key_outcomes: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

@dataclass
class ResponseEvent:
    """Response event or milestone."""
    
    event_id: str
    event_type: str
    event_description: str
    event_timestamp: datetime
    severity: ResponsePriority
    location: Optional[str] = None
    affected_population: int = 0
    response_triggered: bool = False
    
    # Associated data
    event_data: Dict[str, Any] = field(default_factory=dict)
    response_actions: List[str] = field(default_factory=list)

@dataclass
class ResponsePlan:
    """Comprehensive response plan."""
    
    plan_id: str
    response_type: ResponseType
    plan_name: str
    outbreak_id: str
    creation_timestamp: datetime
    
    # Plan details
    priority: ResponsePriority
    objectives: List[str] = field(default_factory=list)
    target_areas: List[str] = field(default_factory=list)
    estimated_duration_days: int = 30
    
    # Interventions and resources
    interventions: List[Intervention] = field(default_factory=list)
    total_resources_required: List[ResponseResource] = field(default_factory=list)
    
    # Timeline and milestones
    key_milestones: List[Dict[str, Any]] = field(default_factory=list)
    critical_path_activities: List[str] = field(default_factory=list)
    
    # Performance tracking
    plan_status: ResponseStatus = ResponseStatus.PLANNED
    overall_progress: float = 0.0              # Overall progress (0-100)
    success_criteria: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    # Outcomes
    total_cost_estimate: float = 0.0
    actual_total_cost: float = 0.0
    effectiveness_rating: float = 0.0          # Overall effectiveness (0-1)
    
    # Coordination
    lead_agency: str = "Public Health"
    partner_agencies: List[str] = field(default_factory=list)
    coordination_challenges: List[str] = field(default_factory=list)

class ResponseCoordinator:
    """Central response coordination system."""
    
    def __init__(self):
        self.response_plans: Dict[str, ResponsePlan] = {}
        self.active_interventions: Dict[str, Intervention] = {}
        self.response_events: List[ResponseEvent] = []
        self.resource_pool: Dict[str, ResponseResource] = {}
        self.coordination_metrics: Dict[str, Any] = {}
        
        # Initialize default resources
        self._initialize_resource_pool()
        
        logger.info("One Health Response Coordinator initialized")
    
    def _initialize_resource_pool(self):
        """Initialize default resource pool."""
        default_resources = [
            # Personnel resources
            {"id": "epidemiologists", "type": ResourceType.PERSONNEL, "name": "Field Epidemiologists", 
             "available": 25, "unit": "persons", "cost": 500},
            {"id": "veterinarians", "type": ResourceType.PERSONNEL, "name": "Veterinarians", 
             "available": 15, "unit": "persons", "cost": 450},
            {"id": "lab_technicians", "type": ResourceType.PERSONNEL, "name": "Laboratory Technicians", 
             "available": 20, "unit": "persons", "cost": 300},
            {"id": "public_health_nurses", "type": ResourceType.PERSONNEL, "name": "Public Health Nurses", 
             "available": 30, "unit": "persons", "cost": 350},
            
            # Equipment resources
            {"id": "sample_collection_kits", "type": ResourceType.EQUIPMENT, "name": "Sample Collection Kits", 
             "available": 500, "unit": "kits", "cost": 25},
            {"id": "ppe_sets", "type": ResourceType.EQUIPMENT, "name": "Personal Protective Equipment", 
             "available": 1000, "unit": "sets", "cost": 50},
            {"id": "mobile_labs", "type": ResourceType.EQUIPMENT, "name": "Mobile Laboratory Units", 
             "available": 5, "unit": "units", "cost": 5000},
            {"id": "communication_equipment", "type": ResourceType.COMMUNICATION, "name": "Communication Equipment", 
             "available": 50, "unit": "sets", "cost": 200},
            
            # Transportation
            {"id": "field_vehicles", "type": ResourceType.TRANSPORTATION, "name": "Field Response Vehicles", 
             "available": 20, "unit": "vehicles", "cost": 150},
            {"id": "emergency_helicopters", "type": ResourceType.TRANSPORTATION, "name": "Emergency Helicopters", 
             "available": 3, "unit": "aircraft", "cost": 2000}
        ]
        
        for res_data in default_resources:
            resource = ResponseResource(
                resource_id=res_data["id"],
                resource_type=res_data["type"],
                resource_name=res_data["name"],
                quantity_available=res_data["available"],
                unit=res_data["unit"],
                cost_per_unit=res_data["cost"]
            )
            self.resource_pool[resource.resource_id] = resource
    
    def create_response_plan(self, outbreak_id: str, response_type: ResponseType,
                           priority: ResponsePriority, objectives: List[str],
                           target_areas: List[str]) -> ResponsePlan:
        """Create comprehensive response plan."""
        
        plan_id = f"RESP_{random.randint(100000, 999999)}"
        
        plan = ResponsePlan(
            plan_id=plan_id,
            response_type=response_type,
            plan_name=f"{response_type.value.title()} Response - {outbreak_id}",
            outbreak_id=outbreak_id,
            creation_timestamp=datetime.now(),
            priority=priority,
            objectives=objectives.copy(),
            target_areas=target_areas.copy()
        )
        
        # Generate default interventions based on response type
        plan.interventions = self._generate_default_interventions(response_type, target_areas)
        
        # Calculate resource requirements
        plan.total_resources_required = self._calculate_resource_requirements(plan.interventions)
        
        # Set success criteria based on response type
        plan.success_criteria = self._define_success_criteria(response_type)
        
        # Generate key milestones
        plan.key_milestones = self._generate_milestones(plan)
        
        # Calculate cost estimates
        plan.total_cost_estimate = self._calculate_total_cost(plan)
        
        # Set partner agencies
        plan.partner_agencies = self._assign_partner_agencies(response_type)
        
        self.response_plans[plan_id] = plan
        
        logger.info(f"Response plan created: {plan_id}")
        
        return plan
    
    def _generate_default_interventions(self, response_type: ResponseType, 
                                      target_areas: List[str]) -> List[Intervention]:
        """Generate default interventions based on response type."""
        
        interventions = []
        base_start = datetime.now() + timedelta(hours=2)  # Start in 2 hours
        
        intervention_templates = {
            ResponseType.INVESTIGATION: [
                {"type": InterventionType.SURVEILLANCE, "name": "Enhanced Surveillance", "duration": 14},
                {"type": InterventionType.LABORATORY, "name": "Diagnostic Testing", "duration": 10},
                {"type": InterventionType.COMMUNICATION, "name": "Stakeholder Notification", "duration": 3}
            ],
            ResponseType.CONTAINMENT: [
                {"type": InterventionType.QUARANTINE, "name": "Isolation/Quarantine", "duration": 21},
                {"type": InterventionType.SURVEILLANCE, "name": "Contact Tracing", "duration": 14},
                {"type": InterventionType.LABORATORY, "name": "Confirmation Testing", "duration": 7}
            ],
            ResponseType.MITIGATION: [
                {"type": InterventionType.TREATMENT, "name": "Medical Treatment", "duration": 30},
                {"type": InterventionType.VACCINATION, "name": "Vaccination Campaign", "duration": 45},
                {"type": InterventionType.COMMUNICATION, "name": "Public Health Communication", "duration": 60}
            ],
            ResponseType.PREVENTION: [
                {"type": InterventionType.VACCINATION, "name": "Preventive Vaccination", "duration": 90},
                {"type": InterventionType.VECTOR_CONTROL, "name": "Vector Control", "duration": 120},
                {"type": InterventionType.ENVIRONMENTAL, "name": "Environmental Sanitation", "duration": 30}
            ]
        }
        
        templates = intervention_templates.get(response_type, [])
        
        for i, template in enumerate(templates):
            for area in target_areas:
                intervention_id = f"INT_{random.randint(100000, 999999)}"
                
                intervention = Intervention(
                    intervention_id=intervention_id,
                    intervention_type=template["type"],
                    intervention_name=f"{template['name']} - {area}",
                    target_population=f"Population in {area}",
                    target_area=area,
                    planned_start=base_start + timedelta(days=i),
                    planned_end=base_start + timedelta(days=i + template["duration"]),
                    target_coverage=0.85 + random.uniform(0, 0.15),  # 85-100%
                    cost_estimate=random.uniform(10000, 100000)
                )
                
                # Assign required resources
                intervention.required_resources = self._assign_intervention_resources(
                    template["type"], area
                )
                
                interventions.append(intervention)
        
        return interventions
    
    def _assign_intervention_resources(self, intervention_type: InterventionType, 
                                     area: str) -> List[ResponseResource]:
        """Assign required resources to intervention."""
        
        resource_requirements = {
            InterventionType.SURVEILLANCE: [
                ("epidemiologists", 3), ("sample_collection_kits", 50), ("field_vehicles", 2)
            ],
            InterventionType.LABORATORY: [
                ("lab_technicians", 5), ("mobile_labs", 1), ("sample_collection_kits", 100)
            ],
            InterventionType.QUARANTINE: [
                ("public_health_nurses", 8), ("ppe_sets", 200), ("communication_equipment", 5)
            ],
            InterventionType.TREATMENT: [
                ("public_health_nurses", 10), ("ppe_sets", 150), ("field_vehicles", 3)
            ],
            InterventionType.VACCINATION: [
                ("public_health_nurses", 15), ("veterinarians", 5), ("field_vehicles", 4)
            ],
            InterventionType.VECTOR_CONTROL: [
                ("epidemiologists", 4), ("equipment", 20), ("field_vehicles", 2)
            ],
            InterventionType.COMMUNICATION: [
                ("communication_equipment", 10), ("field_vehicles", 1)
            ]
        }
        
        requirements = resource_requirements.get(intervention_type, [])
        required_resources = []
        
        for resource_id, quantity in requirements:
            if resource_id in self.resource_pool:
                resource = self.resource_pool[resource_id]
                required_resource = ResponseResource(
                    resource_id=f"{resource.resource_id}_{random.randint(1000, 9999)}",
                    resource_type=resource.resource_type,
                    resource_name=resource.resource_name,
                    quantity_available=resource.quantity_available,
                    quantity_required=quantity,
                    unit=resource.unit,
                    cost_per_unit=resource.cost_per_unit,
                    location=area
                )
                required_resources.append(required_resource)
        
        return required_resources
    
    def _calculate_resource_requirements(self, interventions: List[Intervention]) -> List[ResponseResource]:
        """Calculate total resource requirements across all interventions."""
        
        resource_totals = defaultdict(lambda: {"quantity": 0, "cost": 0})
        
        for intervention in interventions:
            for resource in intervention.required_resources:
                key = resource.resource_type.value
                resource_totals[key]["quantity"] += resource.quantity_required
                resource_totals[key]["cost"] += resource.quantity_required * resource.cost_per_unit
        
        total_resources = []
        for resource_type, totals in resource_totals.items():
            total_resource = ResponseResource(
                resource_id=f"TOTAL_{resource_type.upper()}",
                resource_type=ResourceType(resource_type),
                resource_name=f"Total {resource_type.title()} Requirements",
                quantity_available=0,
                quantity_required=totals["quantity"],
                cost_per_unit=totals["cost"] / totals["quantity"] if totals["quantity"] > 0 else 0
            )
            total_resources.append(total_resource)
        
        return total_resources
    
    def _define_success_criteria(self, response_type: ResponseType) -> List[str]:
        """Define success criteria based on response type."""
        
        criteria_templates = {
            ResponseType.INVESTIGATION: [
                "Source of outbreak identified within 7 days",
                "All cases investigated within 72 hours of notification",
                "Laboratory confirmation rate >80%",
                "Complete case-contact network mapped"
            ],
            ResponseType.CONTAINMENT: [
                "No secondary transmission beyond identified contacts",
                "All contacts traced and monitored",
                "Quarantine compliance rate >95%",
                "Outbreak contained within 21 days"
            ],
            ResponseType.MITIGATION: [
                "Case fatality rate reduced by 50%",
                "Treatment coverage >90% of identified cases",
                "Vaccination coverage >80% of target population",
                "Healthcare system capacity maintained"
            ],
            ResponseType.PREVENTION: [
                "Vaccination coverage >85% of target population",
                "Vector control effectiveness >70%",
                "Zero secondary outbreaks in target areas",
                "Risk communication reaches >90% of population"
            ]
        }
        
        return criteria_templates.get(response_type, ["Response objectives achieved"])
    
    def _generate_milestones(self, plan: ResponsePlan) -> List[Dict[str, Any]]:
        """Generate key milestones for response plan."""
        
        milestones = []
        start_date = datetime.now()
        
        # Common milestones
        milestone_templates = [
            {"name": "Response Activation", "days": 0, "critical": True},
            {"name": "Initial Assessment Complete", "days": 1, "critical": True},
            {"name": "Resources Deployed", "days": 2, "critical": True},
            {"name": "Interventions Active", "days": 3, "critical": True},
            {"name": "First Progress Review", "days": 7, "critical": False},
            {"name": "Mid-Point Assessment", "days": 15, "critical": False},
            {"name": "Final Evaluation", "days": 30, "critical": True}
        ]
        
        for template in milestone_templates:
            milestone = {
                "milestone_id": f"MILE_{random.randint(1000, 9999)}",
                "name": template["name"],
                "target_date": start_date + timedelta(days=template["days"]),
                "is_critical": template["critical"],
                "status": "pending",
                "completion_date": None
            }
            milestones.append(milestone)
        
        return milestones
    
    def _calculate_total_cost(self, plan: ResponsePlan) -> float:
        """Calculate total estimated cost of response plan."""
        
        total_cost = 0.0
        
        for intervention in plan.interventions:
            total_cost += intervention.cost_estimate
            
            for resource in intervention.required_resources:
                total_cost += resource.quantity_required * resource.cost_per_unit
        
        # Add overhead costs (20%)
        total_cost *= 1.2
        
        return total_cost
    
    def _assign_partner_agencies(self, response_type: ResponseType) -> List[str]:
        """Assign partner agencies based on response type."""
        
        agency_assignments = {
            ResponseType.INVESTIGATION: [
                "CDC Field Epidemiology", "State Veterinarian", "Environmental Health", 
                "Laboratory Services"
            ],
            ResponseType.CONTAINMENT: [
                "Emergency Management", "Law Enforcement", "Healthcare Systems", 
                "Transportation Authority"
            ],
            ResponseType.MITIGATION: [
                "Healthcare Systems", "Pharmaceutical Supply", "Emergency Medical Services", 
                "Red Cross"
            ],
            ResponseType.PREVENTION: [
                "Vaccination Services", "Vector Control District", "Environmental Health", 
                "Community Organizations"
            ]
        }
        
        return agency_assignments.get(response_type, ["Public Health"])
    
    def activate_response_plan(self, plan_id: str) -> bool:
        """Activate response plan and begin interventions."""
        
        if plan_id not in self.response_plans:
            return False
        
        plan = self.response_plans[plan_id]
        plan.plan_status = ResponseStatus.ACTIVE
        
        # Activate interventions
        for intervention in plan.interventions:
            intervention.status = ResponseStatus.ACTIVE
            intervention.actual_start = datetime.now()
            self.active_interventions[intervention.intervention_id] = intervention
        
        # Allocate resources
        self._allocate_resources(plan)
        
        # Create activation event
        activation_event = ResponseEvent(
            event_id=f"EVENT_{random.randint(100000, 999999)}",
            event_type="response_activation",
            event_description=f"Response plan {plan_id} activated",
            event_timestamp=datetime.now(),
            severity=plan.priority,
            response_triggered=True
        )
        
        self.response_events.append(activation_event)
        
        logger.info(f"Response plan activated: {plan_id}")
        
        return True
    
    def _allocate_resources(self, plan: ResponsePlan):
        """Allocate available resources to plan interventions."""
        
        for intervention in plan.interventions:
            allocated_resources = []
            
            for required in intervention.required_resources:
                # Find available resource
                base_resource_id = required.resource_name.lower().replace(" ", "_")
                
                for pool_id, pool_resource in self.resource_pool.items():
                    if (pool_resource.resource_type == required.resource_type and 
                        pool_resource.quantity_available >= required.quantity_required and
                        not pool_resource.is_allocated):
                        
                        # Allocate resource
                        allocated = ResponseResource(
                            resource_id=f"ALLOC_{random.randint(1000, 9999)}",
                            resource_type=pool_resource.resource_type,
                            resource_name=pool_resource.resource_name,
                            quantity_available=pool_resource.quantity_available,
                            quantity_required=required.quantity_required,
                            quantity_allocated=required.quantity_required,
                            unit=pool_resource.unit,
                            cost_per_unit=pool_resource.cost_per_unit,
                            location=required.location,
                            is_allocated=True
                        )
                        
                        allocated_resources.append(allocated)
                        
                        # Update pool resource
                        pool_resource.quantity_available -= required.quantity_required
                        pool_resource.quantity_allocated += required.quantity_required
                        
                        break
            
            intervention.allocated_resources = allocated_resources
    
    def update_intervention_progress(self, intervention_id: str, progress: float, 
                                   effectiveness: float = None, actual_coverage: float = None):
        """Update intervention progress and metrics."""
        
        if intervention_id in self.active_interventions:
            intervention = self.active_interventions[intervention_id]
            
            intervention.progress_percentage = min(100.0, max(0.0, progress))
            
            if effectiveness is not None:
                intervention.effectiveness_score = min(1.0, max(0.0, effectiveness))
            
            if actual_coverage is not None:
                intervention.actual_coverage = min(1.0, max(0.0, actual_coverage))
            
            # Mark as completed if 100% progress
            if intervention.progress_percentage >= 100.0:
                intervention.status = ResponseStatus.COMPLETED
                intervention.actual_end = datetime.now()
                
                # Generate completion event
                completion_event = ResponseEvent(
                    event_id=f"EVENT_{random.randint(100000, 999999)}",
                    event_type="intervention_completion",
                    event_description=f"Intervention {intervention.intervention_name} completed",
                    event_timestamp=datetime.now(),
                    severity=ResponsePriority.MEDIUM,
                    response_triggered=False
                )
                
                self.response_events.append(completion_event)
            
            # Update plan progress
            self._update_plan_progress(intervention_id)
    
    def _update_plan_progress(self, intervention_id: str):
        """Update overall plan progress based on intervention updates."""
        
        # Find plan containing this intervention
        target_plan = None
        for plan in self.response_plans.values():
            for intervention in plan.interventions:
                if intervention.intervention_id == intervention_id:
                    target_plan = plan
                    break
            if target_plan:
                break
        
        if target_plan:
            # Calculate overall progress
            total_progress = sum(i.progress_percentage for i in target_plan.interventions)
            target_plan.overall_progress = total_progress / len(target_plan.interventions)
            
            # Calculate overall effectiveness
            completed_interventions = [i for i in target_plan.interventions 
                                     if i.status == ResponseStatus.COMPLETED]
            if completed_interventions:
                avg_effectiveness = statistics.mean(i.effectiveness_score for i in completed_interventions)
                target_plan.effectiveness_rating = avg_effectiveness
    
    def get_response_summary(self) -> Dict[str, Any]:
        """Get comprehensive response coordination summary."""
        
        # Response plan statistics
        plan_stats = {
            "total_plans": len(self.response_plans),
            "active_plans": len([p for p in self.response_plans.values() 
                                if p.plan_status == ResponseStatus.ACTIVE]),
            "completed_plans": len([p for p in self.response_plans.values() 
                                   if p.plan_status == ResponseStatus.COMPLETED])
        }
        
        # Intervention statistics
        intervention_stats = {
            "total_interventions": len(self.active_interventions),
            "completed_interventions": len([i for i in self.active_interventions.values() 
                                           if i.status == ResponseStatus.COMPLETED]),
            "average_progress": statistics.mean([i.progress_percentage 
                                               for i in self.active_interventions.values()]) if self.active_interventions else 0
        }
        
        # Resource utilization
        resource_stats = {}
        for resource in self.resource_pool.values():
            utilization = (resource.quantity_allocated / resource.quantity_available * 100) if resource.quantity_available > 0 else 0
            resource_stats[resource.resource_name] = {
                "available": resource.quantity_available,
                "allocated": resource.quantity_allocated,
                "utilization_percent": utilization
            }
        
        # Cost analysis
        total_estimated_cost = sum(p.total_cost_estimate for p in self.response_plans.values())
        total_actual_cost = sum(p.actual_total_cost for p in self.response_plans.values())
        
        # Performance metrics
        effectiveness_values = [p.effectiveness_rating for p in self.response_plans.values() 
                               if p.effectiveness_rating > 0]
        if effectiveness_values:
            avg_effectiveness = statistics.mean(effectiveness_values)
        else:
            avg_effectiveness = 0.0
        
        return {
            "response_plan_statistics": plan_stats,
            "intervention_statistics": intervention_stats,
            "resource_utilization": resource_stats,
            "cost_analysis": {
                "total_estimated_cost": total_estimated_cost,
                "total_actual_cost": total_actual_cost,
                "cost_variance": total_actual_cost - total_estimated_cost if total_actual_cost > 0 else 0
            },
            "performance_metrics": {
                "average_effectiveness": avg_effectiveness,
                "total_events": len(self.response_events),
                "critical_events": len([e for e in self.response_events 
                                       if e.severity == ResponsePriority.CRITICAL])
            }
        }

def run_demonstration() -> ResponseCoordinator:
    """Run comprehensive response coordination demonstration."""
    
    print("🚨 One Health Response Coordination System - Demonstration")
    print("=" * 70)
    
    coordinator = ResponseCoordinator()
    
    # Create multiple outbreak response scenarios
    outbreak_scenarios = [
        {
            "outbreak_id": "AVIAN_FLU_2026_001",
            "response_type": ResponseType.CONTAINMENT,
            "priority": ResponsePriority.CRITICAL,
            "objectives": [
                "Contain H5N1 outbreak in poultry",
                "Prevent human transmission",
                "Protect food supply chain"
            ],
            "target_areas": ["Northern District", "Central Valley"]
        },
        {
            "outbreak_id": "ZOONOTIC_2026_002", 
            "response_type": ResponseType.INVESTIGATION,
            "priority": ResponsePriority.HIGH,
            "objectives": [
                "Identify zoonotic pathogen source",
                "Trace transmission pathways",
                "Implement control measures"
            ],
            "target_areas": ["Urban Center", "Rural Communities"]
        },
        {
            "outbreak_id": "VECTOR_2026_003",
            "response_type": ResponseType.PREVENTION,
            "priority": ResponsePriority.MEDIUM,
            "objectives": [
                "Prevent vector-borne disease spread",
                "Implement environmental controls",
                "Enhance surveillance capacity"
            ],
            "target_areas": ["Coastal Region"]
        }
    ]
    
    print(f"\n📊 Response Scenarios:")
    for i, scenario in enumerate(outbreak_scenarios, 1):
        print(f"  Scenario {i}: {scenario['outbreak_id']}")
        print(f"    Type: {scenario['response_type'].value.title()}")
        print(f"    Priority: {scenario['priority'].value.upper()}")
        print(f"    Areas: {', '.join(scenario['target_areas'])}")
    
    print(f"\n🚨 Creating Response Plans...")
    
    # Create response plans
    response_plans = []
    for scenario in outbreak_scenarios:
        plan = coordinator.create_response_plan(
            outbreak_id=scenario["outbreak_id"],
            response_type=scenario["response_type"],
            priority=scenario["priority"],
            objectives=scenario["objectives"],
            target_areas=scenario["target_areas"]
        )
        response_plans.append(plan)
        print(f"✅ Plan created: {plan.plan_id}")
    
    print(f"\n🏃‍♂️ Activating Response Plans...")
    
    # Activate all plans
    for plan in response_plans:
        coordinator.activate_response_plan(plan.plan_id)
        print(f"🚀 Activated: {plan.plan_id}")
    
    print(f"\n📈 Simulating Response Progress...")
    
    # Simulate intervention progress
    for plan in response_plans:
        for i, intervention in enumerate(plan.interventions):
            # Simulate realistic progress and effectiveness
            progress = random.uniform(60, 100)  # 60-100% progress
            effectiveness = random.uniform(0.6, 0.95)  # 60-95% effectiveness
            coverage = random.uniform(0.7, 0.98)  # 70-98% coverage
            
            coordinator.update_intervention_progress(
                intervention.intervention_id, 
                progress, 
                effectiveness, 
                coverage
            )
            
            print(f"  📊 {intervention.intervention_name}: {progress:.1f}% complete, {effectiveness:.1%} effective")
    
    return coordinator

def display_response_results(coordinator: ResponseCoordinator):
    """Display comprehensive response coordination results."""
    
    plans = list(coordinator.response_plans.values())
    
    print(f"\n🚨 Response Coordination Results ({len(plans)} plans):")
    
    for i, plan in enumerate(plans, 1):
        print(f"\n{i}. {plan.plan_name}")
        print(f"   Response Type: {plan.response_type.value.replace('_', ' ').title()}")
        print(f"   Priority: {plan.priority.value.upper()}")
        print(f"   Status: {plan.plan_status.value.title()}")
        print(f"   Overall Progress: {plan.overall_progress:.1f}%")
        print(f"   Effectiveness Rating: {plan.effectiveness_rating:.1%}")
        print(f"   Target Areas: {', '.join(plan.target_areas)}")
        print(f"   Total Interventions: {len(plan.interventions)}")
        
        completed_interventions = [i for i in plan.interventions 
                                 if i.status == ResponseStatus.COMPLETED]
        print(f"   Completed Interventions: {len(completed_interventions)}")
        
        print(f"   Cost Estimate: ${plan.total_cost_estimate:,.0f}")
        
        if plan.objectives:
            print(f"   Key Objectives ({len(plan.objectives)}):")
            for obj in plan.objectives:
                print(f"     • {obj}")
        
        if plan.success_criteria:
            print(f"   Success Criteria ({len(plan.success_criteria)}):")
            for criteria in plan.success_criteria[:3]:  # Show first 3
                print(f"     • {criteria}")
        
        if plan.partner_agencies:
            print(f"   Partner Agencies: {', '.join(plan.partner_agencies[:3])}")
    
    # Summary statistics
    summary = coordinator.get_response_summary()
    
    print(f"\n📊 Response Coordination Summary:")
    print(f"  Total Response Plans: {summary['response_plan_statistics']['total_plans']}")
    print(f"  Active Plans: {summary['response_plan_statistics']['active_plans']}")
    print(f"  Total Interventions: {summary['intervention_statistics']['total_interventions']}")
    print(f"  Average Progress: {summary['intervention_statistics']['average_progress']:.1f}%")
    
    print(f"\n💰 Cost Analysis:")
    cost = summary["cost_analysis"]
    print(f"  Total Estimated Cost: ${cost['total_estimated_cost']:,.0f}")
    if cost['total_actual_cost'] > 0:
        print(f"  Total Actual Cost: ${cost['total_actual_cost']:,.0f}")
        print(f"  Cost Variance: ${cost['cost_variance']:,.0f}")
    
    print(f"\n📈 Performance Metrics:")
    perf = summary["performance_metrics"]
    print(f"  Average Effectiveness: {perf['average_effectiveness']:.1%}")
    print(f"  Total Response Events: {perf['total_events']}")
    print(f"  Critical Events: {perf['critical_events']}")
    
    print(f"\n🔧 Resource Utilization:")
    top_resources = list(summary["resource_utilization"].items())[:5]
    for resource_name, stats in top_resources:
        print(f"  {resource_name}: {stats['utilization_percent']:.1f}% utilized")
        print(f"    Available: {stats['available']}, Allocated: {stats['allocated']}")
    
    print(f"\n🏆 TOP PERFORMING Responses:")
    best_plans = sorted(plans, key=lambda p: p.effectiveness_rating, reverse=True)[:3]
    for i, plan in enumerate(best_plans, 1):
        print(f"  {i}. {plan.response_type.value.replace('_', ' ').title()}")
        print(f"     Effectiveness: {plan.effectiveness_rating:.1%}")
        print(f"     Progress: {plan.overall_progress:.1f}%")
        print(f"     Cost: ${plan.total_cost_estimate:,.0f}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    response_coordinator = run_demonstration()
    display_response_results(response_coordinator)
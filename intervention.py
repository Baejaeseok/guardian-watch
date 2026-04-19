"""
Intervention Management System
==============================
Module 4: Response & Control Systems

Advanced intervention planning, execution, and monitoring system for One Health responses,
providing detailed intervention design, resource optimization, and outcome tracking.

NIW Focus: Intervention intelligence ensuring effective, evidence-based outbreak control measures.
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

class InterventionStrategy(Enum):
    """Intervention strategy types."""
    IMMEDIATE_CONTAINMENT = "immediate_containment"     # Rapid containment
    GRADUAL_MITIGATION = "gradual_mitigation"          # Phased mitigation
    TARGETED_PREVENTION = "targeted_prevention"        # Targeted prevention
    COMPREHENSIVE_RESPONSE = "comprehensive_response"   # Multi-faceted response
    ADAPTIVE_CONTROL = "adaptive_control"              # Adaptive control
    EVIDENCE_BASED = "evidence_based"                  # Evidence-based approach

class InterventionCategory(Enum):
    """Intervention categories."""
    MEDICAL = "medical"                        # Medical interventions
    BEHAVIORAL = "behavioral"                  # Behavioral changes
    ENVIRONMENTAL = "environmental"            # Environmental controls
    ADMINISTRATIVE = "administrative"          # Policy/administrative
    EDUCATIONAL = "educational"                # Education/communication
    TECHNOLOGICAL = "technological"            # Technology-based

class InterventionTarget(Enum):
    """Intervention targets."""
    HUMAN_POPULATION = "human_population"      # Human populations
    ANIMAL_POPULATION = "animal_population"    # Animal populations
    ENVIRONMENT = "environment"                # Environmental targets
    VECTORS = "vectors"                        # Vector populations
    FOOD_CHAIN = "food_chain"                  # Food supply chain
    HEALTHCARE_SYSTEM = "healthcare_system"    # Healthcare infrastructure

class ImplementationPhase(Enum):
    """Implementation phases."""
    PLANNING = "planning"                      # Planning phase
    PREPARATION = "preparation"                # Preparation phase
    IMPLEMENTATION = "implementation"          # Active implementation
    MONITORING = "monitoring"                  # Monitoring phase
    EVALUATION = "evaluation"                  # Evaluation phase
    ADAPTATION = "adaptation"                  # Adaptation/refinement

class InterventionOutcome(Enum):
    """Intervention outcomes."""
    HIGHLY_EFFECTIVE = "highly_effective"      # >90% effectiveness
    EFFECTIVE = "effective"                    # 70-90% effectiveness
    MODERATELY_EFFECTIVE = "moderately_effective"  # 50-70% effectiveness
    LIMITED_EFFECTIVENESS = "limited_effectiveness"  # 30-50% effectiveness
    INEFFECTIVE = "ineffective"                # <30% effectiveness
    UNKNOWN = "unknown"                        # Unknown/pending

@dataclass
class InterventionParameter:
    """Single intervention parameter."""
    
    parameter_id: str
    parameter_name: str
    parameter_type: str  # "dosage", "duration", "frequency", "coverage", "intensity"
    current_value: Union[float, int, str]
    optimal_value: Optional[Union[float, int, str]] = None
    min_value: Optional[Union[float, int, str]] = None
    max_value: Optional[Union[float, int, str]] = None
    unit: str = ""
    confidence_level: float = 0.0  # Confidence in parameter setting
    evidence_quality: str = "low"  # "low", "moderate", "high"
    
    # Performance tracking
    effectiveness_score: float = 0.0
    adjustment_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ImplementationBarrier:
    """Implementation barrier or challenge."""
    
    barrier_id: str
    barrier_type: str  # "resource", "logistical", "social", "technical", "regulatory"
    description: str
    severity: str  # "low", "medium", "high", "critical"
    impact_area: str
    
    # Mitigation
    mitigation_strategy: str = ""
    mitigation_cost: float = 0.0
    mitigation_timeline: int = 0  # days
    is_resolved: bool = False
    resolution_date: Optional[datetime] = None

@dataclass
class InterventionProtocol:
    """Detailed intervention protocol."""
    
    protocol_id: str
    protocol_name: str
    intervention_category: InterventionCategory
    intervention_target: InterventionTarget
    strategy: InterventionStrategy
    
    # Protocol details
    description: str
    standard_operating_procedures: List[str] = field(default_factory=list)
    required_training: List[str] = field(default_factory=list)
    quality_indicators: List[str] = field(default_factory=list)
    
    # Implementation parameters
    parameters: List[InterventionParameter] = field(default_factory=list)
    implementation_phases: List[ImplementationPhase] = field(default_factory=list)
    
    # Resource requirements
    personnel_requirements: Dict[str, int] = field(default_factory=dict)
    equipment_requirements: Dict[str, int] = field(default_factory=dict)
    supply_requirements: Dict[str, int] = field(default_factory=dict)
    
    # Timeline and logistics
    minimum_duration_days: int = 1
    typical_duration_days: int = 7
    maximum_duration_days: int = 30
    preparation_time_hours: int = 24
    
    # Evidence base
    evidence_level: str = "expert_opinion"  # "expert_opinion", "observational", "controlled", "randomized"
    literature_references: List[str] = field(default_factory=list)
    success_rate_reported: float = 0.5
    confidence_interval: Tuple[float, float] = (0.3, 0.7)

@dataclass
class InterventionExecution:
    """Intervention execution tracking."""
    
    execution_id: str
    protocol_id: str
    protocol_name: str
    target_population: str
    target_location: str
    
    # Execution timeline
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    current_phase: ImplementationPhase = ImplementationPhase.PLANNING
    
    # Target metrics
    target_population_size: int = 1000
    target_coverage_rate: float = 0.8  # 80% target coverage
    actual_coverage_achieved: float = 0.0
    
    # Implementation tracking
    implementation_barriers: List[ImplementationBarrier] = field(default_factory=list)
    phase_completion: Dict[str, float] = field(default_factory=dict)  # Phase -> % complete
    
    # Quality metrics
    adherence_to_protocol: float = 0.0    # Protocol adherence (0-1)
    quality_score: float = 0.0            # Overall quality (0-1)
    safety_incidents: int = 0
    adverse_events: int = 0
    
    # Outcome measurement
    primary_outcome_measured: bool = False
    primary_outcome_value: float = 0.0
    secondary_outcomes: Dict[str, float] = field(default_factory=dict)
    outcome_classification: InterventionOutcome = InterventionOutcome.UNKNOWN
    
    # Cost tracking
    planned_cost: float = 0.0
    actual_cost: float = 0.0
    cost_per_person_reached: float = 0.0
    
    # Performance summary
    overall_effectiveness: float = 0.0     # Combined effectiveness score
    implementation_success: float = 0.0    # Implementation quality score
    stakeholder_satisfaction: float = 0.0  # Stakeholder feedback
    
    # Key insights
    lessons_learned: List[str] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    improvement_recommendations: List[str] = field(default_factory=list)

class InterventionLibrary:
    """Library of evidence-based intervention protocols."""
    
    def __init__(self):
        self.protocols: Dict[str, InterventionProtocol] = {}
        self._initialize_standard_protocols()
        
        logger.info("Intervention Protocol Library initialized")
    
    def _initialize_standard_protocols(self):
        """Initialize standard One Health intervention protocols."""
        
        # Medical interventions
        self._add_medical_protocols()
        
        # Environmental interventions
        self._add_environmental_protocols()
        
        # Behavioral interventions
        self._add_behavioral_protocols()
        
        # Administrative interventions
        self._add_administrative_protocols()
    
    def _add_medical_protocols(self):
        """Add medical intervention protocols."""
        
        # Vaccination protocol
        vaccination_protocol = InterventionProtocol(
            protocol_id="VAC_STANDARD_001",
            protocol_name="Mass Vaccination Campaign",
            intervention_category=InterventionCategory.MEDICAL,
            intervention_target=InterventionTarget.HUMAN_POPULATION,
            strategy=InterventionStrategy.TARGETED_PREVENTION,
            description="Systematic vaccination of target populations to prevent disease transmission",
            standard_operating_procedures=[
                "Establish vaccination sites",
                "Train vaccination personnel",
                "Implement cold chain management",
                "Administer vaccines according to schedule",
                "Monitor adverse events",
                "Document vaccination coverage"
            ],
            required_training=[
                "Vaccine administration certification",
                "Cold chain management",
                "Adverse event recognition",
                "Documentation procedures"
            ],
            quality_indicators=[
                "Vaccination coverage rate >80%",
                "Cold chain maintenance 100%",
                "Adverse event rate <1%",
                "Documentation completeness >95%"
            ],
            personnel_requirements={
                "nurses": 10,
                "physicians": 2,
                "administrators": 3,
                "logistics_staff": 5
            },
            equipment_requirements={
                "refrigeration_units": 3,
                "vaccination_supplies": 1000,
                "documentation_systems": 5
            },
            typical_duration_days=21,
            evidence_level="randomized",
            success_rate_reported=0.85,
            confidence_interval=(0.78, 0.92)
        )
        
        # Add parameters
        vaccination_protocol.parameters = [
            InterventionParameter("coverage_rate", "Target Coverage Rate", "coverage", 0.8, 0.85, 0.7, 0.95, "%"),
            InterventionParameter("dose_schedule", "Vaccination Schedule", "frequency", "single", "single", None, None, "doses"),
            InterventionParameter("target_age_groups", "Target Age Groups", "demographic", "all_adults", "high_risk_first", None, None, "groups")
        ]
        
        self.protocols[vaccination_protocol.protocol_id] = vaccination_protocol
        
        # Quarantine protocol
        quarantine_protocol = InterventionProtocol(
            protocol_id="QUA_STANDARD_001",
            protocol_name="Isolation and Quarantine",
            intervention_category=InterventionCategory.MEDICAL,
            intervention_target=InterventionTarget.HUMAN_POPULATION,
            strategy=InterventionStrategy.IMMEDIATE_CONTAINMENT,
            description="Isolation of cases and quarantine of contacts to prevent transmission",
            standard_operating_procedures=[
                "Identify cases and contacts",
                "Assess isolation/quarantine needs",
                "Establish isolation facilities",
                "Implement monitoring protocols",
                "Provide support services",
                "Monitor compliance"
            ],
            required_training=[
                "Contact tracing procedures",
                "Isolation protocols",
                "Monitoring techniques",
                "Support service delivery"
            ],
            quality_indicators=[
                "Contact identification rate >90%",
                "Quarantine compliance >85%",
                "Monitoring frequency 100%",
                "Support service delivery >95%"
            ],
            personnel_requirements={
                "contact_tracers": 15,
                "case_managers": 8,
                "support_staff": 10
            },
            typical_duration_days=14,
            evidence_level="controlled",
            success_rate_reported=0.75,
            confidence_interval=(0.65, 0.85)
        )
        
        self.protocols[quarantine_protocol.protocol_id] = quarantine_protocol
    
    def _add_environmental_protocols(self):
        """Add environmental intervention protocols."""
        
        # Vector control protocol
        vector_control = InterventionProtocol(
            protocol_id="VEC_STANDARD_001",
            protocol_name="Integrated Vector Management",
            intervention_category=InterventionCategory.ENVIRONMENTAL,
            intervention_target=InterventionTarget.VECTORS,
            strategy=InterventionStrategy.COMPREHENSIVE_RESPONSE,
            description="Comprehensive vector control using multiple intervention methods",
            standard_operating_procedures=[
                "Conduct vector surveillance",
                "Apply larvicide treatments",
                "Implement adult control measures",
                "Eliminate breeding sites",
                "Monitor resistance patterns",
                "Evaluate control effectiveness"
            ],
            quality_indicators=[
                "Vector density reduction >70%",
                "Breeding site elimination >80%",
                "Treatment coverage >90%",
                "Resistance monitoring 100%"
            ],
            personnel_requirements={
                "entomologists": 3,
                "field_technicians": 12,
                "supervisors": 2
            },
            equipment_requirements={
                "spraying_equipment": 10,
                "monitoring_traps": 50,
                "vehicles": 5
            },
            typical_duration_days=60,
            evidence_level="controlled",
            success_rate_reported=0.72,
            confidence_interval=(0.62, 0.82)
        )
        
        self.protocols[vector_control.protocol_id] = vector_control
    
    def _add_behavioral_protocols(self):
        """Add behavioral intervention protocols."""
        
        # Risk communication protocol
        risk_communication = InterventionProtocol(
            protocol_id="COM_STANDARD_001",
            protocol_name="Risk Communication Campaign",
            intervention_category=InterventionCategory.BEHAVIORAL,
            intervention_target=InterventionTarget.HUMAN_POPULATION,
            strategy=InterventionStrategy.EVIDENCE_BASED,
            description="Systematic risk communication to promote protective behaviors",
            standard_operating_procedures=[
                "Develop key messages",
                "Identify target audiences",
                "Select communication channels",
                "Implement outreach activities",
                "Monitor message uptake",
                "Adapt based on feedback"
            ],
            quality_indicators=[
                "Message reach >85% of target population",
                "Message comprehension >80%",
                "Behavioral uptake >60%",
                "Credibility rating >4.0/5.0"
            ],
            personnel_requirements={
                "communication_specialists": 5,
                "community_liaisons": 8,
                "translators": 4
            },
            typical_duration_days=45,
            evidence_level="observational",
            success_rate_reported=0.68,
            confidence_interval=(0.55, 0.78)
        )
        
        self.protocols[risk_communication.protocol_id] = risk_communication
    
    def _add_administrative_protocols(self):
        """Add administrative intervention protocols."""
        
        # Movement restriction protocol
        movement_restriction = InterventionProtocol(
            protocol_id="MOV_STANDARD_001",
            protocol_name="Movement Restrictions",
            intervention_category=InterventionCategory.ADMINISTRATIVE,
            intervention_target=InterventionTarget.HUMAN_POPULATION,
            strategy=InterventionStrategy.IMMEDIATE_CONTAINMENT,
            description="Coordinated movement restrictions to limit disease spread",
            standard_operating_procedures=[
                "Define restriction zones",
                "Implement checkpoints",
                "Issue movement permits",
                "Enforce restrictions",
                "Monitor compliance",
                "Adjust restrictions based on epidemiology"
            ],
            quality_indicators=[
                "Compliance rate >80%",
                "Permit processing <24 hours",
                "Enforcement coverage >95%",
                "Public acceptance >60%"
            ],
            personnel_requirements={
                "enforcement_officers": 20,
                "administrators": 5,
                "checkpoint_staff": 30
            },
            typical_duration_days=28,
            evidence_level="observational",
            success_rate_reported=0.65,
            confidence_interval=(0.50, 0.78)
        )
        
        self.protocols[movement_restriction.protocol_id] = movement_restriction

class InterventionManager:
    """Central intervention management system."""
    
    def __init__(self):
        self.protocol_library = InterventionLibrary()
        self.active_executions: Dict[str, InterventionExecution] = {}
        self.completed_executions: List[InterventionExecution] = []
        self.performance_metrics: Dict[str, Any] = {}
        
        logger.info("One Health Intervention Manager initialized")
    
    def plan_intervention(self, protocol_id: str, target_population: str,
                         target_location: str, population_size: int,
                         start_date: datetime = None) -> InterventionExecution:
        """Plan intervention execution based on protocol."""
        
        if protocol_id not in self.protocol_library.protocols:
            raise ValueError(f"Protocol {protocol_id} not found in library")
        
        protocol = self.protocol_library.protocols[protocol_id]
        
        if start_date is None:
            start_date = datetime.now() + timedelta(hours=protocol.preparation_time_hours)
        
        execution_id = f"EXEC_{random.randint(100000, 999999)}"
        
        # Calculate planned end date
        planned_duration = protocol.typical_duration_days
        planned_end = start_date + timedelta(days=planned_duration)
        
        # Estimate costs
        base_cost = population_size * random.uniform(10, 50)  # $10-50 per person
        resource_cost = len(protocol.personnel_requirements) * 1000  # Personnel costs
        equipment_cost = len(protocol.equipment_requirements) * 500   # Equipment costs
        total_planned_cost = base_cost + resource_cost + equipment_cost
        
        execution = InterventionExecution(
            execution_id=execution_id,
            protocol_id=protocol_id,
            protocol_name=protocol.protocol_name,
            target_population=target_population,
            target_location=target_location,
            planned_start=start_date,
            planned_end=planned_end,
            target_population_size=population_size,
            target_coverage_rate=0.8,  # Default 80% target
            planned_cost=total_planned_cost
        )
        
        # Initialize phase tracking
        for phase in protocol.implementation_phases:
            execution.phase_completion[phase.value] = 0.0
        
        # Generate potential barriers based on intervention type
        execution.implementation_barriers = self._generate_potential_barriers(protocol)
        
        self.active_executions[execution_id] = execution
        
        logger.info(f"Intervention planned: {execution_id}")
        
        return execution
    
    def _generate_potential_barriers(self, protocol: InterventionProtocol) -> List[ImplementationBarrier]:
        """Generate potential implementation barriers."""
        
        potential_barriers = []
        
        # Resource barriers
        if len(protocol.personnel_requirements) > 5:
            barrier = ImplementationBarrier(
                barrier_id=f"BAR_{random.randint(1000, 9999)}",
                barrier_type="resource",
                description="Insufficient trained personnel available",
                severity="medium",
                impact_area="implementation_capacity",
                mitigation_strategy="Recruit and train additional staff",
                mitigation_cost=15000,
                mitigation_timeline=14
            )
            potential_barriers.append(barrier)
        
        # Logistical barriers
        if protocol.intervention_target == InterventionTarget.VECTORS:
            barrier = ImplementationBarrier(
                barrier_id=f"BAR_{random.randint(1000, 9999)}",
                barrier_type="logistical",
                description="Limited access to vector breeding sites",
                severity="medium",
                impact_area="coverage_achievement",
                mitigation_strategy="Coordinate with property owners for site access",
                mitigation_cost=5000,
                mitigation_timeline=7
            )
            potential_barriers.append(barrier)
        
        # Social barriers
        if protocol.intervention_category == InterventionCategory.BEHAVIORAL:
            barrier = ImplementationBarrier(
                barrier_id=f"BAR_{random.randint(1000, 9999)}",
                barrier_type="social",
                description="Community resistance to behavior change",
                severity="high",
                impact_area="effectiveness",
                mitigation_strategy="Implement community engagement and education",
                mitigation_cost=20000,
                mitigation_timeline=21
            )
            potential_barriers.append(barrier)
        
        return potential_barriers
    
    def execute_intervention(self, execution_id: str) -> bool:
        """Begin intervention execution."""
        
        if execution_id not in self.active_executions:
            return False
        
        execution = self.active_executions[execution_id]
        execution.actual_start = datetime.now()
        execution.current_phase = ImplementationPhase.IMPLEMENTATION
        
        # Initialize implementation tracking
        execution.adherence_to_protocol = random.uniform(0.7, 0.95)
        execution.quality_score = random.uniform(0.6, 0.9)
        
        logger.info(f"Intervention execution started: {execution_id}")
        
        return True
    
    def update_execution_progress(self, execution_id: str, phase: ImplementationPhase,
                                progress: float, quality_metrics: Dict[str, float] = None):
        """Update intervention execution progress."""
        
        if execution_id not in self.active_executions:
            return False
        
        execution = self.active_executions[execution_id]
        
        # Update phase progress
        execution.phase_completion[phase.value] = min(100.0, max(0.0, progress))
        execution.current_phase = phase
        
        # Update quality metrics if provided
        if quality_metrics:
            execution.adherence_to_protocol = quality_metrics.get("adherence", execution.adherence_to_protocol)
            execution.quality_score = quality_metrics.get("quality", execution.quality_score)
            execution.actual_coverage_achieved = quality_metrics.get("coverage", execution.actual_coverage_achieved)
        
        # Check for completion
        if phase == ImplementationPhase.EVALUATION and progress >= 100.0:
            self._complete_intervention(execution_id)
        
        logger.info(f"Progress updated for {execution_id}: {phase.value} {progress:.1f}%")
        
        return True
    
    def _complete_intervention(self, execution_id: str):
        """Complete intervention and calculate final outcomes."""
        
        execution = self.active_executions[execution_id]
        execution.actual_end = datetime.now()
        execution.primary_outcome_measured = True
        
        # Calculate effectiveness based on multiple factors
        protocol_success_rate = 0.7  # Default baseline
        if execution.protocol_id in self.protocol_library.protocols:
            protocol = self.protocol_library.protocols[execution.protocol_id]
            protocol_success_rate = protocol.success_rate_reported
        
        implementation_quality_factor = execution.quality_score
        coverage_factor = execution.actual_coverage_achieved / execution.target_coverage_rate
        
        # Calculate primary outcome
        execution.primary_outcome_value = (protocol_success_rate * 
                                         implementation_quality_factor * 
                                         min(1.0, coverage_factor))
        
        # Classify outcome
        if execution.primary_outcome_value >= 0.9:
            execution.outcome_classification = InterventionOutcome.HIGHLY_EFFECTIVE
        elif execution.primary_outcome_value >= 0.7:
            execution.outcome_classification = InterventionOutcome.EFFECTIVE
        elif execution.primary_outcome_value >= 0.5:
            execution.outcome_classification = InterventionOutcome.MODERATELY_EFFECTIVE
        elif execution.primary_outcome_value >= 0.3:
            execution.outcome_classification = InterventionOutcome.LIMITED_EFFECTIVENESS
        else:
            execution.outcome_classification = InterventionOutcome.INEFFECTIVE
        
        # Calculate overall effectiveness
        execution.overall_effectiveness = execution.primary_outcome_value
        execution.implementation_success = (execution.quality_score + 
                                          execution.adherence_to_protocol) / 2
        
        # Generate lessons learned
        execution.lessons_learned = self._generate_lessons_learned(execution)
        
        # Calculate actual costs
        duration_days = (execution.actual_end - execution.actual_start).days
        cost_factor = 1.0 + random.uniform(-0.2, 0.3)  # +/- 20-30% variance
        execution.actual_cost = execution.planned_cost * cost_factor
        
        if execution.actual_coverage_achieved > 0:
            people_reached = execution.target_population_size * execution.actual_coverage_achieved
            execution.cost_per_person_reached = execution.actual_cost / people_reached
        
        # Move to completed executions
        self.completed_executions.append(execution)
        del self.active_executions[execution_id]
        
        logger.info(f"Intervention completed: {execution_id}")
    
    def _generate_lessons_learned(self, execution: InterventionExecution) -> List[str]:
        """Generate lessons learned based on execution performance."""
        
        lessons = []
        
        # Coverage-based lessons
        if execution.actual_coverage_achieved < 0.7:
            lessons.append("Low coverage achieved - consider enhanced outreach strategies")
        elif execution.actual_coverage_achieved > 0.9:
            lessons.append("Excellent coverage achieved - effective community engagement")
        
        # Quality-based lessons
        if execution.quality_score < 0.6:
            lessons.append("Quality issues identified - strengthen training and supervision")
        elif execution.quality_score > 0.85:
            lessons.append("High quality implementation - protocols well-followed")
        
        # Barrier-based lessons
        unresolved_barriers = [b for b in execution.implementation_barriers if not b.is_resolved]
        if len(unresolved_barriers) > 2:
            lessons.append("Multiple implementation barriers - improve planning phase")
        
        # Effectiveness-based lessons
        if execution.overall_effectiveness > 0.8:
            lessons.append("Intervention highly successful - consider scaling approach")
        elif execution.overall_effectiveness < 0.5:
            lessons.append("Limited effectiveness - review intervention design and implementation")
        
        return lessons
    
    def get_intervention_summary(self) -> Dict[str, Any]:
        """Get comprehensive intervention management summary."""
        
        all_executions = list(self.active_executions.values()) + self.completed_executions
        
        if not all_executions:
            return {"message": "No interventions executed"}
        
        # Execution statistics
        execution_stats = {
            "total_interventions": len(all_executions),
            "active_interventions": len(self.active_executions),
            "completed_interventions": len(self.completed_executions)
        }
        
        # Protocol usage
        protocol_usage = defaultdict(int)
        for execution in all_executions:
            protocol_usage[execution.protocol_name] += 1
        
        # Outcome distribution
        outcome_dist = defaultdict(int)
        effectiveness_scores = []
        for execution in self.completed_executions:
            outcome_dist[execution.outcome_classification.value] += 1
            effectiveness_scores.append(execution.overall_effectiveness)
        
        # Cost analysis
        total_planned_cost = sum(e.planned_cost for e in all_executions)
        total_actual_cost = sum(e.actual_cost for e in self.completed_executions)
        
        # Coverage analysis
        coverage_rates = [e.actual_coverage_achieved for e in all_executions 
                         if e.actual_coverage_achieved > 0]
        
        # Performance metrics
        avg_effectiveness = statistics.mean(effectiveness_scores) if effectiveness_scores else 0.0
        avg_coverage = statistics.mean(coverage_rates) if coverage_rates else 0.0
        
        return {
            "execution_statistics": execution_stats,
            "protocol_usage": dict(protocol_usage),
            "outcome_distribution": dict(outcome_dist),
            "cost_analysis": {
                "total_planned_cost": total_planned_cost,
                "total_actual_cost": total_actual_cost,
                "cost_variance": total_actual_cost - total_planned_cost if total_actual_cost > 0 else 0
            },
            "performance_metrics": {
                "average_effectiveness": avg_effectiveness,
                "average_coverage": avg_coverage,
                "total_people_reached": sum(e.target_population_size * e.actual_coverage_achieved 
                                           for e in all_executions if e.actual_coverage_achieved > 0)
            },
            "protocol_library_size": len(self.protocol_library.protocols)
        }

def run_demonstration() -> InterventionManager:
    """Run comprehensive intervention management demonstration."""
    
    print("💉 One Health Intervention Management System - Demonstration")
    print("=" * 75)
    
    manager = InterventionManager()
    
    # Display available protocols
    print(f"\n📋 Available Intervention Protocols:")
    for protocol_id, protocol in manager.protocol_library.protocols.items():
        print(f"  {protocol_id}: {protocol.protocol_name}")
        print(f"    Category: {protocol.intervention_category.value.title()}")
        print(f"    Target: {protocol.intervention_target.value.replace('_', ' ').title()}")
        print(f"    Evidence: {protocol.evidence_level.title()}")
        print(f"    Success Rate: {protocol.success_rate_reported:.1%}")
    
    # Plan multiple interventions
    intervention_scenarios = [
        {
            "protocol_id": "VAC_STANDARD_001",
            "target_population": "Healthcare Workers",
            "target_location": "Metropolitan Area",
            "population_size": 5000
        },
        {
            "protocol_id": "QUA_STANDARD_001",
            "target_population": "Outbreak Contacts",
            "target_location": "Affected Districts",
            "population_size": 1200
        },
        {
            "protocol_id": "VEC_STANDARD_001",
            "target_population": "Vector Habitats",
            "target_location": "Coastal Region",
            "population_size": 100000  # Area coverage equivalent
        },
        {
            "protocol_id": "COM_STANDARD_001",
            "target_population": "General Public",
            "target_location": "State-wide",
            "population_size": 50000
        },
        {
            "protocol_id": "MOV_STANDARD_001",
            "target_population": "Travelers",
            "target_location": "Border Areas",
            "population_size": 25000
        }
    ]
    
    print(f"\n💉 Planning Interventions...")
    
    # Plan interventions
    executions = []
    for scenario in intervention_scenarios:
        execution = manager.plan_intervention(
            protocol_id=scenario["protocol_id"],
            target_population=scenario["target_population"],
            target_location=scenario["target_location"],
            population_size=scenario["population_size"]
        )
        executions.append(execution)
        print(f"✅ Planned: {execution.protocol_name} - {execution.target_population}")
    
    print(f"\n🚀 Executing Interventions...")
    
    # Execute interventions
    for execution in executions:
        manager.execute_intervention(execution.execution_id)
        print(f"🏃‍♂️ Started: {execution.execution_id}")
    
    print(f"\n📈 Simulating Implementation Progress...")
    
    # Simulate implementation progress
    phases = [
        ImplementationPhase.PREPARATION,
        ImplementationPhase.IMPLEMENTATION, 
        ImplementationPhase.MONITORING,
        ImplementationPhase.EVALUATION
    ]
    
    for execution in executions:
        for phase in phases:
            # Simulate realistic progress
            progress = random.uniform(75, 100)
            coverage = random.uniform(0.65, 0.95)
            quality = random.uniform(0.6, 0.9)
            adherence = random.uniform(0.7, 0.95)
            
            quality_metrics = {
                "coverage": coverage,
                "quality": quality,
                "adherence": adherence
            }
            
            manager.update_execution_progress(
                execution.execution_id,
                phase,
                progress,
                quality_metrics
            )
            
            if phase == ImplementationPhase.EVALUATION:
                print(f"  ✅ Completed: {execution.protocol_name} - {coverage:.1%} coverage, {quality:.1%} quality")
    
    return manager

def display_intervention_results(manager: InterventionManager):
    """Display comprehensive intervention management results."""
    
    all_executions = list(manager.active_executions.values()) + manager.completed_executions
    
    print(f"\n💉 Intervention Management Results ({len(all_executions)} total):")
    
    for i, execution in enumerate(all_executions, 1):
        print(f"\n{i}. {execution.protocol_name}")
        print(f"   Target: {execution.target_population} ({execution.target_population_size:,} people)")
        print(f"   Location: {execution.target_location}")
        print(f"   Status: {execution.current_phase.value.replace('_', ' ').title()}")
        
        if execution in manager.completed_executions:
            print(f"   Outcome: {execution.outcome_classification.value.replace('_', ' ').title()}")
            print(f"   Effectiveness: {execution.overall_effectiveness:.1%}")
            print(f"   Coverage Achieved: {execution.actual_coverage_achieved:.1%}")
            print(f"   Quality Score: {execution.quality_score:.1%}")
            print(f"   Cost per Person: ${execution.cost_per_person_reached:.2f}")
            
            if execution.lessons_learned:
                print(f"   Key Lessons ({len(execution.lessons_learned)}):")
                for lesson in execution.lessons_learned[:2]:
                    print(f"     • {lesson}")
        else:
            overall_progress = sum(execution.phase_completion.values()) / len(execution.phase_completion) if execution.phase_completion else 0
            print(f"   Progress: {overall_progress:.1f}%")
            print(f"   Target Coverage: {execution.target_coverage_rate:.1%}")
        
        if execution.implementation_barriers:
            resolved_barriers = sum(1 for b in execution.implementation_barriers if b.is_resolved)
            print(f"   Barriers: {resolved_barriers}/{len(execution.implementation_barriers)} resolved")
    
    # Summary statistics
    summary = manager.get_intervention_summary()
    
    print(f"\n📊 Intervention Management Summary:")
    print(f"  Total Interventions: {summary['execution_statistics']['total_interventions']}")
    print(f"  Completed Interventions: {summary['execution_statistics']['completed_interventions']}")
    print(f"  Available Protocols: {summary['protocol_library_size']}")
    
    print(f"\n💰 Cost Analysis:")
    cost = summary["cost_analysis"]
    print(f"  Total Planned Cost: ${cost['total_planned_cost']:,.0f}")
    if cost['total_actual_cost'] > 0:
        print(f"  Total Actual Cost: ${cost['total_actual_cost']:,.0f}")
        print(f"  Cost Variance: ${cost['cost_variance']:,.0f}")
    
    print(f"\n📈 Performance Metrics:")
    perf = summary["performance_metrics"]
    print(f"  Average Effectiveness: {perf['average_effectiveness']:.1%}")
    print(f"  Average Coverage: {perf['average_coverage']:.1%}")
    print(f"  Total People Reached: {perf['total_people_reached']:,.0f}")
    
    print(f"\n📋 Protocol Usage:")
    for protocol, count in summary["protocol_usage"].items():
        print(f"  {protocol}: {count} execution(s)")
    
    print(f"\n🏆 Outcome Distribution:")
    for outcome, count in summary["outcome_distribution"].items():
        print(f"  {outcome.replace('_', ' ').title()}: {count}")
    
    print(f"\n🏆 TOP PERFORMING Interventions:")
    top_interventions = sorted(manager.completed_executions, 
                              key=lambda e: e.overall_effectiveness, reverse=True)[:3]
    for i, intervention in enumerate(top_interventions, 1):
        print(f"  {i}. {intervention.protocol_name}")
        print(f"     Effectiveness: {intervention.overall_effectiveness:.1%}")
        print(f"     Coverage: {intervention.actual_coverage_achieved:.1%}")
        print(f"     Quality: {intervention.quality_score:.1%}")
        print(f"     Cost: ${intervention.actual_cost:,.0f}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    intervention_manager = run_demonstration()
    display_intervention_results(intervention_manager)
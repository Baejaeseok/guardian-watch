"""
Module 40: training.py
Training & Capacity Building System for One Health
Zoonotic Disease Surveillance and Response Workforce
"""

import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class TrainingCategory(Enum):
    EPIDEMIOLOGY = "epidemiology"
    CLINICAL_MANAGEMENT = "clinical_management"
    LABORATORY = "laboratory"
    FIELD_RESPONSE = "field_response"
    ONE_HEALTH = "one_health"
    DATA_ANALYTICS = "data_analytics"
    RISK_COMMUNICATION = "risk_communication"
    IHR_COMPLIANCE = "ihr_compliance"

class DeliveryMode(Enum):
    IN_PERSON = "in_person"
    ONLINE = "online"
    HYBRID = "hybrid"
    SIMULATION = "simulation"
    ON_THE_JOB = "on_the_job"
    SELF_PACED = "self_paced"

class CompetencyLevel(Enum):
    NOVICE = "novice"
    BEGINNER = "beginner"
    COMPETENT = "competent"
    PROFICIENT = "proficient"
    EXPERT = "expert"

class TrainingStatus(Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    POSTPONED = "postponed"

class AssessmentType(Enum):
    PRE_TEST = "pre_test"
    POST_TEST = "post_test"
    PRACTICAL_EXAM = "practical_exam"
    SIMULATION = "simulation"
    PORTFOLIO = "portfolio"
    PEER_ASSESSMENT = "peer_assessment"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class LearningObjective:
    objective_id: str
    description: str
    domain: str         # knowledge / skills / attitudes
    bloom_level: str    # remember / understand / apply / analyze / evaluate / create
    assessment_method: str
    time_to_achieve_hours: float

@dataclass
class TrainingModule:
    module_id: str
    title: str
    category: TrainingCategory
    description: str
    duration_hours: float
    delivery_mode: DeliveryMode
    target_audience: list
    prerequisites: list
    learning_objectives: list
    competency_level: CompetencyLevel
    max_participants: int
    language: str
    certification_awarded: bool
    ceu_credits: float  # continuing education units

@dataclass
class TrainingParticipant:
    participant_id: str
    name: str
    profession: str
    organization: str
    country: str
    current_competency: CompetencyLevel
    target_competency: CompetencyLevel
    enrolled_modules: list
    completed_modules: list
    certifications: list
    training_hours: float

@dataclass
class TrainingSession:
    session_id: str
    module_id: str
    facilitator: str
    location: str
    start_date: str
    end_date: str
    participants: list
    status: TrainingStatus
    pre_test_avg: float
    post_test_avg: float
    completion_rate: float
    satisfaction_score: float

@dataclass
class CompetencyAssessment:
    assessment_id: str
    participant_id: str
    module_id: str
    assessment_type: AssessmentType
    score: float          # 0-100
    passing_score: float  # e.g. 70
    passed: bool
    date: str
    feedback: str

@dataclass
class CapacityGap:
    gap_id: str
    domain: str
    description: str
    affected_roles: list
    severity: str         # critical / high / moderate / low
    estimated_staff_affected: int
    recommended_training: str
    priority_rank: int


# ============================================================
# CURRICULUM BUILDER
# ============================================================

class OneHealthCurriculumBuilder:
    """
    Builds comprehensive One Health training curricula
    """

    def __init__(self):
        self.core_modules = self._build_core_curriculum()

    def _build_core_curriculum(self) -> list:
        modules = [
            TrainingModule(
                "MOD_001", "One Health Foundations",
                TrainingCategory.ONE_HEALTH,
                "Introduction to One Health concept, human-animal-environment interface, and integrated surveillance",
                16.0, DeliveryMode.HYBRID,
                ["epidemiologists", "public_health_officers", "veterinarians", "environmental_health_officers"],
                [], [], CompetencyLevel.BEGINNER, 30, "English", True, 1.6
            ),
            TrainingModule(
                "MOD_002", "Zoonotic Disease Epidemiology",
                TrainingCategory.EPIDEMIOLOGY,
                "Advanced epidemiology of zoonotic diseases: H5N1, MERS, Brucellosis, Leptospirosis, Rabies",
                24.0, DeliveryMode.IN_PERSON,
                ["epidemiologists", "field_investigators"],
                ["MOD_001"], [], CompetencyLevel.COMPETENT, 25, "English", True, 2.4
            ),
            TrainingModule(
                "MOD_003", "Field Epidemiology & Outbreak Investigation",
                TrainingCategory.FIELD_RESPONSE,
                "Hands-on field investigation techniques: case finding, contact tracing, environmental sampling",
                40.0, DeliveryMode.SIMULATION,
                ["field_epidemiologists", "disease_detectives"],
                ["MOD_002"], [], CompetencyLevel.PROFICIENT, 20, "English", True, 4.0
            ),
            TrainingModule(
                "MOD_004", "One Health Laboratory Diagnostics",
                TrainingCategory.LABORATORY,
                "Laboratory methods for zoonotic pathogen detection: PCR, serology, culture, genomics",
                32.0, DeliveryMode.IN_PERSON,
                ["laboratory_scientists", "veterinary_diagnosticians"],
                [], [], CompetencyLevel.COMPETENT, 15, "English", True, 3.2
            ),
            TrainingModule(
                "MOD_005", "Risk Communication for Health Emergencies",
                TrainingCategory.RISK_COMMUNICATION,
                "CERC principles, crisis communication, media relations, misinformation management",
                16.0, DeliveryMode.HYBRID,
                ["spokespersons", "public_health_officers", "all_staff"],
                [], [], CompetencyLevel.COMPETENT, 40, "English", True, 1.6
            ),
            TrainingModule(
                "MOD_006", "Health Data Analytics & Surveillance Systems",
                TrainingCategory.DATA_ANALYTICS,
                "Epidemiological data analysis, GIS mapping, outbreak detection algorithms, dashboard development",
                24.0, DeliveryMode.ONLINE,
                ["data_analysts", "epidemiologists"],
                [], [], CompetencyLevel.COMPETENT, 35, "English", True, 2.4
            ),
            TrainingModule(
                "MOD_007", "IHR 2005 Core Capacities",
                TrainingCategory.IHR_COMPLIANCE,
                "International Health Regulations: notification obligations, core capacities, JEE indicators",
                16.0, DeliveryMode.ONLINE,
                ["senior_officials", "ihr_focal_points"],
                [], [], CompetencyLevel.COMPETENT, 30, "English", True, 1.6
            ),
            TrainingModule(
                "MOD_008", "Clinical Management of Zoonotic Diseases",
                TrainingCategory.CLINICAL_MANAGEMENT,
                "Clinical recognition, case management, infection prevention, ICU protocols for zoonotic diseases",
                24.0, DeliveryMode.HYBRID,
                ["physicians", "nurses", "clinical_officers"],
                [], [], CompetencyLevel.PROFICIENT, 30, "English", True, 2.4
            ),
            TrainingModule(
                "MOD_009", "One Health Emergency Operations",
                TrainingCategory.ONE_HEALTH,
                "Incident Command System, EOC operations, multi-sector coordination, resource management",
                32.0, DeliveryMode.SIMULATION,
                ["emergency_managers", "senior_officials"],
                ["MOD_001", "MOD_007"], [], CompetencyLevel.PROFICIENT, 20, "English", True, 3.2
            ),
            TrainingModule(
                "MOD_010", "Advanced Zoonotic Disease Management",
                TrainingCategory.ONE_HEALTH,
                "Master-level integration of epidemiology, response, analytics, and policy for One Health leaders",
                80.0, DeliveryMode.HYBRID,
                ["senior_epidemiologists", "program_directors"],
                ["MOD_002", "MOD_003", "MOD_006"], [], CompetencyLevel.EXPERT, 15, "English", True, 8.0
            )
        ]

        # Add learning objectives to each module
        for mod in modules:
            mod.learning_objectives = self._generate_objectives(mod)

        return modules

    def _generate_objectives(self, module: TrainingModule) -> list:
        obj_templates = {
            TrainingCategory.ONE_HEALTH: [
                ("Explain the One Health approach and its application to zoonotic disease control", "knowledge", "understand"),
                ("Apply integrated surveillance methods across human, animal, and environmental sectors", "skills", "apply"),
                ("Coordinate multi-sector One Health response teams effectively", "skills", "apply"),
            ],
            TrainingCategory.EPIDEMIOLOGY: [
                ("Calculate key epidemiological parameters including R0, CFR, and attack rates", "knowledge", "apply"),
                ("Design and conduct outbreak investigations following standard protocols", "skills", "apply"),
                ("Analyze epidemiological data to identify transmission patterns", "skills", "analyze"),
            ],
            TrainingCategory.FIELD_RESPONSE: [
                ("Conduct field investigation including case finding and environmental sampling", "skills", "apply"),
                ("Manage contact tracing operations for high-risk contacts", "skills", "apply"),
                ("Document findings according to standard formats", "knowledge", "apply"),
            ]
        }

        templates = obj_templates.get(module.category, [
            (f"Demonstrate competency in {module.category.value}", "skills", "apply"),
            (f"Apply {module.title} principles in practice", "skills", "apply"),
        ])

        return [
            LearningObjective(
                f"OBJ_{module.module_id}_{i+1:02d}",
                desc, domain, bloom,
                "written_test" if bloom in ["remember", "understand"] else "practical_assessment",
                module.duration_hours / len(templates)
            )
            for i, (desc, domain, bloom) in enumerate(templates)
        ]

    def get_recommended_modules(self, role: str, current_level: CompetencyLevel) -> list:
        """Get recommended training modules for a role"""
        role_module_map = {
            "epidemiologist": ["MOD_001", "MOD_002", "MOD_003", "MOD_006"],
            "veterinarian": ["MOD_001", "MOD_004", "MOD_002"],
            "physician": ["MOD_001", "MOD_008", "MOD_005"],
            "laboratory_scientist": ["MOD_004", "MOD_001"],
            "emergency_manager": ["MOD_009", "MOD_007", "MOD_005"],
            "public_health_officer": ["MOD_001", "MOD_005", "MOD_007", "MOD_006"]
        }

        recommended_ids = role_module_map.get(role.lower().replace(" ", "_"), ["MOD_001"])
        return [m for m in self.core_modules if m.module_id in recommended_ids]

    def get_curriculum_summary(self) -> dict:
        total_hours = sum(m.duration_hours for m in self.core_modules)
        total_credits = sum(m.ceu_credits for m in self.core_modules)
        return {
            "total_modules": len(self.core_modules),
            "total_training_hours": total_hours,
            "total_ceu_credits": total_credits,
            "categories": list(set(m.category.value for m in self.core_modules)),
            "delivery_modes": list(set(m.delivery_mode.value for m in self.core_modules)),
            "certifications_offered": sum(1 for m in self.core_modules if m.certification_awarded)
        }


# ============================================================
# PARTICIPANT TRACKER
# ============================================================

class ParticipantTracker:
    """
    Tracks participant progress, assessments, and certifications
    """

    def __init__(self):
        self.participants = self._initialize_participants()

    def _initialize_participants(self) -> list:
        roles = [
            ("Dr. Alice Kim", "Field Epidemiologist", "Ministry of Health", "National"),
            ("Dr. John Osei", "Senior Veterinarian", "Ministry of Agriculture", "Regional"),
            ("Sarah Lee", "Public Health Officer", "City Health Department", "Local"),
            ("Dr. Maria Santos", "Laboratory Director", "National Reference Lab", "National"),
            ("James Otieno", "Emergency Manager", "NDMA", "National"),
            ("Dr. Fatima Al-Rashid", "Infectious Disease Physician", "Teaching Hospital", "Regional"),
            ("Chen Wei", "Data Analyst", "Surveillance Division", "National"),
            ("Aisha Diallo", "IHR Focal Point", "Ministry of Health", "National")
        ]

        participants = []
        for i, (name, profession, org, level) in enumerate(roles):
            current_lvl = random.choice([CompetencyLevel.BEGINNER, CompetencyLevel.COMPETENT, CompetencyLevel.NOVICE])
            target_lvl = CompetencyLevel.PROFICIENT if current_lvl != CompetencyLevel.EXPERT else CompetencyLevel.EXPERT

            completed = random.sample(["MOD_001", "MOD_005"], k=random.randint(0, 2))
            enrolled = random.sample(["MOD_002", "MOD_003", "MOD_006"], k=random.randint(1, 2))

            p = TrainingParticipant(
                participant_id=f"PART_{i+1:03d}",
                name=name,
                profession=profession,
                organization=org,
                country="Multi-national",
                current_competency=current_lvl,
                target_competency=target_lvl,
                enrolled_modules=[m for m in enrolled if m not in completed],
                completed_modules=completed,
                certifications=[f"One Health Foundations Certificate" for _ in completed[:1]],
                training_hours=random.uniform(8, 120)
            )
            participants.append(p)

        return participants

    def assess_participant(self, participant_id: str, module_id: str,
                           assessment_type: AssessmentType) -> CompetencyAssessment:
        """Generate competency assessment for participant"""
        participant = next((p for p in self.participants if p.participant_id == participant_id), None)
        if not participant:
            raise ValueError(f"Participant {participant_id} not found")

        # Simulate assessment performance
        base_score = {
            CompetencyLevel.NOVICE: random.uniform(45, 65),
            CompetencyLevel.BEGINNER: random.uniform(60, 75),
            CompetencyLevel.COMPETENT: random.uniform(70, 88),
            CompetencyLevel.PROFICIENT: random.uniform(80, 95),
            CompetencyLevel.EXPERT: random.uniform(88, 100)
        }[participant.current_competency]

        # Post-test improvement
        if assessment_type == AssessmentType.POST_TEST:
            base_score = min(base_score * 1.15, 100)

        score = round(base_score, 1)
        passing = 70.0
        passed = score >= passing

        feedback_map = {
            True: [
                f"Excellent performance. Demonstrated strong competency in {module_id} content.",
                "All learning objectives achieved. Ready for advanced modules.",
                "Strong practical application skills demonstrated."
            ],
            False: [
                "Additional practice needed in clinical application areas.",
                "Review core epidemiological concepts and retry assessment.",
                "Recommend additional supervised field experience before retesting."
            ]
        }

        return CompetencyAssessment(
            assessment_id=f"ASSESS_{participant_id}_{module_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            participant_id=participant_id,
            module_id=module_id,
            assessment_type=assessment_type,
            score=score,
            passing_score=passing,
            passed=passed,
            date=datetime.now().isoformat(),
            feedback=random.choice(feedback_map[passed])
        )

    def get_participant_progress(self, participant_id: str) -> dict:
        participant = next((p for p in self.participants if p.participant_id == participant_id), None)
        if not participant:
            return {}

        completion_rate = (len(participant.completed_modules) /
                          max(len(participant.completed_modules) + len(participant.enrolled_modules), 1)) * 100

        return {
            "participant_id": participant_id,
            "name": participant.name,
            "profession": participant.profession,
            "current_competency": participant.current_competency.value,
            "target_competency": participant.target_competency.value,
            "modules_completed": len(participant.completed_modules),
            "modules_enrolled": len(participant.enrolled_modules),
            "completion_rate": round(completion_rate, 1),
            "certifications": participant.certifications,
            "training_hours": round(participant.training_hours, 1)
        }

    def get_cohort_summary(self) -> dict:
        total = len(self.participants)
        levels = {}
        for p in self.participants:
            level = p.current_competency.value
            levels[level] = levels.get(level, 0) + 1

        avg_hours = sum(p.training_hours for p in self.participants) / total if total > 0 else 0
        total_certs = sum(len(p.certifications) for p in self.participants)

        return {
            "total_participants": total,
            "competency_distribution": levels,
            "avg_training_hours": round(avg_hours, 1),
            "total_certifications_awarded": total_certs,
            "organizations_represented": len(set(p.organization for p in self.participants))
        }


# ============================================================
# CAPACITY GAP ANALYZER
# ============================================================

class CapacityGapAnalyzer:
    """
    Identifies and prioritizes workforce capacity gaps
    """

    def analyze_gaps(self, workforce_data: dict) -> list:
        """Identify capacity gaps from workforce assessment data"""

        gaps = [
            CapacityGap("GAP_001", "Field Epidemiology",
                        "Insufficient trained field epidemiologists for rapid outbreak response",
                        ["epidemiologists", "public_health_officers"],
                        "critical", workforce_data.get("field_epi_gap", 45),
                        "MOD_003: Field Epidemiology & Outbreak Investigation", 1),
            CapacityGap("GAP_002", "Laboratory Diagnostics",
                        "Limited PCR and genomic sequencing capacity for zoonotic pathogens",
                        ["laboratory_scientists"],
                        "high", workforce_data.get("lab_gap", 30),
                        "MOD_004: One Health Laboratory Diagnostics", 2),
            CapacityGap("GAP_003", "Risk Communication",
                        "Inadequate risk communication training for outbreak response",
                        ["all_staff"],
                        "high", workforce_data.get("comm_gap", 120),
                        "MOD_005: Risk Communication for Health Emergencies", 3),
            CapacityGap("GAP_004", "Data Analytics",
                        "Low capacity for real-time epidemiological data analysis",
                        ["data_analysts", "epidemiologists"],
                        "moderate", workforce_data.get("data_gap", 35),
                        "MOD_006: Health Data Analytics & Surveillance Systems", 4),
            CapacityGap("GAP_005", "One Health Coordination",
                        "Limited multi-sector coordination experience among senior staff",
                        ["senior_officials", "emergency_managers"],
                        "moderate", workforce_data.get("coord_gap", 20),
                        "MOD_009: One Health Emergency Operations", 5)
        ]

        return gaps

    def estimate_training_investment(self, gaps: list) -> dict:
        """Estimate resources needed to close capacity gaps"""

        total_staff = sum(g.estimated_staff_affected for g in gaps)
        critical_gaps = sum(1 for g in gaps if g.severity == "critical")
        high_gaps = sum(1 for g in gaps if g.severity == "high")

        # Cost estimates
        cost_per_person_day = 250  # USD
        avg_training_days = 3

        total_cost = total_staff * cost_per_person_day * avg_training_days
        timeline_months = 6 if critical_gaps > 0 else 12

        return {
            "total_staff_to_train": total_staff,
            "critical_gaps": critical_gaps,
            "high_gaps": high_gaps,
            "estimated_cost_usd": total_cost,
            "estimated_timeline_months": timeline_months,
            "priority_training": gaps[0].recommended_training if gaps else None,
            "roi_estimate": f"${total_cost * 3.5:,.0f} in prevented outbreak costs"
        }


# ============================================================
# SIMULATION-BASED TRAINER
# ============================================================

class OutbreakSimulationTrainer:
    """
    Delivers tabletop exercise and simulation-based training for outbreak response
    """

    def run_tabletop_exercise(self, scenario: str, participants: list) -> dict:
        """Run a tabletop exercise simulation"""

        phases = [
            {"phase": 1, "title": "Initial Detection", "duration_min": 30,
             "inject": f"Animal surveillance reports unusual mortality in poultry — {scenario} suspected",
             "expected_actions": ["Notify One Health team", "Activate investigation protocol", "Collect samples"]},
            {"phase": 2, "title": "Escalation", "duration_min": 45,
             "inject": "First human case confirmed. Media inquiries increasing. International notification required.",
             "expected_actions": ["Notify WHO", "Activate EOC", "Issue public statement", "Expand contact tracing"]},
            {"phase": 3, "title": "Response Coordination", "duration_min": 45,
             "inject": "Multiple districts affected. Resources strained. Neighboring country reports cases.",
             "expected_actions": ["Request international support", "Implement containment zones", "Coordinate cross-border response"]},
            {"phase": 4, "title": "Resolution & Recovery", "duration_min": 30,
             "inject": "Cases declining. Containment measures working. Recovery planning begins.",
             "expected_actions": ["Develop demobilization plan", "Document lessons learned", "Prepare after-action review"]}
        ]

        performance_scores = {}
        for p in participants:
            performance_scores[p] = {
                "overall_score": round(random.uniform(65, 95), 1),
                "decision_making": round(random.uniform(60, 95), 1),
                "communication": round(random.uniform(65, 95), 1),
                "coordination": round(random.uniform(60, 95), 1),
                "technical_knowledge": round(random.uniform(70, 98), 1)
            }

        avg_score = sum(v["overall_score"] for v in performance_scores.values()) / len(performance_scores) if performance_scores else 0

        return {
            "exercise_id": f"TTX_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "scenario": scenario,
            "type": "tabletop_exercise",
            "participants": len(participants),
            "phases_completed": len(phases),
            "total_duration_min": sum(p["duration_min"] for p in phases),
            "phases": phases,
            "performance": performance_scores,
            "average_score": round(avg_score, 1),
            "lessons_identified": [
                "Communication delays between sectors require clear escalation protocols",
                "Resource pre-positioning would significantly reduce response time",
                "IHR notification procedures need regular refresher training",
                "Cross-border coordination requires pre-established agreements"
            ],
            "recommendations": [
                "Schedule quarterly tabletop exercises for all response teams",
                "Develop sector-specific response protocols",
                "Strengthen early warning systems for zoonotic threats"
            ]
        }


# ============================================================
# INTEGRATED TRAINING MANAGEMENT SYSTEM
# ============================================================

class OneHealthTrainingSystem:
    """
    Main integrated training and capacity building management system
    """

    def __init__(self):
        self.curriculum = OneHealthCurriculumBuilder()
        self.tracker = ParticipantTracker()
        self.gap_analyzer = CapacityGapAnalyzer()
        self.simulation_trainer = OutbreakSimulationTrainer()

    def run_full_training_cycle(self, context: dict) -> dict:
        """Execute complete training management cycle"""

        print(f"\n{'='*60}")
        print("ONE HEALTH TRAINING & CAPACITY BUILDING SYSTEM")
        print(f"{'='*60}")

        # Curriculum overview
        print("📚 Building One Health Curriculum...")
        curriculum_summary = self.curriculum.get_curriculum_summary()

        # Capacity gap analysis
        print("🔍 Analyzing Capacity Gaps...")
        workforce_data = context.get("workforce", {
            "field_epi_gap": 45, "lab_gap": 30, "comm_gap": 120, "data_gap": 35, "coord_gap": 20
        })
        gaps = self.gap_analyzer.analyze_gaps(workforce_data)
        investment = self.gap_analyzer.estimate_training_investment(gaps)

        # Run assessments for participants
        print("✅ Conducting Competency Assessments...")
        assessments = []
        for participant in self.tracker.participants[:4]:
            if participant.enrolled_modules:
                module_id = participant.enrolled_modules[0]
                pre = self.tracker.assess_participant(participant.participant_id, module_id, AssessmentType.PRE_TEST)
                post = self.tracker.assess_participant(participant.participant_id, module_id, AssessmentType.POST_TEST)
                assessments.append({"participant": participant.name, "module": module_id,
                                   "pre_score": pre.score, "post_score": post.score,
                                   "improvement": round(post.score - pre.score, 1),
                                   "passed": post.passed})

        # Cohort summary
        cohort = self.tracker.get_cohort_summary()

        # Run tabletop exercise
        print("🎯 Running Outbreak Response Simulation...")
        participant_names = [p.name for p in self.tracker.participants[:5]]
        exercise = self.simulation_trainer.run_tabletop_exercise("H5N1 Avian Influenza", participant_names)

        # Session simulation
        print("📋 Scheduling Training Sessions...")
        sessions = []
        for i, module in enumerate(self.curriculum.core_modules[:5]):
            session = TrainingSession(
                session_id=f"SESS_{i+1:03d}",
                module_id=module.module_id,
                facilitator=f"Expert Facilitator {i+1}",
                location="National Training Center" if module.delivery_mode != DeliveryMode.ONLINE else "Online Platform",
                start_date=datetime.now().isoformat(),
                end_date=(datetime.now() + timedelta(hours=module.duration_hours)).isoformat(),
                participants=[p.participant_id for p in self.tracker.participants[:module.max_participants]],
                status=TrainingStatus.COMPLETED if i < 2 else TrainingStatus.ONGOING if i == 2 else TrainingStatus.PLANNED,
                pre_test_avg=round(random.uniform(45, 65), 1),
                post_test_avg=round(random.uniform(70, 92), 1),
                completion_rate=round(random.uniform(0.85, 1.0), 2),
                satisfaction_score=round(random.uniform(3.8, 4.9), 1)
            )
            sessions.append(session)

        return {
            "training_system_id": f"TRN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "curriculum": curriculum_summary,
            "capacity_gaps": {
                "gaps_identified": len(gaps),
                "critical_gaps": sum(1 for g in gaps if g.severity == "critical"),
                "high_gaps": sum(1 for g in gaps if g.severity == "high"),
                "gaps": [{"gap_id": g.gap_id, "domain": g.domain, "severity": g.severity,
                          "affected": g.estimated_staff_affected, "recommended": g.recommended_training}
                         for g in gaps],
                "investment_estimate": investment
            },
            "participant_cohort": cohort,
            "competency_assessments": {
                "total_assessed": len(assessments),
                "pass_rate": round(sum(1 for a in assessments if a["passed"]) / len(assessments) * 100, 1) if assessments else 0,
                "avg_improvement": round(sum(a["improvement"] for a in assessments) / len(assessments), 1) if assessments else 0,
                "results": assessments
            },
            "training_sessions": {
                "total_scheduled": len(sessions),
                "completed": sum(1 for s in sessions if s.status == TrainingStatus.COMPLETED),
                "ongoing": sum(1 for s in sessions if s.status == TrainingStatus.ONGOING),
                "avg_satisfaction": round(sum(s.satisfaction_score for s in sessions) / len(sessions), 2),
                "avg_completion_rate": round(sum(s.completion_rate for s in sessions) / len(sessions) * 100, 1),
                "sessions": [{"id": s.session_id, "module": s.module_id, "status": s.status.value,
                              "pre_avg": s.pre_test_avg, "post_avg": s.post_test_avg,
                              "satisfaction": s.satisfaction_score} for s in sessions]
            },
            "simulation_exercise": exercise
        }


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 40: TRAINING SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    system = OneHealthTrainingSystem()
    result = system.run_full_training_cycle({})

    c = result["curriculum"]
    print(f"\n📚 CURRICULUM:")
    print(f"  Total Modules: {c['total_modules']}")
    print(f"  Total Training Hours: {c['total_training_hours']}")
    print(f"  CEU Credits: {c['total_ceu_credits']}")
    print(f"  Categories: {', '.join(c['categories'])}")
    print(f"  Delivery Modes: {', '.join(c['delivery_modes'])}")
    print(f"  Certifications Offered: {c['certifications_offered']}")

    cg = result["capacity_gaps"]
    print(f"\n🔍 CAPACITY GAPS:")
    print(f"  Gaps Identified: {cg['gaps_identified']}")
    print(f"  Critical: {cg['critical_gaps']} | High: {cg['high_gaps']}")
    inv = cg["investment_estimate"]
    print(f"  Staff to Train: {inv['total_staff_to_train']}")
    print(f"  Estimated Cost: ${inv['estimated_cost_usd']:,}")
    print(f"  Timeline: {inv['estimated_timeline_months']} months")
    print(f"  ROI Estimate: {inv['roi_estimate']}")
    print(f"  Top Gap: {cg['gaps'][0]['domain']} ({cg['gaps'][0]['severity'].upper()})")

    co = result["participant_cohort"]
    print(f"\n👥 PARTICIPANT COHORT:")
    print(f"  Total Participants: {co['total_participants']}")
    print(f"  Avg Training Hours: {co['avg_training_hours']}")
    print(f"  Certifications Awarded: {co['total_certifications_awarded']}")
    print(f"  Organizations: {co['organizations_represented']}")
    print(f"  Competency Levels: {co['competency_distribution']}")

    ca = result["competency_assessments"]
    print(f"\n✅ COMPETENCY ASSESSMENTS:")
    print(f"  Participants Assessed: {ca['total_assessed']}")
    print(f"  Pass Rate: {ca['pass_rate']}%")
    print(f"  Avg Score Improvement: +{ca['avg_improvement']} points")
    for r in ca["results"]:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"    {r['participant'][:25]:<25} Pre:{r['pre_score']:4.1f} → Post:{r['post_score']:4.1f} (+{r['improvement']:4.1f}) {status}")

    ts = result["training_sessions"]
    print(f"\n📋 TRAINING SESSIONS:")
    print(f"  Total: {ts['total_scheduled']} | Completed: {ts['completed']} | Ongoing: {ts['ongoing']}")
    print(f"  Avg Satisfaction: {ts['avg_satisfaction']}/5.0")
    print(f"  Avg Completion Rate: {ts['avg_completion_rate']}%")

    ex = result["simulation_exercise"]
    print(f"\n🎯 TABLETOP EXERCISE:")
    print(f"  Scenario: {ex['scenario']}")
    print(f"  Participants: {ex['participants']}")
    print(f"  Duration: {ex['total_duration_min']} minutes")
    print(f"  Average Score: {ex['average_score']}/100")
    print(f"  Lessons Identified: {len(ex['lessons_identified'])}")
    for lesson in ex["lessons_identified"][:2]:
        print(f"    • {lesson}")

    print(f"\n{'='*70}")
    print("✅ Module 40: training.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
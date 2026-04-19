"""
Module 42: strategic_planning.py
Strategic Planning & Policy Development System for One Health
Zoonotic Disease Prevention, Preparedness, and Response
"""

import random
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class StrategicPillar(Enum):
    PREVENTION = "prevention"
    DETECTION = "detection"
    RESPONSE = "response"
    RECOVERY = "recovery"
    GOVERNANCE = "governance"
    CAPACITY_BUILDING = "capacity_building"
    RESEARCH_INNOVATION = "research_innovation"
    INTERNATIONAL_COOPERATION = "international_cooperation"

class PolicyStatus(Enum):
    DRAFT = "draft"
    CONSULTATION = "consultation"
    REVIEW = "review"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    UNDER_REVISION = "under_revision"
    ARCHIVED = "archived"

class ObjectiveStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    AT_RISK = "at_risk"
    OVERDUE = "overdue"

class StakeholderGroup(Enum):
    GOVERNMENT = "government"
    ACADEMIC = "academic"
    PRIVATE_SECTOR = "private_sector"
    CIVIL_SOCIETY = "civil_society"
    INTERNATIONAL_ORGANIZATION = "international_organization"
    COMMUNITY = "community"

class ResourceType(Enum):
    FINANCIAL = "financial"
    HUMAN = "human"
    TECHNICAL = "technical"
    INFRASTRUCTURE = "infrastructure"
    KNOWLEDGE = "knowledge"

class JEECapacity(Enum):
    NO_CAPACITY = 1
    LIMITED = 2
    DEVELOPED = 3
    DEMONSTRATED = 4
    SUSTAINABLE = 5


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class StrategicObjective:
    objective_id: str
    pillar: StrategicPillar
    title: str
    description: str
    target: str
    baseline: str
    deadline: str
    responsible_agency: str
    status: ObjectiveStatus
    progress_pct: float
    budget_usd: float
    key_activities: list
    success_indicators: list

@dataclass
class PolicyDocument:
    policy_id: str
    title: str
    pillar: StrategicPillar
    policy_type: str    # law / regulation / guideline / protocol / standard
    status: PolicyStatus
    version: str
    effective_date: str
    review_date: str
    responsible_ministry: str
    stakeholders_consulted: list
    key_provisions: list
    implementation_timeline_months: int
    compliance_mechanisms: list
    estimated_impact: str

@dataclass
class ResourceAllocation:
    resource_id: str
    resource_type: ResourceType
    category: str
    total_amount: float
    allocated_amount: float
    remaining_amount: float
    fiscal_year: str
    allocations_by_pillar: dict
    utilization_rate: float

@dataclass
class JEEIndicator:
    indicator_id: str
    capacity_area: str
    indicator_name: str
    current_score: JEECapacity
    target_score: JEECapacity
    gap: int
    priority_actions: list
    estimated_cost_usd: float
    timeline_months: int

@dataclass
class StrategicRisk:
    risk_id: str
    category: str
    description: str
    likelihood: float   # 0-1
    impact: float       # 0-1
    risk_score: float   # likelihood * impact
    mitigation_strategies: list
    contingency_plan: str
    risk_owner: str

@dataclass
class MilestoneTracker:
    milestone_id: str
    objective_id: str
    title: str
    due_date: str
    status: str         # completed / on_track / at_risk / overdue
    completion_date: str
    notes: str


# ============================================================
# STRATEGIC PLAN BUILDER
# ============================================================

class OneHealthStrategicPlanBuilder:
    """
    Builds comprehensive national One Health strategic plans
    """

    def __init__(self):
        self.objectives = self._build_strategic_objectives()

    def _build_strategic_objectives(self) -> list:
        now = datetime.now()

        objectives = [
            StrategicObjective(
                "OBJ_P1_01", StrategicPillar.PREVENTION,
                "Establish National One Health Surveillance Network",
                "Integrate human, animal, and environmental surveillance into unified early warning system",
                "Functional integrated surveillance in all 14 provinces by 2026",
                "3 provinces with partial integration (2024)",
                (now + timedelta(days=730)).strftime("%Y-%m-%d"),
                "Ministry of Health / Ministry of Agriculture",
                ObjectiveStatus.IN_PROGRESS, 35.0, 5000000,
                ["Standardize data reporting formats", "Build data sharing platform",
                 "Train surveillance officers", "Conduct joint investigations"],
                ["Number of provinces with integrated surveillance", "Time to detection",
                 "Cross-sector data sharing events", "Joint investigation rate"]
            ),
            StrategicObjective(
                "OBJ_P2_01", StrategicPillar.DETECTION,
                "Achieve 48-Hour Outbreak Detection Capacity",
                "Reduce time from first case to public health response to <48 hours",
                "≥90% of outbreaks detected within 48 hours by 2025",
                "Current median detection time: 8.5 days (2024)",
                (now + timedelta(days=365)).strftime("%Y-%m-%d"),
                "National Public Health Institute",
                ObjectiveStatus.IN_PROGRESS, 52.0, 3200000,
                ["Deploy real-time electronic surveillance", "Expand lab network",
                 "Train community health workers", "Establish 24/7 EOC"],
                ["Median outbreak detection time", "Lab turnaround time",
                 "Community reporting rate", "EOC activation frequency"]
            ),
            StrategicObjective(
                "OBJ_P3_01", StrategicPillar.RESPONSE,
                "Develop National Pandemic Response Plan",
                "Create comprehensive, tested, and funded multi-hazard pandemic response plan",
                "WHO-validated plan with annual simulation exercises by 2025",
                "Outdated plan from 2019; not WHO-validated",
                (now + timedelta(days=400)).strftime("%Y-%m-%d"),
                "Emergency Operations Center",
                ObjectiveStatus.IN_PROGRESS, 68.0, 1500000,
                ["Update National Action Plan", "Conduct tabletop exercises",
                 "Establish strategic stockpile", "Train response teams"],
                ["Plan completion status", "Exercise conduct rate",
                 "Stockpile adequacy", "Response team readiness score"]
            ),
            StrategicObjective(
                "OBJ_P4_01", StrategicPillar.GOVERNANCE,
                "Establish One Health National Coordinating Mechanism",
                "Create high-level One Health coordination body with legal mandate and resources",
                "Functional One Health Coordination Committee with TOR and budget by 2024",
                "Ad hoc coordination only; no formal structure",
                (now + timedelta(days=180)).strftime("%Y-%m-%d"),
                "Cabinet Office / Prime Minister's Office",
                ObjectiveStatus.IN_PROGRESS, 80.0, 500000,
                ["Draft TOR and legal framework", "Secure political commitment",
                 "Appoint committee members", "Hold inaugural meeting"],
                ["Committee establishment date", "Meeting frequency",
                 "Decision implementation rate", "Budget allocated"]
            ),
            StrategicObjective(
                "OBJ_P5_01", StrategicPillar.CAPACITY_BUILDING,
                "Train 500 One Health Professionals by 2026",
                "Build national workforce with integrated One Health competencies",
                "500 certified One Health professionals by 2026",
                "Estimated 45 trained professionals nationwide (2024)",
                (now + timedelta(days=730)).strftime("%Y-%m-%d"),
                "National Health Training Institute",
                ObjectiveStatus.IN_PROGRESS, 9.0, 4000000,
                ["Develop curricula", "Train trainers", "Conduct training cycles",
                 "Certify professionals", "Track continuing education"],
                ["Number trained and certified", "Training completion rate",
                 "Pre/post knowledge improvement", "Field application rate"]
            ),
            StrategicObjective(
                "OBJ_P6_01", StrategicPillar.RESEARCH_INNOVATION,
                "Establish National One Health Research Agenda",
                "Define and fund priority research for national zoonotic disease burden reduction",
                "National research agenda with $10M funding secured by 2025",
                "No formal research agenda; fragmented funding",
                (now + timedelta(days=500)).strftime("%Y-%m-%d"),
                "National Research Council",
                ObjectiveStatus.IN_PROGRESS, 25.0, 10000000,
                ["Conduct research priority-setting exercise", "Develop funding mechanisms",
                 "Establish research consortium", "Launch priority studies"],
                ["Research agenda adoption", "Funding secured",
                 "Publications", "Policy-relevant findings"]
            ),
            StrategicObjective(
                "OBJ_P7_01", StrategicPillar.INTERNATIONAL_COOPERATION,
                "Achieve IHR Core Capacity Level 4 in All Technical Areas",
                "Strengthen all IHR core capacities to 'demonstrated' level (score 4)",
                "Average JEE score ≥4 across all 19 technical areas by 2026",
                "Current average JEE score: 2.8 (2022 JEE)",
                (now + timedelta(days=730)).strftime("%Y-%m-%d"),
                "Ministry of Health / IHR Focal Point",
                ObjectiveStatus.IN_PROGRESS, 20.0, 8000000,
                ["Conduct self-assessment", "Prioritize gaps", "Implement NAPHS activities",
                 "Request technical assistance", "Conduct review missions"],
                ["Average JEE score", "Number of areas at level 4+",
                 "NAPHS implementation rate", "Technical assistance received"]
            )
        ]
        return objectives

    def get_plan_summary(self) -> dict:
        total_budget = sum(o.budget_usd for o in self.objectives)
        avg_progress = sum(o.progress_pct for o in self.objectives) / len(self.objectives)
        by_status = {}
        by_pillar = {}
        for o in self.objectives:
            s = o.status.value
            p = o.pillar.value
            by_status[s] = by_status.get(s, 0) + 1
            by_pillar[p] = by_pillar.get(p, 0) + 1

        return {
            "total_objectives": len(self.objectives),
            "total_budget_usd": total_budget,
            "average_progress_pct": round(avg_progress, 1),
            "by_status": by_status,
            "by_pillar": by_pillar,
            "on_track": sum(1 for o in self.objectives if o.status == ObjectiveStatus.IN_PROGRESS and o.progress_pct >= 40),
            "at_risk": sum(1 for o in self.objectives if o.status == ObjectiveStatus.AT_RISK)
        }

    def get_objective_dashboard(self) -> list:
        return [
            {
                "objective_id": o.objective_id,
                "pillar": o.pillar.value,
                "title": o.title,
                "status": o.status.value,
                "progress_pct": o.progress_pct,
                "budget_usd": o.budget_usd,
                "deadline": o.deadline,
                "responsible": o.responsible_agency
            }
            for o in self.objectives
        ]


# ============================================================
# POLICY DEVELOPER
# ============================================================

class PolicyDeveloper:
    """
    Develops and tracks One Health policy documents
    """

    def __init__(self):
        self.policies = self._initialize_policies()

    def _initialize_policies(self) -> list:
        now = datetime.now()
        return [
            PolicyDocument(
                "POL_001", "National One Health Act",
                StrategicPillar.GOVERNANCE, "law",
                PolicyStatus.CONSULTATION, "2.0",
                (now + timedelta(days=180)).strftime("%Y-%m-%d"),
                (now + timedelta(days=180 + 365 * 3)).strftime("%Y-%m-%d"),
                "Ministry of Health",
                ["Ministry of Agriculture", "Ministry of Environment", "Attorney General", "Civil Society"],
                ["Legal mandate for One Health coordination mechanism",
                 "Mandatory cross-sector data sharing for disease surveillance",
                 "Establishment of National One Health Technical Committee",
                 "IHR implementation obligations"],
                18, ["Parliamentary oversight", "Annual reporting", "Penalties for non-compliance"],
                "Foundation for all One Health activities; enables coordinated response"
            ),
            PolicyDocument(
                "POL_002", "Zoonotic Disease Surveillance Protocol",
                StrategicPillar.DETECTION, "protocol",
                PolicyStatus.APPROVED, "3.1",
                (now - timedelta(days=90)).strftime("%Y-%m-%d"),
                (now + timedelta(days=275)).strftime("%Y-%m-%d"),
                "National Public Health Institute",
                ["Veterinary Services", "Environmental Health", "Laboratory Network"],
                ["Standardized case definitions for 25 priority zoonoses",
                 "Mandatory 24-hour reporting for CBRN threats",
                 "Cross-sector joint investigation procedures",
                 "Specimen collection and transport standards"],
                6, ["Quarterly compliance audits", "Performance dashboards", "Supervisory visits"],
                "Reduces time-to-detect; standardizes response across all sectors"
            ),
            PolicyDocument(
                "POL_003", "Antimicrobial Resistance National Action Plan",
                StrategicPillar.PREVENTION, "regulation",
                PolicyStatus.IMPLEMENTED, "1.0",
                (now - timedelta(days=365)).strftime("%Y-%m-%d"),
                (now + timedelta(days=365 * 4)).strftime("%Y-%m-%d"),
                "Ministry of Health / Ministry of Agriculture",
                ["Pharmacy Council", "Veterinary Association", "Farmers Federation", "WHO"],
                ["Prescription-only antibiotics for human and veterinary use",
                 "National AMR surveillance in human, animal, and environmental sectors",
                 "Antibiotic stewardship programs in all hospitals",
                 "Phased elimination of growth-promoting antibiotics in livestock"],
                24, ["Annual AMR report", "Pharmacy inspections", "Import controls"],
                "Estimated 15% reduction in AMR-related mortality within 5 years"
            ),
            PolicyDocument(
                "POL_004", "One Health Emergency Response Framework",
                StrategicPillar.RESPONSE, "guideline",
                PolicyStatus.REVIEW, "2.0",
                (now + timedelta(days=60)).strftime("%Y-%m-%d"),
                (now + timedelta(days=60 + 730)).strftime("%Y-%m-%d"),
                "Emergency Operations Center",
                ["All ministries", "Military", "Red Cross", "UN agencies"],
                ["Activation criteria for different emergency levels",
                 "Incident Command System structure and responsibilities",
                 "Resource mobilization and deployment procedures",
                 "International assistance request procedures"],
                12, ["Biannual exercises", "After-action reviews", "Certification requirements"],
                "Reduces response time; ensures coordinated multi-sector action"
            )
        ]

    def track_policy_implementation(self) -> dict:
        by_status = {}
        for p in self.policies:
            s = p.status.value
            by_status[s] = by_status.get(s, 0) + 1

        implemented = [p for p in self.policies if p.status == PolicyStatus.IMPLEMENTED]
        return {
            "total_policies": len(self.policies),
            "by_status": by_status,
            "implementation_rate": round(len(implemented) / len(self.policies) * 100, 1),
            "policies": [
                {"id": p.policy_id, "title": p.title, "type": p.policy_type,
                 "status": p.status.value, "effective": p.effective_date,
                 "responsible": p.responsible_ministry}
                for p in self.policies
            ]
        }


# ============================================================
# JEE CAPACITY TRACKER
# ============================================================

class JEECapacityTracker:
    """
    Tracks IHR Joint External Evaluation (JEE) core capacity scores
    and plans capacity strengthening activities
    """

    def __init__(self):
        self.indicators = self._initialize_jee_indicators()

    def _initialize_jee_indicators(self) -> list:
        indicators_data = [
            ("P.1.1", "National legislation, policy and financing", 2, 4, 400000, 18),
            ("P.2.1", "IHR coordination, communication and advocacy", 3, 4, 150000, 12),
            ("P.3.1", "Antimicrobial resistance", 2, 4, 600000, 24),
            ("P.4.1", "Zoonotic disease", 2, 5, 800000, 30),
            ("P.5.1", "Food safety", 3, 4, 250000, 18),
            ("D.1.1", "National laboratory system", 2, 4, 1200000, 24),
            ("D.2.1", "Real-time surveillance", 2, 4, 900000, 24),
            ("D.3.1", "Reporting", 3, 4, 200000, 12),
            ("D.4.1", "Workforce development", 2, 4, 1500000, 36),
            ("R.1.1", "Preparedness", 2, 4, 700000, 24),
            ("R.2.1", "Emergency response operations", 3, 4, 400000, 18),
            ("R.3.1", "Linking public health and security authorities", 2, 4, 300000, 18),
            ("R.4.1", "Medical countermeasures and personnel deployment", 2, 4, 500000, 24),
            ("R.5.1", "Risk communication", 3, 5, 350000, 18),
            ("PoE.1", "Points of entry", 3, 4, 200000, 12),
            ("CE.1", "Chemical events", 2, 3, 300000, 18),
            ("RE.1", "Radiation emergencies", 2, 3, 250000, 18),
        ]

        indicators = []
        for ind_id, name, current, target, cost, timeline in indicators_data:
            priority_actions = [
                f"Conduct gap assessment for {name}",
                f"Develop capacity strengthening plan",
                f"Implement priority activities with technical assistance",
                f"Monitor progress through quarterly reviews"
            ]
            indicators.append(JEEIndicator(
                indicator_id=ind_id,
                capacity_area=name,
                indicator_name=f"{ind_id}: {name}",
                current_score=JEECapacity(current),
                target_score=JEECapacity(target),
                gap=target - current,
                priority_actions=priority_actions,
                estimated_cost_usd=float(cost),
                timeline_months=timeline
            ))

        return indicators

    def get_jee_summary(self) -> dict:
        avg_current = sum(i.current_score.value for i in self.indicators) / len(self.indicators)
        avg_target = sum(i.target_score.value for i in self.indicators) / len(self.indicators)
        total_cost = sum(i.estimated_cost_usd for i in self.indicators)

        at_target = sum(1 for i in self.indicators if i.current_score.value >= i.target_score.value)
        critical_gaps = [i for i in self.indicators if i.gap >= 2]

        return {
            "total_indicators": len(self.indicators),
            "avg_current_score": round(avg_current, 1),
            "avg_target_score": round(avg_target, 1),
            "avg_gap": round(avg_target - avg_current, 1),
            "at_target": at_target,
            "critical_gaps": len(critical_gaps),
            "total_investment_needed_usd": total_cost,
            "priority_indicators": [
                {"id": i.indicator_id, "name": i.capacity_area,
                 "current": i.current_score.value, "target": i.target_score.value,
                 "gap": i.gap, "cost": i.estimated_cost_usd}
                for i in sorted(critical_gaps, key=lambda x: x.gap, reverse=True)[:5]
            ]
        }


# ============================================================
# STRATEGIC RISK MANAGER
# ============================================================

class StrategicRiskManager:
    """
    Identifies and manages strategic risks to One Health program
    """

    def __init__(self):
        self.risks = self._identify_risks()

    def _identify_risks(self) -> list:
        risk_data = [
            ("RSK_001", "Political", "Change in government priorities reducing One Health funding", 0.4, 0.9,
             ["Advocate for cross-party consensus", "Document ROI evidence", "Engage civil society"],
             "Activate emergency funding from international partners"),
            ("RSK_002", "Financial", "Budget cuts reducing program implementation capacity", 0.5, 0.8,
             ["Diversify funding sources", "Secure multi-year commitments", "Build domestic financing"],
             "Scale down to core activities; seek emergency international support"),
            ("RSK_003", "Operational", "Pandemic or major outbreak overwhelming response system before capacity built", 0.3, 0.95,
             ["Accelerate detection capacity", "Pre-position stockpiles", "Establish mutual aid agreements"],
             "Activate NAPHS emergency protocols; request international assistance"),
            ("RSK_004", "Technical", "Emerging pathogen not covered by existing surveillance systems", 0.4, 0.8,
             ["Implement broad eDNA surveillance", "Strengthen Event-Based Surveillance", "Train for unknown pathogens"],
             "Activate GOARN; implement generic response protocols"),
            ("RSK_005", "Human Resources", "Brain drain of trained One Health professionals", 0.5, 0.6,
             ["Competitive retention packages", "Build domestic training capacity", "Create career pathways"],
             "Deploy international technical assistance; emergency recruitment"),
            ("RSK_006", "Data Quality", "Poor data quality undermining surveillance and response decisions", 0.6, 0.7,
             ["Implement data quality standards", "Automate data validation", "Train data managers"],
             "Deploy data quality task force; manual verification protocols")
        ]

        risks = []
        for r_id, cat, desc, likelihood, impact, mitigations, contingency in risk_data:
            risks.append(StrategicRisk(
                risk_id=r_id,
                category=cat,
                description=desc,
                likelihood=likelihood,
                impact=impact,
                risk_score=round(likelihood * impact, 2),
                mitigation_strategies=mitigations,
                contingency_plan=contingency,
                risk_owner=f"Program Director ({cat})"
            ))

        return sorted(risks, key=lambda x: x.risk_score, reverse=True)

    def get_risk_summary(self) -> dict:
        critical = [r for r in self.risks if r.risk_score >= 0.6]
        high = [r for r in self.risks if 0.4 <= r.risk_score < 0.6]
        moderate = [r for r in self.risks if r.risk_score < 0.4]

        return {
            "total_risks": len(self.risks),
            "critical_risks": len(critical),
            "high_risks": len(high),
            "moderate_risks": len(moderate),
            "top_risk": {
                "id": self.risks[0].risk_id,
                "category": self.risks[0].category,
                "description": self.risks[0].description,
                "score": self.risks[0].risk_score
            },
            "risk_register": [
                {"risk_id": r.risk_id, "category": r.category,
                 "likelihood": r.likelihood, "impact": r.impact,
                 "score": r.risk_score,
                 "level": "CRITICAL" if r.risk_score >= 0.6 else "HIGH" if r.risk_score >= 0.4 else "MODERATE"}
                for r in self.risks
            ]
        }


# ============================================================
# RESOURCE ALLOCATION OPTIMIZER
# ============================================================

class ResourceAllocationOptimizer:
    """
    Optimizes resource allocation across One Health strategic pillars
    """

    def optimize_allocation(self, total_budget: float, priorities: dict) -> ResourceAllocation:
        """Allocate resources based on strategic priorities and objective needs"""

        # Priority-weighted allocation
        total_priority = sum(priorities.values())
        allocations = {}
        for pillar, priority in priorities.items():
            allocations[pillar] = round((priority / total_priority) * total_budget)

        allocated = sum(allocations.values())
        remaining = total_budget - allocated

        return ResourceAllocation(
            resource_id=f"RSRC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            resource_type=ResourceType.FINANCIAL,
            category="Annual One Health Program Budget",
            total_amount=total_budget,
            allocated_amount=allocated,
            remaining_amount=remaining,
            fiscal_year=str(datetime.now().year),
            allocations_by_pillar=allocations,
            utilization_rate=round(allocated / total_budget * 100, 1)
        )

    def generate_resource_report(self, allocation: ResourceAllocation) -> dict:
        top_pillar = max(allocation.allocations_by_pillar, key=allocation.allocations_by_pillar.get)
        return {
            "fiscal_year": allocation.fiscal_year,
            "total_budget_usd": allocation.total_amount,
            "total_allocated_usd": allocation.allocated_amount,
            "utilization_rate": allocation.utilization_rate,
            "top_funded_pillar": top_pillar,
            "top_funded_amount": allocation.allocations_by_pillar[top_pillar],
            "allocations": allocation.allocations_by_pillar
        }


# ============================================================
# INTEGRATED STRATEGIC PLANNING SYSTEM
# ============================================================

class OneHealthStrategicPlanningSystem:
    """
    Main integrated strategic planning and policy development system
    """

    def __init__(self):
        self.plan_builder = OneHealthStrategicPlanBuilder()
        self.policy_dev = PolicyDeveloper()
        self.jee_tracker = JEECapacityTracker()
        self.risk_manager = StrategicRiskManager()
        self.resource_optimizer = ResourceAllocationOptimizer()

    def run_strategic_review(self, context: dict) -> dict:
        """Execute comprehensive strategic planning review"""

        print(f"\n{'='*60}")
        print("ONE HEALTH STRATEGIC PLANNING SYSTEM")
        print(f"{'='*60}")

        # Strategic plan
        print("🎯 Reviewing Strategic Plan...")
        plan_summary = self.plan_builder.get_plan_summary()
        obj_dashboard = self.plan_builder.get_objective_dashboard()

        # Policy tracking
        print("📋 Tracking Policy Implementation...")
        policy_status = self.policy_dev.track_policy_implementation()

        # JEE capacity
        print("🌍 Assessing IHR/JEE Core Capacities...")
        jee_summary = self.jee_tracker.get_jee_summary()

        # Risk assessment
        print("⚠️  Assessing Strategic Risks...")
        risk_summary = self.risk_manager.get_risk_summary()

        # Resource allocation
        print("💰 Optimizing Resource Allocation...")
        total_budget = context.get("total_budget_usd", 25000000)
        priorities = {
            StrategicPillar.DETECTION.value: 5,
            StrategicPillar.RESPONSE.value: 4,
            StrategicPillar.PREVENTION.value: 4,
            StrategicPillar.CAPACITY_BUILDING.value: 3,
            StrategicPillar.GOVERNANCE.value: 3,
            StrategicPillar.RESEARCH_INNOVATION.value: 3,
            StrategicPillar.INTERNATIONAL_COOPERATION.value: 2,
            StrategicPillar.RECOVERY.value: 1
        }
        allocation = self.resource_optimizer.optimize_allocation(total_budget, priorities)
        resource_report = self.resource_optimizer.generate_resource_report(allocation)

        # Milestone tracking
        print("📅 Tracking Milestones...")
        milestones = self._generate_milestone_tracker()

        # Build strategic scorecard
        scorecard = self._build_scorecard(plan_summary, policy_status, jee_summary, risk_summary)

        return {
            "strategic_review_id": f"STRAT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "review_period": f"{datetime.now().strftime('%Y')} Annual Review",
            "strategic_plan": plan_summary,
            "objective_dashboard": obj_dashboard,
            "policy_implementation": policy_status,
            "jee_capacities": jee_summary,
            "risk_assessment": risk_summary,
            "resource_allocation": resource_report,
            "milestone_tracker": milestones,
            "strategic_scorecard": scorecard,
            "priority_recommendations": self._generate_recommendations(plan_summary, jee_summary, risk_summary)
        }

    def _generate_milestone_tracker(self) -> dict:
        statuses = ["completed", "on_track", "on_track", "at_risk"]
        milestones = []
        for i, obj in enumerate(self.plan_builder.objectives[:5]):
            for j, activity in enumerate(obj.key_activities[:2]):
                status = random.choice(statuses)
                due = (datetime.now() + timedelta(days=random.randint(-30, 180))).strftime("%Y-%m-%d")
                milestones.append({
                    "objective": obj.title[:40],
                    "activity": activity[:50],
                    "due_date": due,
                    "status": status
                })

        return {
            "total_milestones": len(milestones),
            "completed": sum(1 for m in milestones if m["status"] == "completed"),
            "on_track": sum(1 for m in milestones if m["status"] == "on_track"),
            "at_risk": sum(1 for m in milestones if m["status"] == "at_risk"),
            "milestones": milestones
        }

    def _build_scorecard(self, plan, policy, jee, risk) -> dict:
        """Build balanced scorecard"""
        plan_score = plan["average_progress_pct"]
        policy_score = policy["implementation_rate"]
        jee_score = (jee["avg_current_score"] / 5.0) * 100
        risk_score = max(0, 100 - (risk["critical_risks"] * 20 + risk["high_risks"] * 10))

        overall = (plan_score * 0.35 + policy_score * 0.25 + jee_score * 0.25 + risk_score * 0.15)

        return {
            "overall_score": round(overall, 1),
            "performance_grade": "A" if overall >= 80 else "B" if overall >= 70 else "C" if overall >= 60 else "D",
            "components": {
                "strategic_objectives_progress": round(plan_score, 1),
                "policy_implementation": round(policy_score, 1),
                "ihr_jee_capacity": round(jee_score, 1),
                "risk_management": round(risk_score, 1)
            },
            "trend": "improving",
            "areas_of_strength": ["Governance structure", "Policy development"],
            "areas_for_improvement": ["JEE core capacity scores", "Strategic objective completion rate"]
        }

    def _generate_recommendations(self, plan, jee, risk) -> list:
        recommendations = [
            "IMMEDIATE: Convene One Health National Coordinating Committee — highest-progress objective (80%) — formalize within 30 days",
            f"SHORT-TERM: Accelerate IHR capacity strengthening — average JEE score {jee['avg_current_score']:.1f}/5.0 requires ${jee['total_investment_needed_usd']:,.0f} investment",
            f"RESOURCE: Increase budget allocation to Detection pillar — current highest strategic priority with 52% progress",
            f"RISK: Develop financial resilience plan — budget cuts identified as top strategic risk (score: {risk['top_risk']['score']:.2f})",
            "PARTNERSHIP: Expand international cooperation under IHR framework; request WHO technical assistance for laboratory capacity",
            f"MONITORING: Establish quarterly strategic review cycle with all {plan['total_objectives']} objective owners",
            "INNOVATION: Fast-track AI early warning system pilot from 35% to operational — highest-impact technology investment"
        ]
        return recommendations


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 42: STRATEGIC PLANNING SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    system = OneHealthStrategicPlanningSystem()
    result = system.run_strategic_review({"total_budget_usd": 25000000})

    sp = result["strategic_plan"]
    print(f"\n🎯 STRATEGIC PLAN:")
    print(f"  Total Objectives: {sp['total_objectives']}")
    print(f"  Total Budget: ${sp['total_budget_usd']:,.0f}")
    print(f"  Average Progress: {sp['average_progress_pct']}%")
    print(f"  By Status: {sp['by_status']}")
    print(f"  On Track: {sp['on_track']} objectives")

    print(f"\n  📊 OBJECTIVE DASHBOARD:")
    for obj in result["objective_dashboard"]:
        bar = "█" * int(obj["progress_pct"] / 10)
        print(f"  {obj['pillar'][:12]:<12} {obj['title'][:45]:<45} {obj['progress_pct']:4.0f}% {bar}")

    pi = result["policy_implementation"]
    print(f"\n📋 POLICY IMPLEMENTATION:")
    print(f"  Total Policies: {pi['total_policies']}")
    print(f"  Implementation Rate: {pi['implementation_rate']}%")
    print(f"  By Status: {pi['by_status']}")

    jee = result["jee_capacities"]
    print(f"\n🌍 IHR/JEE CORE CAPACITIES:")
    print(f"  Indicators Tracked: {jee['total_indicators']}")
    print(f"  Current Avg Score: {jee['avg_current_score']}/5.0")
    print(f"  Target Avg Score: {jee['avg_target_score']}/5.0")
    print(f"  Critical Gaps: {jee['critical_gaps']}")
    print(f"  Investment Needed: ${jee['total_investment_needed_usd']:,.0f}")
    print(f"  Priority Gaps:")
    for pi_item in jee["priority_indicators"][:3]:
        print(f"    • {pi_item['id']} {pi_item['name']:<40} {pi_item['current']}→{pi_item['target']} (gap:{pi_item['gap']})")

    rs = result["risk_assessment"]
    print(f"\n⚠️  STRATEGIC RISKS:")
    print(f"  Total Risks: {rs['total_risks']}")
    print(f"  Critical: {rs['critical_risks']} | High: {rs['high_risks']} | Moderate: {rs['moderate_risks']}")
    tr = rs["top_risk"]
    print(f"  Top Risk: [{tr['category']}] {tr['description'][:60]} (Score: {tr['score']:.2f})")
    for r in rs["risk_register"][:4]:
        print(f"    {r['risk_id']} {r['category']:<12} L:{r['likelihood']:.1f} I:{r['impact']:.1f} Score:{r['score']:.2f} [{r['level']}]")

    ra = result["resource_allocation"]
    print(f"\n💰 RESOURCE ALLOCATION (FY{ra['fiscal_year']}):")
    print(f"  Total Budget: ${ra['total_budget_usd']:,.0f}")
    print(f"  Allocated: ${ra['total_allocated_usd']:,.0f} ({ra['utilization_rate']}%)")
    print(f"  Top Funded: {ra['top_funded_pillar']} (${ra['top_funded_amount']:,.0f})")
    print(f"  Pillar Allocations:")
    for pillar, amount in sorted(ra["allocations"].items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(amount / ra['total_budget_usd'] * 30)
        print(f"    {pillar[:25]:<25} ${amount:>10,.0f} {bar}")

    mt = result["milestone_tracker"]
    print(f"\n📅 MILESTONE TRACKER:")
    print(f"  Total: {mt['total_milestones']} | Completed: {mt['completed']} | On Track: {mt['on_track']} | At Risk: {mt['at_risk']}")

    sc = result["strategic_scorecard"]
    print(f"\n📊 STRATEGIC SCORECARD:")
    print(f"  Overall Score: {sc['overall_score']}/100 — Grade: {sc['performance_grade']}")
    for component, score in sc["components"].items():
        bar = "█" * int(score / 5)
        print(f"  {component:<40} {score:5.1f}% {bar}")
    print(f"  Trend: {sc['trend'].upper()}")

    print(f"\n🏆 PRIORITY RECOMMENDATIONS:")
    for i, rec in enumerate(result["priority_recommendations"][:5], 1):
        print(f"  {i}. {rec[:90]}")

    print(f"\n{'='*70}")
    print("✅ Module 42: strategic_planning.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
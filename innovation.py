"""
Module 41: innovation.py
Research Innovation & Technology Pipeline for One Health
Zoonotic Disease Prevention and Response
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

class InnovationType(Enum):
    DIAGNOSTIC = "diagnostic"
    THERAPEUTIC = "therapeutic"
    VACCINE = "vaccine"
    SURVEILLANCE = "surveillance"
    ANALYTICS = "analytics"
    COMMUNICATION = "communication"
    ENVIRONMENTAL = "environmental"
    ONE_HEALTH_PLATFORM = "one_health_platform"

class DevelopmentStage(Enum):
    CONCEPT = "concept"
    RESEARCH = "research"
    PROTOTYPE = "prototype"
    PILOT = "pilot"
    VALIDATION = "validation"
    SCALE_UP = "scale_up"
    DEPLOYED = "deployed"

class FundingStatus(Enum):
    SEEKING = "seeking"
    PARTIALLY_FUNDED = "partially_funded"
    FULLY_FUNDED = "fully_funded"
    COMPLETED = "completed"

class TechReadinessLevel(Enum):
    TRL1 = "basic_research"           # TRL 1
    TRL2 = "concept_formulated"       # TRL 2
    TRL3 = "proof_of_concept"         # TRL 3
    TRL4 = "lab_validated"            # TRL 4
    TRL5 = "field_validated"          # TRL 5
    TRL6 = "system_demonstrated"      # TRL 6
    TRL7 = "prototype_demonstrated"   # TRL 7
    TRL8 = "system_complete"          # TRL 8
    TRL9 = "deployed"                 # TRL 9

class ResearchPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"

class CollaborationRole(Enum):
    LEAD = "lead"
    PARTNER = "partner"
    FUNDER = "funder"
    ADVISORY = "advisory"
    IMPLEMENTING = "implementing"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class InnovationProject:
    project_id: str
    title: str
    innovation_type: InnovationType
    description: str
    target_pathogen: str
    development_stage: DevelopmentStage
    trl: TechReadinessLevel
    priority: ResearchPriority
    lead_institution: str
    collaborators: list
    budget_total_usd: float
    budget_spent_usd: float
    funding_status: FundingStatus
    start_date: str
    expected_completion: str
    key_milestones: list
    current_milestone: str
    impact_estimate: str
    publications: int
    patents: int

@dataclass
class ResearchFinding:
    finding_id: str
    project_id: str
    title: str
    description: str
    significance: str   # breakthrough / significant / incremental
    pathogen: str
    date_published: str
    doi: str
    citations: int
    policy_relevance: str

@dataclass
class TechnologyAssessment:
    tech_id: str
    technology_name: str
    category: str
    current_trl: int
    target_trl: int
    strengths: list
    weaknesses: list
    opportunities: list
    threats: list  # SWOT
    feasibility_score: float    # 0-100
    impact_score: float         # 0-100
    investment_required_usd: float
    time_to_deploy_months: int
    recommendation: str

@dataclass
class GrantOpportunity:
    grant_id: str
    title: str
    funder: str
    focus_area: str
    amount_usd: float
    deadline: str
    eligibility: list
    alignment_score: float  # 0-1
    recommended: bool

@dataclass
class IntellectualProperty:
    ip_id: str
    title: str
    type: str       # patent / copyright / trade_secret / trademark
    status: str     # pending / granted / expired / licensed
    filing_date: str
    country: str
    inventors: list
    commercial_potential: str


# ============================================================
# INNOVATION PORTFOLIO MANAGER
# ============================================================

class InnovationPortfolioManager:
    """
    Manages One Health research and innovation portfolio
    """

    def __init__(self):
        self.projects = self._initialize_portfolio()

    def _initialize_portfolio(self) -> list:
        projects = [
            InnovationProject(
                "PROJ_001", "AI-Powered Zoonotic Early Warning System",
                InnovationType.SURVEILLANCE,
                "Machine learning model integrating animal, human, and environmental data for real-time zoonotic risk prediction",
                "Multi-pathogen", DevelopmentStage.PILOT, TechReadinessLevel.TRL6,
                ResearchPriority.CRITICAL, "National AI Health Institute",
                ["WHO", "FAO", "CIRAD", "National Veterinary Lab"],
                2500000, 1750000, FundingStatus.FULLY_FUNDED,
                "2023-01-01", "2025-12-31",
                ["Data integration complete", "Model training", "Pilot deployment", "Validation", "Scale-up"],
                "Pilot deployment", "Early detection of zoonotic events 14 days earlier than conventional methods",
                8, 2
            ),
            InnovationProject(
                "PROJ_002", "Rapid Point-of-Care H5N1 Diagnostic Kit",
                InnovationType.DIAGNOSTIC,
                "CRISPR-based lateral flow assay for field diagnosis of H5N1 with 98% sensitivity in <30 minutes",
                "H5N1 Avian Influenza", DevelopmentStage.VALIDATION, TechReadinessLevel.TRL7,
                ResearchPriority.CRITICAL, "BioTech Diagnostics Ltd",
                ["Ministry of Health", "FDA", "Manufacturing Partner"],
                1800000, 1400000, FundingStatus.FULLY_FUNDED,
                "2022-06-01", "2024-12-31",
                ["CRISPR design", "Lab validation", "Field validation", "Regulatory submission", "Production"],
                "Regulatory submission", "98% sensitivity/specificity; enables immediate field diagnosis",
                5, 1
            ),
            InnovationProject(
                "PROJ_003", "mRNA Universal Zoonotic Vaccine Platform",
                InnovationType.VACCINE,
                "mRNA platform adaptable for rapid vaccine development against emerging zoonotic pathogens",
                "Broad-spectrum zoonotic", DevelopmentStage.RESEARCH, TechReadinessLevel.TRL4,
                ResearchPriority.HIGH, "Vaccine Innovation Center",
                ["NIH", "CEPI", "Pharma Partner"],
                5000000, 800000, FundingStatus.PARTIALLY_FUNDED,
                "2024-01-01", "2028-12-31",
                ["Platform design", "Animal trials", "Phase I trial", "Phase II trial", "Regulatory", "Production"],
                "Animal trials", "100-day vaccine development capability for novel zoonotic threats",
                2, 3
            ),
            InnovationProject(
                "PROJ_004", "Environmental DNA (eDNA) Pathogen Surveillance",
                InnovationType.ENVIRONMENTAL,
                "Wastewater and environmental eDNA monitoring system for early detection of zoonotic pathogen emergence",
                "Multi-pathogen", DevelopmentStage.PROTOTYPE, TechReadinessLevel.TRL5,
                ResearchPriority.HIGH, "Environmental Health Research Center",
                ["Environmental Agency", "Water Authority", "Universities"],
                900000, 450000, FundingStatus.FULLY_FUNDED,
                "2023-06-01", "2025-06-30",
                ["Protocol development", "Lab validation", "Field prototype", "Multi-site pilot", "Scale"],
                "Multi-site pilot", "Detect pathogen emergence 3-4 weeks before clinical cases present",
                3, 0
            ),
            InnovationProject(
                "PROJ_005", "One Health Digital Twin Platform",
                InnovationType.ONE_HEALTH_PLATFORM,
                "Digital twin simulation platform modeling human-animal-environment disease dynamics for policy testing",
                "Multi-pathogen", DevelopmentStage.CONCEPT, TechReadinessLevel.TRL2,
                ResearchPriority.MODERATE, "Digital Health Innovation Lab",
                ["Tech Industry Partner", "Academia", "Government"],
                3200000, 100000, FundingStatus.SEEKING,
                "2025-01-01", "2028-12-31",
                ["Requirements", "Architecture", "Core model", "Validation", "User interface", "Deployment"],
                "Requirements gathering", "Real-time policy simulation for One Health interventions",
                0, 0
            ),
            InnovationProject(
                "PROJ_006", "Antimicrobial Resistance One Health Monitor",
                InnovationType.SURVEILLANCE,
                "Integrated AMR surveillance system across human clinical, animal, and environmental settings",
                "AMR Pathogens", DevelopmentStage.PILOT, TechReadinessLevel.TRL6,
                ResearchPriority.HIGH, "AMR Research Alliance",
                ["WHO GLASS", "OIE", "National Labs", "Agricultural Ministry"],
                1500000, 900000, FundingStatus.FULLY_FUNDED,
                "2023-03-01", "2025-09-30",
                ["Data standards", "Lab network", "Pilot sites", "Analysis platform", "Report system"],
                "Analysis platform", "Comprehensive AMR tracking across One Health domains",
                6, 1
            )
        ]
        return projects

    def get_portfolio_summary(self) -> dict:
        total_budget = sum(p.budget_total_usd for p in self.projects)
        spent = sum(p.budget_spent_usd for p in self.projects)
        by_stage = {}
        by_type = {}
        for p in self.projects:
            stage = p.development_stage.value
            ptype = p.innovation_type.value
            by_stage[stage] = by_stage.get(stage, 0) + 1
            by_type[ptype] = by_type.get(ptype, 0) + 1

        return {
            "total_projects": len(self.projects),
            "total_portfolio_value_usd": total_budget,
            "total_spent_usd": spent,
            "utilization_rate": round(spent / total_budget * 100, 1) if total_budget > 0 else 0,
            "by_stage": by_stage,
            "by_innovation_type": by_type,
            "critical_priority": sum(1 for p in self.projects if p.priority == ResearchPriority.CRITICAL),
            "total_publications": sum(p.publications for p in self.projects),
            "total_patents": sum(p.patents for p in self.projects)
        }

    def prioritize_projects(self) -> list:
        """Score and rank projects by impact and feasibility"""
        scored = []
        for proj in self.projects:
            trl_num = int(proj.trl.name.replace("TRL", ""))
            stage_score = {"concept": 10, "research": 20, "prototype": 40,
                           "pilot": 60, "validation": 75, "scale_up": 90, "deployed": 100}
            priority_score = {"critical": 100, "high": 75, "moderate": 50, "low": 25}

            score = (stage_score.get(proj.development_stage.value, 50) * 0.3 +
                     priority_score.get(proj.priority.value, 50) * 0.4 +
                     trl_num * 5 * 0.3)

            scored.append({
                "project_id": proj.project_id,
                "title": proj.title,
                "type": proj.innovation_type.value,
                "stage": proj.development_stage.value,
                "priority": proj.priority.value,
                "score": round(score, 1),
                "budget_usd": proj.budget_total_usd,
                "expected_completion": proj.expected_completion
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        for i, p in enumerate(scored):
            p["rank"] = i + 1

        return scored


# ============================================================
# TECHNOLOGY ASSESSOR
# ============================================================

class TechnologyAssessor:
    """
    Evaluates emerging technologies for One Health applications
    """

    def assess_technology(self, tech_name: str, category: str, current_trl: int) -> TechnologyAssessment:
        """Perform SWOT-based technology assessment"""

        swot = {
            "AI/ML Surveillance": {
                "strengths": ["High sensitivity for pattern detection", "Processes large datasets in real-time", "Continuous learning capability"],
                "weaknesses": ["Requires large training datasets", "Black-box explainability challenges", "Infrastructure dependencies"],
                "opportunities": ["Integration with global surveillance networks", "Predictive modeling for emerging threats", "Cost reduction over time"],
                "threats": ["Data privacy concerns", "Algorithmic bias", "Adversarial manipulation"]
            },
            "CRISPR Diagnostics": {
                "strengths": ["High sensitivity and specificity", "Rapid results (<30min)", "Low-cost reagents"],
                "weaknesses": ["Temperature sensitivity", "Limited multiplex capacity", "Regulatory pathway complexity"],
                "opportunities": ["Point-of-care deployment", "Adaptation to new pathogens", "Global health applications"],
                "threats": ["Emerging pathogen variants", "Patent restrictions", "Trained operator requirements"]
            },
            "Digital Twin": {
                "strengths": ["Real-time scenario modeling", "Policy impact prediction", "Multi-sector integration"],
                "weaknesses": ["High development cost", "Data requirements", "Validation complexity"],
                "opportunities": ["Pandemic preparedness planning", "Resource optimization", "Training simulation"],
                "threats": ["Model accuracy limitations", "Data silos", "Stakeholder adoption barriers"]
            }
        }

        default_swot = {
            "strengths": ["Novel approach to existing problem", "Leverages current technology", "Scalable design"],
            "weaknesses": ["Early development stage", "Limited field validation", "High initial investment"],
            "opportunities": ["Market gap exists", "International interest", "Integration potential"],
            "threats": ["Competing solutions", "Regulatory uncertainty", "Funding sustainability"]
        }

        selected_swot = swot.get(category, default_swot)

        feasibility = min(current_trl * 10 + random.uniform(-10, 10), 100)
        impact = random.uniform(60, 95)
        target_trl = min(current_trl + 2, 9)
        investment = (target_trl - current_trl) * random.uniform(200000, 800000)
        timeline = (target_trl - current_trl) * random.randint(6, 18)

        if feasibility > 70 and impact > 75:
            recommendation = "STRONGLY RECOMMENDED - High feasibility and impact"
        elif feasibility > 60 or impact > 70:
            recommendation = "RECOMMENDED - Good potential with manageable risks"
        else:
            recommendation = "CONDITIONAL - Further research needed before investment"

        return TechnologyAssessment(
            tech_id=f"TECH_{tech_name[:5].upper()}_{datetime.now().strftime('%Y%m%d')}",
            technology_name=tech_name,
            category=category,
            current_trl=current_trl,
            target_trl=target_trl,
            strengths=selected_swot["strengths"],
            weaknesses=selected_swot["weaknesses"],
            opportunities=selected_swot["opportunities"],
            threats=selected_swot["threats"],
            feasibility_score=round(feasibility, 1),
            impact_score=round(impact, 1),
            investment_required_usd=round(investment),
            time_to_deploy_months=timeline,
            recommendation=recommendation
        )

    def compare_technologies(self, technologies: list) -> dict:
        """Compare multiple technologies"""
        assessments = [self.assess_technology(t["name"], t["category"], t["trl"]) for t in technologies]
        assessments.sort(key=lambda x: (x.feasibility_score + x.impact_score) / 2, reverse=True)

        return {
            "comparison_date": datetime.now().isoformat(),
            "technologies_assessed": len(assessments),
            "rankings": [
                {
                    "rank": i + 1,
                    "name": a.technology_name,
                    "category": a.category,
                    "trl": a.current_trl,
                    "feasibility": a.feasibility_score,
                    "impact": a.impact_score,
                    "composite_score": round((a.feasibility_score + a.impact_score) / 2, 1),
                    "investment_usd": a.investment_required_usd,
                    "timeline_months": a.time_to_deploy_months,
                    "recommendation": a.recommendation
                }
                for i, a in enumerate(assessments)
            ],
            "top_recommendation": assessments[0].technology_name if assessments else None
        }


# ============================================================
# GRANT & FUNDING MANAGER
# ============================================================

class GrantFundingManager:
    """
    Identifies and manages grant opportunities for One Health research
    """

    def __init__(self):
        self.opportunities = self._load_opportunities()

    def _load_opportunities(self) -> list:
        return [
            GrantOpportunity("GRN_001", "WHO Global Health Security R&D Fund",
                             "WHO", "Pandemic preparedness and early warning systems",
                             3000000, (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                             ["National research institutions", "WHO member states"], 0.92, True),
            GrantOpportunity("GRN_002", "NIH One Health Research Initiative",
                             "NIH/NIAID", "Zoonotic disease prevention and control",
                             2500000, (datetime.now() + timedelta(days=120)).strftime("%Y-%m-%d"),
                             ["Academic institutions", "Government agencies"], 0.88, True),
            GrantOpportunity("GRN_003", "CEPI Rapid Vaccine Development",
                             "CEPI", "Platform technologies for epidemic vaccines",
                             5000000, (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                             ["Biotech companies", "Research institutions"], 0.75, True),
            GrantOpportunity("GRN_004", "Bill & Melinda Gates Foundation - Global Health",
                             "BMGF", "Diagnostic tools for low-resource settings",
                             1500000, (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                             ["NGOs", "Research institutions", "Social enterprises"], 0.80, True),
            GrantOpportunity("GRN_005", "EU Horizon Europe - Health Cluster",
                             "European Commission", "Infectious disease surveillance systems",
                             4000000, (datetime.now() + timedelta(days=150)).strftime("%Y-%m-%d"),
                             ["EU member state institutions", "International partners"], 0.70, False),
            GrantOpportunity("GRN_006", "USAID Global Health Security",
                             "USAID", "Emerging threats detection and response",
                             2000000, (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
                             ["LMIC institutions", "US implementing partners"], 0.85, True)
        ]

    def get_top_opportunities(self, min_alignment: float = 0.75) -> list:
        filtered = [g for g in self.opportunities if g.alignment_score >= min_alignment and g.recommended]
        filtered.sort(key=lambda x: x.alignment_score, reverse=True)

        return [
            {
                "grant_id": g.grant_id,
                "title": g.title,
                "funder": g.funder,
                "amount_usd": g.amount_usd,
                "deadline": g.deadline,
                "alignment_score": g.alignment_score,
                "days_until_deadline": (datetime.strptime(g.deadline, "%Y-%m-%d") - datetime.now()).days
            }
            for g in filtered
        ]

    def get_funding_summary(self) -> dict:
        total_potential = sum(g.amount_usd for g in self.opportunities if g.recommended)
        return {
            "total_opportunities": len(self.opportunities),
            "recommended": sum(1 for g in self.opportunities if g.recommended),
            "total_potential_funding_usd": total_potential,
            "avg_alignment_score": round(sum(g.alignment_score for g in self.opportunities) / len(self.opportunities), 2)
        }


# ============================================================
# KNOWLEDGE MANAGEMENT SYSTEM
# ============================================================

class KnowledgeManagementSystem:
    """
    Manages research findings, publications, and intellectual property
    """

    def __init__(self):
        self.findings = self._initialize_findings()
        self.ip_portfolio = self._initialize_ip()

    def _initialize_findings(self) -> list:
        return [
            ResearchFinding("RES_001", "PROJ_001", "Real-time AI zoonotic risk prediction achieves 87% accuracy",
                            "LSTM-based model integrating livestock density, climate, and human mobility achieves 87% accuracy in predicting zoonotic spillover events 14 days in advance",
                            "significant", "Multi-pathogen", (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                            "10.1016/j.onehealth.2024.001", 24,
                            "Direct application to national zoonotic early warning systems"),
            ResearchFinding("RES_002", "PROJ_002", "CRISPR-Cas12 H5N1 diagnostic: 98.7% sensitivity in field conditions",
                            "CRISPR-Cas12a lateral flow assay demonstrated 98.7% sensitivity and 99.1% specificity for H5N1 detection in <30 minutes under field conditions",
                            "breakthrough", "H5N1 Avian Influenza", (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d"),
                            "10.1016/j.diagnostics.2024.002", 67,
                            "Could replace expensive PCR for field diagnosis; regulatory submission pending"),
            ResearchFinding("RES_003", "PROJ_004", "eDNA surveillance detects HPAI 3.2 weeks before first human case",
                            "Environmental DNA monitoring of water sources detected H5N1 genetic material 3.2 weeks (±0.8 weeks) before the first confirmed human case across 12 outbreak settings",
                            "breakthrough", "H5N1 Avian Influenza", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                            "10.1016/j.envint.2024.003", 43,
                            "Immediate integration into national surveillance recommended"),
            ResearchFinding("RES_004", "PROJ_006", "One Health AMR surveillance reveals 40% community-level cross-contamination",
                            "Integrated AMR surveillance across clinical, agricultural, and environmental settings reveals 40% of community-level AMR isolates share identical resistance genes with livestock sources",
                            "significant", "AMR Pathogens", (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                            "10.1016/j.ijamac.2024.004", 12,
                            "Urgent need for integrated One Health AMR policy")
        ]

    def _initialize_ip(self) -> list:
        return [
            IntellectualProperty("IP_001", "CRISPR-Based H5N1 Rapid Diagnostic Kit",
                                 "patent", "granted", "2023-06-15", "International PCT",
                                 ["Dr. Kim", "Dr. Santos", "Dr. Lee"], "HIGH - commercial licensing potential"),
            IntellectualProperty("IP_002", "AI Zoonotic Risk Prediction Algorithm",
                                 "patent", "pending", "2024-01-10", "US/EU/CN",
                                 ["Dr. Chen", "Dr. Osei"], "MODERATE - open source considerations"),
            IntellectualProperty("IP_003", "eDNA Pathogen Surveillance Protocol",
                                 "copyright", "granted", "2023-09-01", "International",
                                 ["Dr. Santos", "Environmental Health Team"], "MODERATE")
        ]

    def get_research_summary(self) -> dict:
        return {
            "total_findings": len(self.findings),
            "breakthrough_findings": sum(1 for f in self.findings if f.significance == "breakthrough"),
            "total_citations": sum(f.citations for f in self.findings),
            "ip_portfolio": {
                "total_ip": len(self.ip_portfolio),
                "patents": sum(1 for ip in self.ip_portfolio if ip.type == "patent"),
                "granted": sum(1 for ip in self.ip_portfolio if ip.status == "granted")
            },
            "top_finding": max(self.findings, key=lambda x: x.citations).title if self.findings else None
        }


# ============================================================
# INTEGRATED INNOVATION SYSTEM
# ============================================================

class OneHealthInnovationSystem:
    """
    Main integrated innovation and research management system
    """

    def __init__(self):
        self.portfolio = InnovationPortfolioManager()
        self.assessor = TechnologyAssessor()
        self.grants = GrantFundingManager()
        self.knowledge = KnowledgeManagementSystem()

    def run_innovation_review(self) -> dict:
        """Comprehensive innovation portfolio review"""

        print(f"\n{'='*60}")
        print("ONE HEALTH INNOVATION & RESEARCH SYSTEM")
        print(f"{'='*60}")

        # Portfolio summary
        print("📊 Reviewing Innovation Portfolio...")
        portfolio_summary = self.portfolio.get_portfolio_summary()
        ranked_projects = self.portfolio.prioritize_projects()

        # Technology assessment
        print("🔬 Assessing Key Technologies...")
        tech_list = [
            {"name": "AI/ML Surveillance Platform", "category": "AI/ML Surveillance", "trl": 6},
            {"name": "CRISPR Rapid Diagnostics", "category": "CRISPR Diagnostics", "trl": 7},
            {"name": "One Health Digital Twin", "category": "Digital Twin", "trl": 2},
            {"name": "mRNA Vaccine Platform", "category": "Vaccine Technology", "trl": 4},
            {"name": "eDNA Environmental Monitoring", "category": "Environmental Tech", "trl": 5}
        ]
        tech_comparison = self.assessor.compare_technologies(tech_list)

        # Funding opportunities
        print("💰 Scanning Funding Opportunities...")
        top_grants = self.grants.get_top_opportunities(0.75)
        funding_summary = self.grants.get_funding_summary()

        # Research knowledge base
        print("📚 Compiling Research Knowledge Base...")
        research_summary = self.knowledge.get_research_summary()

        return {
            "review_id": f"INNOV_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "portfolio": portfolio_summary,
            "top_projects": ranked_projects[:5],
            "technology_assessment": tech_comparison,
            "funding": {
                "summary": funding_summary,
                "top_opportunities": top_grants
            },
            "research_knowledge": research_summary,
            "strategic_recommendations": [
                f"Prioritize {ranked_projects[0]['title']} — highest composite score",
                f"Apply for {top_grants[0]['title']} by {top_grants[0]['deadline']} (${top_grants[0]['amount_usd']:,.0f})",
                f"Fast-track {tech_comparison['top_recommendation']} technology deployment",
                "Strengthen IP portfolio to protect CRISPR diagnostic innovations",
                "Establish global One Health data sharing consortium to accelerate AI model development"
            ]
        }


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 41: INNOVATION SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    system = OneHealthInnovationSystem()
    result = system.run_innovation_review()

    p = result["portfolio"]
    print(f"\n📊 INNOVATION PORTFOLIO:")
    print(f"  Total Projects: {p['total_projects']}")
    print(f"  Portfolio Value: ${p['total_portfolio_value_usd']:,.0f}")
    print(f"  Budget Utilized: {p['utilization_rate']}%")
    print(f"  Critical Priority: {p['critical_priority']} projects")
    print(f"  Publications: {p['total_publications']} | Patents: {p['total_patents']}")
    print(f"  By Stage: {p['by_stage']}")

    print(f"\n🏆 TOP RANKED PROJECTS:")
    for proj in result["top_projects"][:5]:
        print(f"  #{proj['rank']} {proj['title'][:50]:<50} Score:{proj['score']:5.1f} [{proj['stage'].upper()}]")

    ta = result["technology_assessment"]
    print(f"\n🔬 TECHNOLOGY ASSESSMENT:")
    print(f"  Technologies Evaluated: {ta['technologies_assessed']}")
    print(f"  Top Recommendation: {ta['top_recommendation']}")
    print(f"\n  Rankings:")
    for r in ta["rankings"]:
        print(f"  #{r['rank']} {r['name']:<35} Feasibility:{r['feasibility']:4.0f} Impact:{r['impact']:4.0f} Composite:{r['composite_score']:4.0f}")
        print(f"      → {r['recommendation'][:60]}")

    f = result["funding"]
    fs = f["summary"]
    print(f"\n💰 FUNDING LANDSCAPE:")
    print(f"  Total Opportunities: {fs['total_opportunities']}")
    print(f"  Recommended: {fs['recommended']}")
    print(f"  Total Potential: ${fs['total_potential_funding_usd']:,.0f}")
    print(f"  Avg Alignment: {fs['avg_alignment_score']:.0%}")
    print(f"\n  Top Opportunities:")
    for g in f["top_opportunities"][:4]:
        print(f"  • {g['title'][:45]:<45} ${g['amount_usd']:>10,.0f} | Alignment: {g['alignment_score']:.0%} | Due: {g['deadline']}")

    rk = result["research_knowledge"]
    print(f"\n📚 RESEARCH KNOWLEDGE BASE:")
    print(f"  Total Findings: {rk['total_findings']}")
    print(f"  Breakthrough Findings: {rk['breakthrough_findings']}")
    print(f"  Total Citations: {rk['total_citations']}")
    print(f"  IP Portfolio: {rk['ip_portfolio']['total_ip']} items ({rk['ip_portfolio']['granted']} granted)")
    print(f"  Top Finding: {rk['top_finding']}")

    print(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
    for i, rec in enumerate(result["strategic_recommendations"], 1):
        print(f"  {i}. {rec}")

    print(f"\n{'='*70}")
    print("✅ Module 41: innovation.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
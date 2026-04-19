"""
Module 37: decision_support.py
Advanced Decision Support System for One Health Zoonotic Disease Management
Supports NIW (National Interest Waiver) petition demonstration
"""

import json
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class DecisionType(Enum):
    CLINICAL = "clinical"
    PUBLIC_HEALTH = "public_health"
    POLICY = "policy"
    RESOURCE = "resource"
    STRATEGIC = "strategic"

class UrgencyLevel(Enum):
    IMMEDIATE = "immediate"      # < 1 hour
    URGENT = "urgent"            # < 24 hours
    HIGH = "high"                # < 72 hours
    MODERATE = "moderate"        # < 1 week
    LOW = "low"                  # > 1 week

class EvidenceLevel(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    EXPERT_OPINION = "expert_opinion"

class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class DecisionCriteria:
    criterion_id: str
    name: str
    description: str
    weight: float          # 0.0 - 1.0
    unit: str
    higher_is_better: bool = True

@dataclass
class DecisionOption:
    option_id: str
    name: str
    description: str
    scores: dict           # criterion_id -> score (0-100)
    cost: float
    feasibility: float     # 0-1
    implementation_time_days: int
    risks: list
    benefits: list

@dataclass
class EvidenceItem:
    evidence_id: str
    source: str
    evidence_type: str
    level: EvidenceLevel
    summary: str
    relevance_score: float  # 0-1
    publication_date: str
    supports_action: bool

@dataclass
class DecisionRecommendation:
    recommendation_id: str
    decision_type: DecisionType
    urgency: UrgencyLevel
    recommended_option: str
    confidence_score: float
    rationale: str
    supporting_evidence: list
    alternative_options: list
    risks: list
    implementation_steps: list
    monitoring_metrics: list
    review_date: str
    generated_at: str

@dataclass
class RiskBenefitAnalysis:
    option_id: str
    option_name: str
    benefits: list
    risks: list
    benefit_score: float    # 0-100
    risk_score: float       # 0-100
    net_value: float        # benefit - risk
    recommendation: str

@dataclass
class PolicyScenario:
    scenario_id: str
    name: str
    description: str
    parameters: dict
    projected_outcomes: dict
    probability: float
    time_horizon_days: int


# ============================================================
# MULTI-CRITERIA DECISION ANALYSIS (MCDA)
# ============================================================

class MultiCriteriaDecisionAnalyzer:
    """
    Advanced Multi-Criteria Decision Analysis for One Health interventions
    Uses weighted scoring with sensitivity analysis
    """

    def __init__(self):
        self.default_criteria = self._define_default_criteria()

    def _define_default_criteria(self) -> list:
        return [
            DecisionCriteria("effectiveness", "Effectiveness", "Intervention effectiveness rate", 0.30, "%", True),
            DecisionCriteria("cost_efficiency", "Cost Efficiency", "Cost per prevented case", 0.20, "USD", False),
            DecisionCriteria("feasibility", "Feasibility", "Implementation feasibility", 0.20, "score", True),
            DecisionCriteria("speed", "Implementation Speed", "Time to full deployment", 0.15, "days", False),
            DecisionCriteria("safety", "Safety Profile", "Adverse event rate", 0.10, "score", True),
            DecisionCriteria("equity", "Health Equity", "Impact on vulnerable populations", 0.05, "score", True),
        ]

    def analyze(self, options: list, criteria: list = None) -> dict:
        """Perform MCDA on intervention options"""
        if criteria is None:
            criteria = self.default_criteria

        # Normalize weights
        total_weight = sum(c.weight for c in criteria)
        normalized_weights = {c.criterion_id: c.weight / total_weight for c in criteria}

        results = []
        for option in options:
            weighted_score = 0.0
            criterion_scores = {}

            for criterion in criteria:
                raw_score = option.scores.get(criterion.criterion_id, 50)
                # Invert score if lower is better
                if not criterion.higher_is_better:
                    raw_score = 100 - raw_score
                weighted = raw_score * normalized_weights[criterion.criterion_id]
                weighted_score += weighted
                criterion_scores[criterion.criterion_id] = {
                    "raw_score": option.scores.get(criterion.criterion_id, 50),
                    "normalized_score": raw_score,
                    "weighted_score": weighted
                }

            results.append({
                "option_id": option.option_id,
                "option_name": option.name,
                "total_score": round(weighted_score, 2),
                "criterion_scores": criterion_scores,
                "cost": option.cost,
                "feasibility": option.feasibility,
                "implementation_days": option.implementation_time_days,
                "rank": 0
            })

        # Rank options
        results.sort(key=lambda x: x["total_score"], reverse=True)
        for i, r in enumerate(results):
            r["rank"] = i + 1

        return {
            "analysis_type": "multi_criteria_decision_analysis",
            "timestamp": datetime.now().isoformat(),
            "options_evaluated": len(options),
            "criteria_used": len(criteria),
            "ranked_options": results,
            "best_option": results[0] if results else None,
            "recommendation": f"Option '{results[0]['option_name']}' ranks highest with score {results[0]['total_score']:.1f}/100" if results else "No options"
        }

    def sensitivity_analysis(self, options: list, criteria: list = None) -> dict:
        """Test how robust ranking is to weight changes"""
        if criteria is None:
            criteria = self.default_criteria

        baseline = self.analyze(options, criteria)
        baseline_best = baseline["best_option"]["option_name"] if baseline["best_option"] else "None"

        perturbations = []
        for criterion in criteria:
            # Increase weight by 50%
            modified = []
            total_w = 0
            for c in criteria:
                w = c.weight * 1.5 if c.criterion_id == criterion.criterion_id else c.weight
                total_w += w
                modified.append(DecisionCriteria(c.criterion_id, c.name, c.description, w, c.unit, c.higher_is_better))

            result = self.analyze(options, modified)
            new_best = result["best_option"]["option_name"] if result["best_option"] else "None"

            perturbations.append({
                "criterion_modified": criterion.name,
                "weight_change": "+50%",
                "new_best_option": new_best,
                "ranking_changed": new_best != baseline_best
            })

        stable = sum(1 for p in perturbations if not p["ranking_changed"])
        return {
            "baseline_best": baseline_best,
            "stability_ratio": round(stable / len(perturbations), 2) if perturbations else 0,
            "perturbation_results": perturbations,
            "robust_recommendation": stable >= len(perturbations) * 0.7
        }


# ============================================================
# EVIDENCE-BASED RECOMMENDATION ENGINE
# ============================================================

class EvidenceBasedRecommendationEngine:
    """
    Generates evidence-based recommendations for One Health interventions
    """

    def __init__(self):
        self.evidence_weights = {
            EvidenceLevel.STRONG: 1.0,
            EvidenceLevel.MODERATE: 0.7,
            EvidenceLevel.WEAK: 0.4,
            EvidenceLevel.EXPERT_OPINION: 0.2
        }

    def generate_recommendation(self, situation: dict, evidence_items: list, options: list) -> DecisionRecommendation:
        """Generate comprehensive recommendation based on evidence"""

        # Score evidence
        evidence_score = self._calculate_evidence_score(evidence_items)
        risk_level = situation.get("risk_level", RiskLevel.MODERATE)
        urgency = self._determine_urgency(risk_level, situation)

        # Select best option
        best_option = self._select_best_option(options, evidence_items, situation)

        # Build recommendation
        steps = self._generate_implementation_steps(best_option, urgency)
        monitoring = self._define_monitoring_metrics(situation)

        rec = DecisionRecommendation(
            recommendation_id=f"REC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            decision_type=DecisionType[situation.get("decision_type", "PUBLIC_HEALTH")],
            urgency=urgency,
            recommended_option=best_option.name if best_option else "No clear recommendation",
            confidence_score=round(evidence_score * 100, 1),
            rationale=self._build_rationale(situation, evidence_items, best_option),
            supporting_evidence=[e.evidence_id for e in evidence_items if e.supports_action],
            alternative_options=[o.name for o in options if o != best_option],
            risks=best_option.risks if best_option else [],
            implementation_steps=steps,
            monitoring_metrics=monitoring,
            review_date=(datetime.now() + timedelta(days=7)).isoformat(),
            generated_at=datetime.now().isoformat()
        )
        return rec

    def _calculate_evidence_score(self, evidence_items: list) -> float:
        if not evidence_items:
            return 0.3
        total = sum(self.evidence_weights[e.level] * e.relevance_score for e in evidence_items)
        max_possible = sum(self.evidence_weights[EvidenceLevel.STRONG] for _ in evidence_items)
        return min(total / max_possible, 1.0) if max_possible > 0 else 0.3

    def _determine_urgency(self, risk_level, situation: dict) -> UrgencyLevel:
        active_outbreak = situation.get("active_outbreak", False)
        case_count = situation.get("case_count", 0)

        if active_outbreak and case_count > 50:
            return UrgencyLevel.IMMEDIATE
        elif risk_level == RiskLevel.CRITICAL:
            return UrgencyLevel.URGENT
        elif risk_level == RiskLevel.HIGH:
            return UrgencyLevel.HIGH
        elif risk_level == RiskLevel.MODERATE:
            return UrgencyLevel.MODERATE
        return UrgencyLevel.LOW

    def _select_best_option(self, options: list, evidence: list, situation: dict):
        if not options:
            return None
        # Score each option based on evidence support and feasibility
        scored = []
        for option in options:
            score = option.feasibility * 50
            score += min(option.scores.get("effectiveness", 50), 100) * 0.3
            score += max(0, 100 - option.cost / 10000) * 0.2
            scored.append((option, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[0][0]

    def _build_rationale(self, situation: dict, evidence: list, option) -> str:
        strong_evidence = [e for e in evidence if e.level == EvidenceLevel.STRONG]
        rationale = f"Based on {len(evidence)} evidence sources "
        rationale += f"({len(strong_evidence)} strong), "
        rationale += f"current risk level ({situation.get('risk_level', 'unknown')}), "
        if option:
            rationale += f"option '{option.name}' offers optimal balance of effectiveness and feasibility."
        return rationale

    def _generate_implementation_steps(self, option, urgency: UrgencyLevel) -> list:
        base_steps = [
            "1. Convene One Health response team (human, animal, environment sectors)",
            "2. Conduct rapid situation assessment and confirm diagnosis",
            "3. Activate incident command structure",
            "4. Mobilize required resources and personnel",
            "5. Implement primary intervention strategy",
            "6. Establish real-time monitoring and reporting",
            "7. Coordinate with international partners if needed",
            "8. Document outcomes for after-action review"
        ]
        if urgency == UrgencyLevel.IMMEDIATE:
            return ["IMMEDIATE: " + s for s in base_steps[:4]] + base_steps[4:]
        return base_steps

    def _define_monitoring_metrics(self, situation: dict) -> list:
        return [
            "Case incidence rate (daily)",
            "Animal-to-human transmission rate",
            "Intervention coverage percentage",
            "Healthcare system utilization",
            "Environmental pathogen detection",
            "Public compliance rate",
            "Response resource utilization",
            "Outbreak containment progress"
        ]


# ============================================================
# RISK-BENEFIT ANALYZER
# ============================================================

class RiskBenefitAnalyzer:
    """
    Quantitative risk-benefit analysis for One Health interventions
    """

    def analyze_option(self, option: DecisionOption, population_size: int = 100000) -> RiskBenefitAnalysis:
        """Calculate risk-benefit score for an intervention option"""

        # Quantify benefits
        benefit_items = []
        benefit_score = 0.0

        effectiveness = option.scores.get("effectiveness", 50)
        cases_prevented = int(population_size * (effectiveness / 100) * 0.01)
        benefit_items.append({"type": "cases_prevented", "value": cases_prevented, "score": effectiveness * 0.4})
        benefit_score += effectiveness * 0.4

        economic_benefit = cases_prevented * 5000  # avg cost per case
        benefit_items.append({"type": "economic_benefit_usd", "value": economic_benefit, "score": min(economic_benefit / 100000 * 10, 30)})
        benefit_score += min(economic_benefit / 100000 * 10, 30)

        equity_score = option.scores.get("equity", 50)
        benefit_items.append({"type": "health_equity", "value": equity_score, "score": equity_score * 0.3})
        benefit_score += equity_score * 0.3

        # Quantify risks
        risk_items = []
        risk_score = 0.0

        cost_risk = min(option.cost / 1000000 * 20, 30)
        risk_items.append({"type": "financial_risk", "value": option.cost, "score": cost_risk})
        risk_score += cost_risk

        impl_risk = min(option.implementation_time_days / 30 * 10, 20)
        risk_items.append({"type": "implementation_delay_risk", "value": option.implementation_time_days, "score": impl_risk})
        risk_score += impl_risk

        safety = option.scores.get("safety", 80)
        adverse_risk = (100 - safety) * 0.5
        risk_items.append({"type": "adverse_events_risk", "value": 100 - safety, "score": adverse_risk})
        risk_score += adverse_risk

        net = benefit_score - risk_score
        if net > 40:
            recommendation = "STRONGLY RECOMMENDED"
        elif net > 20:
            recommendation = "RECOMMENDED"
        elif net > 0:
            recommendation = "CONDITIONALLY RECOMMENDED"
        else:
            recommendation = "NOT RECOMMENDED"

        return RiskBenefitAnalysis(
            option_id=option.option_id,
            option_name=option.name,
            benefits=benefit_items,
            risks=risk_items,
            benefit_score=round(benefit_score, 1),
            risk_score=round(risk_score, 1),
            net_value=round(net, 1),
            recommendation=recommendation
        )

    def compare_options(self, options: list, population_size: int = 100000) -> dict:
        analyses = [self.analyze_option(opt, population_size) for opt in options]
        analyses.sort(key=lambda x: x.net_value, reverse=True)

        return {
            "timestamp": datetime.now().isoformat(),
            "population_size": population_size,
            "options_compared": len(analyses),
            "analyses": [
                {
                    "rank": i + 1,
                    "option_name": a.option_name,
                    "benefit_score": a.benefit_score,
                    "risk_score": a.risk_score,
                    "net_value": a.net_value,
                    "recommendation": a.recommendation
                }
                for i, a in enumerate(analyses)
            ],
            "top_option": analyses[0].option_name if analyses else None
        }


# ============================================================
# POLICY SIMULATION ENGINE
# ============================================================

class PolicySimulationEngine:
    """
    Simulates policy scenarios and their public health outcomes
    """

    def simulate_scenario(self, scenario: PolicyScenario, baseline_cases: int) -> dict:
        """Run a policy scenario simulation"""

        intervention_effect = scenario.parameters.get("intervention_coverage", 0.5)
        transmission_reduction = scenario.parameters.get("transmission_reduction", 0.3)
        compliance_rate = scenario.parameters.get("compliance_rate", 0.75)
        resource_level = scenario.parameters.get("resource_level", 1.0)

        # SIR-inspired simplified model
        effective_reduction = intervention_effect * transmission_reduction * compliance_rate * resource_level

        # Project outcomes
        days = scenario.time_horizon_days
        daily_cases_baseline = baseline_cases / max(days, 1)
        daily_cases_intervention = daily_cases_baseline * (1 - effective_reduction)

        cases_with = int(daily_cases_intervention * days)
        cases_without = baseline_cases
        cases_averted = max(cases_without - cases_with, 0)

        cost_per_case = scenario.parameters.get("cost_per_case_usd", 8500)
        total_cost = scenario.parameters.get("total_intervention_cost", 500000)
        net_economic_benefit = (cases_averted * cost_per_case) - total_cost
        cost_effectiveness = total_cost / max(cases_averted, 1)

        return {
            "scenario_id": scenario.scenario_id,
            "scenario_name": scenario.name,
            "time_horizon_days": days,
            "probability": scenario.probability,
            "outcomes": {
                "cases_without_intervention": cases_without,
                "cases_with_intervention": cases_with,
                "cases_averted": cases_averted,
                "effectiveness_rate": round(effective_reduction * 100, 1),
                "net_economic_benefit_usd": round(net_economic_benefit),
                "cost_per_case_averted_usd": round(cost_effectiveness, 0),
                "cost_effective": cost_effectiveness < cost_per_case
            },
            "projected_impact": "HIGH" if cases_averted > baseline_cases * 0.5 else "MODERATE" if cases_averted > baseline_cases * 0.25 else "LOW"
        }

    def compare_scenarios(self, scenarios: list, baseline_cases: int) -> dict:
        results = [self.simulate_scenario(s, baseline_cases) for s in scenarios]
        results.sort(key=lambda x: x["outcomes"]["cases_averted"], reverse=True)

        return {
            "timestamp": datetime.now().isoformat(),
            "baseline_cases": baseline_cases,
            "scenarios_compared": len(results),
            "scenario_results": results,
            "optimal_scenario": results[0]["scenario_name"] if results else None,
            "total_avoidable_cases": results[0]["outcomes"]["cases_averted"] if results else 0
        }


# ============================================================
# INTEGRATED DECISION SUPPORT SYSTEM
# ============================================================

class OneHealthDecisionSupportSystem:
    """
    Main integrated decision support system for One Health zoonotic disease management
    Combines MCDA, evidence-based recommendations, risk-benefit analysis, and policy simulation
    """

    def __init__(self):
        self.mcda = MultiCriteriaDecisionAnalyzer()
        self.recommendation_engine = EvidenceBasedRecommendationEngine()
        self.risk_benefit_analyzer = RiskBenefitAnalyzer()
        self.policy_simulator = PolicySimulationEngine()
        self.decision_log = []

    def full_decision_analysis(self, situation: dict, options: list, evidence: list, scenarios: list = None) -> dict:
        """Comprehensive decision analysis combining all methods"""

        print(f"\n{'='*60}")
        print("ONE HEALTH DECISION SUPPORT SYSTEM")
        print(f"{'='*60}")
        print(f"Situation: {situation.get('disease', 'Unknown')} outbreak")
        print(f"Risk Level: {situation.get('risk_level', 'Unknown')}")
        print(f"Options: {len(options)} | Evidence Items: {len(evidence)}")
        print(f"{'='*60}\n")

        # 1. Multi-Criteria Analysis
        print("📊 Running Multi-Criteria Decision Analysis...")
        mcda_result = self.mcda.analyze(options)
        sensitivity = self.mcda.sensitivity_analysis(options)

        # 2. Evidence-based Recommendation
        print("🔬 Generating Evidence-Based Recommendation...")
        recommendation = self.recommendation_engine.generate_recommendation(situation, evidence, options)

        # 3. Risk-Benefit Analysis
        print("⚖️  Conducting Risk-Benefit Analysis...")
        rb_comparison = self.risk_benefit_analyzer.compare_options(options, situation.get("population", 100000))

        # 4. Policy Simulation (if scenarios provided)
        simulation_results = None
        if scenarios:
            print("🔮 Running Policy Scenario Simulations...")
            simulation_results = self.policy_simulator.compare_scenarios(scenarios, situation.get("baseline_cases", 500))

        # Consolidate final recommendation
        final = self._consolidate_recommendation(mcda_result, recommendation, rb_comparison, simulation_results)

        result = {
            "analysis_id": f"DSS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "situation_summary": situation,
            "mcda_analysis": {
                "best_option": mcda_result["best_option"]["option_name"] if mcda_result["best_option"] else None,
                "top_score": mcda_result["best_option"]["total_score"] if mcda_result["best_option"] else 0,
                "sensitivity_stable": sensitivity["robust_recommendation"],
                "ranked_options": [{"rank": r["rank"], "name": r["option_name"], "score": r["total_score"]} for r in mcda_result["ranked_options"]]
            },
            "evidence_recommendation": {
                "recommended_option": recommendation.recommended_option,
                "confidence_score": recommendation.confidence_score,
                "urgency": recommendation.urgency.value,
                "rationale": recommendation.rationale,
                "implementation_steps": recommendation.implementation_steps[:4]
            },
            "risk_benefit_analysis": rb_comparison,
            "policy_simulation": simulation_results,
            "final_recommendation": final,
            "monitoring_plan": recommendation.monitoring_metrics
        }

        # Log decision
        self.decision_log.append({
            "timestamp": result["timestamp"],
            "disease": situation.get("disease"),
            "recommended_option": final["recommended_action"],
            "confidence": final["confidence"]
        })

        return result

    def _consolidate_recommendation(self, mcda, recommendation, rb_comparison, simulation) -> dict:
        """Consolidate results from all analyses into single recommendation"""

        votes = {}
        # MCDA vote
        if mcda["best_option"]:
            votes[mcda["best_option"]["option_name"]] = votes.get(mcda["best_option"]["option_name"], 0) + 1
        # Evidence vote
        if recommendation.recommended_option:
            votes[recommendation.recommended_option] = votes.get(recommendation.recommended_option, 0) + 1
        # Risk-benefit vote
        if rb_comparison.get("top_option"):
            votes[rb_comparison["top_option"]] = votes.get(rb_comparison["top_option"], 0) + 1

        best = max(votes, key=votes.get) if votes else "Insufficient data"
        max_votes = votes.get(best, 0)
        confidence = "HIGH" if max_votes >= 3 else "MODERATE" if max_votes == 2 else "LOW"

        return {
            "recommended_action": best,
            "confidence": confidence,
            "consensus_votes": votes,
            "urgency": recommendation.urgency.value,
            "key_rationale": recommendation.rationale,
            "expected_impact": f"Up to {simulation['total_avoidable_cases']} cases averted" if simulation else "See risk-benefit analysis",
            "immediate_actions": recommendation.implementation_steps[:3],
            "review_required_by": (datetime.now() + timedelta(days=3)).isoformat()
        }

    def get_decision_summary(self) -> dict:
        return {
            "total_decisions": len(self.decision_log),
            "recent_decisions": self.decision_log[-5:],
            "system_status": "operational"
        }


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 37: DECISION SUPPORT SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    # Define H5N1 response options
    options = [
        DecisionOption(
            "opt_001", "Mass Vaccination Campaign",
            "Large-scale poultry and human vaccination program",
            scores={"effectiveness": 85, "cost_efficiency": 40, "feasibility": 70,
                    "speed": 30, "safety": 90, "equity": 75},
            cost=2500000, feasibility=0.70, implementation_time_days=45,
            risks=["Vaccine hesitancy", "Supply chain constraints", "Cold chain requirements"],
            benefits=["High herd immunity", "Long-term protection", "Reduces transmission reservoir"]
        ),
        DecisionOption(
            "opt_002", "Targeted Culling + Surveillance",
            "Selective culling of infected flocks with enhanced monitoring",
            scores={"effectiveness": 75, "cost_efficiency": 65, "feasibility": 85,
                    "speed": 75, "safety": 70, "equity": 50},
            cost=800000, feasibility=0.85, implementation_time_days=14,
            risks=["Economic impact on farmers", "Incomplete coverage", "Resistance from communities"],
            benefits=["Rapid source elimination", "Proven approach", "Reduces spillover risk"]
        ),
        DecisionOption(
            "opt_003", "Enhanced Surveillance + PPE Distribution",
            "Intensive monitoring with protective equipment for high-risk groups",
            scores={"effectiveness": 55, "cost_efficiency": 80, "feasibility": 95,
                    "speed": 90, "safety": 95, "equity": 85},
            cost=150000, feasibility=0.95, implementation_time_days=7,
            risks=["Insufficient alone for high-risk outbreaks", "Compliance variability"],
            benefits=["Immediate implementation", "Low cost", "No culling required", "High safety"]
        ),
        DecisionOption(
            "opt_004", "Integrated One Health Response",
            "Coordinated human-animal-environment multi-sector response",
            scores={"effectiveness": 90, "cost_efficiency": 55, "feasibility": 65,
                    "speed": 45, "safety": 88, "equity": 90},
            cost=1800000, feasibility=0.65, implementation_time_days=30,
            risks=["Complex coordination", "Multiple stakeholders", "Longer setup time"],
            benefits=["Comprehensive coverage", "Best long-term outcomes", "Addresses root causes"]
        )
    ]

    # Evidence items
    evidence = [
        EvidenceItem("ev_001", "WHO Guidelines 2024", "systematic_review", EvidenceLevel.STRONG,
                     "Vaccination + surveillance is most effective for H5N1 control", 0.95, "2024-01-15", True),
        EvidenceItem("ev_002", "CDC Field Study 2023", "cohort_study", EvidenceLevel.MODERATE,
                     "Targeted culling reduces transmission by 60-75% within 2 weeks", 0.85, "2023-09-20", True),
        EvidenceItem("ev_003", "FAO Technical Report", "expert_opinion", EvidenceLevel.MODERATE,
                     "One Health integrated approach yields best sustainable outcomes", 0.80, "2024-03-01", True),
        EvidenceItem("ev_004", "Local Epidemiology Data", "observational", EvidenceLevel.WEAK,
                     "PPE alone insufficient during active outbreaks", 0.70, "2024-04-10", False),
    ]

    # Situation context
    situation = {
        "disease": "H5N1 Avian Influenza",
        "risk_level": RiskLevel.HIGH,
        "decision_type": "PUBLIC_HEALTH",
        "active_outbreak": True,
        "case_count": 47,
        "animal_cases": 2300,
        "population": 250000,
        "baseline_cases": 500,
        "setting": "Rural agricultural community with high poultry density"
    }

    # Policy scenarios
    scenarios = [
        PolicyScenario("sc_001", "Aggressive Intervention", "Maximum resources deployed",
                       {"intervention_coverage": 0.85, "transmission_reduction": 0.70,
                        "compliance_rate": 0.80, "resource_level": 1.2,
                        "cost_per_case_usd": 8500, "total_intervention_cost": 2500000},
                       {}, 0.60, 90),
        PolicyScenario("sc_002", "Moderate Response", "Standard response protocol",
                       {"intervention_coverage": 0.65, "transmission_reduction": 0.50,
                        "compliance_rate": 0.75, "resource_level": 1.0,
                        "cost_per_case_usd": 8500, "total_intervention_cost": 800000},
                       {}, 0.30, 90),
        PolicyScenario("sc_003", "Minimal Intervention", "Surveillance and PPE only",
                       {"intervention_coverage": 0.40, "transmission_reduction": 0.25,
                        "compliance_rate": 0.85, "resource_level": 0.5,
                        "cost_per_case_usd": 8500, "total_intervention_cost": 150000},
                       {}, 0.10, 90)
    ]

    # Run full analysis
    dss = OneHealthDecisionSupportSystem()
    result = dss.full_decision_analysis(situation, options, evidence, scenarios)

    # Print results
    print("\n📊 MCDA RESULTS:")
    for r in result["mcda_analysis"]["ranked_options"]:
        bar = "█" * int(r["score"] / 5)
        print(f"  #{r['rank']} {r['name']:<40} Score: {r['score']:5.1f} {bar}")
    print(f"  Ranking Stability: {'✅ ROBUST' if result['mcda_analysis']['sensitivity_stable'] else '⚠️ SENSITIVE'}")

    print("\n🔬 EVIDENCE-BASED RECOMMENDATION:")
    ev_rec = result["evidence_recommendation"]
    print(f"  Recommended: {ev_rec['recommended_option']}")
    print(f"  Confidence: {ev_rec['confidence_score']}%")
    print(f"  Urgency: {ev_rec['urgency'].upper()}")
    print(f"  Rationale: {ev_rec['rationale']}")

    print("\n⚖️  RISK-BENEFIT ANALYSIS:")
    for opt in result["risk_benefit_analysis"]["analyses"]:
        print(f"  #{opt['rank']} {opt['option_name']:<40} Net: {opt['net_value']:+5.1f}  [{opt['recommendation']}]")

    print("\n🔮 POLICY SIMULATION:")
    if result["policy_simulation"]:
        for sc in result["policy_simulation"]["scenario_results"]:
            out = sc["outcomes"]
            print(f"  {sc['scenario_name']:<30} Cases Averted: {out['cases_averted']:,}  Effective: {out['effectiveness_rate']}%  Cost-Effective: {'✅' if out['cost_effective'] else '❌'}")

    print("\n🎯 FINAL RECOMMENDATION:")
    final = result["final_recommendation"]
    print(f"  ✅ Recommended Action: {final['recommended_action']}")
    print(f"  Confidence: {final['confidence']} (votes: {final['consensus_votes']})")
    print(f"  Urgency: {final['urgency'].upper()}")
    print(f"  Expected Impact: {final['expected_impact']}")
    print(f"\n  Immediate Steps:")
    for step in final["immediate_actions"]:
        print(f"    {step}")
    print(f"\n  Review Required By: {final['review_required_by'][:10]}")

    print("\n📋 MONITORING PLAN:")
    for metric in result["monitoring_plan"][:4]:
        print(f"  • {metric}")

    print(f"\n{'='*70}")
    print("✅ Module 37: decision_support.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
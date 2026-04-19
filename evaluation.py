"""
Response Evaluation System
==========================
Module 4: Response & Control Systems

Advanced response evaluation and lessons learned system for One Health responses,
providing comprehensive assessment, performance analysis, and improvement recommendations.

NIW Focus: Evaluation intelligence enabling continuous improvement and preparedness enhancement.
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

class EvaluationPhase(Enum):
    """Evaluation phase types."""
    REAL_TIME = "real_time"                   # During response
    POST_ACTION = "post_action"               # Immediate post-response
    COMPREHENSIVE = "comprehensive"           # Detailed retrospective
    LONGITUDINAL = "longitudinal"             # Long-term follow-up
    COMPARATIVE = "comparative"               # Cross-outbreak comparison

class EvaluationDomain(Enum):
    """Evaluation domains."""
    PREPAREDNESS = "preparedness"             # Pre-outbreak readiness
    DETECTION = "detection"                   # Early detection capability
    RESPONSE_COORDINATION = "response_coordination"  # Coordination effectiveness
    INTERVENTION = "intervention"             # Intervention effectiveness
    CONTAINMENT = "containment"               # Containment success
    COMMUNICATION = "communication"           # Risk communication
    RESOURCE_MANAGEMENT = "resource_management"  # Resource allocation
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement"  # Stakeholder coordination
    RECOVERY = "recovery"                     # Post-outbreak recovery

class PerformanceLevel(Enum):
    """Performance assessment levels."""
    EXCELLENT = "excellent"                   # >90% performance
    GOOD = "good"                            # 70-90% performance
    SATISFACTORY = "satisfactory"            # 50-70% performance
    NEEDS_IMPROVEMENT = "needs_improvement"   # 30-50% performance
    POOR = "poor"                           # <30% performance

class EvidenceType(Enum):
    """Types of evaluation evidence."""
    QUANTITATIVE = "quantitative"            # Numerical data/metrics
    QUALITATIVE = "qualitative"              # Interviews, observations
    DOCUMENTARY = "documentary"               # Document analysis
    COMPARATIVE = "comparative"               # Comparison with standards
    STAKEHOLDER_FEEDBACK = "stakeholder_feedback"  # Stakeholder input

@dataclass
class EvaluationMetric:
    """Individual evaluation metric."""
    
    metric_id: str
    metric_name: str
    evaluation_domain: EvaluationDomain
    metric_description: str
    
    # Metric measurement
    measurement_method: str
    data_source: str
    target_value: Optional[float] = None
    actual_value: Optional[float] = None
    performance_percentage: Optional[float] = None
    
    # Assessment
    performance_level: PerformanceLevel = PerformanceLevel.SATISFACTORY
    evidence_type: EvidenceType = EvidenceType.QUANTITATIVE
    confidence_level: str = "medium"  # "low", "medium", "high"
    
    # Context and analysis
    contributing_factors: List[str] = field(default_factory=list)
    barriers_encountered: List[str] = field(default_factory=list)
    success_factors: List[str] = field(default_factory=list)
    
    # Recommendations
    improvement_recommendations: List[str] = field(default_factory=list)
    priority_level: str = "medium"  # "low", "medium", "high", "critical"

@dataclass
class LessonLearned:
    """Lesson learned from response."""
    
    lesson_id: str
    lesson_title: str
    evaluation_domain: EvaluationDomain
    lesson_description: str
    
    # Context
    situation_context: str
    what_happened: str
    what_worked_well: str
    what_could_improve: str
    
    # Analysis
    root_cause_analysis: List[str] = field(default_factory=list)
    impact_assessment: str = ""
    stakeholders_affected: List[str] = field(default_factory=list)
    
    # Recommendations
    specific_recommendations: List[str] = field(default_factory=list)
    implementation_priority: str = "medium"
    resource_requirements: List[str] = field(default_factory=list)
    responsible_parties: List[str] = field(default_factory=list)
    
    # Follow-up
    implementation_timeline: str = ""
    success_indicators: List[str] = field(default_factory=list)
    monitoring_approach: str = ""

@dataclass
class EvaluationFindings:
    """Comprehensive evaluation findings."""
    
    findings_id: str
    evaluation_phase: EvaluationPhase
    outbreak_id: str
    evaluation_date: datetime
    
    # Overall assessment
    overall_response_effectiveness: float = 0.0  # 0-1 scale
    overall_performance_level: PerformanceLevel = PerformanceLevel.SATISFACTORY
    
    # Domain-specific findings
    domain_assessments: Dict[EvaluationDomain, float] = field(default_factory=dict)
    evaluation_metrics: List[EvaluationMetric] = field(default_factory=list)
    lessons_learned: List[LessonLearned] = field(default_factory=list)
    
    # Key insights
    major_strengths: List[str] = field(default_factory=list)
    critical_gaps: List[str] = field(default_factory=list)
    unexpected_challenges: List[str] = field(default_factory=list)
    innovation_highlights: List[str] = field(default_factory=list)
    
    # Impact assessment
    human_health_impact: Dict[str, Any] = field(default_factory=dict)
    animal_health_impact: Dict[str, Any] = field(default_factory=dict)
    economic_impact: Dict[str, Any] = field(default_factory=dict)
    social_impact: Dict[str, Any] = field(default_factory=dict)
    
    # Recommendations
    immediate_actions: List[str] = field(default_factory=list)
    short_term_improvements: List[str] = field(default_factory=list)
    long_term_strategic_changes: List[str] = field(default_factory=list)
    
    # Quality assurance
    evaluation_methods_used: List[str] = field(default_factory=list)
    data_quality_assessment: str = "good"  # "poor", "fair", "good", "excellent"
    limitations: List[str] = field(default_factory=list)
    evaluators: List[str] = field(default_factory=list)

@dataclass
class ComparisonAnalysis:
    """Comparative analysis across outbreaks or standards."""
    
    analysis_id: str
    comparison_type: str  # "historical", "peer", "standard", "simulation"
    reference_cases: List[str] = field(default_factory=list)
    
    # Comparison results
    performance_comparisons: Dict[str, Dict[str, float]] = field(default_factory=dict)
    best_practices_identified: List[str] = field(default_factory=list)
    common_challenges: List[str] = field(default_factory=list)
    unique_innovations: List[str] = field(default_factory=list)
    
    # Insights
    relative_performance_summary: str = ""
    key_differentiators: List[str] = field(default_factory=list)
    transferable_lessons: List[str] = field(default_factory=list)

class ResponseEvaluationManager:
    """Central response evaluation management system."""
    
    def __init__(self):
        self.evaluation_findings: Dict[str, EvaluationFindings] = {}
        self.comparison_analyses: Dict[str, ComparisonAnalysis] = {}
        self.metric_library: Dict[str, EvaluationMetric] = {}
        self.evaluation_templates: Dict[EvaluationPhase, List[str]] = {}
        
        # Initialize evaluation framework
        self._initialize_evaluation_framework()
        
        logger.info("One Health Response Evaluation Manager initialized")
    
    def _initialize_evaluation_framework(self):
        """Initialize evaluation framework with standard metrics."""
        
        # Standard evaluation metrics
        standard_metrics = [
            # Detection metrics
            {
                "id": "detection_time", "name": "Time to Detection", "domain": EvaluationDomain.DETECTION,
                "description": "Time from first case to outbreak detection",
                "method": "Timeline analysis", "source": "Surveillance records"
            },
            {
                "id": "detection_sensitivity", "name": "Detection Sensitivity", "domain": EvaluationDomain.DETECTION,
                "description": "Proportion of cases detected by surveillance",
                "method": "Case investigation review", "source": "Epidemiological data"
            },
            
            # Response coordination metrics
            {
                "id": "coordination_speed", "name": "Response Activation Speed", "domain": EvaluationDomain.RESPONSE_COORDINATION,
                "description": "Time from detection to response activation",
                "method": "Timeline analysis", "source": "Response records"
            },
            {
                "id": "stakeholder_engagement", "name": "Stakeholder Engagement Effectiveness", 
                "domain": EvaluationDomain.STAKEHOLDER_ENGAGEMENT,
                "description": "Quality and timeliness of stakeholder coordination",
                "method": "Survey and interview", "source": "Stakeholder feedback"
            },
            
            # Intervention metrics
            {
                "id": "intervention_coverage", "name": "Intervention Coverage Rate", "domain": EvaluationDomain.INTERVENTION,
                "description": "Proportion of target population reached by interventions",
                "method": "Coverage survey", "source": "Intervention records"
            },
            {
                "id": "intervention_timeliness", "name": "Intervention Timeliness", "domain": EvaluationDomain.INTERVENTION,
                "description": "Time from decision to intervention implementation",
                "method": "Timeline analysis", "source": "Implementation records"
            },
            
            # Containment metrics
            {
                "id": "containment_effectiveness", "name": "Containment Effectiveness", "domain": EvaluationDomain.CONTAINMENT,
                "description": "Success in limiting outbreak spread",
                "method": "Transmission analysis", "source": "Epidemiological data"
            },
            {
                "id": "secondary_attack_rate", "name": "Secondary Attack Rate", "domain": EvaluationDomain.CONTAINMENT,
                "description": "Rate of secondary transmission after containment",
                "method": "Contact tracing analysis", "source": "Contact investigation"
            },
            
            # Communication metrics
            {
                "id": "communication_reach", "name": "Communication Reach", "domain": EvaluationDomain.COMMUNICATION,
                "description": "Proportion of target population reached by messages",
                "method": "Reach analysis", "source": "Communication metrics"
            },
            {
                "id": "message_comprehension", "name": "Message Comprehension Rate", "domain": EvaluationDomain.COMMUNICATION,
                "description": "Proportion understanding key health messages",
                "method": "Survey", "source": "Public surveys"
            },
            
            # Resource management metrics
            {
                "id": "resource_adequacy", "name": "Resource Adequacy", "domain": EvaluationDomain.RESOURCE_MANAGEMENT,
                "description": "Sufficiency of resources for response needs",
                "method": "Gap analysis", "source": "Resource tracking"
            },
            {
                "id": "resource_efficiency", "name": "Resource Use Efficiency", "domain": EvaluationDomain.RESOURCE_MANAGEMENT,
                "description": "Effective utilization of available resources",
                "method": "Efficiency analysis", "source": "Resource allocation data"
            }
        ]
        
        for metric_data in standard_metrics:
            metric = EvaluationMetric(
                metric_id=metric_data["id"],
                metric_name=metric_data["name"],
                evaluation_domain=metric_data["domain"],
                metric_description=metric_data["description"],
                measurement_method=metric_data["method"],
                data_source=metric_data["source"]
            )
            self.metric_library[metric.metric_id] = metric
        
        # Evaluation templates by phase
        self.evaluation_templates = {
            EvaluationPhase.REAL_TIME: [
                "response_speed", "resource_deployment", "coordination_effectiveness"
            ],
            EvaluationPhase.POST_ACTION: [
                "intervention_coverage", "containment_effectiveness", "communication_reach"
            ],
            EvaluationPhase.COMPREHENSIVE: [
                "overall_effectiveness", "lessons_learned", "improvement_recommendations"
            ]
        }
    
    def conduct_evaluation(self, outbreak_id: str, evaluation_phase: EvaluationPhase,
                          response_data: Dict[str, Any]) -> EvaluationFindings:
        """Conduct comprehensive response evaluation."""
        
        findings_id = f"EVAL_{random.randint(100000, 999999)}"
        
        findings = EvaluationFindings(
            findings_id=findings_id,
            evaluation_phase=evaluation_phase,
            outbreak_id=outbreak_id,
            evaluation_date=datetime.now()
        )
        
        # Evaluate each domain
        domain_scores = {}
        for domain in EvaluationDomain:
            domain_metrics = [m for m in self.metric_library.values() if m.evaluation_domain == domain]
            if domain_metrics:
                domain_score = self._evaluate_domain(domain, domain_metrics, response_data)
                domain_scores[domain] = domain_score
        
        findings.domain_assessments = domain_scores
        
        # Calculate overall effectiveness
        if domain_scores:
            findings.overall_response_effectiveness = statistics.mean(domain_scores.values())
            
            # Determine overall performance level
            if findings.overall_response_effectiveness >= 0.9:
                findings.overall_performance_level = PerformanceLevel.EXCELLENT
            elif findings.overall_response_effectiveness >= 0.7:
                findings.overall_performance_level = PerformanceLevel.GOOD
            elif findings.overall_response_effectiveness >= 0.5:
                findings.overall_performance_level = PerformanceLevel.SATISFACTORY
            elif findings.overall_response_effectiveness >= 0.3:
                findings.overall_performance_level = PerformanceLevel.NEEDS_IMPROVEMENT
            else:
                findings.overall_performance_level = PerformanceLevel.POOR
        
        # Generate evaluation metrics with simulated data
        findings.evaluation_metrics = self._generate_evaluation_metrics(response_data)
        
        # Generate lessons learned
        findings.lessons_learned = self._generate_lessons_learned(findings, response_data)
        
        # Identify key insights
        findings.major_strengths = self._identify_major_strengths(findings)
        findings.critical_gaps = self._identify_critical_gaps(findings)
        findings.unexpected_challenges = self._identify_unexpected_challenges(response_data)
        findings.innovation_highlights = self._identify_innovations(response_data)
        
        # Assess impact
        findings.human_health_impact = self._assess_human_health_impact(response_data)
        findings.animal_health_impact = self._assess_animal_health_impact(response_data)
        findings.economic_impact = self._assess_economic_impact(response_data)
        findings.social_impact = self._assess_social_impact(response_data)
        
        # Generate recommendations
        findings.immediate_actions = self._generate_immediate_actions(findings)
        findings.short_term_improvements = self._generate_short_term_improvements(findings)
        findings.long_term_strategic_changes = self._generate_strategic_changes(findings)
        
        # Set evaluation metadata
        findings.evaluation_methods_used = ["document_review", "stakeholder_interviews", "data_analysis", "timeline_analysis"]
        findings.data_quality_assessment = "good"
        findings.evaluators = ["Lead Evaluator", "Domain Experts", "External Reviewer"]
        
        self.evaluation_findings[findings_id] = findings
        
        logger.info(f"Evaluation completed: {findings_id}")
        
        return findings
    
    def _evaluate_domain(self, domain: EvaluationDomain, domain_metrics: List[EvaluationMetric],
                        response_data: Dict[str, Any]) -> float:
        """Evaluate specific domain performance."""
        
        # Simulate domain evaluation with realistic performance ranges
        domain_performance = {
            EvaluationDomain.PREPAREDNESS: random.uniform(0.6, 0.9),
            EvaluationDomain.DETECTION: random.uniform(0.7, 0.95),
            EvaluationDomain.RESPONSE_COORDINATION: random.uniform(0.65, 0.85),
            EvaluationDomain.INTERVENTION: random.uniform(0.7, 0.9),
            EvaluationDomain.CONTAINMENT: random.uniform(0.6, 0.85),
            EvaluationDomain.COMMUNICATION: random.uniform(0.75, 0.9),
            EvaluationDomain.RESOURCE_MANAGEMENT: random.uniform(0.6, 0.8),
            EvaluationDomain.STAKEHOLDER_ENGAGEMENT: random.uniform(0.7, 0.85),
            EvaluationDomain.RECOVERY: random.uniform(0.5, 0.8)
        }
        
        return domain_performance.get(domain, 0.7)
    
    def _generate_evaluation_metrics(self, response_data: Dict[str, Any]) -> List[EvaluationMetric]:
        """Generate evaluation metrics with simulated measurements."""
        
        metrics = []
        
        for metric_id, metric_template in self.metric_library.items():
            metric = EvaluationMetric(
                metric_id=metric_id,
                metric_name=metric_template.metric_name,
                evaluation_domain=metric_template.evaluation_domain,
                metric_description=metric_template.metric_description,
                measurement_method=metric_template.measurement_method,
                data_source=metric_template.data_source
            )
            
            # Simulate metric measurements
            if "time" in metric_id.lower():
                metric.target_value = 24.0  # 24 hours target
                metric.actual_value = random.uniform(6, 48)  # 6-48 hours actual
                metric.performance_percentage = max(0, min(100, (metric.target_value / metric.actual_value) * 100))
            elif "rate" in metric_id.lower() or "coverage" in metric_id.lower():
                metric.target_value = 0.8  # 80% target
                metric.actual_value = random.uniform(0.5, 0.95)  # 50-95% actual
                metric.performance_percentage = (metric.actual_value / metric.target_value) * 100
            elif "effectiveness" in metric_id.lower():
                metric.target_value = 0.85  # 85% target
                metric.actual_value = random.uniform(0.6, 0.9)  # 60-90% actual
                metric.performance_percentage = (metric.actual_value / metric.target_value) * 100
            else:
                metric.actual_value = random.uniform(0.6, 0.9)
                metric.performance_percentage = metric.actual_value * 100
            
            # Determine performance level
            if metric.performance_percentage >= 90:
                metric.performance_level = PerformanceLevel.EXCELLENT
            elif metric.performance_percentage >= 70:
                metric.performance_level = PerformanceLevel.GOOD
            elif metric.performance_percentage >= 50:
                metric.performance_level = PerformanceLevel.SATISFACTORY
            elif metric.performance_percentage >= 30:
                metric.performance_level = PerformanceLevel.NEEDS_IMPROVEMENT
            else:
                metric.performance_level = PerformanceLevel.POOR
            
            # Add contextual factors
            metric.success_factors = self._generate_success_factors(metric)
            metric.barriers_encountered = self._generate_barriers(metric)
            metric.improvement_recommendations = self._generate_metric_recommendations(metric)
            
            metrics.append(metric)
        
        return metrics
    
    def _generate_success_factors(self, metric: EvaluationMetric) -> List[str]:
        """Generate success factors for metric."""
        
        success_factor_templates = {
            EvaluationDomain.DETECTION: [
                "Well-trained surveillance staff",
                "Integrated surveillance systems",
                "Strong laboratory capacity"
            ],
            EvaluationDomain.RESPONSE_COORDINATION: [
                "Clear command structure",
                "Regular coordination meetings",
                "Established communication protocols"
            ],
            EvaluationDomain.INTERVENTION: [
                "Pre-positioned resources",
                "Trained response teams",
                "Community cooperation"
            ],
            EvaluationDomain.COMMUNICATION: [
                "Trusted messengers",
                "Multi-channel approach",
                "Clear, consistent messaging"
            ]
        }
        
        factors = success_factor_templates.get(metric.evaluation_domain, ["Effective planning", "Good coordination"])
        return random.sample(factors, min(len(factors), 2))
    
    def _generate_barriers(self, metric: EvaluationMetric) -> List[str]:
        """Generate barriers encountered for metric."""
        
        barrier_templates = {
            EvaluationDomain.DETECTION: [
                "Limited laboratory capacity",
                "Delayed reporting from field",
                "Insufficient surveillance coverage"
            ],
            EvaluationDomain.RESPONSE_COORDINATION: [
                "Communication delays",
                "Unclear authority boundaries",
                "Resource competition"
            ],
            EvaluationDomain.INTERVENTION: [
                "Resource shortages",
                "Access restrictions",
                "Community resistance"
            ],
            EvaluationDomain.COMMUNICATION: [
                "Misinformation spread",
                "Language barriers",
                "Limited media cooperation"
            ]
        }
        
        barriers = barrier_templates.get(metric.evaluation_domain, ["Resource constraints", "Coordination challenges"])
        return random.sample(barriers, min(len(barriers), 2))
    
    def _generate_metric_recommendations(self, metric: EvaluationMetric) -> List[str]:
        """Generate improvement recommendations for metric."""
        
        recommendations = []
        
        if metric.performance_level in [PerformanceLevel.POOR, PerformanceLevel.NEEDS_IMPROVEMENT]:
            recommendations.extend([
                f"Enhance {metric.metric_name.lower()} through targeted improvements",
                f"Develop specific protocols for {metric.evaluation_domain.value.replace('_', ' ')}"
            ])
        
        if "time" in metric.metric_id:
            recommendations.append("Streamline decision-making processes to reduce delays")
        
        if "coverage" in metric.metric_id:
            recommendations.append("Expand outreach capacity and improve targeting strategies")
        
        return recommendations[:2]  # Limit to 2 recommendations
    
    def _generate_lessons_learned(self, findings: EvaluationFindings, 
                                response_data: Dict[str, Any]) -> List[LessonLearned]:
        """Generate lessons learned from evaluation."""
        
        lessons = []
        
        # Generate lessons based on performance gaps
        low_performing_domains = [
            domain for domain, score in findings.domain_assessments.items()
            if score < 0.6
        ]
        
        for domain in low_performing_domains:
            lesson_id = f"LESSON_{random.randint(1000, 9999)}"
            
            lesson = LessonLearned(
                lesson_id=lesson_id,
                lesson_title=f"Improving {domain.value.replace('_', ' ').title()} Effectiveness",
                evaluation_domain=domain,
                lesson_description=f"Challenges and opportunities identified in {domain.value.replace('_', ' ')} during response",
                situation_context=f"During the outbreak response, {domain.value.replace('_', ' ')} faced significant challenges",
                what_happened=f"Performance in {domain.value.replace('_', ' ')} was below optimal levels",
                what_worked_well=f"Some aspects of {domain.value.replace('_', ' ')} showed good results",
                what_could_improve=f"Several areas for improvement were identified in {domain.value.replace('_', ' ')}"
            )
            
            # Generate specific recommendations
            lesson.specific_recommendations = self._generate_lesson_recommendations(domain)
            lesson.implementation_priority = "high" if findings.domain_assessments[domain] < 0.4 else "medium"
            lesson.responsible_parties = self._identify_responsible_parties(domain)
            
            lessons.append(lesson)
        
        # Generate positive lessons from high-performing areas
        high_performing_domains = [
            domain for domain, score in findings.domain_assessments.items()
            if score > 0.8
        ]
        
        for domain in high_performing_domains[:2]:  # Limit to 2 positive lessons
            lesson_id = f"LESSON_{random.randint(1000, 9999)}"
            
            lesson = LessonLearned(
                lesson_id=lesson_id,
                lesson_title=f"Best Practices in {domain.value.replace('_', ' ').title()}",
                evaluation_domain=domain,
                lesson_description=f"Successful approaches and practices in {domain.value.replace('_', ' ')}",
                situation_context=f"{domain.value.replace('_', ' ').title()} performed exceptionally well during response",
                what_happened=f"Excellent performance achieved in {domain.value.replace('_', ' ')}",
                what_worked_well=f"Multiple factors contributed to success in {domain.value.replace('_', ' ')}",
                what_could_improve=f"Opportunities to scale and replicate success"
            )
            
            lesson.specific_recommendations = self._generate_positive_lesson_recommendations(domain)
            lesson.implementation_priority = "medium"
            lesson.responsible_parties = self._identify_responsible_parties(domain)
            
            lessons.append(lesson)
        
        return lessons
    
    def _generate_lesson_recommendations(self, domain: EvaluationDomain) -> List[str]:
        """Generate specific recommendations for domain improvement."""
        
        recommendation_templates = {
            EvaluationDomain.DETECTION: [
                "Strengthen laboratory diagnostic capacity",
                "Enhance surveillance network coverage",
                "Improve case reporting timeliness"
            ],
            EvaluationDomain.RESPONSE_COORDINATION: [
                "Establish clearer command structures",
                "Improve inter-agency communication protocols",
                "Enhance coordination training programs"
            ],
            EvaluationDomain.INTERVENTION: [
                "Pre-position critical resources",
                "Develop rapid deployment capabilities",
                "Strengthen community engagement strategies"
            ],
            EvaluationDomain.COMMUNICATION: [
                "Develop multi-language communication materials",
                "Establish trusted community messengers",
                "Improve social media monitoring capabilities"
            ]
        }
        
        recommendations = recommendation_templates.get(domain, [
            "Conduct targeted capability assessments",
            "Develop domain-specific improvement plans"
        ])
        
        return random.sample(recommendations, min(len(recommendations), 3))
    
    def _generate_positive_lesson_recommendations(self, domain: EvaluationDomain) -> List[str]:
        """Generate recommendations to scale successful practices."""
        
        return [
            f"Document and standardize successful {domain.value.replace('_', ' ')} practices",
            f"Share {domain.value.replace('_', ' ')} lessons across similar jurisdictions",
            f"Integrate {domain.value.replace('_', ' ')} best practices into training programs"
        ]
    
    def _identify_responsible_parties(self, domain: EvaluationDomain) -> List[str]:
        """Identify responsible parties for domain improvements."""
        
        responsibility_mapping = {
            EvaluationDomain.DETECTION: ["Surveillance Team", "Laboratory Services", "Epidemiology Unit"],
            EvaluationDomain.RESPONSE_COORDINATION: ["Emergency Management", "Incident Command", "Public Health Leadership"],
            EvaluationDomain.INTERVENTION: ["Response Teams", "Field Operations", "Logistics Coordination"],
            EvaluationDomain.COMMUNICATION: ["Public Information Officer", "Communication Team", "Media Relations"],
            EvaluationDomain.CONTAINMENT: ["Containment Teams", "Enforcement Units", "Border Health"],
            EvaluationDomain.RESOURCE_MANAGEMENT: ["Resource Management", "Logistics", "Finance"]
        }
        
        return responsibility_mapping.get(domain, ["Program Management", "Operations Team"])
    
    def _identify_major_strengths(self, findings: EvaluationFindings) -> List[str]:
        """Identify major strengths from evaluation."""
        
        strengths = []
        
        # High-performing domains
        high_performers = [
            domain.value.replace('_', ' ').title() 
            for domain, score in findings.domain_assessments.items()
            if score > 0.8
        ]
        
        if high_performers:
            strengths.append(f"Exceptional performance in {', '.join(high_performers[:3])}")
        
        # Overall effectiveness
        if findings.overall_response_effectiveness > 0.8:
            strengths.append("Strong overall response coordination and effectiveness")
        
        # Add domain-specific strengths
        domain_strengths = [
            "Rapid outbreak detection and confirmation",
            "Effective stakeholder engagement and coordination",
            "Successful implementation of containment measures",
            "Clear and timely risk communication",
            "Efficient resource mobilization and deployment"
        ]
        
        strengths.extend(random.sample(domain_strengths, 2))
        
        return strengths[:4]
    
    def _identify_critical_gaps(self, findings: EvaluationFindings) -> List[str]:
        """Identify critical gaps from evaluation."""
        
        gaps = []
        
        # Low-performing domains
        low_performers = [
            domain.value.replace('_', ' ').title()
            for domain, score in findings.domain_assessments.items()
            if score < 0.5
        ]
        
        if low_performers:
            gaps.append(f"Performance gaps in {', '.join(low_performers[:3])}")
        
        # Overall effectiveness concerns
        if findings.overall_response_effectiveness < 0.6:
            gaps.append("Overall response effectiveness below target levels")
        
        # Add specific gap areas
        common_gaps = [
            "Limited surge capacity for extended responses",
            "Insufficient cross-sector coordination mechanisms",
            "Gaps in community engagement and trust-building",
            "Resource allocation and logistics challenges"
        ]
        
        gaps.extend(random.sample(common_gaps, 2))
        
        return gaps[:4]
    
    def _identify_unexpected_challenges(self, response_data: Dict[str, Any]) -> List[str]:
        """Identify unexpected challenges encountered."""
        
        challenge_templates = [
            "Rapid evolution of pathogen characteristics during response",
            "Unprecedented scale of community resistance to interventions",
            "Supply chain disruptions affecting critical resources",
            "Information warfare and coordinated misinformation campaigns",
            "Cross-border coordination complexities",
            "Technology failures during critical response phases",
            "Weather-related impacts on response operations",
            "Simultaneous competing health emergencies"
        ]
        
        return random.sample(challenge_templates, 3)
    
    def _identify_innovations(self, response_data: Dict[str, Any]) -> List[str]:
        """Identify innovations and creative solutions."""
        
        innovation_templates = [
            "Novel digital contact tracing integration with traditional methods",
            "Creative community engagement through trusted local leaders",
            "Innovative resource sharing agreements across jurisdictions",
            "Real-time data visualization dashboards for decision support",
            "Mobile laboratory deployment for rapid field diagnosis",
            "AI-powered risk communication message optimization",
            "Drone-based sample collection from remote areas",
            "Virtual reality training for response personnel"
        ]
        
        return random.sample(innovation_templates, 2)
    
    def _assess_human_health_impact(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess human health impact of outbreak and response."""
        
        return {
            "total_cases": random.randint(150, 800),
            "hospitalizations": random.randint(20, 150),
            "deaths": random.randint(0, 25),
            "attack_rate": random.uniform(0.02, 0.15),
            "case_fatality_rate": random.uniform(0.01, 0.08),
            "years_life_lost": random.randint(50, 500),
            "healthcare_burden": "moderate",  # "low", "moderate", "high", "severe"
            "vulnerable_populations_impact": "disproportionate"
        }
    
    def _assess_animal_health_impact(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess animal health impact of outbreak and response."""
        
        return {
            "animals_affected": random.randint(5000, 50000),
            "farms_affected": random.randint(15, 75),
            "animals_culled": random.randint(2000, 25000),
            "species_involved": ["poultry", "cattle", "swine"],
            "geographic_spread": random.uniform(100, 1000),  # km²
            "production_losses": random.uniform(2, 20),  # million dollars
            "trade_restrictions_imposed": True,
            "industry_recovery_time_months": random.randint(6, 18)
        }
    
    def _assess_economic_impact(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess economic impact of outbreak and response."""
        
        return {
            "direct_response_costs": random.uniform(5, 25),  # million dollars
            "healthcare_costs": random.uniform(2, 15),  # million dollars
            "agricultural_losses": random.uniform(10, 50),  # million dollars
            "trade_impact": random.uniform(5, 30),  # million dollars
            "tourism_losses": random.uniform(1, 10),  # million dollars
            "total_estimated_impact": random.uniform(25, 100),  # million dollars
            "jobs_affected": random.randint(500, 5000),
            "businesses_impacted": random.randint(100, 1000)
        }
    
    def _assess_social_impact(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess social impact of outbreak and response."""
        
        return {
            "community_trust_level": random.uniform(0.6, 0.9),  # 0-1 scale
            "social_cohesion_impact": "strengthened",  # "weakened", "neutral", "strengthened"
            "stigmatization_reported": random.choice([True, False]),
            "mental_health_impact": "moderate",  # "low", "moderate", "high", "severe"
            "education_disruption": random.randint(5, 30),  # days
            "social_services_strain": "manageable",  # "minimal", "manageable", "significant", "overwhelmed"
            "community_resilience_rating": random.uniform(0.7, 0.95)
        }
    
    def _generate_immediate_actions(self, findings: EvaluationFindings) -> List[str]:
        """Generate immediate action recommendations."""
        
        actions = []
        
        # Address critical performance gaps
        for domain, score in findings.domain_assessments.items():
            if score < 0.4:
                actions.append(f"Immediate review and reinforcement of {domain.value.replace('_', ' ')} capabilities")
        
        # General immediate actions
        immediate_action_templates = [
            "Conduct after-action review with all response partners",
            "Update emergency contact lists and communication protocols",
            "Replenish depleted emergency response supplies",
            "Debrief response teams and document lessons learned",
            "Review and update standard operating procedures"
        ]
        
        actions.extend(random.sample(immediate_action_templates, 3))
        
        return actions[:5]
    
    def _generate_short_term_improvements(self, findings: EvaluationFindings) -> List[str]:
        """Generate short-term improvement recommendations."""
        
        improvements = [
            "Enhance cross-sector coordination training and exercises",
            "Develop improved resource sharing agreements",
            "Strengthen surveillance and detection capabilities",
            "Improve community engagement and risk communication strategies",
            "Upgrade information management and decision support systems",
            "Expand laboratory diagnostic capacity",
            "Enhance staff training and competency development"
        ]
        
        return random.sample(improvements, 4)
    
    def _generate_strategic_changes(self, findings: EvaluationFindings) -> List[str]:
        """Generate long-term strategic change recommendations."""
        
        strategic_changes = [
            "Develop integrated One Health response framework",
            "Establish regional response coordination mechanisms",
            "Invest in advanced surveillance and early warning systems",
            "Build sustainable emergency response financing mechanisms",
            "Strengthen preparedness through regular simulation exercises",
            "Develop community resilience and social capital initiatives",
            "Establish international cooperation and resource sharing agreements"
        ]
        
        return random.sample(strategic_changes, 3)
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get comprehensive evaluation system summary."""
        
        if not self.evaluation_findings:
            return {"message": "No evaluations completed"}
        
        # Overall statistics
        total_evaluations = len(self.evaluation_findings)
        evaluation_phases = [f.evaluation_phase for f in self.evaluation_findings.values()]
        
        # Performance analysis
        overall_scores = [f.overall_response_effectiveness for f in self.evaluation_findings.values()]
        performance_levels = [f.overall_performance_level for f in self.evaluation_findings.values()]
        
        # Domain performance analysis
        domain_performance = defaultdict(list)
        for findings in self.evaluation_findings.values():
            for domain, score in findings.domain_assessments.items():
                domain_performance[domain].append(score)
        
        # Average domain performance
        avg_domain_performance = {
            domain.value: statistics.mean(scores) 
            for domain, scores in domain_performance.items()
        }
        
        # Lessons learned analysis
        total_lessons = sum(len(f.lessons_learned) for f in self.evaluation_findings.values())
        lesson_domains = []
        for findings in self.evaluation_findings.values():
            lesson_domains.extend([l.evaluation_domain for l in findings.lessons_learned])
        
        return {
            "evaluation_statistics": {
                "total_evaluations": total_evaluations,
                "evaluation_phases": list(set(phase.value for phase in evaluation_phases)),
                "average_overall_effectiveness": statistics.mean(overall_scores) if overall_scores else 0,
                "performance_level_distribution": {
                    level.value: sum(1 for p in performance_levels if p == level)
                    for level in PerformanceLevel
                }
            },
            "domain_performance": avg_domain_performance,
            "lessons_learned": {
                "total_lessons": total_lessons,
                "lessons_by_domain": {
                    domain.value: sum(1 for d in lesson_domains if d == domain)
                    for domain in EvaluationDomain
                }
            },
            "evaluation_framework": {
                "total_metrics": len(self.metric_library),
                "evaluation_templates": {
                    phase.value: len(metrics) 
                    for phase, metrics in self.evaluation_templates.items()
                }
            }
        }

def run_demonstration() -> ResponseEvaluationManager:
    """Run comprehensive response evaluation demonstration."""
    
    print("📊 One Health Response Evaluation System - Demonstration")
    print("=" * 75)
    
    manager = ResponseEvaluationManager()
    
    print(f"\n📊 Evaluation Framework:")
    print(f"  Standard Metrics: {len(manager.metric_library)}")
    print(f"  Evaluation Domains: {len(EvaluationDomain)}")
    print(f"  Performance Levels: {len(PerformanceLevel)}")
    
    # Simulate outbreak response data for evaluation
    outbreak_scenarios = [
        {
            "outbreak_id": "H5N1_2026_001",
            "outbreak_name": "H5N1 Avian Influenza Outbreak",
            "evaluation_phase": EvaluationPhase.COMPREHENSIVE,
            "response_data": {
                "duration_days": 45,
                "cases_total": 234,
                "interventions_deployed": 8,
                "resources_mobilized": 15,
                "stakeholders_engaged": 12
            }
        },
        {
            "outbreak_id": "ZOONOTIC_2026_002",
            "outbreak_name": "Zoonotic Pathogen Investigation",
            "evaluation_phase": EvaluationPhase.POST_ACTION,
            "response_data": {
                "duration_days": 21,
                "cases_total": 45,
                "interventions_deployed": 5,
                "resources_mobilized": 8,
                "stakeholders_engaged": 6
            }
        }
    ]
    
    print(f"\n📊 Evaluation Scenarios:")
    for scenario in outbreak_scenarios:
        print(f"  {scenario['outbreak_id']}: {scenario['outbreak_name']}")
        print(f"    Phase: {scenario['evaluation_phase'].value.replace('_', ' ').title()}")
        print(f"    Duration: {scenario['response_data']['duration_days']} days")
        print(f"    Cases: {scenario['response_data']['cases_total']}")
    
    print(f"\n📊 Conducting Evaluations...")
    
    # Conduct evaluations
    evaluation_results = []
    for scenario in outbreak_scenarios:
        findings = manager.conduct_evaluation(
            outbreak_id=scenario["outbreak_id"],
            evaluation_phase=scenario["evaluation_phase"],
            response_data=scenario["response_data"]
        )
        evaluation_results.append(findings)
        
        effectiveness_pct = findings.overall_response_effectiveness * 100
        print(f"  ✅ {scenario['outbreak_id']}: {effectiveness_pct:.1f}% effectiveness, "
              f"{findings.overall_performance_level.value.replace('_', ' ').title()}")
    
    return manager

def display_evaluation_results(manager: ResponseEvaluationManager):
    """Display comprehensive evaluation results."""
    
    evaluations = list(manager.evaluation_findings.values())
    
    print(f"\n📊 Response Evaluation Results ({len(evaluations)} evaluations):")
    
    for i, findings in enumerate(evaluations, 1):
        print(f"\n{i}. Evaluation {findings.findings_id}")
        print(f"   Outbreak: {findings.outbreak_id}")
        print(f"   Phase: {findings.evaluation_phase.value.replace('_', ' ').title()}")
        print(f"   Overall Effectiveness: {findings.overall_response_effectiveness:.1%}")
        print(f"   Performance Level: {findings.overall_performance_level.value.replace('_', ' ').title()}")
        print(f"   Date: {findings.evaluation_date.strftime('%Y-%m-%d')}")
        
        print(f"   Domain Performance:")
        for domain, score in sorted(findings.domain_assessments.items(), key=lambda x: x[1], reverse=True):
            print(f"     {domain.value.replace('_', ' ').title()}: {score:.1%}")
        
        if findings.major_strengths:
            print(f"   Major Strengths ({len(findings.major_strengths)}):")
            for strength in findings.major_strengths[:2]:
                print(f"     • {strength}")
        
        if findings.critical_gaps:
            print(f"   Critical Gaps ({len(findings.critical_gaps)}):")
            for gap in findings.critical_gaps[:2]:
                print(f"     • {gap}")
        
        if findings.lessons_learned:
            print(f"   Lessons Learned: {len(findings.lessons_learned)} identified")
        
        # Show impact assessment
        human_impact = findings.human_health_impact
        if human_impact:
            print(f"   Human Health Impact: {human_impact.get('total_cases', 0)} cases, "
                  f"{human_impact.get('attack_rate', 0):.1%} attack rate")
    
    # System summary
    summary = manager.get_evaluation_summary()
    
    print(f"\n📊 Evaluation System Summary:")
    
    eval_stats = summary["evaluation_statistics"]
    print(f"  Total Evaluations: {eval_stats['total_evaluations']}")
    print(f"  Average Effectiveness: {eval_stats['average_overall_effectiveness']:.1%}")
    print(f"  Evaluation Phases: {', '.join(eval_stats['evaluation_phases'])}")
    
    print(f"\n📈 Performance Level Distribution:")
    for level, count in eval_stats["performance_level_distribution"].items():
        if count > 0:
            print(f"  {level.replace('_', ' ').title()}: {count}")
    
    print(f"\n📊 Domain Performance (Average):")
    top_domains = sorted(summary["domain_performance"].items(), key=lambda x: x[1], reverse=True)
    for domain, avg_score in top_domains[:5]:
        print(f"  {domain.replace('_', ' ').title()}: {avg_score:.1%}")
    
    print(f"\n📚 Lessons Learned Analysis:")
    lessons = summary["lessons_learned"]
    print(f"  Total Lessons: {lessons['total_lessons']}")
    
    lesson_domains = [(domain, count) for domain, count in lessons["lessons_by_domain"].items() if count > 0]
    if lesson_domains:
        print(f"  Top Learning Domains:")
        for domain, count in sorted(lesson_domains, key=lambda x: x[1], reverse=True)[:3]:
            print(f"    {domain.replace('_', ' ').title()}: {count} lessons")
    
    print(f"\n🛠️ Evaluation Framework:")
    framework = summary["evaluation_framework"]
    print(f"  Total Metrics: {framework['total_metrics']}")
    print(f"  Evaluation Templates: {len(framework['evaluation_templates'])} phases")
    
    # Show detailed lessons from first evaluation
    if evaluations and evaluations[0].lessons_learned:
        print(f"\n📚 Sample Lessons Learned:")
        for i, lesson in enumerate(evaluations[0].lessons_learned[:2], 1):
            print(f"  {i}. {lesson.lesson_title}")
            print(f"     Domain: {lesson.evaluation_domain.value.replace('_', ' ').title()}")
            print(f"     Priority: {lesson.implementation_priority.title()}")
            if lesson.specific_recommendations:
                print(f"     Recommendations: {len(lesson.specific_recommendations)} identified")
    
    print(f"\n🏆 TOP PERFORMING Domains:")
    top_performers = sorted(summary["domain_performance"].items(), 
                          key=lambda x: x[1], reverse=True)[:3]
    for i, (domain, score) in enumerate(top_performers, 1):
        print(f"  {i}. {domain.replace('_', ' ').title()}: {score:.1%}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    evaluation_manager = run_demonstration()
    display_evaluation_results(evaluation_manager)
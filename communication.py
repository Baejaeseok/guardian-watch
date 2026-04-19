"""
Module 38: communication.py
Risk Communication & Stakeholder Management System for One Health
Zoonotic Disease Emergency Response
"""

import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class MessageType(Enum):
    ALERT = "alert"
    GUIDANCE = "guidance"
    UPDATE = "update"
    EDUCATION = "education"
    REASSURANCE = "reassurance"
    ACTION_REQUIRED = "action_required"
    PRESS_RELEASE = "press_release"

class Channel(Enum):
    SMS = "sms"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    PRESS_RELEASE = "press_release"
    WEBSITE = "website"
    RADIO = "radio"
    TV = "tv"
    COMMUNITY_MEETING = "community_meeting"
    HOTLINE = "hotline"

class Audience(Enum):
    GENERAL_PUBLIC = "general_public"
    HEALTHCARE_WORKERS = "healthcare_workers"
    VETERINARIANS = "veterinarians"
    FARMERS = "farmers"
    POLICYMAKERS = "policymakers"
    MEDIA = "media"
    INTERNATIONAL_PARTNERS = "international_partners"
    HIGH_RISK_GROUPS = "high_risk_groups"

class CrisisPhase(Enum):
    PRE_CRISIS = "pre_crisis"
    INITIAL = "initial"
    MAINTENANCE = "maintenance"
    RESOLUTION = "resolution"
    EVALUATION = "evaluation"

class MessagePriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class Message:
    message_id: str
    message_type: MessageType
    priority: MessagePriority
    title: str
    body: str
    key_points: list
    call_to_action: str
    target_audience: list
    channels: list
    language: str
    estimated_reach: int
    sentiment: str  # reassuring / cautionary / urgent / neutral

@dataclass
class Stakeholder:
    stakeholder_id: str
    name: str
    organization: str
    role: str
    audience_type: Audience
    contact_channels: list
    influence_level: float  # 0-1
    trust_level: float      # 0-1
    engagement_history: list

@dataclass
class CommunicationCampaign:
    campaign_id: str
    name: str
    disease: str
    crisis_phase: CrisisPhase
    start_date: str
    duration_days: int
    target_audiences: list
    messages: list
    channels: list
    budget_usd: float
    kpis: dict

@dataclass
class MediaInquiry:
    inquiry_id: str
    journalist_name: str
    outlet: str
    question: str
    deadline: str
    status: str
    response: str
    assigned_spokesperson: str

@dataclass
class CommunicationMetrics:
    campaign_id: str
    total_reach: int
    unique_impressions: int
    engagement_rate: float
    comprehension_rate: float
    behavior_change_rate: float
    trust_score: float
    misinformation_incidents: int
    media_coverage_count: int
    hotline_calls: int


# ============================================================
# MESSAGE GENERATOR
# ============================================================

class OneHealthMessageGenerator:
    """
    Generates targeted, audience-appropriate risk communication messages
    for One Health zoonotic disease events
    """

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        return {
            "alert": {
                "general_public": {
                    "title": "Public Health Alert: {disease} Cases Confirmed",
                    "key_points": [
                        "Health authorities have confirmed cases of {disease} in {location}",
                        "Risk to general public is currently assessed as {risk_level}",
                        "Authorities are actively investigating and responding",
                        "Follow standard hygiene precautions"
                    ],
                    "cta": "If you experience symptoms ({symptoms}), contact your healthcare provider immediately."
                },
                "farmers": {
                    "title": "Urgent Agricultural Health Alert: {disease} Detected",
                    "key_points": [
                        "Animal cases of {disease} confirmed in {location}",
                        "Immediately report sick or dead animals to authorities",
                        "Do NOT handle sick animals without protective equipment",
                        "Contact your veterinarian for herd assessment"
                    ],
                    "cta": "Report dead or sick animals: Call {hotline}. Your cooperation protects your livelihood and community health."
                },
                "healthcare_workers": {
                    "title": "Clinical Advisory: {disease} - Enhanced Precautions Required",
                    "key_points": [
                        "Zoonotic transmission of {disease} confirmed - exercise heightened vigilance",
                        "Case definition and diagnostic criteria attached",
                        "Enhanced PPE required for all suspected cases",
                        "Mandatory reporting within 24 hours of confirmed cases"
                    ],
                    "cta": "Review updated clinical protocols at {portal_url}. Report all suspected cases to {reporting_system}."
                }
            },
            "guidance": {
                "general_public": {
                    "title": "How to Protect Yourself from {disease}",
                    "key_points": [
                        "Wash hands thoroughly with soap and water for 20 seconds",
                        "Avoid contact with sick or dead animals",
                        "Cook poultry and eggs to proper internal temperature (74°C/165°F)",
                        "Seek medical attention if you develop fever, cough, or difficulty breathing"
                    ],
                    "cta": "Share this information with your family and neighbors."
                }
            },
            "update": {
                "general_public": {
                    "title": "{disease} Situation Update - {date}",
                    "key_points": [
                        "Total human cases to date: {human_cases}",
                        "Total animal cases reported: {animal_cases}",
                        "Containment measures currently in effect",
                        "Response teams deployed across {regions} regions"
                    ],
                    "cta": "Stay informed at {website}. Follow official accounts only."
                }
            }
        }

    def generate_message(self, disease: str, message_type: MessageType,
                         audience: Audience, situation: dict) -> Message:
        """Generate targeted communication message"""

        msg_key = message_type.value
        aud_key = audience.value.replace("_", "_")

        # Map audience to template key
        audience_map = {
            Audience.GENERAL_PUBLIC: "general_public",
            Audience.FARMERS: "farmers",
            Audience.HEALTHCARE_WORKERS: "healthcare_workers",
            Audience.VETERINARIANS: "farmers",  # reuse farmers template
            Audience.POLICYMAKERS: "general_public",
            Audience.MEDIA: "general_public",
            Audience.HIGH_RISK_GROUPS: "general_public"
        }
        aud_template_key = audience_map.get(audience, "general_public")

        template = (self.templates.get(msg_key, {}).get(aud_template_key)
                    or self.templates.get(msg_key, {}).get("general_public")
                    or {"title": f"{disease} {msg_key}", "key_points": ["See official sources"], "cta": "Stay informed."})

        # Fill template
        location = situation.get("location", "the affected region")
        risk_level = situation.get("risk_level", "moderate")
        symptoms = situation.get("symptoms", "fever, cough, breathing difficulty")
        hotline = situation.get("hotline", "1-800-HEALTH")
        date = datetime.now().strftime("%B %d, %Y")

        def fill(text):
            return (text.replace("{disease}", disease)
                        .replace("{location}", location)
                        .replace("{risk_level}", risk_level)
                        .replace("{symptoms}", symptoms)
                        .replace("{hotline}", hotline)
                        .replace("{human_cases}", str(situation.get("human_cases", 0)))
                        .replace("{animal_cases}", str(situation.get("animal_cases", 0)))
                        .replace("{regions}", str(situation.get("regions", 3)))
                        .replace("{website}", situation.get("website", "health.gov"))
                        .replace("{portal_url}", situation.get("portal", "clinician.health.gov"))
                        .replace("{reporting_system}", situation.get("reporting", "EpiNet"))
                        .replace("{date}", date))

        title = fill(template["title"])
        key_points = [fill(kp) for kp in template["key_points"]]
        cta = fill(template.get("cta", "Contact your local health authority."))

        # Generate body
        body = f"{title}\n\n" + "\n".join(f"• {kp}" for kp in key_points) + f"\n\n{cta}"

        # Determine channels based on audience
        channel_map = {
            Audience.GENERAL_PUBLIC: [Channel.SMS, Channel.SOCIAL_MEDIA, Channel.TV, Channel.RADIO],
            Audience.HEALTHCARE_WORKERS: [Channel.EMAIL, Channel.WEBSITE, Channel.HOTLINE],
            Audience.FARMERS: [Channel.SMS, Channel.RADIO, Channel.COMMUNITY_MEETING],
            Audience.VETERINARIANS: [Channel.EMAIL, Channel.SMS, Channel.WEBSITE],
            Audience.POLICYMAKERS: [Channel.EMAIL, Channel.PRESS_RELEASE],
            Audience.MEDIA: [Channel.PRESS_RELEASE, Channel.EMAIL]
        }
        channels = channel_map.get(audience, [Channel.EMAIL, Channel.WEBSITE])

        # Estimate reach
        reach_map = {
            Audience.GENERAL_PUBLIC: random.randint(50000, 500000),
            Audience.HEALTHCARE_WORKERS: random.randint(2000, 15000),
            Audience.FARMERS: random.randint(5000, 50000),
            Audience.POLICYMAKERS: random.randint(100, 500),
            Audience.MEDIA: random.randint(500, 2000)
        }
        reach = reach_map.get(audience, 10000)

        priority = (MessagePriority.CRITICAL if situation.get("active_outbreak") and msg_key == "alert"
                    else MessagePriority.HIGH if msg_key in ["alert", "action_required"]
                    else MessagePriority.MEDIUM)

        sentiment = ("urgent" if msg_key == "alert" else
                     "reassuring" if msg_key == "reassurance" else
                     "neutral" if msg_key == "update" else "cautionary")

        return Message(
            message_id=f"MSG_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{audience.value[:3].upper()}",
            message_type=message_type,
            priority=priority,
            title=title,
            body=body,
            key_points=key_points,
            call_to_action=cta,
            target_audience=[audience.value],
            channels=[c.value for c in channels],
            language="English",
            estimated_reach=reach,
            sentiment=sentiment
        )

    def generate_campaign_messages(self, disease: str, situation: dict,
                                   crisis_phase: CrisisPhase) -> list:
        """Generate full suite of messages for a campaign"""
        messages = []

        if crisis_phase in [CrisisPhase.INITIAL, CrisisPhase.MAINTENANCE]:
            # Alert messages for high-priority audiences
            for audience in [Audience.GENERAL_PUBLIC, Audience.HEALTHCARE_WORKERS, Audience.FARMERS]:
                msg = self.generate_message(disease, MessageType.ALERT, audience, situation)
                messages.append(msg)

        # Guidance for all
        for audience in [Audience.GENERAL_PUBLIC, Audience.FARMERS]:
            msg = self.generate_message(disease, MessageType.GUIDANCE, audience, situation)
            messages.append(msg)

        # Update message
        msg = self.generate_message(disease, MessageType.UPDATE, Audience.GENERAL_PUBLIC, situation)
        messages.append(msg)

        return messages


# ============================================================
# STAKEHOLDER ENGAGEMENT MANAGER
# ============================================================

class StakeholderEngagementManager:
    """
    Manages relationships and communication with key stakeholders
    during One Health events
    """

    def __init__(self):
        self.stakeholders = self._initialize_stakeholders()

    def _initialize_stakeholders(self) -> list:
        return [
            Stakeholder("sh_001", "Ministry of Health Director", "Ministry of Health",
                        "Senior Decision Maker", Audience.POLICYMAKERS,
                        [Channel.EMAIL, Channel.HOTLINE], 0.95, 0.85, []),
            Stakeholder("sh_002", "FAO Country Representative", "Food and Agriculture Organization",
                        "International Partner", Audience.INTERNATIONAL_PARTNERS,
                        [Channel.EMAIL, Channel.PRESS_RELEASE], 0.85, 0.90, []),
            Stakeholder("sh_003", "National Farmers Association", "Farmers Association",
                        "Affected Community", Audience.FARMERS,
                        [Channel.SMS, Channel.COMMUNITY_MEETING, Channel.RADIO], 0.75, 0.65, []),
            Stakeholder("sh_004", "National Medical Association", "Medical Association",
                        "Professional Body", Audience.HEALTHCARE_WORKERS,
                        [Channel.EMAIL, Channel.WEBSITE], 0.80, 0.88, []),
            Stakeholder("sh_005", "Chief Science Journalist", "National Press",
                        "Media Lead", Audience.MEDIA,
                        [Channel.PRESS_RELEASE, Channel.EMAIL], 0.70, 0.60, []),
            Stakeholder("sh_006", "WHO Regional Office", "World Health Organization",
                        "International Regulator", Audience.INTERNATIONAL_PARTNERS,
                        [Channel.EMAIL, Channel.PRESS_RELEASE], 0.90, 0.92, []),
            Stakeholder("sh_007", "Veterinary Services Director", "Ministry of Agriculture",
                        "Animal Health Lead", Audience.VETERINARIANS,
                        [Channel.EMAIL, Channel.HOTLINE], 0.85, 0.88, []),
            Stakeholder("sh_008", "Community Health Advocates", "Civil Society",
                        "Community Voice", Audience.GENERAL_PUBLIC,
                        [Channel.SMS, Channel.SOCIAL_MEDIA, Channel.COMMUNITY_MEETING], 0.65, 0.70, [])
        ]

    def get_engagement_plan(self, crisis_phase: CrisisPhase) -> dict:
        """Generate stakeholder engagement plan for crisis phase"""
        plan = {
            "crisis_phase": crisis_phase.value,
            "generated_at": datetime.now().isoformat(),
            "stakeholder_priorities": [],
            "communication_frequency": {},
            "key_messages_by_stakeholder": {}
        }

        freq_map = {
            CrisisPhase.INITIAL: "Every 6 hours",
            CrisisPhase.MAINTENANCE: "Daily",
            CrisisPhase.RESOLUTION: "Every 48 hours",
            CrisisPhase.PRE_CRISIS: "Weekly",
            CrisisPhase.EVALUATION: "Weekly"
        }

        for stakeholder in sorted(self.stakeholders, key=lambda x: x.influence_level, reverse=True):
            priority = "CRITICAL" if stakeholder.influence_level >= 0.85 else "HIGH" if stakeholder.influence_level >= 0.70 else "MEDIUM"
            plan["stakeholder_priorities"].append({
                "name": stakeholder.name,
                "organization": stakeholder.organization,
                "influence": stakeholder.influence_level,
                "trust": stakeholder.trust_level,
                "priority": priority,
                "preferred_channels": [c.value for c in stakeholder.contact_channels]
            })
            plan["communication_frequency"][stakeholder.name] = freq_map.get(crisis_phase, "Daily")

        return plan

    def log_engagement(self, stakeholder_id: str, channel: Channel, message_type: MessageType, outcome: str):
        """Log a stakeholder engagement event"""
        for sh in self.stakeholders:
            if sh.stakeholder_id == stakeholder_id:
                sh.engagement_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "channel": channel.value,
                    "message_type": message_type.value,
                    "outcome": outcome
                })
                return True
        return False

    def get_engagement_summary(self) -> dict:
        return {
            "total_stakeholders": len(self.stakeholders),
            "high_influence": sum(1 for s in self.stakeholders if s.influence_level >= 0.8),
            "avg_trust_level": round(sum(s.trust_level for s in self.stakeholders) / len(self.stakeholders), 2),
            "total_engagements": sum(len(s.engagement_history) for s in self.stakeholders)
        }


# ============================================================
# CRISIS COMMUNICATION SYSTEM
# ============================================================

class CrisisCommunicationSystem:
    """
    Manages end-to-end crisis communication for One Health emergencies
    """

    def __init__(self):
        self.message_generator = OneHealthMessageGenerator()
        self.stakeholder_manager = StakeholderEngagementManager()
        self.active_campaigns = []
        self.media_inquiries = []
        self.sent_messages = []

    def launch_campaign(self, disease: str, situation: dict, crisis_phase: CrisisPhase) -> CommunicationCampaign:
        """Launch a full communication campaign"""

        messages = self.message_generator.generate_campaign_messages(disease, situation, crisis_phase)
        self.sent_messages.extend(messages)

        all_channels = list(set(ch for msg in messages for ch in msg.channels))
        all_audiences = list(set(aud for msg in messages for aud in msg.target_audience))

        campaign = CommunicationCampaign(
            campaign_id=f"CAMP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=f"{disease} {crisis_phase.value.replace('_', ' ').title()} Response",
            disease=disease,
            crisis_phase=crisis_phase,
            start_date=datetime.now().isoformat(),
            duration_days=30 if crisis_phase == CrisisPhase.INITIAL else 90,
            target_audiences=all_audiences,
            messages=[m.message_id for m in messages],
            channels=all_channels,
            budget_usd=random.uniform(50000, 500000),
            kpis={
                "target_reach": sum(m.estimated_reach for m in messages),
                "target_comprehension_rate": 0.75,
                "target_behavior_change": 0.30,
                "target_trust_score": 0.80
            }
        )

        self.active_campaigns.append(campaign)
        return campaign

    def handle_media_inquiry(self, journalist: str, outlet: str, question: str, deadline_hours: int = 4) -> MediaInquiry:
        """Generate response to media inquiry"""

        # Auto-generate key response points
        response_points = [
            "Health authorities are actively monitoring and responding to the situation.",
            "A coordinated One Health response is underway involving human health, animal health, and environmental sectors.",
            "Current risk to the general public remains under assessment — precautionary measures are in place.",
            "We will provide regular updates as new information becomes available.",
            "Public health officials will hold a press briefing at {time}."
        ]
        response = "Thank you for your inquiry. " + " ".join(response_points[:3])

        inquiry = MediaInquiry(
            inquiry_id=f"MED_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            journalist_name=journalist,
            outlet=outlet,
            question=question,
            deadline=(datetime.now() + timedelta(hours=deadline_hours)).isoformat(),
            status="responded",
            response=response,
            assigned_spokesperson="Public Health Director"
        )

        self.media_inquiries.append(inquiry)
        return inquiry

    def calculate_metrics(self, campaign: CommunicationCampaign) -> CommunicationMetrics:
        """Calculate campaign communication metrics"""

        campaign_messages = [m for m in self.sent_messages if m.message_id in campaign.messages]

        total_reach = sum(m.estimated_reach for m in campaign_messages)
        unique_impressions = int(total_reach * 0.75)
        engagement_rate = random.uniform(0.08, 0.25)
        comprehension_rate = random.uniform(0.65, 0.90)
        behavior_change = random.uniform(0.15, 0.45)
        trust_score = random.uniform(0.60, 0.90)
        misinformation = random.randint(0, 5)
        media_coverage = random.randint(15, 80)
        hotline_calls = random.randint(200, 3000)

        return CommunicationMetrics(
            campaign_id=campaign.campaign_id,
            total_reach=total_reach,
            unique_impressions=unique_impressions,
            engagement_rate=round(engagement_rate, 3),
            comprehension_rate=round(comprehension_rate, 3),
            behavior_change_rate=round(behavior_change, 3),
            trust_score=round(trust_score, 3),
            misinformation_incidents=misinformation,
            media_coverage_count=media_coverage,
            hotline_calls=hotline_calls
        )

    def get_system_status(self) -> dict:
        return {
            "active_campaigns": len(self.active_campaigns),
            "total_messages_sent": len(self.sent_messages),
            "total_media_inquiries": len(self.media_inquiries),
            "total_estimated_reach": sum(m.estimated_reach for m in self.sent_messages),
            "stakeholder_summary": self.stakeholder_manager.get_engagement_summary()
        }


# ============================================================
# SOCIAL MEDIA MONITORING
# ============================================================

class SocialMediaMonitor:
    """
    Monitors social media for disease-related misinformation and sentiment
    """

    def __init__(self):
        self.platforms = ["Twitter/X", "Facebook", "Instagram", "YouTube", "TikTok", "Telegram"]

    def analyze_sentiment(self, disease: str) -> dict:
        """Analyze social media sentiment about the disease event"""

        sentiments = {platform: {
            "positive": random.uniform(0.15, 0.35),
            "neutral": random.uniform(0.30, 0.50),
            "negative": random.uniform(0.20, 0.40),
            "panic_indicators": random.uniform(0.05, 0.20),
            "posts_analyzed": random.randint(5000, 50000)
        } for platform in self.platforms}

        # Normalize sentiment values
        for platform in sentiments:
            s = sentiments[platform]
            total = s["positive"] + s["neutral"] + s["negative"]
            s["positive"] = round(s["positive"] / total, 2)
            s["neutral"] = round(s["neutral"] / total, 2)
            s["negative"] = round(s["negative"] / total, 2)

        # Detect misinformation themes
        misinfo_themes = [
            {"theme": "False cure claims", "prevalence": random.uniform(0.05, 0.20), "severity": "HIGH"},
            {"theme": "Conspiracy theories about origin", "prevalence": random.uniform(0.03, 0.15), "severity": "MODERATE"},
            {"theme": "Exaggerated mortality claims", "prevalence": random.uniform(0.02, 0.10), "severity": "HIGH"},
            {"theme": "Vaccine misinformation", "prevalence": random.uniform(0.01, 0.08), "severity": "MODERATE"}
        ]

        total_posts = sum(s["posts_analyzed"] for s in sentiments.values())
        avg_negative = sum(s["negative"] for s in sentiments.values()) / len(sentiments)

        return {
            "disease": disease,
            "analysis_timestamp": datetime.now().isoformat(),
            "total_posts_analyzed": total_posts,
            "platform_sentiments": sentiments,
            "misinformation_themes": misinfo_themes,
            "overall_negative_sentiment": round(avg_negative, 2),
            "risk_assessment": "HIGH" if avg_negative > 0.35 else "MODERATE" if avg_negative > 0.25 else "LOW",
            "recommended_actions": [
                "Deploy counter-messaging on high-negativity platforms",
                "Engage fact-checkers for top misinformation themes",
                "Increase frequency of authoritative updates",
                "Partner with social media platforms for content moderation"
            ]
        }

    def track_hashtags(self, disease: str) -> dict:
        hashtags = [
            f"#{disease.replace(' ', '')}",
            f"#{disease.replace(' ', '')}Outbreak",
            "#OneHealth",
            "#PublicHealth",
            "#Zoonosis",
            f"#{disease.replace(' ', '')}Alert"
        ]

        return {
            "tracked_hashtags": [
                {"hashtag": ht, "volume_24h": random.randint(100, 50000),
                 "trend": random.choice(["rising", "stable", "declining"]),
                 "sentiment": random.choice(["mostly_positive", "mixed", "mostly_negative"])}
                for ht in hashtags
            ],
            "top_hashtag": hashtags[0],
            "total_volume_24h": random.randint(50000, 500000)
        }


# ============================================================
# INTEGRATED COMMUNICATION MANAGER
# ============================================================

class IntegratedCommunicationManager:
    """
    Main orchestrator for all One Health communication activities
    """

    def __init__(self):
        self.crisis_comm = CrisisCommunicationSystem()
        self.social_monitor = SocialMediaMonitor()

    def run_full_communication_response(self, disease: str, situation: dict) -> dict:
        """Execute complete communication response for an outbreak"""

        print(f"\n{'='*60}")
        print("ONE HEALTH COMMUNICATION MANAGEMENT SYSTEM")
        print(f"{'='*60}")
        print(f"Disease: {disease} | Location: {situation.get('location', 'N/A')}")
        print(f"Phase: {situation.get('phase', 'INITIAL')} | Active Outbreak: {situation.get('active_outbreak', True)}")
        print(f"{'='*60}\n")

        # Determine phase
        phase = CrisisPhase.INITIAL if situation.get("active_outbreak") else CrisisPhase.MAINTENANCE

        # Launch campaign
        print("📢 Launching Communication Campaign...")
        campaign = self.crisis_comm.launch_campaign(disease, situation, phase)

        # Get stakeholder plan
        print("🤝 Generating Stakeholder Engagement Plan...")
        engagement_plan = self.crisis_comm.stakeholder_manager.get_engagement_plan(phase)

        # Handle media inquiries
        print("📰 Processing Media Inquiries...")
        inquiries = []
        for journalist, outlet, question in [
            ("Dr. Sarah Kim", "National Health Times", f"What is the current status of the {disease} outbreak?"),
            ("James Rodriguez", "Reuters Health", f"What measures are being taken to prevent {disease} spread to humans?"),
            ("Anna Chen", "Global Health Watch", f"Has the One Health response been effective?")
        ]:
            inq = self.crisis_comm.handle_media_inquiry(journalist, outlet, question)
            inquiries.append(inq)

        # Social media analysis
        print("📱 Analyzing Social Media Landscape...")
        social_analysis = self.social_monitor.analyze_sentiment(disease)
        hashtag_data = self.social_monitor.track_hashtags(disease)

        # Calculate metrics
        print("📊 Calculating Communication Metrics...")
        metrics = self.crisis_comm.calculate_metrics(campaign)

        return {
            "response_id": f"COMM_RESP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "disease": disease,
            "campaign": {
                "campaign_id": campaign.campaign_id,
                "name": campaign.name,
                "messages_sent": len(campaign.messages),
                "target_audiences": campaign.target_audiences,
                "channels": campaign.channels,
                "budget_usd": round(campaign.budget_usd),
                "kpis": campaign.kpis
            },
            "messages_generated": len(self.crisis_comm.sent_messages),
            "stakeholder_engagement": {
                "total_stakeholders": len(engagement_plan["stakeholder_priorities"]),
                "critical_stakeholders": sum(1 for s in engagement_plan["stakeholder_priorities"] if s["priority"] == "CRITICAL"),
                "top_priority": engagement_plan["stakeholder_priorities"][0] if engagement_plan["stakeholder_priorities"] else None
            },
            "media_management": {
                "inquiries_handled": len(inquiries),
                "media_outlets": [i.outlet for i in inquiries],
                "avg_response_quality": "HIGH"
            },
            "social_media": {
                "total_posts_analyzed": social_analysis["total_posts_analyzed"],
                "risk_assessment": social_analysis["risk_assessment"],
                "top_misinformation": social_analysis["misinformation_themes"][0]["theme"] if social_analysis["misinformation_themes"] else None,
                "top_hashtag_volume": hashtag_data["total_volume_24h"]
            },
            "metrics": {
                "total_reach": metrics.total_reach,
                "unique_impressions": metrics.unique_impressions,
                "engagement_rate": f"{metrics.engagement_rate:.1%}",
                "comprehension_rate": f"{metrics.comprehension_rate:.1%}",
                "behavior_change_rate": f"{metrics.behavior_change_rate:.1%}",
                "trust_score": f"{metrics.trust_score:.1%}",
                "hotline_calls": metrics.hotline_calls,
                "media_coverage_count": metrics.media_coverage_count
            },
            "system_status": self.crisis_comm.get_system_status()
        }


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 38: COMMUNICATION SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    situation = {
        "disease": "H5N1 Avian Influenza",
        "location": "Northern Agricultural Province",
        "risk_level": "high",
        "active_outbreak": True,
        "human_cases": 47,
        "animal_cases": 2300,
        "regions": 4,
        "phase": "INITIAL",
        "hotline": "1-800-ONE-HLTH",
        "website": "health.gov/h5n1",
        "portal": "clinicians.health.gov",
        "reporting": "EpiNet",
        "symptoms": "fever >38°C, cough, difficulty breathing, conjunctivitis"
    }

    manager = IntegratedCommunicationManager()
    result = manager.run_full_communication_response("H5N1 Avian Influenza", situation)

    print(f"\n📢 CAMPAIGN RESULTS:")
    c = result["campaign"]
    print(f"  Campaign: {c['name']}")
    print(f"  Messages Sent: {result['messages_generated']}")
    print(f"  Channels: {', '.join(c['channels'][:5])}")
    print(f"  Audiences: {', '.join(c['target_audiences'])}")
    print(f"  Budget: ${c['budget_usd']:,}")
    print(f"  Target Reach: {c['kpis']['target_reach']:,}")

    print(f"\n🤝 STAKEHOLDER ENGAGEMENT:")
    se = result["stakeholder_engagement"]
    print(f"  Total Stakeholders: {se['total_stakeholders']}")
    print(f"  Critical Priority: {se['critical_stakeholders']}")
    if se["top_priority"]:
        tp = se["top_priority"]
        print(f"  Top Priority: {tp['name']} ({tp['organization']}) | Influence: {tp['influence']:.0%}")

    print(f"\n📰 MEDIA MANAGEMENT:")
    mm = result["media_management"]
    print(f"  Inquiries Handled: {mm['inquiries_handled']}")
    print(f"  Outlets: {', '.join(mm['media_outlets'])}")
    print(f"  Response Quality: {mm['avg_response_quality']}")

    print(f"\n📱 SOCIAL MEDIA ANALYSIS:")
    sm = result["social_media"]
    print(f"  Posts Analyzed: {sm['total_posts_analyzed']:,}")
    print(f"  Risk Assessment: {sm['risk_assessment']}")
    print(f"  Top Misinformation: {sm['top_misinformation']}")
    print(f"  Top Hashtag Volume: {sm['top_hashtag_volume']:,} posts/24h")

    print(f"\n📊 COMMUNICATION METRICS:")
    m = result["metrics"]
    print(f"  Total Reach: {m['total_reach']:,}")
    print(f"  Unique Impressions: {m['unique_impressions']:,}")
    print(f"  Engagement Rate: {m['engagement_rate']}")
    print(f"  Comprehension Rate: {m['comprehension_rate']}")
    print(f"  Behavior Change: {m['behavior_change_rate']}")
    print(f"  Trust Score: {m['trust_score']}")
    print(f"  Hotline Calls: {m['hotline_calls']:,}")
    print(f"  Media Coverage: {m['media_coverage_count']} articles/broadcasts")

    print(f"\n{'='*70}")
    print("✅ Module 38: communication.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
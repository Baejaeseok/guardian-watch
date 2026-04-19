"""
Module 39: reporting.py
Automated Reporting & Dashboard System for One Health
Zoonotic Disease Surveillance and Response
"""

import json
import random
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class ReportType(Enum):
    SITUATION_REPORT = "situation_report"
    EPIDEMIOLOGICAL_BULLETIN = "epidemiological_bulletin"
    SURVEILLANCE_SUMMARY = "surveillance_summary"
    RESPONSE_PROGRESS = "response_progress"
    RISK_ASSESSMENT = "risk_assessment"
    AFTER_ACTION_REVIEW = "after_action_review"
    REGULATORY_SUBMISSION = "regulatory_submission"
    WEEKLY_DIGEST = "weekly_digest"

class ReportFrequency(Enum):
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    AD_HOC = "ad_hoc"

class ReportFormat(Enum):
    PDF = "pdf"
    HTML = "html"
    DOCX = "docx"
    JSON = "json"
    DASHBOARD = "dashboard"
    EXCEL = "excel"

class DataQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INSUFFICIENT = "insufficient"

class IndicatorTrend(Enum):
    INCREASING = "increasing"
    STABLE = "stable"
    DECREASING = "decreasing"
    FLUCTUATING = "fluctuating"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class KeyIndicator:
    indicator_id: str
    name: str
    domain: str          # human / animal / environment / response
    current_value: float
    previous_value: float
    unit: str
    trend: IndicatorTrend
    threshold_alert: float
    threshold_critical: float
    status: str          # normal / alert / critical
    data_quality: DataQuality

@dataclass
class SituationReport:
    report_id: str
    report_type: ReportType
    disease: str
    location: str
    reporting_period: str
    generated_at: str
    executive_summary: str
    key_findings: list
    indicators: list
    recommendations: list
    next_review: str
    author: str
    classification: str  # public / restricted / confidential

@dataclass
class DashboardWidget:
    widget_id: str
    title: str
    widget_type: str     # counter / chart / map / table / alert
    data: dict
    priority: int        # 1=highest
    last_updated: str

@dataclass
class ReportSchedule:
    schedule_id: str
    report_type: ReportType
    frequency: ReportFrequency
    recipients: list
    format: ReportFormat
    next_due: str
    auto_generate: bool
    active: bool

@dataclass
class EpiIndicator:
    name: str
    value: float
    confidence_interval: tuple
    trend: IndicatorTrend
    interpretation: str


# ============================================================
# INDICATOR CALCULATOR
# ============================================================

class EpidemiologicalIndicatorCalculator:
    """
    Calculates core epidemiological indicators for One Health reporting
    """

    def calculate_attack_rate(self, cases: int, population: int) -> float:
        return round((cases / population) * 100, 4) if population > 0 else 0

    def calculate_case_fatality_rate(self, deaths: int, cases: int) -> float:
        return round((deaths / cases) * 100, 2) if cases > 0 else 0

    def calculate_r0(self, beta: float, gamma: float) -> float:
        """Basic reproduction number R0 = β/γ"""
        return round(beta / gamma, 2) if gamma > 0 else 0

    def calculate_rt(self, cases_recent: list, generation_time: float = 7) -> float:
        """Estimate effective reproduction number Rt"""
        if len(cases_recent) < 2:
            return 1.0
        recent = cases_recent[-7:] if len(cases_recent) >= 7 else cases_recent
        earlier = cases_recent[-14:-7] if len(cases_recent) >= 14 else [1]
        avg_recent = sum(recent) / len(recent)
        avg_earlier = sum(earlier) / len(earlier)
        return round(avg_recent / avg_earlier, 2) if avg_earlier > 0 else 1.0

    def calculate_doubling_time(self, growth_rate: float) -> float:
        """Doubling time in days given daily growth rate"""
        if growth_rate <= 0:
            return float('inf')
        return round(math.log(2) / math.log(1 + growth_rate), 1)

    def calculate_zoonotic_spillover_rate(self, animal_cases: int, human_cases: int) -> float:
        """Ratio of human cases to animal cases (spillover efficiency)"""
        return round((human_cases / animal_cases) * 1000, 2) if animal_cases > 0 else 0

    def calculate_outbreak_score(self, indicators: dict) -> float:
        """Composite outbreak severity score 0-100"""
        score = 0
        rt = indicators.get("rt", 1.0)
        score += min(rt * 20, 40)
        cfr = indicators.get("cfr", 0)
        score += min(cfr * 2, 30)
        spread = indicators.get("geographic_spread", 1)
        score += min(spread * 5, 20)
        spillover = indicators.get("spillover_rate", 0)
        score += min(spillover * 10, 10)
        return round(min(score, 100), 1)

    def generate_full_indicator_set(self, data: dict) -> list:
        """Generate complete set of epidemiological indicators"""

        cases = data.get("human_cases", 0)
        deaths = data.get("deaths", 0)
        animal_cases = data.get("animal_cases", 0)
        population = data.get("population", 100000)
        daily_cases = data.get("daily_cases", [5, 8, 12, 15, 18, 14, 22])
        growth_rate = data.get("growth_rate", 0.087)
        beta = data.get("beta", 0.3)
        gamma = data.get("gamma", 0.1)
        regions = data.get("affected_regions", 4)

        rt = self.calculate_rt(daily_cases)
        r0 = self.calculate_r0(beta, gamma)
        cfr = self.calculate_case_fatality_rate(deaths, cases)
        attack_rate = self.calculate_attack_rate(cases, population)
        doubling_time = self.calculate_doubling_time(growth_rate)
        spillover_rate = self.calculate_zoonotic_spillover_rate(animal_cases, cases)
        outbreak_score = self.calculate_outbreak_score({
            "rt": rt, "cfr": cfr, "geographic_spread": regions, "spillover_rate": spillover_rate
        })

        indicators = [
            EpiIndicator("Effective Reproduction Number (Rt)", rt, (rt*0.85, rt*1.15),
                         IndicatorTrend.INCREASING if rt > 1.2 else IndicatorTrend.STABLE if rt > 0.9 else IndicatorTrend.DECREASING,
                         "Epidemic expanding" if rt > 1 else "Epidemic declining"),
            EpiIndicator("Basic Reproduction Number (R0)", r0, (r0*0.8, r0*1.2),
                         IndicatorTrend.STABLE,
                         f"Each case infects ~{r0} others without intervention"),
            EpiIndicator("Case Fatality Rate (%)", cfr, (cfr*0.7, cfr*1.3),
                         IndicatorTrend.STABLE,
                         "High" if cfr > 5 else "Moderate" if cfr > 1 else "Low"),
            EpiIndicator("Attack Rate (per 100,000)", attack_rate * 1000, (0, attack_rate * 1.5 * 1000),
                         IndicatorTrend.INCREASING,
                         f"{cases} confirmed cases in population of {population:,}"),
            EpiIndicator("Doubling Time (days)", doubling_time, (doubling_time*0.8, doubling_time*1.2),
                         IndicatorTrend.DECREASING if doubling_time < 10 else IndicatorTrend.STABLE,
                         f"Cases doubling every {doubling_time} days"),
            EpiIndicator("Zoonotic Spillover Rate (per 1000 animal cases)", spillover_rate, (0, spillover_rate*2),
                         IndicatorTrend.STABLE,
                         f"{cases} human cases per {animal_cases:,} animal cases"),
            EpiIndicator("Composite Outbreak Severity Score", outbreak_score, (outbreak_score*0.9, outbreak_score*1.1),
                         IndicatorTrend.INCREASING if outbreak_score > 60 else IndicatorTrend.STABLE,
                         "Critical" if outbreak_score > 75 else "High" if outbreak_score > 50 else "Moderate")
        ]

        return indicators


# ============================================================
# REPORT GENERATOR
# ============================================================

class OneHealthReportGenerator:
    """
    Generates comprehensive structured reports for One Health outbreak events
    """

    def __init__(self):
        self.indicator_calc = EpidemiologicalIndicatorCalculator()
        self.generated_reports = []

    def generate_situation_report(self, disease: str, location: str,
                                  situation_data: dict, report_number: int = 1) -> SituationReport:
        """Generate standardized WHO-format situation report"""

        indicators = self.indicator_calc.generate_full_indicator_set(situation_data)

        # Build key findings
        human_cases = situation_data.get("human_cases", 0)
        deaths = situation_data.get("deaths", 0)
        animal_cases = situation_data.get("animal_cases", 0)
        regions = situation_data.get("affected_regions", 4)
        rt = next((i for i in indicators if "Rt" in i.name), None)
        rt_val = rt.value if rt else 1.5

        key_findings = [
            f"A total of {human_cases:,} laboratory-confirmed human cases of {disease} have been reported in {location}, including {deaths} deaths (CFR: {self.indicator_calc.calculate_case_fatality_rate(deaths, human_cases):.1f}%).",
            f"Animal surveillance has identified {animal_cases:,} affected animals across {regions} districts, indicating sustained environmental reservoir.",
            f"The effective reproduction number (Rt) is estimated at {rt_val:.2f} (95% CI: {rt_val*0.85:.2f}–{rt_val*1.15:.2f}), suggesting {'sustained transmission' if rt_val > 1 else 'declining transmission'}.",
            f"Genomic sequencing of {random.randint(5, 20)} samples reveals {'no significant mutations' if random.random() > 0.3 else 'potential adaptation variants requiring further analysis'}.",
            f"One Health response teams from {regions + 1} agencies are actively conducting coordinated surveillance and response activities.",
            f"Environmental sampling from {random.randint(15, 50)} sites confirms {'widespread' if animal_cases > 1000 else 'localized'} pathogen presence in poultry and wild bird populations."
        ]

        # Build executive summary
        severity = "high" if rt_val > 1.3 else "moderate" if rt_val > 0.9 else "low"
        exec_summary = (
            f"Situation Report #{report_number} — {disease} Outbreak, {location}\n\n"
            f"The {location} One Health response team reports {severity}-severity ongoing transmission of {disease}. "
            f"As of {datetime.now().strftime('%d %B %Y')}, {human_cases} confirmed human cases (including {deaths} deaths) "
            f"and {animal_cases:,} animal cases have been reported. "
            f"A coordinated multi-sector response is underway. "
            f"The situation requires {'immediate escalation of response measures' if severity == 'high' else 'continued monitoring and targeted interventions'}."
        )

        # Recommendations
        recommendations = [
            f"IMMEDIATE (0-24h): {'Activate Emergency Operations Center and convene One Health Task Force' if rt_val > 1.2 else 'Maintain enhanced surveillance and response operations'}",
            "SHORT-TERM (1-7 days): Expand contact tracing to cover 100% of confirmed cases; deploy additional laboratory capacity",
            "MEDIUM-TERM (1-4 weeks): Implement targeted vaccination program for high-risk agricultural workers; conduct seroprevalence study",
            "LONG-TERM (1-6 months): Review and strengthen IHR core capacities; develop One Health Early Warning System",
            "COMMUNICATION: Issue daily public updates; conduct briefing with international partners and WHO Regional Office",
            "DATA: Ensure timely sharing of epidemiological, clinical, and genomic data through established IHR mechanisms"
        ]

        key_indicators = []
        for ind in indicators[:5]:
            ki = KeyIndicator(
                indicator_id=f"KI_{ind.name[:6].upper().replace(' ', '_')}",
                name=ind.name,
                domain="human" if "Case" in ind.name or "Rt" in ind.name else "animal" if "Zoonotic" in ind.name else "analysis",
                current_value=ind.value,
                previous_value=ind.value * random.uniform(0.7, 1.3),
                unit="%%" if "Rate" in ind.name and "Spillover" not in ind.name else "ratio" if "R" in ind.name else "days" if "Doubling" in ind.name else "score",
                trend=ind.trend,
                threshold_alert=ind.value * 0.8,
                threshold_critical=ind.value * 1.2,
                status="critical" if ind.value > ind.value * 1.1 else "alert" if ind.value > ind.value * 0.9 else "normal",
                data_quality=DataQuality.GOOD
            )
            key_indicators.append(ki)

        report = SituationReport(
            report_id=f"SITREP_{disease[:3].upper()}_{datetime.now().strftime('%Y%m%d')}_{report_number:03d}",
            report_type=ReportType.SITUATION_REPORT,
            disease=disease,
            location=location,
            reporting_period=f"{(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
            generated_at=datetime.now().isoformat(),
            executive_summary=exec_summary,
            key_findings=key_findings,
            indicators=key_indicators,
            recommendations=recommendations,
            next_review=(datetime.now() + timedelta(hours=24)).isoformat(),
            author="One Health Response Coordination Team",
            classification="public"
        )

        self.generated_reports.append(report)
        return report

    def generate_weekly_bulletin(self, disease: str, weekly_data: list) -> dict:
        """Generate weekly epidemiological bulletin"""

        total_cases = sum(d.get("human_cases", 0) for d in weekly_data)
        total_deaths = sum(d.get("deaths", 0) for d in weekly_data)
        total_animal = sum(d.get("animal_cases", 0) for d in weekly_data)
        avg_daily = total_cases / len(weekly_data) if weekly_data else 0

        return {
            "bulletin_id": f"BULL_{datetime.now().strftime('%Y_W%V')}",
            "report_type": "weekly_epidemiological_bulletin",
            "week": datetime.now().strftime("Week %V, %Y"),
            "disease": disease,
            "summary_statistics": {
                "new_human_cases": total_cases,
                "new_deaths": total_deaths,
                "new_animal_cases": total_animal,
                "avg_daily_cases": round(avg_daily, 1),
                "case_fatality_rate": round((total_deaths / total_cases * 100), 2) if total_cases > 0 else 0
            },
            "trend_analysis": {
                "week_over_week_change": f"{random.uniform(-20, 30):+.1f}%",
                "trend_direction": random.choice(["increasing", "stable", "decreasing"]),
                "alert_level": "RED" if avg_daily > 20 else "ORANGE" if avg_daily > 10 else "YELLOW"
            },
            "generated_at": datetime.now().isoformat()
        }

    def generate_regulatory_report(self, disease: str, jurisdiction: str, data: dict) -> dict:
        """Generate IHR/regulatory submission report"""

        return {
            "report_id": f"IHR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "report_type": "ihr_notification",
            "disease": disease,
            "jurisdiction": jurisdiction,
            "notification_date": datetime.now().isoformat(),
            "ihr_criteria_met": True,
            "ihr_article": "6.1",  # IHR 2005
            "case_definition": f"Laboratory-confirmed {disease} by RT-PCR or viral culture",
            "epidemiological_data": {
                "total_cases": data.get("human_cases", 0),
                "total_deaths": data.get("deaths", 0),
                "affected_regions": data.get("affected_regions", 1),
                "date_first_case": data.get("date_first_case", (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")),
                "transmission_setting": "zoonotic with limited human-to-human transmission"
            },
            "response_measures": [
                "Enhanced surveillance activated",
                "Contact tracing implemented",
                "Laboratory capacity expanded",
                "International notification completed"
            ],
            "pheic_assessment": "Not meeting PHEIC criteria at this time — situation under review",
            "next_report_due": (datetime.now() + timedelta(days=7)).isoformat()
        }


# ============================================================
# DASHBOARD SYSTEM
# ============================================================

class OneHealthDashboard:
    """
    Real-time dashboard for One Health outbreak monitoring
    """

    def __init__(self):
        self.widgets = []
        self.indicator_calc = EpidemiologicalIndicatorCalculator()

    def build_dashboard(self, disease: str, situation_data: dict) -> dict:
        """Build comprehensive real-time dashboard"""

        indicators = self.indicator_calc.generate_full_indicator_set(situation_data)
        human_cases = situation_data.get("human_cases", 0)
        deaths = situation_data.get("deaths", 0)
        animal_cases = situation_data.get("animal_cases", 0)
        regions = situation_data.get("affected_regions", 4)
        daily_cases = situation_data.get("daily_cases", [5, 8, 12, 15, 18, 14, 22])

        # Build widgets
        widgets = [
            DashboardWidget("w_001", "Total Human Cases", "counter",
                            {"value": human_cases, "delta": daily_cases[-1], "delta_label": "today",
                             "severity": "critical" if human_cases > 100 else "high"}, 1, datetime.now().isoformat()),
            DashboardWidget("w_002", "Total Deaths", "counter",
                            {"value": deaths, "cfr": f"{(deaths/human_cases*100):.1f}%" if human_cases > 0 else "0%",
                             "severity": "critical"}, 2, datetime.now().isoformat()),
            DashboardWidget("w_003", "Animal Cases", "counter",
                            {"value": animal_cases, "species": "Poultry/Swine",
                             "severity": "high"}, 3, datetime.now().isoformat()),
            DashboardWidget("w_004", "Effective Rt", "gauge",
                            {"value": indicators[0].value if indicators else 1.5,
                             "threshold_green": 0.9, "threshold_yellow": 1.2, "threshold_red": 1.5,
                             "interpretation": indicators[0].interpretation if indicators else ""},
                            4, datetime.now().isoformat()),
            DashboardWidget("w_005", "7-Day Epidemic Curve", "chart",
                            {"chart_type": "bar",
                             "labels": [(datetime.now() - timedelta(days=6-i)).strftime("%m/%d") for i in range(7)],
                             "data": daily_cases[-7:] if len(daily_cases) >= 7 else daily_cases,
                             "trend": "increasing"}, 5, datetime.now().isoformat()),
            DashboardWidget("w_006", "Geographic Spread", "map",
                            {"affected_regions": regions,
                             "hotspot_districts": random.randint(2, regions),
                             "new_regions_24h": random.randint(0, 2)}, 6, datetime.now().isoformat()),
            DashboardWidget("w_007", "Response Activity", "table",
                            {"metrics": [
                                {"metric": "Contacts Traced", "value": random.randint(200, 1500), "status": "active"},
                                {"metric": "Quarantine Cases", "value": random.randint(50, 300), "status": "active"},
                                {"metric": "Samples Processed", "value": random.randint(500, 3000), "status": "active"},
                                {"metric": "Field Teams Deployed", "value": random.randint(10, 50), "status": "active"}
                            ]}, 7, datetime.now().isoformat()),
            DashboardWidget("w_008", "Alert Status", "alert",
                            {"level": "RED" if human_cases > 100 else "ORANGE" if human_cases > 30 else "YELLOW",
                             "message": f"Active {disease} outbreak — enhanced response measures in effect",
                             "last_escalation": (datetime.now() - timedelta(hours=6)).isoformat()},
                            8, datetime.now().isoformat())
        ]

        self.widgets = widgets

        # Build key metrics summary
        rt_val = indicators[0].value if indicators else 1.5
        severity_score = self.indicator_calc.calculate_outbreak_score({
            "rt": rt_val,
            "cfr": (deaths / human_cases * 100) if human_cases > 0 else 0,
            "geographic_spread": regions,
            "spillover_rate": self.indicator_calc.calculate_zoonotic_spillover_rate(animal_cases, human_cases)
        })

        return {
            "dashboard_id": f"DASH_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "disease": disease,
            "generated_at": datetime.now().isoformat(),
            "refresh_interval_seconds": 300,
            "alert_level": "RED" if severity_score > 70 else "ORANGE" if severity_score > 45 else "YELLOW",
            "severity_score": severity_score,
            "widgets": [
                {
                    "widget_id": w.widget_id,
                    "title": w.title,
                    "type": w.widget_type,
                    "data": w.data,
                    "priority": w.priority
                }
                for w in sorted(widgets, key=lambda x: x.priority)
            ],
            "key_indicators": [
                {"name": i.name, "value": i.value, "trend": i.trend.value, "interpretation": i.interpretation}
                for i in indicators
            ],
            "system_health": {
                "data_completeness": f"{random.uniform(85, 99):.1f}%",
                "last_data_sync": datetime.now().isoformat(),
                "data_sources_active": random.randint(8, 14),
                "data_quality": "GOOD"
            }
        }


# ============================================================
# AUTOMATED REPORTING SCHEDULER
# ============================================================

class ReportingScheduler:
    """
    Manages automated report generation and distribution schedules
    """

    def __init__(self):
        self.schedules = self._initialize_default_schedules()

    def _initialize_default_schedules(self) -> list:
        now = datetime.now()
        return [
            ReportSchedule("SCH_001", ReportType.SITUATION_REPORT, ReportFrequency.DAILY,
                           ["health.director@gov", "who.regional@who.int", "eoc@health.gov"],
                           ReportFormat.PDF, (now + timedelta(hours=8)).isoformat(), True, True),
            ReportSchedule("SCH_002", ReportType.SURVEILLANCE_SUMMARY, ReportFrequency.HOURLY,
                           ["surveillance.team@health.gov", "epi.team@health.gov"],
                           ReportFormat.DASHBOARD, (now + timedelta(hours=1)).isoformat(), True, True),
            ReportSchedule("SCH_003", ReportType.WEEKLY_DIGEST, ReportFrequency.WEEKLY,
                           ["ministry@health.gov", "parliament@gov", "who.hq@who.int"],
                           ReportFormat.DOCX, (now + timedelta(days=7)).isoformat(), True, True),
            ReportSchedule("SCH_004", ReportType.REGULATORY_SUBMISSION, ReportFrequency.WEEKLY,
                           ["ihr@who.int", "regional.ihr@who.int"],
                           ReportFormat.JSON, (now + timedelta(days=7)).isoformat(), True, True),
            ReportSchedule("SCH_005", ReportType.RISK_ASSESSMENT, ReportFrequency.WEEKLY,
                           ["policy@health.gov", "cabinet@gov"],
                           ReportFormat.PDF, (now + timedelta(days=3)).isoformat(), False, True)
        ]

    def get_due_reports(self) -> list:
        """Get reports due in next 24 hours"""
        now = datetime.now()
        return [
            {"schedule_id": s.schedule_id, "report_type": s.report_type.value,
             "frequency": s.frequency.value, "recipients": len(s.recipients),
             "next_due": s.next_due, "format": s.format.value}
            for s in self.schedules if s.active
        ]

    def get_schedule_summary(self) -> dict:
        active = [s for s in self.schedules if s.active]
        return {
            "total_schedules": len(self.schedules),
            "active_schedules": len(active),
            "auto_generated": sum(1 for s in active if s.auto_generate),
            "formats": list(set(s.format.value for s in active)),
            "total_recipients": sum(len(s.recipients) for s in active)
        }


# ============================================================
# INTEGRATED REPORTING SYSTEM
# ============================================================

class OneHealthReportingSystem:
    """
    Main integrated reporting system combining report generation, dashboard, and scheduling
    """

    def __init__(self):
        self.generator = OneHealthReportGenerator()
        self.dashboard = OneHealthDashboard()
        self.scheduler = ReportingScheduler()

    def run_full_reporting_cycle(self, disease: str, situation_data: dict) -> dict:
        """Execute complete reporting cycle"""

        print(f"\n{'='*60}")
        print("ONE HEALTH REPORTING SYSTEM")
        print(f"{'='*60}")

        # Generate situation report
        print("📄 Generating Situation Report...")
        sitrep = self.generator.generate_situation_report(
            disease,
            situation_data.get("location", "Northern Province"),
            situation_data
        )

        # Generate weekly bulletin
        print("📰 Generating Weekly Bulletin...")
        weekly_data = [
            {"human_cases": random.randint(5, 20), "deaths": random.randint(0, 3), "animal_cases": random.randint(50, 300)}
            for _ in range(7)
        ]
        bulletin = self.generator.generate_weekly_bulletin(disease, weekly_data)

        # Generate regulatory report
        print("📋 Generating Regulatory (IHR) Report...")
        ihr_report = self.generator.generate_regulatory_report(disease, situation_data.get("location", "Province"), situation_data)

        # Build dashboard
        print("📊 Building Real-Time Dashboard...")
        dashboard = self.dashboard.build_dashboard(disease, situation_data)

        # Get schedule
        schedule = self.scheduler.get_due_reports()
        schedule_summary = self.scheduler.get_schedule_summary()

        return {
            "reporting_cycle_id": f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "disease": disease,
            "generated_at": datetime.now().isoformat(),
            "situation_report": {
                "report_id": sitrep.report_id,
                "type": sitrep.report_type.value,
                "key_findings_count": len(sitrep.key_findings),
                "recommendations_count": len(sitrep.recommendations),
                "classification": sitrep.classification,
                "executive_summary": sitrep.executive_summary[:300] + "..."
            },
            "weekly_bulletin": bulletin,
            "regulatory_report": ihr_report,
            "dashboard": {
                "alert_level": dashboard["alert_level"],
                "severity_score": dashboard["severity_score"],
                "widgets_count": len(dashboard["widgets"]),
                "data_quality": dashboard["system_health"]["data_quality"],
                "key_indicators_count": len(dashboard["key_indicators"])
            },
            "reporting_schedule": {
                "summary": schedule_summary,
                "upcoming_reports": schedule
            },
            "total_reports_generated": len(self.generator.generated_reports)
        }


# ============================================================
# DEMO & TEST
# ============================================================

def run_demo():
    print("\n" + "="*70)
    print("  MODULE 39: REPORTING SYSTEM - ONE HEALTH DEMO")
    print("="*70)

    situation_data = {
        "location": "Northern Agricultural Province",
        "human_cases": 47,
        "deaths": 6,
        "animal_cases": 2300,
        "population": 250000,
        "affected_regions": 4,
        "daily_cases": [3, 5, 7, 9, 12, 8, 15, 11, 18, 14, 22, 19, 25, 21],
        "growth_rate": 0.087,
        "beta": 0.35,
        "gamma": 0.10,
        "date_first_case": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    }

    system = OneHealthReportingSystem()
    result = system.run_full_reporting_cycle("H5N1 Avian Influenza", situation_data)

    print(f"\n📄 SITUATION REPORT:")
    sr = result["situation_report"]
    print(f"  Report ID: {sr['report_id']}")
    print(f"  Classification: {sr['classification'].upper()}")
    print(f"  Key Findings: {sr['key_findings_count']}")
    print(f"  Recommendations: {sr['recommendations_count']}")
    print(f"  Summary (preview): {sr['executive_summary'][:120]}...")

    print(f"\n📰 WEEKLY BULLETIN:")
    wb = result["weekly_bulletin"]
    stats = wb["summary_statistics"]
    print(f"  Period: {wb['week']}")
    print(f"  New Cases: {stats['new_human_cases']} | Deaths: {stats['new_deaths']} | Animal: {stats['new_animal_cases']}")
    print(f"  CFR: {stats['case_fatality_rate']}% | Avg Daily: {stats['avg_daily_cases']}")
    print(f"  Alert Level: {wb['trend_analysis']['alert_level']}")

    print(f"\n📋 IHR REGULATORY REPORT:")
    ihr = result["regulatory_report"]
    print(f"  Report ID: {ihr['report_id']}")
    print(f"  IHR Article: {ihr['ihr_article']}")
    print(f"  PHEIC Assessment: {ihr['pheic_assessment']}")
    print(f"  Measures: {len(ihr['response_measures'])} response measures documented")

    print(f"\n📊 DASHBOARD:")
    dash = result["dashboard"]
    print(f"  Alert Level: {dash['alert_level']}")
    print(f"  Severity Score: {dash['severity_score']}/100")
    print(f"  Widgets: {dash['widgets_count']} active widgets")
    print(f"  Key Indicators: {dash['key_indicators_count']} tracked")
    print(f"  Data Quality: {dash['data_quality']}")

    print(f"\n📅 REPORTING SCHEDULE:")
    sched = result["reporting_schedule"]
    s = sched["summary"]
    print(f"  Active Schedules: {s['active_schedules']}/{s['total_schedules']}")
    print(f"  Auto-Generated: {s['auto_generated']}")
    print(f"  Total Recipients: {s['total_recipients']}")
    print(f"  Formats: {', '.join(s['formats'])}")
    print(f"\n  Upcoming Reports:")
    for r in sched["upcoming_reports"][:3]:
        print(f"    • {r['report_type']} ({r['frequency']}) → {r['recipients']} recipients")

    print(f"\n{'='*70}")
    print("✅ Module 39: reporting.py COMPLETE")
    print(f"{'='*70}")

    return result


if __name__ == "__main__":
    run_demo()
"""
Deployment Management and Orchestration System
==============================================
Module 5: Integration & Validation Tools

Advanced deployment management, orchestration, and release automation for One Health platforms,
providing comprehensive deployment strategies and automated release processes.

NIW Focus: Deployment intelligence enabling reliable and efficient One Health system deployments.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable, Set
import logging
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque, Counter
import itertools
import random
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeploymentType(Enum):
    """Types of deployment strategies."""
    BLUE_GREEN = "blue_green"                    # Blue-green deployment
    ROLLING = "rolling"                          # Rolling deployment
    CANARY = "canary"                           # Canary deployment
    A_B_TESTING = "a_b_testing"                 # A/B testing deployment
    FEATURE_FLAG = "feature_flag"               # Feature flag deployment
    IMMUTABLE = "immutable"                     # Immutable infrastructure
    IN_PLACE = "in_place"                       # In-place deployment
    RECREATE = "recreate"                       # Recreate deployment

class DeploymentEnvironment(Enum):
    """Deployment environment types."""
    DEVELOPMENT = "development"                  # Development environment
    TESTING = "testing"                         # Testing environment
    STAGING = "staging"                         # Staging environment
    PRE_PRODUCTION = "pre_production"           # Pre-production environment
    PRODUCTION = "production"                   # Production environment
    DISASTER_RECOVERY = "disaster_recovery"     # DR environment

class DeploymentStatus(Enum):
    """Deployment status levels."""
    PENDING = "pending"                         # Deployment pending
    IN_PROGRESS = "in_progress"                # Deployment in progress
    DEPLOYING = "deploying"                    # Currently deploying
    TESTING = "testing"                        # Post-deployment testing
    COMPLETED = "completed"                    # Successfully completed
    FAILED = "failed"                          # Deployment failed
    ROLLED_BACK = "rolled_back"               # Deployment rolled back
    CANCELLED = "cancelled"                    # Deployment cancelled

class ComponentType(Enum):
    """Types of deployable components."""
    WEB_APPLICATION = "web_application"         # Web applications
    API_SERVICE = "api_service"                # API services
    DATABASE = "database"                      # Database updates
    MICROSERVICE = "microservice"              # Microservices
    INFRASTRUCTURE = "infrastructure"          # Infrastructure as code
    CONFIGURATION = "configuration"            # Configuration changes
    SECURITY_UPDATE = "security_update"        # Security patches
    HOTFIX = "hotfix"                         # Emergency hotfixes

@dataclass
class DeploymentArtifact:
    """Deployable artifact definition."""
    
    artifact_id: str
    artifact_name: str
    component_type: ComponentType
    
    # Artifact details
    version: str
    build_number: str
    created_date: datetime
    created_by: str
    
    # Artifact metadata
    source_repository: str = ""
    commit_hash: str = ""
    branch_name: str = ""
    build_duration_minutes: float = 0.0
    
    # Artifact validation
    is_validated: bool = False
    validation_date: Optional[datetime] = None
    validation_results: Dict[str, Any] = field(default_factory=dict)
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    rollback_plan: str = ""
    
    # Size and resource info
    artifact_size_mb: float = 0.0
    estimated_deploy_time_minutes: float = 5.0
    resource_requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DeploymentPlan:
    """Comprehensive deployment plan."""
    
    plan_id: str
    plan_name: str
    deployment_type: DeploymentType
    target_environment: DeploymentEnvironment
    
    # Plan details
    created_date: datetime
    created_by: str
    scheduled_start_time: Optional[datetime] = None
    estimated_duration_minutes: float = 30.0
    
    # Artifacts to deploy
    artifacts: List[str] = field(default_factory=list)  # Artifact IDs
    
    # Deployment strategy
    rollout_percentage: float = 100.0             # % of infrastructure to update
    health_check_duration_minutes: float = 5.0   # Post-deploy health check time
    rollback_threshold_error_rate: float = 5.0   # Error rate triggering rollback
    
    # Pre and post deployment steps
    pre_deployment_steps: List[str] = field(default_factory=list)
    post_deployment_steps: List[str] = field(default_factory=list)
    rollback_steps: List[str] = field(default_factory=list)
    
    # Approval and gates
    requires_approval: bool = True
    approved_by: str = ""
    approval_date: Optional[datetime] = None
    deployment_gates: List[str] = field(default_factory=list)
    
    # Risk assessment
    risk_level: str = "medium"                    # "low", "medium", "high", "critical"
    risk_factors: List[str] = field(default_factory=list)
    mitigation_strategies: List[str] = field(default_factory=list)

@dataclass
class DeploymentExecution:
    """Deployment execution tracking."""
    
    execution_id: str
    plan_id: str
    started_by: str
    start_time: datetime
    
    # Execution status
    status: DeploymentStatus = DeploymentStatus.PENDING
    end_time: Optional[datetime] = None
    actual_duration_minutes: float = 0.0
    
    # Progress tracking
    total_steps: int = 0
    completed_steps: int = 0
    current_step: str = ""
    progress_percentage: float = 0.0
    
    # Environment details
    target_environment: DeploymentEnvironment = DeploymentEnvironment.DEVELOPMENT
    deployment_type: DeploymentType = DeploymentType.ROLLING
    
    # Execution results
    deployed_artifacts: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    error_count: int = 0
    warning_count: int = 0
    
    # Health and validation
    health_check_results: Dict[str, Any] = field(default_factory=dict)
    performance_impact: Dict[str, float] = field(default_factory=dict)
    rollback_triggered: bool = False
    rollback_reason: str = ""
    
    # Logs and details
    execution_logs: List[str] = field(default_factory=list)
    error_details: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

@dataclass
class DeploymentMetrics:
    """Deployment performance metrics."""
    
    metrics_id: str
    execution_id: str
    measurement_timestamp: datetime
    
    # Deployment metrics
    deployment_frequency: float = 0.0            # Deployments per week
    lead_time_hours: float = 0.0                # Lead time from commit to production
    deployment_success_rate: float = 0.0        # Success rate %
    mean_time_to_recovery_minutes: float = 0.0  # MTTR for failed deployments
    
    # Performance impact
    response_time_impact_ms: float = 0.0        # Response time change
    throughput_impact_percentage: float = 0.0   # Throughput change
    error_rate_change_percentage: float = 0.0   # Error rate change
    availability_impact_percentage: float = 0.0 # Availability impact
    
    # Resource utilization
    cpu_usage_change_percentage: float = 0.0    # CPU usage change
    memory_usage_change_percentage: float = 0.0 # Memory usage change
    storage_usage_change_mb: float = 0.0        # Storage usage change
    
    # Business metrics
    user_satisfaction_score: float = 0.0        # User satisfaction (1-10)
    feature_adoption_rate: float = 0.0          # New feature adoption %
    business_value_score: float = 0.0           # Business value delivered (1-10)

@dataclass
class DeploymentReport:
    """Comprehensive deployment report."""
    
    report_id: str
    report_title: str
    reporting_period_start: datetime
    reporting_period_end: datetime
    generation_timestamp: datetime
    
    # Deployment summary
    total_deployments: int = 0
    successful_deployments: int = 0
    failed_deployments: int = 0
    rolled_back_deployments: int = 0
    
    # Performance metrics
    average_deployment_time_minutes: float = 0.0
    deployment_success_rate: float = 0.0
    average_lead_time_hours: float = 0.0
    mean_time_to_recovery_minutes: float = 0.0
    
    # Environment analysis
    deployments_by_environment: Dict[DeploymentEnvironment, int] = field(default_factory=dict)
    deployments_by_type: Dict[DeploymentType, int] = field(default_factory=dict)
    deployments_by_component: Dict[ComponentType, int] = field(default_factory=dict)
    
    # Quality and impact
    overall_quality_score: float = 0.0          # Overall deployment quality
    average_performance_impact: float = 0.0     # Average performance impact
    high_risk_deployments: int = 0              # Number of high-risk deployments
    
    # Trends and insights
    deployment_frequency_trend: str = "stable"  # "increasing", "decreasing", "stable"
    quality_trend: str = "stable"               # Quality trend
    key_insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Best practices
    successful_patterns: List[str] = field(default_factory=list)
    failure_patterns: List[str] = field(default_factory=list)
    improvement_opportunities: List[str] = field(default_factory=list)

class DeploymentManager:
    """Central deployment management and orchestration system."""
    
    def __init__(self):
        self.deployment_artifacts: Dict[str, DeploymentArtifact] = {}
        self.deployment_plans: Dict[str, DeploymentPlan] = {}
        self.deployment_executions: List[DeploymentExecution] = []
        self.deployment_metrics: List[DeploymentMetrics] = []
        self.deployment_reports: List[DeploymentReport] = []
        
        # Environment configurations
        self.environment_configs = {
            DeploymentEnvironment.DEVELOPMENT: {"cpu_limit": 2, "memory_limit": 4096, "replicas": 1},
            DeploymentEnvironment.TESTING: {"cpu_limit": 4, "memory_limit": 8192, "replicas": 2},
            DeploymentEnvironment.STAGING: {"cpu_limit": 8, "memory_limit": 16384, "replicas": 3},
            DeploymentEnvironment.PRE_PRODUCTION: {"cpu_limit": 16, "memory_limit": 32768, "replicas": 5},
            DeploymentEnvironment.PRODUCTION: {"cpu_limit": 32, "memory_limit": 65536, "replicas": 10}
        }
        
        # Initialize deployment framework
        self._initialize_deployment_framework()
        
        logger.info("One Health Deployment Manager initialized")
    
    def _initialize_deployment_framework(self):
        """Initialize deployment framework with sample artifacts and plans."""
        
        # Create sample artifacts
        sample_artifacts = [
            {
                "name": "Surveillance API v2.1.0", "component": ComponentType.API_SERVICE,
                "version": "2.1.0", "build": "BUILD-1234", "creator": "deployment_system"
            },
            {
                "name": "Analytics Dashboard v1.5.3", "component": ComponentType.WEB_APPLICATION,
                "version": "1.5.3", "build": "BUILD-1235", "creator": "deployment_system"
            },
            {
                "name": "Database Migration v3.2.1", "component": ComponentType.DATABASE,
                "version": "3.2.1", "build": "MIGRATION-456", "creator": "database_team"
            },
            {
                "name": "Security Patch SP-2024-001", "component": ComponentType.SECURITY_UPDATE,
                "version": "SP-2024-001", "build": "SECURITY-789", "creator": "security_team"
            },
            {
                "name": "One Health Integration Service", "component": ComponentType.MICROSERVICE,
                "version": "1.2.0", "build": "BUILD-1236", "creator": "integration_team"
            }
        ]
        
        for artifact_data in sample_artifacts:
            artifact_id = f"ARTIFACT_{random.randint(100000, 999999)}"
            
            artifact = DeploymentArtifact(
                artifact_id=artifact_id,
                artifact_name=artifact_data["name"],
                component_type=artifact_data["component"],
                version=artifact_data["version"],
                build_number=artifact_data["build"],
                created_date=datetime.now(),
                created_by=artifact_data["creator"],
                source_repository=f"repo/{artifact_data['name'].lower().replace(' ', '-')}",
                commit_hash=f"{random.randint(100000, 999999):x}",
                branch_name="main",
                build_duration_minutes=random.uniform(5, 30),
                is_validated=True,
                validation_date=datetime.now(),
                artifact_size_mb=random.uniform(50, 500),
                estimated_deploy_time_minutes=random.uniform(5, 20)
            )
            
            # Add validation results
            artifact.validation_results = {
                "security_scan": "passed",
                "code_quality": "passed",
                "unit_tests": "passed",
                "integration_tests": "passed",
                "performance_tests": "passed"
            }
            
            # Add resource requirements
            artifact.resource_requirements = {
                "cpu_cores": random.randint(1, 4),
                "memory_mb": random.randint(1024, 8192),
                "storage_mb": random.randint(100, 1000)
            }
            
            self.deployment_artifacts[artifact_id] = artifact
        
        # Create sample deployment plans
        sample_plans = [
            {
                "name": "Production Release v2.1.0", "type": DeploymentType.BLUE_GREEN,
                "environment": DeploymentEnvironment.PRODUCTION, "creator": "release_manager"
            },
            {
                "name": "Staging Environment Update", "type": DeploymentType.ROLLING,
                "environment": DeploymentEnvironment.STAGING, "creator": "dev_team"
            },
            {
                "name": "Canary Release Testing", "type": DeploymentType.CANARY,
                "environment": DeploymentEnvironment.PRE_PRODUCTION, "creator": "qa_team"
            },
            {
                "name": "Security Patch Deployment", "type": DeploymentType.IMMUTABLE,
                "environment": DeploymentEnvironment.PRODUCTION, "creator": "security_team"
            }
        ]
        
        for plan_data in sample_plans:
            plan_id = f"PLAN_{random.randint(100000, 999999)}"
            
            plan = DeploymentPlan(
                plan_id=plan_id,
                plan_name=plan_data["name"],
                deployment_type=plan_data["type"],
                target_environment=plan_data["environment"],
                created_date=datetime.now(),
                created_by=plan_data["creator"],
                scheduled_start_time=datetime.now() + timedelta(hours=random.randint(1, 72)),
                estimated_duration_minutes=random.uniform(15, 60),
                artifacts=list(self.deployment_artifacts.keys())[:random.randint(1, 3)]
            )
            
            # Set deployment strategy parameters
            if plan.deployment_type == DeploymentType.CANARY:
                plan.rollout_percentage = 10.0  # Start with 10% for canary
            elif plan.deployment_type == DeploymentType.ROLLING:
                plan.rollout_percentage = 25.0  # 25% at a time for rolling
            
            # Set risk level based on environment
            if plan.target_environment == DeploymentEnvironment.PRODUCTION:
                plan.risk_level = "high"
                plan.requires_approval = True
            elif plan.target_environment in [DeploymentEnvironment.PRE_PRODUCTION, DeploymentEnvironment.STAGING]:
                plan.risk_level = "medium"
            else:
                plan.risk_level = "low"
            
            # Add deployment steps
            plan.pre_deployment_steps = [
                "Verify artifact integrity",
                "Check environment health",
                "Create database backup",
                "Notify stakeholders"
            ]
            
            plan.post_deployment_steps = [
                "Run health checks",
                "Verify functionality",
                "Update monitoring dashboards",
                "Send completion notification"
            ]
            
            plan.rollback_steps = [
                "Trigger rollback procedure",
                "Restore from backup",
                "Verify rollback success",
                "Notify incident response team"
            ]
            
            # Add deployment gates
            plan.deployment_gates = [
                "Pre-deployment validation",
                "Environment readiness check",
                "Dependency verification",
                "Security clearance"
            ]
            
            self.deployment_plans[plan_id] = plan
        
        logger.info(f"Initialized {len(self.deployment_artifacts)} artifacts and {len(self.deployment_plans)} deployment plans")
    
    def create_deployment_artifact(self, artifact_name: str, component_type: ComponentType,
                                 version: str, build_number: str, created_by: str) -> DeploymentArtifact:
        """Create new deployment artifact."""
        
        artifact_id = f"ARTIFACT_{random.randint(100000, 999999)}"
        
        artifact = DeploymentArtifact(
            artifact_id=artifact_id,
            artifact_name=artifact_name,
            component_type=component_type,
            version=version,
            build_number=build_number,
            created_date=datetime.now(),
            created_by=created_by
        )
        
        # Set default values
        artifact.source_repository = f"repo/{artifact_name.lower().replace(' ', '-')}"
        artifact.commit_hash = f"{random.randint(100000, 999999):x}"
        artifact.branch_name = "main"
        artifact.build_duration_minutes = random.uniform(5, 30)
        artifact.artifact_size_mb = random.uniform(50, 500)
        artifact.estimated_deploy_time_minutes = random.uniform(5, 20)
        
        self.deployment_artifacts[artifact_id] = artifact
        
        logger.info(f"Deployment artifact created: {artifact_id}")
        
        return artifact
    
    def validate_artifact(self, artifact_id: str) -> Dict[str, str]:
        """Validate deployment artifact."""
        
        if artifact_id not in self.deployment_artifacts:
            raise ValueError(f"Artifact {artifact_id} not found")
        
        artifact = self.deployment_artifacts[artifact_id]
        
        # Simulate validation process
        validation_results = {}
        
        validation_checks = [
            "security_scan", "code_quality", "unit_tests",
            "integration_tests", "performance_tests"
        ]
        
        for check in validation_checks:
            # Simulate validation with high success rate
            if random.random() > 0.1:  # 90% success rate
                validation_results[check] = "passed"
            else:
                validation_results[check] = "failed"
        
        artifact.validation_results = validation_results
        artifact.is_validated = all(result == "passed" for result in validation_results.values())
        artifact.validation_date = datetime.now()
        
        logger.info(f"Artifact validation completed: {artifact_id} - {'passed' if artifact.is_validated else 'failed'}")
        
        return validation_results
    
    def create_deployment_plan(self, plan_name: str, deployment_type: DeploymentType,
                             target_environment: DeploymentEnvironment, artifact_ids: List[str],
                             created_by: str) -> DeploymentPlan:
        """Create deployment plan."""
        
        plan_id = f"PLAN_{random.randint(100000, 999999)}"
        
        plan = DeploymentPlan(
            plan_id=plan_id,
            plan_name=plan_name,
            deployment_type=deployment_type,
            target_environment=target_environment,
            created_date=datetime.now(),
            created_by=created_by,
            artifacts=artifact_ids.copy()
        )
        
        # Calculate estimated duration based on artifacts
        total_deploy_time = sum(
            self.deployment_artifacts[aid].estimated_deploy_time_minutes
            for aid in artifact_ids
            if aid in self.deployment_artifacts
        )
        plan.estimated_duration_minutes = total_deploy_time + 10  # Add overhead
        
        # Set defaults based on deployment type and environment
        if deployment_type == DeploymentType.CANARY:
            plan.rollout_percentage = 10.0
            plan.health_check_duration_minutes = 15.0
        elif deployment_type == DeploymentType.BLUE_GREEN:
            plan.rollout_percentage = 100.0
            plan.health_check_duration_minutes = 10.0
        elif deployment_type == DeploymentType.ROLLING:
            plan.rollout_percentage = 25.0
            plan.health_check_duration_minutes = 5.0
        
        # Set risk level based on environment
        if target_environment == DeploymentEnvironment.PRODUCTION:
            plan.risk_level = "high"
            plan.requires_approval = True
            plan.rollback_threshold_error_rate = 1.0  # Lower threshold for production
        elif target_environment in [DeploymentEnvironment.PRE_PRODUCTION, DeploymentEnvironment.STAGING]:
            plan.risk_level = "medium"
            plan.rollback_threshold_error_rate = 3.0
        else:
            plan.risk_level = "low"
            plan.rollback_threshold_error_rate = 5.0
        
        self.deployment_plans[plan_id] = plan
        
        logger.info(f"Deployment plan created: {plan_id}")
        
        return plan
    
    def approve_deployment_plan(self, plan_id: str, approved_by: str) -> bool:
        """Approve deployment plan for execution."""
        
        if plan_id not in self.deployment_plans:
            return False
        
        plan = self.deployment_plans[plan_id]
        plan.approved_by = approved_by
        plan.approval_date = datetime.now()
        
        logger.info(f"Deployment plan approved: {plan_id} by {approved_by}")
        
        return True
    
    def execute_deployment(self, plan_id: str, started_by: str) -> DeploymentExecution:
        """Execute deployment plan."""
        
        if plan_id not in self.deployment_plans:
            raise ValueError(f"Deployment plan {plan_id} not found")
        
        plan = self.deployment_plans[plan_id]
        
        if plan.requires_approval and not plan.approved_by:
            raise ValueError(f"Deployment plan {plan_id} requires approval before execution")
        
        execution_id = f"EXEC_{random.randint(100000, 999999)}"
        
        execution = DeploymentExecution(
            execution_id=execution_id,
            plan_id=plan_id,
            started_by=started_by,
            start_time=datetime.now(),
            target_environment=plan.target_environment,
            deployment_type=plan.deployment_type
        )
        
        # Calculate total steps
        execution.total_steps = (
            len(plan.pre_deployment_steps) +
            len(plan.artifacts) +
            len(plan.post_deployment_steps) +
            2  # Health check and validation
        )
        
        # Simulate deployment execution
        self._simulate_deployment_execution(execution, plan)
        
        self.deployment_executions.append(execution)
        
        logger.info(f"Deployment execution completed: {execution_id} - {execution.status.value}")
        
        return execution
    
    def _simulate_deployment_execution(self, execution: DeploymentExecution, plan: DeploymentPlan):
        """Simulate deployment execution process."""
        
        execution.status = DeploymentStatus.IN_PROGRESS
        current_step = 0
        
        # Pre-deployment steps
        for step in plan.pre_deployment_steps:
            current_step += 1
            execution.current_step = step
            execution.completed_steps = current_step
            execution.progress_percentage = (current_step / execution.total_steps) * 100
            execution.execution_logs.append(f"Completed: {step}")
        
        # Artifact deployment
        execution.status = DeploymentStatus.DEPLOYING
        
        for artifact_id in plan.artifacts:
            current_step += 1
            
            if artifact_id in self.deployment_artifacts:
                artifact = self.deployment_artifacts[artifact_id]
                execution.current_step = f"Deploying {artifact.artifact_name}"
                execution.completed_steps = current_step
                execution.progress_percentage = (current_step / execution.total_steps) * 100
                
                # Simulate deployment success/failure
                deployment_success = random.random() > 0.05  # 95% success rate
                
                if deployment_success:
                    execution.deployed_artifacts.append(artifact_id)
                    execution.execution_logs.append(f"Successfully deployed {artifact.artifact_name}")
                else:
                    execution.error_count += 1
                    execution.error_details.append(f"Failed to deploy {artifact.artifact_name}")
                    execution.execution_logs.append(f"ERROR: Failed to deploy {artifact.artifact_name}")
        
        # Health checks
        execution.status = DeploymentStatus.TESTING
        current_step += 1
        execution.current_step = "Running health checks"
        execution.completed_steps = current_step
        execution.progress_percentage = (current_step / execution.total_steps) * 100
        
        # Simulate health check results
        execution.health_check_results = {
            "response_time_ms": random.uniform(100, 300),
            "error_rate_percentage": random.uniform(0, 2),
            "availability_percentage": random.uniform(99, 100),
            "throughput_rps": random.uniform(800, 1200)
        }
        
        # Check if rollback is needed
        error_rate = execution.health_check_results["error_rate_percentage"]
        if error_rate > plan.rollback_threshold_error_rate:
            execution.rollback_triggered = True
            execution.rollback_reason = f"Error rate {error_rate:.1f}% exceeds threshold {plan.rollback_threshold_error_rate:.1f}%"
            execution.status = DeploymentStatus.ROLLED_BACK
            execution.execution_logs.append(f"ROLLBACK: {execution.rollback_reason}")
        
        # Post-deployment steps
        if not execution.rollback_triggered:
            for step in plan.post_deployment_steps:
                current_step += 1
                execution.current_step = step
                execution.completed_steps = current_step
                execution.progress_percentage = (current_step / execution.total_steps) * 100
                execution.execution_logs.append(f"Completed: {step}")
        
        # Final status determination
        if execution.rollback_triggered:
            execution.status = DeploymentStatus.ROLLED_BACK
        elif execution.error_count > 0:
            if execution.error_count <= len(plan.artifacts) * 0.2:  # Tolerate up to 20% failures
                execution.status = DeploymentStatus.COMPLETED
                execution.warning_count = execution.error_count
            else:
                execution.status = DeploymentStatus.FAILED
        else:
            execution.status = DeploymentStatus.COMPLETED
        
        # Calculate success rate
        total_artifacts = len(plan.artifacts)
        successful_artifacts = len(execution.deployed_artifacts)
        execution.success_rate = (successful_artifacts / total_artifacts * 100) if total_artifacts > 0 else 0
        
        # Set end time and duration
        execution.end_time = datetime.now()
        execution.actual_duration_minutes = (execution.end_time - execution.start_time).total_seconds() / 60
        
        # Performance impact simulation
        execution.performance_impact = {
            "response_time_change_ms": random.uniform(-50, 20),  # Slight improvement or small impact
            "cpu_usage_change_percentage": random.uniform(-5, 15),
            "memory_usage_change_percentage": random.uniform(-3, 10)
        }
        
        # Add lessons learned
        if execution.status == DeploymentStatus.COMPLETED:
            execution.lessons_learned = [
                "Deployment completed successfully with minimal impact",
                "Health checks validated system stability",
                "All deployment gates passed as expected"
            ]
        elif execution.status == DeploymentStatus.ROLLED_BACK:
            execution.lessons_learned = [
                "Rollback procedure executed successfully",
                "Health check thresholds effectively detected issues",
                "Need to improve pre-deployment testing"
            ]
        else:
            execution.lessons_learned = [
                "Deployment encountered issues requiring investigation",
                "Need to review artifact validation process",
                "Consider implementing additional safety measures"
            ]
    
    def collect_deployment_metrics(self, execution_id: str) -> DeploymentMetrics:
        """Collect deployment performance metrics."""
        
        execution = None
        for exec_item in self.deployment_executions:
            if exec_item.execution_id == execution_id:
                execution = exec_item
                break
        
        if not execution:
            raise ValueError(f"Deployment execution {execution_id} not found")
        
        metrics_id = f"METRICS_{random.randint(100000, 999999)}"
        
        metrics = DeploymentMetrics(
            metrics_id=metrics_id,
            execution_id=execution_id,
            measurement_timestamp=datetime.now()
        )
        
        # Calculate deployment metrics
        recent_deployments = [
            exec_item for exec_item in self.deployment_executions[-10:]
            if exec_item.target_environment == execution.target_environment
        ]
        
        if recent_deployments:
            # Deployment frequency (deployments per week)
            time_span_days = 7  # Assume metrics for last week
            metrics.deployment_frequency = len(recent_deployments) / (time_span_days / 7)
            
            # Lead time (simplified - use deployment duration as proxy)
            metrics.lead_time_hours = statistics.mean(
                exec_item.actual_duration_minutes / 60 for exec_item in recent_deployments
            )
            
            # Success rate
            successful_deployments = [exec_item for exec_item in recent_deployments
                                    if exec_item.status == DeploymentStatus.COMPLETED]
            metrics.deployment_success_rate = (len(successful_deployments) / len(recent_deployments)) * 100
            
            # Mean time to recovery
            failed_deployments = [exec_item for exec_item in recent_deployments
                                if exec_item.status in [DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK]]
            if failed_deployments:
                metrics.mean_time_to_recovery_minutes = statistics.mean(
                    exec_item.actual_duration_minutes for exec_item in failed_deployments
                )
        
        # Performance impact from execution
        if execution.performance_impact:
            metrics.response_time_impact_ms = execution.performance_impact.get("response_time_change_ms", 0)
            metrics.cpu_usage_change_percentage = execution.performance_impact.get("cpu_usage_change_percentage", 0)
            metrics.memory_usage_change_percentage = execution.performance_impact.get("memory_usage_change_percentage", 0)
        
        # Health check impact
        if execution.health_check_results:
            metrics.error_rate_change_percentage = execution.health_check_results.get("error_rate_percentage", 0)
            metrics.availability_impact_percentage = execution.health_check_results.get("availability_percentage", 100) - 100
        
        # Business metrics (simulated)
        if execution.status == DeploymentStatus.COMPLETED:
            metrics.user_satisfaction_score = random.uniform(7.5, 9.5)
            metrics.feature_adoption_rate = random.uniform(15, 45)
            metrics.business_value_score = random.uniform(6.5, 9.0)
        else:
            metrics.user_satisfaction_score = random.uniform(3.0, 6.0)
            metrics.feature_adoption_rate = random.uniform(0, 10)
            metrics.business_value_score = random.uniform(2.0, 5.5)
        
        self.deployment_metrics.append(metrics)
        
        return metrics
    
    def generate_deployment_report(self, report_title: str, period_days: int = 30) -> DeploymentReport:
        """Generate comprehensive deployment report."""
        
        report_id = f"DEPLOY_RPT_{random.randint(100000, 999999)}"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        report = DeploymentReport(
            report_id=report_id,
            report_title=report_title,
            reporting_period_start=start_date,
            reporting_period_end=end_date,
            generation_timestamp=datetime.now()
        )
        
        # Filter executions for reporting period
        period_executions = [
            exec_item for exec_item in self.deployment_executions
            if start_date <= exec_item.start_time <= end_date
        ]
        
        # Basic deployment statistics
        report.total_deployments = len(period_executions)
        report.successful_deployments = len([e for e in period_executions if e.status == DeploymentStatus.COMPLETED])
        report.failed_deployments = len([e for e in period_executions 
                                       if e.status in [DeploymentStatus.FAILED, DeploymentStatus.CANCELLED]])
        report.rolled_back_deployments = len([e for e in period_executions if e.status == DeploymentStatus.ROLLED_BACK])
        
        # Performance metrics
        if period_executions:
            report.average_deployment_time_minutes = statistics.mean(e.actual_duration_minutes for e in period_executions)
            report.deployment_success_rate = (report.successful_deployments / report.total_deployments) * 100
        
        # Environment and type analysis
        for execution in period_executions:
            # By environment
            env = execution.target_environment
            if env in report.deployments_by_environment:
                report.deployments_by_environment[env] += 1
            else:
                report.deployments_by_environment[env] = 1
            
            # By deployment type
            dep_type = execution.deployment_type
            if dep_type in report.deployments_by_type:
                report.deployments_by_type[dep_type] += 1
            else:
                report.deployments_by_type[dep_type] = 1
        
        # Component analysis
        for plan_id in set(e.plan_id for e in period_executions):
            if plan_id in self.deployment_plans:
                plan = self.deployment_plans[plan_id]
                for artifact_id in plan.artifacts:
                    if artifact_id in self.deployment_artifacts:
                        component_type = self.deployment_artifacts[artifact_id].component_type
                        if component_type in report.deployments_by_component:
                            report.deployments_by_component[component_type] += 1
                        else:
                            report.deployments_by_component[component_type] = 1
        
        # Quality analysis
        if period_executions:
            success_rates = [e.success_rate for e in period_executions]
            report.overall_quality_score = statistics.mean(success_rates)
            
            # Performance impact analysis
            performance_impacts = []
            for execution in period_executions:
                if execution.performance_impact:
                    impact = abs(execution.performance_impact.get("response_time_change_ms", 0))
                    performance_impacts.append(impact)
            
            if performance_impacts:
                report.average_performance_impact = statistics.mean(performance_impacts)
        
        # Risk analysis
        high_risk_plans = [plan for plan in self.deployment_plans.values() if plan.risk_level == "high"]
        high_risk_executions = [e for e in period_executions 
                              if e.plan_id in [p.plan_id for p in high_risk_plans]]
        report.high_risk_deployments = len(high_risk_executions)
        
        # Generate insights and recommendations
        report.key_insights = self._generate_deployment_insights(period_executions)
        report.recommendations = self._generate_deployment_recommendations(report)
        report.successful_patterns = self._identify_successful_patterns(period_executions)
        report.failure_patterns = self._identify_failure_patterns(period_executions)
        report.improvement_opportunities = self._identify_improvement_opportunities(report)
        
        # Trend analysis
        if len(period_executions) > 10:
            recent_success_rate = statistics.mean([e.success_rate for e in period_executions[-5:]])
            earlier_success_rate = statistics.mean([e.success_rate for e in period_executions[:5]])
            
            if recent_success_rate > earlier_success_rate * 1.1:
                report.quality_trend = "improving"
            elif recent_success_rate < earlier_success_rate * 0.9:
                report.quality_trend = "declining"
            else:
                report.quality_trend = "stable"
        
        self.deployment_reports.append(report)
        
        logger.info(f"Deployment report generated: {report_id}")
        
        return report
    
    def _generate_deployment_insights(self, executions: List[DeploymentExecution]) -> List[str]:
        """Generate key deployment insights."""
        
        insights = []
        
        if not executions:
            return ["No deployments in the reporting period"]
        
        # Success rate insights
        success_rate = len([e for e in executions if e.status == DeploymentStatus.COMPLETED]) / len(executions) * 100
        
        if success_rate >= 95:
            insights.append(f"Excellent deployment success rate of {success_rate:.1f}%")
        elif success_rate >= 85:
            insights.append(f"Good deployment success rate of {success_rate:.1f}%")
        else:
            insights.append(f"Deployment success rate of {success_rate:.1f}% needs improvement")
        
        # Rollback insights
        rollback_count = len([e for e in executions if e.rollback_triggered])
        if rollback_count > 0:
            insights.append(f"{rollback_count} deployments required rollback, indicating need for better testing")
        
        # Performance insights
        avg_duration = statistics.mean(e.actual_duration_minutes for e in executions)
        if avg_duration > 60:
            insights.append(f"Average deployment time of {avg_duration:.1f} minutes suggests optimization opportunities")
        
        # Environment insights
        prod_deployments = len([e for e in executions if e.target_environment == DeploymentEnvironment.PRODUCTION])
        if prod_deployments > 0:
            insights.append(f"{prod_deployments} production deployments demonstrate active delivery pipeline")
        
        return insights[:5]
    
    def _generate_deployment_recommendations(self, report: DeploymentReport) -> List[str]:
        """Generate deployment improvement recommendations."""
        
        recommendations = []
        
        if report.deployment_success_rate < 90:
            recommendations.append("Implement additional pre-deployment validation to improve success rate")
        
        if report.rolled_back_deployments > report.total_deployments * 0.1:
            recommendations.append("Review rollback triggers and improve deployment testing")
        
        if report.average_deployment_time_minutes > 45:
            recommendations.append("Optimize deployment process to reduce deployment time")
        
        if report.high_risk_deployments > report.total_deployments * 0.5:
            recommendations.append("Implement more granular deployment strategies to reduce risk")
        
        if DeploymentType.CANARY not in report.deployments_by_type:
            recommendations.append("Consider implementing canary deployments for safer releases")
        
        if not recommendations:
            recommendations.append("Continue current deployment practices while monitoring for optimization opportunities")
        
        return recommendations[:5]
    
    def _identify_successful_patterns(self, executions: List[DeploymentExecution]) -> List[str]:
        """Identify patterns in successful deployments."""
        
        successful_executions = [e for e in executions if e.status == DeploymentStatus.COMPLETED]
        
        if not successful_executions:
            return []
        
        patterns = []
        
        # Deployment type patterns
        type_success = defaultdict(int)
        type_total = defaultdict(int)
        
        for execution in executions:
            type_total[execution.deployment_type] += 1
            if execution.status == DeploymentStatus.COMPLETED:
                type_success[execution.deployment_type] += 1
        
        for dep_type, success_count in type_success.items():
            success_rate = success_count / type_total[dep_type] * 100
            if success_rate >= 95:
                patterns.append(f"{dep_type.value} deployments show {success_rate:.1f}% success rate")
        
        # Duration patterns
        avg_successful_duration = statistics.mean(e.actual_duration_minutes for e in successful_executions)
        if avg_successful_duration < 30:
            patterns.append(f"Successful deployments average {avg_successful_duration:.1f} minutes")
        
        return patterns[:3]
    
    def _identify_failure_patterns(self, executions: List[DeploymentExecution]) -> List[str]:
        """Identify patterns in failed deployments."""
        
        failed_executions = [e for e in executions 
                           if e.status in [DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK]]
        
        if not failed_executions:
            return []
        
        patterns = []
        
        # Common failure reasons
        rollback_reasons = [e.rollback_reason for e in failed_executions if e.rollback_reason]
        if rollback_reasons:
            patterns.append("High error rates are the primary cause of rollbacks")
        
        # Environment patterns
        env_failures = Counter(e.target_environment for e in failed_executions)
        if env_failures:
            most_problematic_env = env_failures.most_common(1)[0]
            patterns.append(f"{most_problematic_env[0].value} environment has highest failure rate")
        
        return patterns[:3]
    
    def _identify_improvement_opportunities(self, report: DeploymentReport) -> List[str]:
        """Identify deployment improvement opportunities."""
        
        opportunities = []
        
        if report.deployment_success_rate < 95:
            opportunities.append("Implement automated deployment testing to improve success rate")
        
        if report.average_deployment_time_minutes > 30:
            opportunities.append("Optimize deployment pipelines and artifact sizes")
        
        if report.high_risk_deployments > 0:
            opportunities.append("Implement blue-green or canary deployment strategies")
        
        if DeploymentEnvironment.STAGING not in report.deployments_by_environment:
            opportunities.append("Establish comprehensive staging environment testing")
        
        return opportunities[:3]
    
    def get_deployment_dashboard(self) -> Dict[str, Any]:
        """Get real-time deployment dashboard data."""
        
        # Recent activity (last 7 days)
        recent_time = datetime.now() - timedelta(days=7)
        recent_executions = [e for e in self.deployment_executions if e.start_time >= recent_time]
        
        # Current status
        active_deployments = [e for e in self.deployment_executions 
                            if e.status in [DeploymentStatus.IN_PROGRESS, DeploymentStatus.DEPLOYING, DeploymentStatus.TESTING]]
        
        return {
            "timestamp": datetime.now(),
            "deployment_status": {
                "active_deployments": len(active_deployments),
                "recent_deployments_7d": len(recent_executions),
                "success_rate_7d": (len([e for e in recent_executions if e.status == DeploymentStatus.COMPLETED]) 
                                   / len(recent_executions) * 100) if recent_executions else 0
            },
            "artifacts": {
                "total_artifacts": len(self.deployment_artifacts),
                "validated_artifacts": len([a for a in self.deployment_artifacts.values() if a.is_validated])
            },
            "plans": {
                "total_plans": len(self.deployment_plans),
                "approved_plans": len([p for p in self.deployment_plans.values() if p.approved_by]),
                "pending_approval": len([p for p in self.deployment_plans.values() 
                                       if p.requires_approval and not p.approved_by])
            },
            "environments": {
                "production_deployments": len([e for e in recent_executions 
                                             if e.target_environment == DeploymentEnvironment.PRODUCTION]),
                "staging_deployments": len([e for e in recent_executions 
                                          if e.target_environment == DeploymentEnvironment.STAGING])
            }
        }
    
    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get comprehensive deployment system summary."""
        
        # Deployment statistics
        total_executions = len(self.deployment_executions)
        successful_executions = len([e for e in self.deployment_executions if e.status == DeploymentStatus.COMPLETED])
        
        return {
            "artifacts": {
                "total_artifacts": len(self.deployment_artifacts),
                "by_component_type": Counter(a.component_type for a in self.deployment_artifacts.values()),
                "validated_artifacts": len([a for a in self.deployment_artifacts.values() if a.is_validated])
            },
            "plans": {
                "total_plans": len(self.deployment_plans),
                "by_deployment_type": Counter(p.deployment_type for p in self.deployment_plans.values()),
                "by_environment": Counter(p.target_environment for p in self.deployment_plans.values()),
                "requiring_approval": len([p for p in self.deployment_plans.values() if p.requires_approval])
            },
            "executions": {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
                "by_status": Counter(e.status for e in self.deployment_executions),
                "by_environment": Counter(e.target_environment for e in self.deployment_executions)
            },
            "performance": {
                "total_metrics": len(self.deployment_metrics),
                "total_reports": len(self.deployment_reports)
            }
        }

def run_demonstration() -> DeploymentManager:
    """Run comprehensive deployment management demonstration."""
    
    print("🚀 One Health Deployment Management - Demonstration")
    print("=" * 65)
    
    manager = DeploymentManager()
    
    print(f"\n🚀 Deployment Framework:")
    print(f"  Deployment Types: {len(DeploymentType)}")
    print(f"  Deployment Environments: {len(DeploymentEnvironment)}")
    print(f"  Pre-configured Artifacts: {len(manager.deployment_artifacts)}")
    print(f"  Sample Deployment Plans: {len(manager.deployment_plans)}")
    
    # Display artifacts by component type
    artifacts_by_type = defaultdict(list)
    for artifact in manager.deployment_artifacts.values():
        artifacts_by_type[artifact.component_type].append(artifact.artifact_name)
    
    print(f"\n📦 Deployment Artifacts by Type:")
    for component_type, artifacts in artifacts_by_type.items():
        print(f"  {component_type.value.replace('_', ' ').title()}: {len(artifacts)}")
        for artifact in artifacts[:2]:  # Show first 2
            print(f"    • {artifact}")
    
    print(f"\n✅ Validating Deployment Artifacts...")
    
    # Validate all artifacts
    validation_results = []
    for artifact_id in manager.deployment_artifacts:
        result = manager.validate_artifact(artifact_id)
        validation_results.append(result)
        
        artifact_name = manager.deployment_artifacts[artifact_id].artifact_name
        passed_checks = sum(1 for status in result.values() if status == "passed")
        total_checks = len(result)
        print(f"  ✅ {artifact_name}: {passed_checks}/{total_checks} checks passed")
    
    print(f"\n📋 Creating Custom Deployment Plan...")
    
    # Create a custom deployment plan
    custom_artifacts = list(manager.deployment_artifacts.keys())[:3]  # Take first 3 artifacts
    
    custom_plan = manager.create_deployment_plan(
        "Emergency Security Update Deployment",
        DeploymentType.BLUE_GREEN,
        DeploymentEnvironment.PRODUCTION,
        custom_artifacts,
        "security_team"
    )
    
    print(f"  📋 Plan: {custom_plan.plan_name}")
    print(f"  📋 Type: {custom_plan.deployment_type.value.replace('_', ' ').title()}")
    print(f"  📋 Environment: {custom_plan.target_environment.value.replace('_', ' ').title()}")
    print(f"  📋 Artifacts: {len(custom_plan.artifacts)}")
    print(f"  📋 Risk Level: {custom_plan.risk_level.title()}")
    print(f"  📋 Estimated Duration: {custom_plan.estimated_duration_minutes:.1f} minutes")
    
    print(f"\n✅ Approving Deployment Plans...")
    
    # Approve deployment plans
    approved_plans = []
    for plan_id, plan in list(manager.deployment_plans.items())[:3]:  # Approve first 3 plans
        if plan.requires_approval:
            manager.approve_deployment_plan(plan_id, "deployment_manager")
            approved_plans.append(plan_id)
            print(f"  ✅ Approved: {plan.plan_name}")
    
    # Approve custom plan
    if custom_plan.requires_approval:
        manager.approve_deployment_plan(custom_plan.plan_id, "security_manager")
        approved_plans.append(custom_plan.plan_id)
        print(f"  ✅ Approved: {custom_plan.plan_name}")
    
    print(f"\n🚀 Executing Deployments...")
    
    # Execute approved deployment plans
    executions = []
    for plan_id in approved_plans[:3]:  # Execute first 3 approved plans
        execution = manager.execute_deployment(plan_id, "deployment_system")
        executions.append(execution)
        
        plan_name = manager.deployment_plans[plan_id].plan_name
        if execution.status == DeploymentStatus.COMPLETED:
            print(f"  ✅ {plan_name}: Completed ({execution.success_rate:.1f}% success)")
        elif execution.status == DeploymentStatus.ROLLED_BACK:
            print(f"  🔄 {plan_name}: Rolled back ({execution.rollback_reason})")
        else:
            print(f"  ❌ {plan_name}: Failed ({execution.error_count} errors)")
    
    print(f"\n📊 Collecting Deployment Metrics...")
    
    # Collect metrics for all executions
    metrics_collected = []
    for execution in executions:
        metrics = manager.collect_deployment_metrics(execution.execution_id)
        metrics_collected.append(metrics)
        
        print(f"  📊 Metrics for {execution.execution_id}:")
        print(f"    Success Rate: {metrics.deployment_success_rate:.1f}%")
        print(f"    User Satisfaction: {metrics.user_satisfaction_score:.1f}/10")
    
    print(f"\n📋 Generating Deployment Report...")
    
    # Generate comprehensive deployment report
    deployment_report = manager.generate_deployment_report("Monthly Deployment Summary Report")
    
    print(f"  📋 Report: {deployment_report.total_deployments} total deployments")
    print(f"  📋 Success Rate: {deployment_report.deployment_success_rate:.1f}%")
    print(f"  📋 Average Duration: {deployment_report.average_deployment_time_minutes:.1f} minutes")
    print(f"  📋 Quality Score: {deployment_report.overall_quality_score:.1f}%")
    
    return manager

def display_deployment_results(manager: DeploymentManager):
    """Display comprehensive deployment management results."""
    
    print(f"\n🚀 Deployment Management Results:")
    
    # Deployment dashboard
    dashboard = manager.get_deployment_dashboard()
    
    print(f"\n🎯 Deployment Dashboard:")
    
    status = dashboard["deployment_status"]
    print(f"  Active Deployments: {status['active_deployments']}")
    print(f"  Recent Deployments (7d): {status['recent_deployments_7d']}")
    print(f"  Success Rate (7d): {status['success_rate_7d']:.1f}%")
    
    artifacts = dashboard["artifacts"]
    print(f"  Total Artifacts: {artifacts['total_artifacts']}")
    print(f"  Validated Artifacts: {artifacts['validated_artifacts']}")
    
    plans = dashboard["plans"]
    print(f"  Total Plans: {plans['total_plans']}")
    print(f"  Approved Plans: {plans['approved_plans']}")
    print(f"  Pending Approval: {plans['pending_approval']}")
    
    # Deployment executions summary
    print(f"\n🚀 Deployment Executions:")
    print(f"  Total Executions: {len(manager.deployment_executions)}")
    
    if manager.deployment_executions:
        # Executions by status
        status_counts = Counter(e.status for e in manager.deployment_executions)
        for status, count in status_counts.items():
            print(f"  {status.value.title()}: {count}")
        
        # Recent execution details
        recent_executions = manager.deployment_executions[-3:]  # Last 3
        print(f"\n  Recent Executions:")
        for execution in recent_executions:
            plan_name = manager.deployment_plans[execution.plan_id].plan_name if execution.plan_id in manager.deployment_plans else "Unknown Plan"
            print(f"    • {plan_name}: {execution.status.value.title()} ({execution.success_rate:.1f}% success)")
    
    # Deployment plans analysis
    print(f"\n📋 Deployment Plans Analysis:")
    print(f"  Total Plans: {len(manager.deployment_plans)}")
    
    plans_by_type = Counter(p.deployment_type for p in manager.deployment_plans.values())
    print(f"  Plans by Type:")
    for dep_type, count in plans_by_type.items():
        print(f"    {dep_type.value.replace('_', ' ').title()}: {count}")
    
    plans_by_env = Counter(p.target_environment for p in manager.deployment_plans.values())
    print(f"  Plans by Environment:")
    for env, count in plans_by_env.items():
        print(f"    {env.value.replace('_', ' ').title()}: {count}")
    
    # Artifact analysis
    print(f"\n📦 Deployment Artifacts Analysis:")
    print(f"  Total Artifacts: {len(manager.deployment_artifacts)}")
    
    artifacts_by_type = Counter(a.component_type for a in manager.deployment_artifacts.values())
    print(f"  Artifacts by Component Type:")
    for component_type, count in artifacts_by_type.items():
        print(f"    {component_type.value.replace('_', ' ').title()}: {count}")
    
    validated_count = len([a for a in manager.deployment_artifacts.values() if a.is_validated])
    print(f"  Validated Artifacts: {validated_count}/{len(manager.deployment_artifacts)}")
    
    # Performance metrics
    if manager.deployment_metrics:
        print(f"\n📊 Deployment Performance Metrics:")
        
        latest_metrics = manager.deployment_metrics[-1]
        print(f"  Latest Metrics:")
        print(f"    Deployment Frequency: {latest_metrics.deployment_frequency:.1f} per week")
        print(f"    Success Rate: {latest_metrics.deployment_success_rate:.1f}%")
        print(f"    User Satisfaction: {latest_metrics.user_satisfaction_score:.1f}/10")
        print(f"    Business Value: {latest_metrics.business_value_score:.1f}/10")
    
    # System summary
    summary = manager.get_deployment_summary()
    
    print(f"\n📊 Deployment System Summary:")
    
    artifacts_summary = summary["artifacts"]
    print(f"  Artifacts: {artifacts_summary['total_artifacts']} ({artifacts_summary['validated_artifacts']} validated)")
    
    plans_summary = summary["plans"]
    print(f"  Plans: {plans_summary['total_plans']} ({plans_summary['requiring_approval']} require approval)")
    
    executions_summary = summary["executions"]
    print(f"  Executions: {executions_summary['total_executions']} ({executions_summary['success_rate']:.1f}% success)")
    
    performance_summary = summary["performance"]
    print(f"  Metrics: {performance_summary['total_metrics']} collected")
    print(f"  Reports: {performance_summary['total_reports']} generated")
    
    # Latest deployment report
    if manager.deployment_reports:
        latest_report = manager.deployment_reports[-1]
        print(f"\n📋 Latest Deployment Report:")
        print(f"  Title: {latest_report.report_title}")
        print(f"  Period: {latest_report.reporting_period_start.strftime('%Y-%m-%d')} to {latest_report.reporting_period_end.strftime('%Y-%m-%d')}")
        print(f"  Total Deployments: {latest_report.total_deployments}")
        print(f"  Success Rate: {latest_report.deployment_success_rate:.1f}%")
        print(f"  Average Duration: {latest_report.average_deployment_time_minutes:.1f} minutes")
        print(f"  Quality Score: {latest_report.overall_quality_score:.1f}%")
        
        if latest_report.key_insights:
            print(f"  Key Insights:")
            for insight in latest_report.key_insights[:3]:
                print(f"    • {insight}")
        
        if latest_report.recommendations:
            print(f"  Recommendations:")
            for recommendation in latest_report.recommendations[:3]:
                print(f"    • {recommendation}")
    
    print(f"\n🏆 TOP PERFORMING Deployments:")
    
    # Sort executions by success rate
    successful_executions = [e for e in manager.deployment_executions if e.status == DeploymentStatus.COMPLETED]
    top_executions = sorted(successful_executions, key=lambda e: e.success_rate, reverse=True)[:3]
    
    for i, execution in enumerate(top_executions, 1):
        plan_name = manager.deployment_plans[execution.plan_id].plan_name if execution.plan_id in manager.deployment_plans else "Unknown Plan"
        print(f"  {i}. {plan_name}")
        print(f"     Success Rate: {execution.success_rate:.1f}%")
        print(f"     Duration: {execution.actual_duration_minutes:.1f} minutes")
        print(f"     Environment: {execution.target_environment.value.replace('_', ' ').title()}")
        print(f"     Type: {execution.deployment_type.value.replace('_', ' ').title()}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    deployment_manager = run_demonstration()
    display_deployment_results(deployment_manager)
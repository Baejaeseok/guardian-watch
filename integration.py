"""
System Integration Framework
============================
Module 5: Integration & Validation Tools

Advanced system integration and interoperability framework for One Health platforms,
providing seamless data flow, API coordination, and cross-system communication.

NIW Focus: Integration intelligence enabling unified One Health surveillance and response ecosystem.
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
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemType(Enum):
    """Types of integrated systems."""
    SURVEILLANCE = "surveillance"                 # Disease surveillance systems
    LABORATORY = "laboratory"                     # Laboratory information systems
    RESPONSE = "response"                        # Emergency response systems
    COMMUNICATION = "communication"              # Communication platforms
    HEALTHCARE = "healthcare"                    # Healthcare information systems
    VETERINARY = "veterinary"                    # Veterinary health systems
    ENVIRONMENTAL = "environmental"              # Environmental monitoring
    AGRICULTURE = "agriculture"                  # Agricultural monitoring
    EXTERNAL_API = "external_api"               # External API services
    LEGACY_SYSTEM = "legacy_system"             # Legacy system integration

class IntegrationMethod(Enum):
    """Integration methods and protocols."""
    REST_API = "rest_api"                        # RESTful API integration
    SOAP_API = "soap_api"                        # SOAP web services
    MESSAGING = "messaging"                      # Message queue integration
    DATABASE = "database"                        # Direct database integration
    FILE_TRANSFER = "file_transfer"              # File-based data exchange
    WEBHOOK = "webhook"                          # Webhook notifications
    STREAMING = "streaming"                      # Real-time data streaming
    BATCH_PROCESSING = "batch_processing"        # Batch data processing

class DataFormat(Enum):
    """Supported data formats."""
    JSON = "json"                               # JSON format
    XML = "xml"                                 # XML format
    CSV = "csv"                                 # CSV format
    HL7 = "hl7"                                # HL7 healthcare standard
    FHIR = "fhir"                              # FHIR healthcare standard
    EDI = "edi"                                # Electronic Data Interchange
    CUSTOM = "custom"                          # Custom format
    BINARY = "binary"                          # Binary data

class IntegrationStatus(Enum):
    """Integration connection status."""
    ACTIVE = "active"                           # Successfully integrated
    INACTIVE = "inactive"                       # Not currently integrated
    ERROR = "error"                            # Integration error
    PENDING = "pending"                        # Integration pending
    TESTING = "testing"                        # Under testing
    MAINTENANCE = "maintenance"                # Under maintenance

@dataclass
class SystemEndpoint:
    """System endpoint configuration."""
    
    endpoint_id: str
    endpoint_name: str
    system_type: SystemType
    integration_method: IntegrationMethod
    
    # Connection details
    base_url: str
    authentication_type: str = "api_key"        # "none", "api_key", "oauth", "basic"
    credentials: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 30
    
    # Data specifications
    supported_formats: List[DataFormat] = field(default_factory=list)
    data_schema: Dict[str, Any] = field(default_factory=dict)
    rate_limit_per_minute: int = 60
    
    # Quality and reliability
    availability_sla: float = 0.99              # 99% availability SLA
    response_time_sla_ms: int = 1000            # 1 second response time SLA
    data_quality_score: float = 0.95           # Data quality rating
    
    # Operational metrics
    status: IntegrationStatus = IntegrationStatus.INACTIVE
    last_successful_connection: Optional[datetime] = None
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time_ms: float = 0.0
    
    # Error handling
    retry_attempts: int = 3
    circuit_breaker_threshold: int = 5          # Failures before circuit breaker
    maintenance_windows: List[str] = field(default_factory=list)

@dataclass
class DataMapping:
    """Data field mapping between systems."""
    
    mapping_id: str
    source_system: str
    target_system: str
    mapping_name: str
    
    # Field mappings
    field_mappings: Dict[str, str] = field(default_factory=dict)  # source_field -> target_field
    data_transformations: Dict[str, str] = field(default_factory=dict)  # field -> transformation_rule
    validation_rules: Dict[str, str] = field(default_factory=dict)  # field -> validation_rule
    
    # Data processing
    data_enrichment: Dict[str, Any] = field(default_factory=dict)
    data_filtering: Dict[str, Any] = field(default_factory=dict)
    aggregation_rules: Dict[str, str] = field(default_factory=dict)
    
    # Quality assurance
    mapping_confidence: float = 1.0            # Confidence in mapping accuracy
    data_loss_tolerance: float = 0.01          # Acceptable data loss percentage
    transformation_accuracy: float = 0.99      # Transformation accuracy requirement
    
    # Performance
    processing_time_ms: float = 0.0
    throughput_records_per_second: int = 1000
    error_rate: float = 0.0

@dataclass
class IntegrationWorkflow:
    """Integration workflow definition."""
    
    workflow_id: str
    workflow_name: str
    workflow_description: str
    
    # Workflow steps
    source_systems: List[str] = field(default_factory=list)
    target_systems: List[str] = field(default_factory=list)
    processing_steps: List[Dict[str, Any]] = field(default_factory=list)
    
    # Execution configuration
    trigger_type: str = "scheduled"             # "manual", "scheduled", "event", "api"
    schedule_expression: str = "*/15 * * * *"   # Cron expression for scheduling
    parallel_execution: bool = False
    max_concurrent_executions: int = 1
    
    # Data flow
    data_flow_direction: str = "bidirectional"  # "source_to_target", "target_to_source", "bidirectional"
    batch_size: int = 1000
    processing_timeout_minutes: int = 30
    
    # Quality and monitoring
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    failure_handling: str = "retry_and_alert"  # "ignore", "retry", "alert", "retry_and_alert"
    monitoring_enabled: bool = True
    
    # Execution history
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    last_execution_time: Optional[datetime] = None
    average_execution_time_minutes: float = 0.0

@dataclass
class IntegrationEvent:
    """Integration event for monitoring and logging."""
    
    event_id: str
    event_timestamp: datetime
    event_type: str                            # "data_sync", "error", "status_change", "performance"
    
    # Event details
    source_system: str
    target_system: Optional[str] = None
    workflow_id: Optional[str] = None
    
    # Event data
    records_processed: int = 0
    processing_time_ms: float = 0.0
    success: bool = True
    error_message: Optional[str] = None
    
    # Performance metrics
    throughput_per_second: float = 0.0
    response_time_ms: float = 0.0
    data_quality_score: float = 1.0
    
    # Context information
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    additional_metadata: Dict[str, Any] = field(default_factory=dict)

class SystemIntegrationManager:
    """Central system integration management platform."""
    
    def __init__(self):
        self.system_endpoints: Dict[str, SystemEndpoint] = {}
        self.data_mappings: Dict[str, DataMapping] = {}
        self.integration_workflows: Dict[str, IntegrationWorkflow] = {}
        self.integration_events: List[IntegrationEvent] = []
        self.active_connections: Dict[str, Any] = {}
        
        # Performance monitoring
        self.performance_metrics: Dict[str, Any] = {}
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        
        # Initialize default integrations
        self._initialize_system_integrations()
        
        logger.info("One Health System Integration Manager initialized")
    
    def _initialize_system_integrations(self):
        """Initialize default system integrations."""
        
        # Define default system endpoints
        default_endpoints = [
            {
                "id": "surveillance_api", "name": "Disease Surveillance API", "type": SystemType.SURVEILLANCE,
                "method": IntegrationMethod.REST_API, "url": "https://surveillance.health.gov/api/v1",
                "formats": [DataFormat.JSON, DataFormat.XML], "rate_limit": 100
            },
            {
                "id": "lab_lis", "name": "Laboratory Information System", "type": SystemType.LABORATORY,
                "method": IntegrationMethod.REST_API, "url": "https://lab.health.gov/api/v2",
                "formats": [DataFormat.HL7, DataFormat.JSON], "rate_limit": 200
            },
            {
                "id": "vet_health", "name": "Veterinary Health System", "type": SystemType.VETERINARY,
                "method": IntegrationMethod.REST_API, "url": "https://vetnet.usda.gov/api/v1",
                "formats": [DataFormat.JSON, DataFormat.XML], "rate_limit": 60
            },
            {
                "id": "response_coord", "name": "Response Coordination Platform", "type": SystemType.RESPONSE,
                "method": IntegrationMethod.MESSAGING, "url": "https://response.fema.gov/api/v1",
                "formats": [DataFormat.JSON], "rate_limit": 150
            },
            {
                "id": "env_monitor", "name": "Environmental Monitoring Network", "type": SystemType.ENVIRONMENTAL,
                "method": IntegrationMethod.STREAMING, "url": "https://env.epa.gov/stream/v1",
                "formats": [DataFormat.JSON, DataFormat.CSV], "rate_limit": 300
            },
            {
                "id": "agri_data", "name": "Agricultural Data Exchange", "type": SystemType.AGRICULTURE,
                "method": IntegrationMethod.BATCH_PROCESSING, "url": "https://data.agriculture.gov/api/v1",
                "formats": [DataFormat.CSV, DataFormat.JSON], "rate_limit": 50
            }
        ]
        
        for endpoint_data in default_endpoints:
            endpoint = SystemEndpoint(
                endpoint_id=endpoint_data["id"],
                endpoint_name=endpoint_data["name"],
                system_type=endpoint_data["type"],
                integration_method=endpoint_data["method"],
                base_url=endpoint_data["url"],
                supported_formats=endpoint_data["formats"],
                rate_limit_per_minute=endpoint_data["rate_limit"]
            )
            
            # Set authentication
            endpoint.credentials = {"api_key": f"key_{random.randint(100000, 999999)}"}
            
            # Set realistic performance metrics
            endpoint.data_quality_score = random.uniform(0.85, 0.98)
            endpoint.availability_sla = random.uniform(0.95, 0.999)
            endpoint.response_time_sla_ms = random.randint(500, 2000)
            
            self.system_endpoints[endpoint.endpoint_id] = endpoint
    
    def register_system_endpoint(self, endpoint_config: Dict[str, Any]) -> SystemEndpoint:
        """Register new system endpoint for integration."""
        
        endpoint_id = endpoint_config.get("endpoint_id", f"endpoint_{random.randint(100000, 999999)}")
        
        endpoint = SystemEndpoint(
            endpoint_id=endpoint_id,
            endpoint_name=endpoint_config["endpoint_name"],
            system_type=SystemType(endpoint_config["system_type"]),
            integration_method=IntegrationMethod(endpoint_config["integration_method"]),
            base_url=endpoint_config["base_url"],
            authentication_type=endpoint_config.get("authentication_type", "api_key"),
            supported_formats=[DataFormat(fmt) for fmt in endpoint_config.get("supported_formats", ["json"])],
            rate_limit_per_minute=endpoint_config.get("rate_limit", 60)
        )
        
        # Set credentials if provided
        if "credentials" in endpoint_config:
            endpoint.credentials = endpoint_config["credentials"]
        
        # Set SLA requirements
        endpoint.availability_sla = endpoint_config.get("availability_sla", 0.99)
        endpoint.response_time_sla_ms = endpoint_config.get("response_time_sla_ms", 1000)
        endpoint.data_quality_score = endpoint_config.get("data_quality_score", 0.95)
        
        self.system_endpoints[endpoint_id] = endpoint
        
        logger.info(f"System endpoint registered: {endpoint_id}")
        
        return endpoint
    
    def create_data_mapping(self, source_system: str, target_system: str,
                           field_mappings: Dict[str, str], mapping_name: str = "") -> DataMapping:
        """Create data mapping between systems."""
        
        if source_system not in self.system_endpoints:
            raise ValueError(f"Source system {source_system} not found")
        
        if target_system not in self.system_endpoints:
            raise ValueError(f"Target system {target_system} not found")
        
        mapping_id = f"mapping_{hashlib.md5(f'{source_system}_{target_system}'.encode()).hexdigest()[:8]}"
        
        mapping = DataMapping(
            mapping_id=mapping_id,
            source_system=source_system,
            target_system=target_system,
            mapping_name=mapping_name or f"{source_system} to {target_system} mapping",
            field_mappings=field_mappings
        )
        
        # Generate automatic data transformations and validations
        mapping.data_transformations = self._generate_transformations(field_mappings)
        mapping.validation_rules = self._generate_validation_rules(field_mappings)
        
        # Set performance characteristics
        mapping.mapping_confidence = random.uniform(0.9, 1.0)
        mapping.transformation_accuracy = random.uniform(0.95, 0.999)
        mapping.throughput_records_per_second = random.randint(500, 2000)
        
        self.data_mappings[mapping_id] = mapping
        
        logger.info(f"Data mapping created: {mapping_id}")
        
        return mapping
    
    def _generate_transformations(self, field_mappings: Dict[str, str]) -> Dict[str, str]:
        """Generate automatic data transformations."""
        
        transformations = {}
        
        for source_field, target_field in field_mappings.items():
            # Common transformation patterns
            if "date" in source_field.lower() and "timestamp" in target_field.lower():
                transformations[source_field] = "date_to_timestamp"
            elif "id" in source_field.lower() and target_field.lower().endswith("_uuid"):
                transformations[source_field] = "id_to_uuid"
            elif source_field.lower() == "temperature_f" and target_field.lower() == "temperature_c":
                transformations[source_field] = "fahrenheit_to_celsius"
            elif "status" in source_field.lower():
                transformations[source_field] = "normalize_status_codes"
        
        return transformations
    
    def _generate_validation_rules(self, field_mappings: Dict[str, str]) -> Dict[str, str]:
        """Generate automatic validation rules."""
        
        validation_rules = {}
        
        for source_field, target_field in field_mappings.items():
            # Common validation patterns
            if "email" in source_field.lower():
                validation_rules[source_field] = "validate_email_format"
            elif "date" in source_field.lower():
                validation_rules[source_field] = "validate_date_format"
            elif "id" in source_field.lower():
                validation_rules[source_field] = "validate_not_null"
            elif "status" in source_field.lower():
                validation_rules[source_field] = "validate_status_enum"
            elif "count" in source_field.lower() or "number" in source_field.lower():
                validation_rules[source_field] = "validate_positive_number"
        
        return validation_rules
    
    def create_integration_workflow(self, workflow_config: Dict[str, Any]) -> IntegrationWorkflow:
        """Create integration workflow."""
        
        workflow_id = workflow_config.get("workflow_id", f"workflow_{random.randint(100000, 999999)}")
        
        workflow = IntegrationWorkflow(
            workflow_id=workflow_id,
            workflow_name=workflow_config["workflow_name"],
            workflow_description=workflow_config.get("workflow_description", ""),
            source_systems=workflow_config.get("source_systems", []),
            target_systems=workflow_config.get("target_systems", []),
            trigger_type=workflow_config.get("trigger_type", "scheduled"),
            schedule_expression=workflow_config.get("schedule_expression", "*/15 * * * *"),
            batch_size=workflow_config.get("batch_size", 1000)
        )
        
        # Create processing steps
        workflow.processing_steps = self._generate_processing_steps(workflow)
        
        # Set success criteria
        workflow.success_criteria = {
            "min_success_rate": 0.95,
            "max_error_rate": 0.05,
            "max_processing_time_minutes": 30
        }
        
        self.integration_workflows[workflow_id] = workflow
        
        logger.info(f"Integration workflow created: {workflow_id}")
        
        return workflow
    
    def _generate_processing_steps(self, workflow: IntegrationWorkflow) -> List[Dict[str, Any]]:
        """Generate processing steps for workflow."""
        
        steps = []
        
        # Step 1: Data extraction
        steps.append({
            "step_id": "extract",
            "step_name": "Data Extraction",
            "step_type": "extraction",
            "description": "Extract data from source systems",
            "timeout_minutes": 10,
            "retry_attempts": 3
        })
        
        # Step 2: Data transformation
        if workflow.source_systems and workflow.target_systems:
            steps.append({
                "step_id": "transform",
                "step_name": "Data Transformation",
                "step_type": "transformation", 
                "description": "Transform and map data between systems",
                "timeout_minutes": 15,
                "retry_attempts": 2
            })
        
        # Step 3: Data validation
        steps.append({
            "step_id": "validate",
            "step_name": "Data Validation",
            "step_type": "validation",
            "description": "Validate data quality and compliance",
            "timeout_minutes": 5,
            "retry_attempts": 1
        })
        
        # Step 4: Data loading
        steps.append({
            "step_id": "load",
            "step_name": "Data Loading",
            "step_type": "loading",
            "description": "Load data into target systems",
            "timeout_minutes": 10,
            "retry_attempts": 3
        })
        
        return steps
    
    async def execute_workflow(self, workflow_id: str, manual_trigger: bool = False) -> Dict[str, Any]:
        """Execute integration workflow."""
        
        if workflow_id not in self.integration_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.integration_workflows[workflow_id]
        execution_start = datetime.now()
        
        # Log workflow execution start
        start_event = IntegrationEvent(
            event_id=f"exec_{random.randint(100000, 999999)}",
            event_timestamp=execution_start,
            event_type="workflow_start",
            source_system="integration_manager",
            workflow_id=workflow_id
        )
        self.integration_events.append(start_event)
        
        execution_result = {
            "workflow_id": workflow_id,
            "execution_start": execution_start,
            "steps_completed": 0,
            "total_steps": len(workflow.processing_steps),
            "records_processed": 0,
            "success": False,
            "errors": []
        }
        
        try:
            # Execute each processing step
            total_records = 0
            
            for step in workflow.processing_steps:
                step_start = datetime.now()
                
                # Simulate step execution
                step_result = await self._execute_processing_step(step, workflow)
                
                execution_result["steps_completed"] += 1
                total_records += step_result.get("records_processed", 0)
                
                # Log step completion
                step_event = IntegrationEvent(
                    event_id=f"step_{random.randint(100000, 999999)}",
                    event_timestamp=datetime.now(),
                    event_type="step_completed",
                    source_system="integration_manager",
                    workflow_id=workflow_id,
                    records_processed=step_result.get("records_processed", 0),
                    processing_time_ms=(datetime.now() - step_start).total_seconds() * 1000,
                    success=step_result.get("success", True)
                )
                self.integration_events.append(step_event)
                
                # Handle step failure
                if not step_result.get("success", True):
                    execution_result["errors"].append(f"Step {step['step_name']} failed: {step_result.get('error')}")
                    if workflow.failure_handling in ["retry", "retry_and_alert"]:
                        # Implement retry logic here
                        pass
            
            execution_result["records_processed"] = total_records
            execution_result["success"] = len(execution_result["errors"]) == 0
            
            # Update workflow metrics
            workflow.total_executions += 1
            if execution_result["success"]:
                workflow.successful_executions += 1
            else:
                workflow.failed_executions += 1
            
            workflow.last_execution_time = execution_start
            
            execution_time_minutes = (datetime.now() - execution_start).total_seconds() / 60
            if workflow.total_executions > 0:
                workflow.average_execution_time_minutes = (
                    (workflow.average_execution_time_minutes * (workflow.total_executions - 1) + execution_time_minutes) 
                    / workflow.total_executions
                )
            else:
                workflow.average_execution_time_minutes = execution_time_minutes
            
        except Exception as e:
            execution_result["success"] = False
            execution_result["errors"].append(f"Workflow execution failed: {str(e)}")
            workflow.failed_executions += 1
        
        # Log workflow completion
        completion_event = IntegrationEvent(
            event_id=f"comp_{random.randint(100000, 999999)}",
            event_timestamp=datetime.now(),
            event_type="workflow_completed",
            source_system="integration_manager",
            workflow_id=workflow_id,
            records_processed=execution_result["records_processed"],
            processing_time_ms=(datetime.now() - execution_start).total_seconds() * 1000,
            success=execution_result["success"]
        )
        self.integration_events.append(completion_event)
        
        logger.info(f"Workflow executed: {workflow_id} - {'Success' if execution_result['success'] else 'Failed'}")
        
        return execution_result
    
    async def _execute_processing_step(self, step: Dict[str, Any], 
                                     workflow: IntegrationWorkflow) -> Dict[str, Any]:
        """Execute individual processing step."""
        
        step_type = step["step_type"]
        
        # Simulate step execution time
        processing_time_ms = random.uniform(100, 5000)
        await asyncio.sleep(processing_time_ms / 1000)
        
        # Simulate step results based on type
        if step_type == "extraction":
            records_processed = random.randint(500, 2000)
            success_rate = 0.98
        elif step_type == "transformation":
            records_processed = random.randint(450, 1900)  # Some data loss
            success_rate = 0.95
        elif step_type == "validation":
            records_processed = random.randint(400, 1800)  # Validation filtering
            success_rate = 0.92
        elif step_type == "loading":
            records_processed = random.randint(380, 1750)  # Loading may fail some records
            success_rate = 0.94
        else:
            records_processed = random.randint(100, 1000)
            success_rate = 0.90
        
        # Determine success based on random chance
        success = random.random() < success_rate
        
        return {
            "step_id": step["step_id"],
            "records_processed": records_processed,
            "processing_time_ms": processing_time_ms,
            "success": success,
            "error": None if success else f"{step['step_name']} processing error"
        }
    
    def test_system_connectivity(self, endpoint_id: str) -> Dict[str, Any]:
        """Test connectivity to system endpoint."""
        
        if endpoint_id not in self.system_endpoints:
            raise ValueError(f"Endpoint {endpoint_id} not found")
        
        endpoint = self.system_endpoints[endpoint_id]
        test_start = datetime.now()
        
        # Simulate connectivity test
        response_time_ms = random.uniform(50, 2000)
        success = random.random() < 0.95  # 95% success rate
        
        # Update endpoint metrics
        endpoint.total_requests += 1
        if success:
            endpoint.successful_requests += 1
            endpoint.status = IntegrationStatus.ACTIVE
            endpoint.last_successful_connection = test_start
        else:
            endpoint.failed_requests += 1
            if endpoint.failed_requests >= endpoint.circuit_breaker_threshold:
                endpoint.status = IntegrationStatus.ERROR
        
        # Update average response time
        if endpoint.total_requests > 0:
            endpoint.average_response_time_ms = (
                (endpoint.average_response_time_ms * (endpoint.total_requests - 1) + response_time_ms)
                / endpoint.total_requests
            )
        else:
            endpoint.average_response_time_ms = response_time_ms
        
        # Log connectivity test
        test_event = IntegrationEvent(
            event_id=f"test_{random.randint(100000, 999999)}",
            event_timestamp=test_start,
            event_type="connectivity_test",
            source_system=endpoint_id,
            processing_time_ms=response_time_ms,
            success=success,
            error_message=None if success else "Connection timeout"
        )
        self.integration_events.append(test_event)
        
        return {
            "endpoint_id": endpoint_id,
            "success": success,
            "response_time_ms": response_time_ms,
            "status": endpoint.status.value,
            "test_timestamp": test_start,
            "error_message": None if success else "Connection failed"
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status."""
        
        # System endpoint status
        endpoint_status = {}
        total_endpoints = len(self.system_endpoints)
        active_endpoints = 0
        
        for endpoint_id, endpoint in self.system_endpoints.items():
            endpoint_status[endpoint_id] = {
                "name": endpoint.endpoint_name,
                "type": endpoint.system_type.value,
                "status": endpoint.status.value,
                "success_rate": (endpoint.successful_requests / endpoint.total_requests) 
                               if endpoint.total_requests > 0 else 0,
                "avg_response_time_ms": endpoint.average_response_time_ms,
                "data_quality_score": endpoint.data_quality_score
            }
            
            if endpoint.status == IntegrationStatus.ACTIVE:
                active_endpoints += 1
        
        # Workflow status
        workflow_status = {}
        for workflow_id, workflow in self.integration_workflows.items():
            workflow_status[workflow_id] = {
                "name": workflow.workflow_name,
                "total_executions": workflow.total_executions,
                "success_rate": (workflow.successful_executions / workflow.total_executions)
                               if workflow.total_executions > 0 else 0,
                "avg_execution_time_minutes": workflow.average_execution_time_minutes,
                "last_execution": workflow.last_execution_time
            }
        
        # Recent events analysis
        recent_events = [e for e in self.integration_events 
                        if e.event_timestamp > datetime.now() - timedelta(hours=24)]
        
        event_summary = {
            "total_events_24h": len(recent_events),
            "successful_events": len([e for e in recent_events if e.success]),
            "failed_events": len([e for e in recent_events if not e.success]),
            "avg_processing_time_ms": statistics.mean([e.processing_time_ms for e in recent_events]) 
                                    if recent_events else 0
        }
        
        return {
            "integration_overview": {
                "total_endpoints": total_endpoints,
                "active_endpoints": active_endpoints,
                "integration_health": (active_endpoints / total_endpoints) if total_endpoints > 0 else 0,
                "total_workflows": len(self.integration_workflows),
                "total_data_mappings": len(self.data_mappings)
            },
            "endpoint_status": endpoint_status,
            "workflow_status": workflow_status,
            "event_summary": event_summary,
            "system_performance": {
                "overall_availability": statistics.mean([ep.availability_sla for ep in self.system_endpoints.values()]) 
                                      if self.system_endpoints else 0,
                "average_data_quality": statistics.mean([ep.data_quality_score for ep in self.system_endpoints.values()])
                                       if self.system_endpoints else 0,
                "total_records_processed_24h": sum([e.records_processed for e in recent_events])
            }
        }

def run_demonstration() -> SystemIntegrationManager:
    """Run comprehensive system integration demonstration."""
    
    print("🔗 One Health System Integration Framework - Demonstration")
    print("=" * 75)
    
    manager = SystemIntegrationManager()
    
    print(f"\n🔗 Integration Infrastructure:")
    print(f"  System Endpoints: {len(manager.system_endpoints)}")
    print(f"  Integration Methods: {len(IntegrationMethod)}")
    print(f"  Supported Formats: {len(DataFormat)}")
    
    # Display registered systems
    print(f"\n🔗 Registered Systems:")
    for endpoint_id, endpoint in manager.system_endpoints.items():
        print(f"  {endpoint.endpoint_name} ({endpoint_id})")
        print(f"    Type: {endpoint.system_type.value.replace('_', ' ').title()}")
        print(f"    Method: {endpoint.integration_method.value.replace('_', ' ').title()}")
        print(f"    Formats: {', '.join([fmt.value.upper() for fmt in endpoint.supported_formats])}")
    
    print(f"\n🔗 Testing System Connectivity...")
    
    # Test connectivity to all systems
    connectivity_results = []
    for endpoint_id in manager.system_endpoints.keys():
        result = manager.test_system_connectivity(endpoint_id)
        connectivity_results.append(result)
        status_icon = "✅" if result["success"] else "❌"
        print(f"  {status_icon} {endpoint_id}: {result['response_time_ms']:.1f}ms")
    
    print(f"\n🔗 Creating Data Mappings...")
    
    # Create sample data mappings
    mapping_configs = [
        {
            "source": "surveillance_api", "target": "lab_lis", "name": "Surveillance to Lab Mapping",
            "mappings": {
                "case_id": "specimen_id",
                "patient_id": "patient_uuid", 
                "symptom_onset_date": "collection_date",
                "diagnosis": "test_request"
            }
        },
        {
            "source": "vet_health", "target": "surveillance_api", "name": "Veterinary to Surveillance Mapping",
            "mappings": {
                "animal_id": "case_id",
                "species": "host_species",
                "disease_status": "health_status",
                "farm_location": "location_coordinates"
            }
        },
        {
            "source": "env_monitor", "target": "agri_data", "name": "Environmental to Agricultural Mapping",
            "mappings": {
                "monitoring_station_id": "station_reference",
                "measurement_value": "environmental_reading",
                "timestamp": "observation_datetime",
                "parameter_type": "measurement_category"
            }
        }
    ]
    
    data_mappings = []
    for config in mapping_configs:
        mapping = manager.create_data_mapping(
            source_system=config["source"],
            target_system=config["target"],
            field_mappings=config["mappings"],
            mapping_name=config["name"]
        )
        data_mappings.append(mapping)
        print(f"  ✅ {mapping.mapping_name}: {len(mapping.field_mappings)} field mappings")
    
    print(f"\n🔗 Creating Integration Workflows...")
    
    # Create sample workflows
    workflow_configs = [
        {
            "workflow_name": "Real-time Surveillance Integration",
            "workflow_description": "Continuous integration of surveillance data across systems",
            "source_systems": ["surveillance_api", "vet_health"],
            "target_systems": ["response_coord", "lab_lis"],
            "trigger_type": "scheduled",
            "schedule_expression": "*/5 * * * *",  # Every 5 minutes
            "batch_size": 500
        },
        {
            "workflow_name": "Environmental-Agricultural Data Sync",
            "workflow_description": "Daily synchronization of environmental and agricultural data",
            "source_systems": ["env_monitor"],
            "target_systems": ["agri_data"],
            "trigger_type": "scheduled", 
            "schedule_expression": "0 2 * * *",  # Daily at 2 AM
            "batch_size": 2000
        },
        {
            "workflow_name": "Laboratory Results Distribution",
            "workflow_description": "Distribute laboratory results to relevant systems",
            "source_systems": ["lab_lis"],
            "target_systems": ["surveillance_api", "response_coord"],
            "trigger_type": "event",
            "batch_size": 100
        }
    ]
    
    workflows = []
    for config in workflow_configs:
        workflow = manager.create_integration_workflow(config)
        workflows.append(workflow)
        print(f"  ✅ {workflow.workflow_name}: {len(workflow.processing_steps)} steps")
    
    print(f"\n🔗 Executing Integration Workflows...")
    
    # Execute workflows (simulated)
    import asyncio
    
    async def execute_all_workflows():
        execution_results = []
        for workflow in workflows:
            result = await manager.execute_workflow(workflow.workflow_id)
            execution_results.append(result)
            success_icon = "✅" if result["success"] else "❌"
            print(f"  {success_icon} {workflow.workflow_name}: {result['records_processed']} records processed")
        return execution_results
    
    # Run the async function
    execution_results = asyncio.run(execute_all_workflows())
    
    return manager

def display_integration_results(manager: SystemIntegrationManager):
    """Display comprehensive integration results."""
    
    status = manager.get_integration_status()
    
    print(f"\n🔗 System Integration Results:")
    
    # Integration overview
    overview = status["integration_overview"]
    print(f"\n📊 Integration Overview:")
    print(f"  Total Endpoints: {overview['total_endpoints']}")
    print(f"  Active Endpoints: {overview['active_endpoints']}")
    print(f"  Integration Health: {overview['integration_health']:.1%}")
    print(f"  Total Workflows: {overview['total_workflows']}")
    print(f"  Data Mappings: {overview['total_data_mappings']}")
    
    # System performance
    performance = status["system_performance"]
    print(f"\n📈 System Performance:")
    print(f"  Overall Availability: {performance['overall_availability']:.1%}")
    print(f"  Average Data Quality: {performance['average_data_quality']:.1%}")
    print(f"  Records Processed (24h): {performance['total_records_processed_24h']:,}")
    
    # Endpoint status
    print(f"\n🔗 Endpoint Status:")
    for endpoint_id, endpoint_info in status["endpoint_status"].items():
        status_icon = "✅" if endpoint_info["status"] == "active" else "❌"
        print(f"  {status_icon} {endpoint_info['name']}:")
        print(f"    Type: {endpoint_info['type'].replace('_', ' ').title()}")
        print(f"    Success Rate: {endpoint_info['success_rate']:.1%}")
        print(f"    Response Time: {endpoint_info['avg_response_time_ms']:.1f}ms")
        print(f"    Data Quality: {endpoint_info['data_quality_score']:.1%}")
    
    # Workflow status
    print(f"\n⚙️ Workflow Status:")
    for workflow_id, workflow_info in status["workflow_status"].items():
        print(f"  {workflow_info['name']}:")
        print(f"    Executions: {workflow_info['total_executions']}")
        print(f"    Success Rate: {workflow_info['success_rate']:.1%}")
        print(f"    Avg Execution Time: {workflow_info['avg_execution_time_minutes']:.1f} minutes")
        if workflow_info["last_execution"]:
            print(f"    Last Execution: {workflow_info['last_execution'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Data mappings
    print(f"\n🗂️ Data Mappings ({len(manager.data_mappings)}):")
    for mapping_id, mapping in manager.data_mappings.items():
        print(f"  {mapping.mapping_name}:")
        print(f"    Source: {mapping.source_system}")
        print(f"    Target: {mapping.target_system}")
        print(f"    Field Mappings: {len(mapping.field_mappings)}")
        print(f"    Confidence: {mapping.mapping_confidence:.1%}")
        print(f"    Accuracy: {mapping.transformation_accuracy:.1%}")
    
    # Event summary
    events = status["event_summary"]
    print(f"\n📋 Event Summary (24h):")
    print(f"  Total Events: {events['total_events_24h']}")
    print(f"  Successful Events: {events['successful_events']}")
    print(f"  Failed Events: {events['failed_events']}")
    if events['total_events_24h'] > 0:
        success_rate = (events['successful_events'] / events['total_events_24h']) * 100
        print(f"  Success Rate: {success_rate:.1f}%")
    print(f"  Avg Processing Time: {events['avg_processing_time_ms']:.1f}ms")
    
    # Top performing systems
    print(f"\n🏆 TOP PERFORMING Systems:")
    endpoint_performance = [
        (ep_id, ep_info["success_rate"]) 
        for ep_id, ep_info in status["endpoint_status"].items()
    ]
    top_systems = sorted(endpoint_performance, key=lambda x: x[1], reverse=True)[:3]
    
    for i, (endpoint_id, success_rate) in enumerate(top_systems, 1):
        endpoint = manager.system_endpoints[endpoint_id]
        print(f"  {i}. {endpoint.endpoint_name}")
        print(f"     Success Rate: {success_rate:.1%}")
        print(f"     Response Time: {endpoint.average_response_time_ms:.1f}ms")
        print(f"     Data Quality: {endpoint.data_quality_score:.1%}")

if __name__ == "__main__":
    # Run comprehensive demonstration
    integration_manager = run_demonstration()
    display_integration_results(integration_manager)
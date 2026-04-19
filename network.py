"""
Network Analysis System
=======================
Module 3: Analysis & Modeling Tools

Advanced network analysis system for One Health surveillance, providing
transmission network mapping, contact tracing, and network epidemiology analysis.

NIW Focus: Network intelligence revealing disease transmission pathways and contact patterns.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable, Set
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import itertools
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetworkType(Enum):
    """Types of networks."""
    TRANSMISSION = "transmission"               # Disease transmission network
    CONTACT = "contact"                        # Contact tracing network
    TRADE = "trade"                           # Trade/movement network
    SPATIAL = "spatial"                       # Geographic proximity network
    TEMPORAL = "temporal"                     # Time-based connections
    HYBRID = "hybrid"                         # Combined network types

class NodeType(Enum):
    """Types of network nodes."""
    FARM = "farm"                             # Animal production facility
    HUMAN = "human"                           # Human case/contact
    FACILITY = "facility"                     # Healthcare/veterinary facility
    LOCATION = "location"                     # Geographic location
    VECTOR = "vector"                         # Disease vector
    ENVIRONMENT = "environment"               # Environmental source

class EdgeType(Enum):
    """Types of network edges/connections."""
    DIRECT_TRANSMISSION = "direct_transmission"    # Direct disease transmission
    INDIRECT_TRANSMISSION = "indirect_transmission" # Indirect transmission
    CONTACT = "contact"                           # Physical contact
    MOVEMENT = "movement"                         # Movement/trade connection
    PROXIMITY = "proximity"                       # Geographic proximity
    TEMPORAL = "temporal"                         # Time-based association

@dataclass
class NetworkNode:
    """Represents a node in the network."""
    node_id: str
    node_type: NodeType
    attributes: Dict[str, Any]
    
    # Geographic information
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Temporal information
    first_detection: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    
    # Node characteristics
    risk_level: Optional[str] = None          # "low", "medium", "high", "critical"
    case_count: int = 0
    population_size: Optional[int] = None
    
    # Network metrics (calculated)
    degree_centrality: Optional[float] = None
    betweenness_centrality: Optional[float] = None
    eigenvector_centrality: Optional[float] = None
    clustering_coefficient: Optional[float] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.attributes is None:
            self.attributes = {}

@dataclass
class NetworkEdge:
    """Represents an edge/connection in the network."""
    edge_id: str
    source_node: str
    target_node: str
    edge_type: EdgeType
    
    # Edge characteristics
    weight: float = 1.0                       # Connection strength
    confidence: Optional[float] = None        # Confidence in connection
    temporal_window_days: Optional[int] = None # Time window for connection
    
    # Transmission characteristics
    transmission_probability: Optional[float] = None
    transmission_rate: Optional[float] = None
    latency_days: Optional[int] = None       # Transmission delay
    
    # Temporal information
    connection_date: Optional[datetime] = None
    last_transmission: Optional[datetime] = None
    
    # Evidence supporting connection
    evidence_strength: str = "medium"        # "weak", "medium", "strong"
    evidence_sources: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.evidence_sources is None:
            self.evidence_sources = []

@dataclass
class NetworkCluster:
    """Represents a cluster within the network."""
    cluster_id: str
    cluster_type: str                         # "component", "community", "outbreak"
    nodes: List[str]
    edges: List[str]
    
    # Cluster characteristics
    cluster_size: int = 0
    cluster_density: Optional[float] = None
    cluster_cohesion: Optional[float] = None
    
    # Temporal characteristics
    cluster_start_date: Optional[datetime] = None
    cluster_end_date: Optional[datetime] = None
    cluster_duration_days: Optional[int] = None
    
    # Geographic characteristics
    geographic_radius_km: Optional[float] = None
    geographic_center: Optional[Tuple[float, float]] = None
    
    # Epidemiological characteristics
    total_cases: int = 0
    attack_rate: Optional[float] = None
    generation_time: Optional[float] = None
    
    def __post_init__(self):
        """Calculate derived metrics."""
        self.cluster_size = len(self.nodes)
        
        if self.cluster_start_date and self.cluster_end_date:
            self.cluster_duration_days = (self.cluster_end_date - self.cluster_start_date).days

@dataclass
class NetworkAnalysisResult:
    """Result of network analysis."""
    
    analysis_id: str
    network_type: NetworkType
    analysis_timestamp: datetime
    
    # Network structure
    total_nodes: int
    total_edges: int
    network_density: float
    average_degree: float
    
    # Network components
    connected_components: int
    largest_component_size: int
    clusters_detected: List[NetworkCluster]
    
    # Network metrics
    diameter: Optional[int] = None            # Network diameter
    average_path_length: Optional[float] = None
    global_clustering_coefficient: Optional[float] = None
    assortativity: Optional[float] = None     # Degree correlation
    
    # Centrality analysis
    most_central_nodes: List[Tuple[str, float]] = None  # (node_id, centrality_score)
    bridge_nodes: List[str] = None            # Critical bridge nodes
    hub_nodes: List[str] = None               # Highly connected hubs
    
    # Transmission analysis
    transmission_paths: List[List[str]] = None # Likely transmission paths
    super_spreader_nodes: List[str] = None    # High transmission potential
    bottleneck_nodes: List[str] = None        # Network bottlenecks
    
    # Temporal analysis
    network_evolution: Optional[Dict[str, int]] = None  # Time-based changes
    outbreak_timeline: List[Tuple[datetime, str]] = None # Key events
    
    # Performance metrics
    analysis_duration_seconds: float = 0.0
    
    # Key insights
    key_findings: List[str] = None
    risk_assessment: List[str] = None
    intervention_recommendations: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.most_central_nodes is None:
            self.most_central_nodes = []
        if self.bridge_nodes is None:
            self.bridge_nodes = []
        if self.hub_nodes is None:
            self.hub_nodes = []
        if self.transmission_paths is None:
            self.transmission_paths = []
        if self.super_spreader_nodes is None:
            self.super_spreader_nodes = []
        if self.bottleneck_nodes is None:
            self.bottleneck_nodes = []
        if self.outbreak_timeline is None:
            self.outbreak_timeline = []
        if self.key_findings is None:
            self.key_findings = []
        if self.risk_assessment is None:
            self.risk_assessment = []
        if self.intervention_recommendations is None:
            self.intervention_recommendations = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['network_type'] = self.network_type.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        
        # Convert clusters
        data['clusters_detected'] = [
            {
                'cluster_id': c.cluster_id,
                'cluster_type': c.cluster_type,
                'cluster_size': c.cluster_size,
                'total_cases': c.total_cases,
                'cluster_duration_days': c.cluster_duration_days,
                'geographic_radius_km': c.geographic_radius_km
            }
            for c in self.clusters_detected
        ]
        
        # Convert outbreak timeline
        if self.outbreak_timeline:
            data['outbreak_timeline'] = [
                (dt.isoformat(), event) for dt, event in self.outbreak_timeline
            ]
        
        return data

class NetworkBuilder:
    """Builds networks from surveillance data."""
    
    @staticmethod
    def build_transmission_network(animal_data: List[Dict],
                                 human_data: List[Dict],
                                 max_distance_km: float = 50.0,
                                 max_time_window_days: int = 14) -> Tuple[List[NetworkNode], List[NetworkEdge]]:
        """Build transmission network from surveillance data."""
        
        nodes = []
        edges = []
        
        # Create nodes from animal data
        for record in animal_data:
            node_id = record.get('animal_id', f"ANIMAL_{len(nodes)}")
            
            node = NetworkNode(
                node_id=node_id,
                node_type=NodeType.FARM,
                attributes=record,
                latitude=record.get('location_lat'),
                longitude=record.get('location_lon'),
                first_detection=NetworkBuilder._parse_timestamp(record.get('timestamp')),
                case_count=record.get('mortality_count', 0),
                risk_level=NetworkBuilder._assess_risk_level(record.get('mortality_count', 0), "animal")
            )
            
            nodes.append(node)
        
        # Create nodes from human data
        for record in human_data:
            node_id = record.get('case_id', f"HUMAN_{len(nodes)}")
            
            node = NetworkNode(
                node_id=node_id,
                node_type=NodeType.HUMAN,
                attributes=record,
                latitude=record.get('location_lat'),
                longitude=record.get('location_lon'),
                first_detection=NetworkBuilder._parse_timestamp(record.get('timestamp')),
                case_count=record.get('case_count', 1),
                risk_level=NetworkBuilder._assess_risk_level_human(record.get('severity', "mild"))
            )
            
            nodes.append(node)
        
        # Create edges based on spatial and temporal proximity
        edge_id = 0
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                
                # Check temporal window
                if (node1.first_detection and node2.first_detection and
                    abs((node2.first_detection - node1.first_detection).days) <= max_time_window_days):
                    
                    # Check spatial proximity
                    if (node1.latitude and node1.longitude and 
                        node2.latitude and node2.longitude):
                        
                        distance = NetworkBuilder._haversine_distance(
                            node1.latitude, node1.longitude,
                            node2.latitude, node2.longitude
                        )
                        
                        if distance <= max_distance_km:
                            # Determine edge type and weight
                            edge_type, weight, transmission_prob = NetworkBuilder._determine_edge_characteristics(
                                node1, node2, distance
                            )
                            
                            edge = NetworkEdge(
                                edge_id=f"EDGE_{edge_id}",
                                source_node=node1.node_id,
                                target_node=node2.node_id,
                                edge_type=edge_type,
                                weight=weight,
                                transmission_probability=transmission_prob,
                                temporal_window_days=abs((node2.first_detection - node1.first_detection).days),
                                connection_date=min(node1.first_detection, node2.first_detection),
                                evidence_strength=NetworkBuilder._assess_evidence_strength(distance, abs((node2.first_detection - node1.first_detection).days))
                            )
                            
                            edges.append(edge)
                            edge_id += 1
        
        return nodes, edges
    
    @staticmethod
    def build_contact_network(human_data: List[Dict],
                            contact_radius_km: float = 5.0,
                            contact_window_days: int = 7) -> Tuple[List[NetworkNode], List[NetworkEdge]]:
        """Build contact tracing network."""
        
        nodes = []
        edges = []
        
        # Create human nodes
        for record in human_data:
            node_id = record.get('case_id', f"CONTACT_{len(nodes)}")
            
            # Simulate contact information
            household_size = random.randint(2, 6)
            occupation_risk = random.choice(["low", "medium", "high"])
            
            attributes = record.copy()
            attributes.update({
                'household_size': household_size,
                'occupation_risk': occupation_risk,
                'daily_contacts': random.randint(5, 50) if occupation_risk == "high" else random.randint(2, 15)
            })
            
            node = NetworkNode(
                node_id=node_id,
                node_type=NodeType.HUMAN,
                attributes=attributes,
                latitude=record.get('location_lat'),
                longitude=record.get('location_lon'),
                first_detection=NetworkBuilder._parse_timestamp(record.get('timestamp')),
                case_count=1,
                population_size=household_size,
                risk_level=NetworkBuilder._assess_risk_level_human(record.get('severity', "mild"))
            )
            
            nodes.append(node)
        
        # Create contact edges
        edge_id = 0
        
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes[i+1:], i+1):
                
                # Contact likelihood based on proximity and timing
                if (node1.first_detection and node2.first_detection and
                    abs((node2.first_detection - node1.first_detection).days) <= contact_window_days):
                    
                    if (node1.latitude and node1.longitude and 
                        node2.latitude and node2.longitude):
                        
                        distance = NetworkBuilder._haversine_distance(
                            node1.latitude, node1.longitude,
                            node2.latitude, node2.longitude
                        )
                        
                        # Contact probability decreases with distance
                        contact_probability = max(0, 1 - (distance / contact_radius_km))
                        
                        # Higher contact probability for high-risk occupations
                        if (node1.attributes.get('occupation_risk') == "high" or 
                            node2.attributes.get('occupation_risk') == "high"):
                            contact_probability *= 2.0
                        
                        if contact_probability > 0.3:  # Threshold for meaningful contact
                            edge = NetworkEdge(
                                edge_id=f"CONTACT_{edge_id}",
                                source_node=node1.node_id,
                                target_node=node2.node_id,
                                edge_type=EdgeType.CONTACT,
                                weight=contact_probability,
                                transmission_probability=contact_probability * 0.5,  # 50% transmission efficiency
                                temporal_window_days=abs((node2.first_detection - node1.first_detection).days),
                                connection_date=min(node1.first_detection, node2.first_detection),
                                evidence_strength="strong" if contact_probability > 0.7 else "medium"
                            )
                            
                            edges.append(edge)
                            edge_id += 1
        
        return nodes, edges
    
    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp string to datetime."""
        if not timestamp_str:
            return None
        
        try:
            return datetime.fromisoformat(timestamp_str[:19])
        except ValueError:
            return None
    
    @staticmethod
    def _assess_risk_level(case_count: int, domain: str) -> str:
        """Assess risk level based on case count."""
        if domain == "animal":
            if case_count >= 20:
                return "critical"
            elif case_count >= 10:
                return "high"
            elif case_count >= 5:
                return "medium"
            else:
                return "low"
        else:
            if case_count >= 10:
                return "critical"
            elif case_count >= 5:
                return "high"
            elif case_count >= 2:
                return "medium"
            else:
                return "low"
    
    @staticmethod
    def _assess_risk_level_human(severity: str) -> str:
        """Assess risk level based on severity."""
        severity_lower = severity.lower()
        if severity_lower == "critical":
            return "critical"
        elif severity_lower == "severe":
            return "high"
        elif severity_lower == "moderate":
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers."""
        R = 6371.0  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    @staticmethod
    def _determine_edge_characteristics(node1: NetworkNode, node2: NetworkNode, 
                                      distance: float) -> Tuple[EdgeType, float, float]:
        """Determine edge characteristics based on nodes and distance."""
        
        # Determine edge type
        if node1.node_type == NodeType.FARM and node2.node_type == NodeType.FARM:
            edge_type = EdgeType.INDIRECT_TRANSMISSION  # Farm-to-farm transmission
        elif node1.node_type == NodeType.HUMAN and node2.node_type == NodeType.HUMAN:
            edge_type = EdgeType.DIRECT_TRANSMISSION    # Human-to-human transmission
        elif ((node1.node_type == NodeType.FARM and node2.node_type == NodeType.HUMAN) or
              (node1.node_type == NodeType.HUMAN and node2.node_type == NodeType.FARM)):
            edge_type = EdgeType.DIRECT_TRANSMISSION    # Zoonotic transmission
        else:
            edge_type = EdgeType.PROXIMITY
        
        # Calculate weight (inverse of distance)
        weight = max(0.1, 1.0 - (distance / 50.0))  # Normalize by max distance
        
        # Calculate transmission probability
        if edge_type == EdgeType.DIRECT_TRANSMISSION:
            transmission_prob = weight * 0.7  # Higher probability for direct transmission
        else:
            transmission_prob = weight * 0.3  # Lower probability for indirect
        
        return edge_type, weight, transmission_prob
    
    @staticmethod
    def _assess_evidence_strength(distance: float, time_diff_days: int) -> str:
        """Assess strength of evidence for connection."""
        
        # Closer in space and time = stronger evidence
        distance_score = max(0, 1 - (distance / 20.0))
        time_score = max(0, 1 - (time_diff_days / 7.0))
        
        combined_score = (distance_score + time_score) / 2
        
        if combined_score >= 0.7:
            return "strong"
        elif combined_score >= 0.4:
            return "medium"
        else:
            return "weak"

class NetworkAnalyzer:
    """Analyzes network structure and characteristics."""
    
    @staticmethod
    def analyze_network_structure(nodes: List[NetworkNode], 
                                edges: List[NetworkEdge]) -> Dict[str, Any]:
        """Analyze basic network structure."""
        
        if not nodes:
            return {}
        
        # Build adjacency list
        adjacency = defaultdict(set)
        node_degrees = defaultdict(int)
        
        for edge in edges:
            adjacency[edge.source_node].add(edge.target_node)
            adjacency[edge.target_node].add(edge.source_node)
            node_degrees[edge.source_node] += 1
            node_degrees[edge.target_node] += 1
        
        # Basic metrics
        total_nodes = len(nodes)
        total_edges = len(edges)
        
        # Network density
        max_possible_edges = total_nodes * (total_nodes - 1) / 2
        network_density = total_edges / max_possible_edges if max_possible_edges > 0 else 0
        
        # Average degree
        total_degree = sum(node_degrees.values())
        average_degree = total_degree / total_nodes if total_nodes > 0 else 0
        
        # Connected components
        components = NetworkAnalyzer._find_connected_components(nodes, adjacency)
        largest_component_size = max(len(comp) for comp in components) if components else 0
        
        # Clustering coefficient
        clustering_coefficient = NetworkAnalyzer._calculate_clustering_coefficient(adjacency)
        
        return {
            'total_nodes': total_nodes,
            'total_edges': total_edges,
            'network_density': network_density,
            'average_degree': average_degree,
            'connected_components': len(components),
            'largest_component_size': largest_component_size,
            'global_clustering_coefficient': clustering_coefficient,
            'degree_distribution': dict(node_degrees)
        }
    
    @staticmethod
    def calculate_centrality_measures(nodes: List[NetworkNode], 
                                    edges: List[NetworkEdge]) -> Dict[str, Dict[str, float]]:
        """Calculate centrality measures for nodes."""
        
        if not nodes or not edges:
            return {}
        
        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge.source_node].add(edge.target_node)
            adjacency[edge.target_node].add(edge.source_node)
        
        node_ids = [node.node_id for node in nodes]
        centrality_measures = {}
        
        # Degree centrality
        degree_centrality = {}
        for node_id in node_ids:
            degree = len(adjacency[node_id])
            normalized_degree = degree / (len(nodes) - 1) if len(nodes) > 1 else 0
            degree_centrality[node_id] = normalized_degree
        
        # Betweenness centrality (simplified)
        betweenness_centrality = NetworkAnalyzer._calculate_betweenness_centrality(node_ids, adjacency)
        
        # Combine measures
        for node_id in node_ids:
            centrality_measures[node_id] = {
                'degree': degree_centrality.get(node_id, 0),
                'betweenness': betweenness_centrality.get(node_id, 0)
            }
        
        return centrality_measures
    
    @staticmethod
    def identify_key_nodes(nodes: List[NetworkNode], 
                          edges: List[NetworkEdge],
                          centrality_measures: Dict[str, Dict[str, float]]) -> Dict[str, List[str]]:
        """Identify key nodes in the network."""
        
        key_nodes = {
            'hubs': [],
            'bridges': [],
            'super_spreaders': []
        }
        
        if not centrality_measures:
            return key_nodes
        
        # Sort nodes by degree centrality for hubs
        degree_sorted = sorted(centrality_measures.items(), 
                             key=lambda x: x[1]['degree'], reverse=True)
        
        # Top 20% as hubs
        hub_count = max(1, len(degree_sorted) // 5)
        key_nodes['hubs'] = [node_id for node_id, _ in degree_sorted[:hub_count]]
        
        # Sort nodes by betweenness centrality for bridges
        betweenness_sorted = sorted(centrality_measures.items(),
                                  key=lambda x: x[1]['betweenness'], reverse=True)
        
        # Top nodes with high betweenness as bridges
        bridge_threshold = 0.1
        key_nodes['bridges'] = [node_id for node_id, measures in betweenness_sorted 
                               if measures['betweenness'] > bridge_threshold]
        
        # Identify super spreaders (high degree + high case count)
        node_dict = {node.node_id: node for node in nodes}
        
        for node_id, measures in centrality_measures.items():
            node = node_dict.get(node_id)
            if node and measures['degree'] > 0.3 and node.case_count > 5:
                key_nodes['super_spreaders'].append(node_id)
        
        return key_nodes
    
    @staticmethod
    def detect_network_clusters(nodes: List[NetworkNode], 
                              edges: List[NetworkEdge]) -> List[NetworkCluster]:
        """Detect clusters/communities in the network."""
        
        if not nodes or not edges:
            return []
        
        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge.source_node].add(edge.target_node)
            adjacency[edge.target_node].add(edge.source_node)
        
        # Find connected components as clusters
        components = NetworkAnalyzer._find_connected_components(nodes, adjacency)
        
        clusters = []
        node_dict = {node.node_id: node for node in nodes}
        edge_dict = {(edge.source_node, edge.target_node): edge for edge in edges}
        
        for i, component in enumerate(components):
            if len(component) >= 3:  # Minimum cluster size
                cluster_nodes = list(component)
                
                # Find edges within cluster
                cluster_edges = []
                for edge in edges:
                    if edge.source_node in component and edge.target_node in component:
                        cluster_edges.append(edge.edge_id)
                
                # Calculate cluster characteristics
                total_cases = sum(node_dict[node_id].case_count for node_id in cluster_nodes 
                                if node_id in node_dict)
                
                # Calculate geographic characteristics
                cluster_lats = [node_dict[node_id].latitude for node_id in cluster_nodes 
                               if node_id in node_dict and node_dict[node_id].latitude]
                cluster_lons = [node_dict[node_id].longitude for node_id in cluster_nodes 
                               if node_id in node_dict and node_dict[node_id].longitude]
                
                if cluster_lats and cluster_lons:
                    center_lat = statistics.mean(cluster_lats)
                    center_lon = statistics.mean(cluster_lons)
                    geographic_center = (center_lat, center_lon)
                    
                    # Calculate cluster radius
                    distances = []
                    for lat, lon in zip(cluster_lats, cluster_lons):
                        distance = NetworkBuilder._haversine_distance(center_lat, center_lon, lat, lon)
                        distances.append(distance)
                    geographic_radius = max(distances) if distances else 0
                else:
                    geographic_center = None
                    geographic_radius = None
                
                # Temporal characteristics
                detection_dates = [node_dict[node_id].first_detection for node_id in cluster_nodes 
                                 if node_id in node_dict and node_dict[node_id].first_detection]
                
                if detection_dates:
                    start_date = min(detection_dates)
                    end_date = max(detection_dates)
                else:
                    start_date = None
                    end_date = None
                
                # Calculate cluster density
                cluster_size = len(cluster_nodes)
                possible_edges = cluster_size * (cluster_size - 1) / 2
                actual_edges = len(cluster_edges)
                cluster_density = actual_edges / possible_edges if possible_edges > 0 else 0
                
                cluster = NetworkCluster(
                    cluster_id=f"CLUSTER_{i+1}",
                    cluster_type="component",
                    nodes=cluster_nodes,
                    edges=cluster_edges,
                    cluster_density=cluster_density,
                    cluster_start_date=start_date,
                    cluster_end_date=end_date,
                    geographic_radius_km=geographic_radius,
                    geographic_center=geographic_center,
                    total_cases=total_cases
                )
                
                clusters.append(cluster)
        
        return clusters
    
    @staticmethod
    def _find_connected_components(nodes: List[NetworkNode], 
                                 adjacency: Dict[str, Set[str]]) -> List[Set[str]]:
        """Find connected components using DFS."""
        
        visited = set()
        components = []
        
        for node in nodes:
            node_id = node.node_id
            if node_id not in visited:
                component = set()
                stack = [node_id]
                
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        component.add(current)
                        
                        for neighbor in adjacency[current]:
                            if neighbor not in visited:
                                stack.append(neighbor)
                
                components.append(component)
        
        return components
    
    @staticmethod
    def _calculate_clustering_coefficient(adjacency: Dict[str, Set[str]]) -> float:
        """Calculate global clustering coefficient."""
        
        if not adjacency:
            return 0.0
        
        total_clustering = 0.0
        valid_nodes = 0
        
        for node, neighbors in adjacency.items():
            if len(neighbors) < 2:
                continue
            
            valid_nodes += 1
            
            # Count triangles
            triangles = 0
            possible_triangles = len(neighbors) * (len(neighbors) - 1) / 2
            
            neighbors_list = list(neighbors)
            for i in range(len(neighbors_list)):
                for j in range(i + 1, len(neighbors_list)):
                    neighbor1 = neighbors_list[i]
                    neighbor2 = neighbors_list[j]
                    
                    if neighbor2 in adjacency[neighbor1]:
                        triangles += 1
            
            local_clustering = triangles / possible_triangles if possible_triangles > 0 else 0
            total_clustering += local_clustering
        
        return total_clustering / valid_nodes if valid_nodes > 0 else 0.0
    
    @staticmethod
    def _calculate_betweenness_centrality(node_ids: List[str], 
                                        adjacency: Dict[str, Set[str]]) -> Dict[str, float]:
        """Calculate betweenness centrality (simplified version)."""
        
        betweenness = {node_id: 0.0 for node_id in node_ids}
        
        # For each pair of nodes, find shortest path and count passages
        for source in node_ids:
            for target in node_ids:
                if source != target:
                    path = NetworkAnalyzer._find_shortest_path(source, target, adjacency)
                    
                    if path and len(path) > 2:
                        # Add 1 to betweenness of intermediate nodes
                        for intermediate in path[1:-1]:
                            betweenness[intermediate] += 1.0
        
        # Normalize
        n = len(node_ids)
        normalizer = (n - 1) * (n - 2) / 2 if n > 2 else 1
        
        for node_id in betweenness:
            betweenness[node_id] /= normalizer
        
        return betweenness
    
    @staticmethod
    def _find_shortest_path(start: str, end: str, adjacency: Dict[str, Set[str]]) -> Optional[List[str]]:
        """Find shortest path between two nodes using BFS."""
        
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            
            for neighbor in adjacency[node]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

class OneHealthNetworkAnalyzer:
    """Main network analyzer for One Health surveillance."""
    
    def __init__(self):
        self.analysis_results: List[NetworkAnalysisResult] = []
        self.networks: Dict[str, Tuple[List[NetworkNode], List[NetworkEdge]]] = {}
        self.analysis_log: List[Dict] = []
        
        logger.info("One Health Network Analyzer initialized")
    
    def comprehensive_network_analysis(self, animal_data: List[Dict],
                                     human_data: List[Dict],
                                     environmental_data: List[Dict] = None) -> List[NetworkAnalysisResult]:
        """Perform comprehensive network analysis across domains."""
        
        analysis_start = datetime.now()
        results = []
        
        logger.info(f"Starting comprehensive network analysis")
        
        # Build different types of networks
        
        # 1. Transmission network (animal + human)
        if animal_data and human_data:
            try:
                trans_nodes, trans_edges = NetworkBuilder.build_transmission_network(
                    animal_data, human_data
                )
                
                if trans_nodes and trans_edges:
                    self.networks['transmission'] = (trans_nodes, trans_edges)
                    
                    result = self._analyze_network(trans_nodes, trans_edges, 
                                                 NetworkType.TRANSMISSION, "transmission")
                    if result:
                        results.append(result)
                        
            except Exception as e:
                logger.error(f"Error in transmission network analysis: {e}")
        
        # 2. Contact network (human only)
        if human_data:
            try:
                contact_nodes, contact_edges = NetworkBuilder.build_contact_network(human_data)
                
                if contact_nodes and contact_edges:
                    self.networks['contact'] = (contact_nodes, contact_edges)
                    
                    result = self._analyze_network(contact_nodes, contact_edges,
                                                 NetworkType.CONTACT, "contact")
                    if result:
                        results.append(result)
                        
            except Exception as e:
                logger.error(f"Error in contact network analysis: {e}")
        
        # Store results
        self.analysis_results.extend(results)
        
        # Log performance
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "networks_analyzed": len(results),
            "total_nodes": sum(r.total_nodes for r in results),
            "total_edges": sum(r.total_edges for r in results),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data) if environmental_data else 0
            }
        })
        
        logger.info(f"Network analysis completed: {len(results)} networks in {analysis_time:.2f}s")
        
        return results
    
    def _analyze_network(self, nodes: List[NetworkNode], edges: List[NetworkEdge],
                        network_type: NetworkType, network_name: str) -> Optional[NetworkAnalysisResult]:
        """Analyze a specific network."""
        
        analysis_start = datetime.now()
        
        # Basic network structure
        structure_analysis = NetworkAnalyzer.analyze_network_structure(nodes, edges)
        
        # Centrality measures
        centrality_measures = NetworkAnalyzer.calculate_centrality_measures(nodes, edges)
        
        # Key nodes identification
        key_nodes = NetworkAnalyzer.identify_key_nodes(nodes, edges, centrality_measures)
        
        # Cluster detection
        clusters = NetworkAnalyzer.detect_network_clusters(nodes, edges)
        
        # Update node centrality values
        for node in nodes:
            if node.node_id in centrality_measures:
                measures = centrality_measures[node.node_id]
                node.degree_centrality = measures['degree']
                node.betweenness_centrality = measures['betweenness']
        
        # Generate key findings
        key_findings = []
        
        if structure_analysis.get('network_density', 0) > 0.3:
            key_findings.append("High network density indicates extensive connections")
        
        if structure_analysis.get('connected_components', 0) > 1:
            key_findings.append(f"Network fragmented into {structure_analysis['connected_components']} components")
        
        if key_nodes['super_spreaders']:
            key_findings.append(f"Identified {len(key_nodes['super_spreaders'])} potential super-spreader nodes")
        
        if clusters:
            total_cluster_cases = sum(c.total_cases for c in clusters)
            key_findings.append(f"Detected {len(clusters)} transmission clusters with {total_cluster_cases} total cases")
        
        # Risk assessment
        risk_assessment = []
        
        high_risk_nodes = [node for node in nodes if node.risk_level in ["high", "critical"]]
        if high_risk_nodes:
            risk_assessment.append(f"{len(high_risk_nodes)} high/critical risk nodes detected")
        
        if key_nodes['bridges']:
            risk_assessment.append("Critical bridge nodes present - removal would fragment network")
        
        large_clusters = [c for c in clusters if c.cluster_size > 5]
        if large_clusters:
            risk_assessment.append(f"{len(large_clusters)} large transmission clusters detected")
        
        # Intervention recommendations
        recommendations = []
        
        if key_nodes['hubs']:
            recommendations.append("Target hub nodes for surveillance intensification")
        
        if key_nodes['super_spreaders']:
            recommendations.append("Implement strict isolation for potential super-spreaders")
        
        if structure_analysis.get('network_density', 0) > 0.5:
            recommendations.append("High connectivity - consider broad intervention strategies")
        
        if clusters:
            recommendations.append("Implement cluster-specific containment measures")
        
        # Generate outbreak timeline
        outbreak_timeline = []
        all_dates = []
        
        for node in nodes:
            if node.first_detection:
                all_dates.append((node.first_detection, f"Detection at {node.node_id}"))
        
        # Sort by date and take key events
        all_dates.sort()
        outbreak_timeline = all_dates[:10]  # First 10 events
        
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        
        result = NetworkAnalysisResult(
            analysis_id=f"NETWORK_{network_name.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            network_type=network_type,
            analysis_timestamp=analysis_start,
            total_nodes=structure_analysis.get('total_nodes', 0),
            total_edges=structure_analysis.get('total_edges', 0),
            network_density=structure_analysis.get('network_density', 0),
            average_degree=structure_analysis.get('average_degree', 0),
            connected_components=structure_analysis.get('connected_components', 0),
            largest_component_size=structure_analysis.get('largest_component_size', 0),
            clusters_detected=clusters,
            global_clustering_coefficient=structure_analysis.get('global_clustering_coefficient'),
            most_central_nodes=[(node_id, measures['degree']) 
                              for node_id, measures in sorted(centrality_measures.items(),
                                                             key=lambda x: x[1]['degree'], reverse=True)[:5]],
            hub_nodes=key_nodes['hubs'],
            bridge_nodes=key_nodes['bridges'],
            super_spreader_nodes=key_nodes['super_spreaders'],
            outbreak_timeline=outbreak_timeline,
            analysis_duration_seconds=analysis_duration,
            key_findings=key_findings,
            risk_assessment=risk_assessment,
            intervention_recommendations=recommendations
        )
        
        return result
    
    def get_network_summary(self) -> Dict:
        """Get summary of network analysis results."""
        
        if not self.analysis_results:
            return {"message": "No network analyses performed"}
        
        # Aggregate statistics
        total_nodes = sum(r.total_nodes for r in self.analysis_results)
        total_edges = sum(r.total_edges for r in self.analysis_results)
        total_clusters = sum(len(r.clusters_detected) for r in self.analysis_results)
        
        # Network types analyzed
        network_types = [r.network_type.value for r in self.analysis_results]
        
        # Key nodes summary
        total_hubs = sum(len(r.hub_nodes) for r in self.analysis_results)
        total_bridges = sum(len(r.bridge_nodes) for r in self.analysis_results)
        total_super_spreaders = sum(len(r.super_spreader_nodes) for r in self.analysis_results)
        
        # Performance statistics
        analysis_times = [r.analysis_duration_seconds for r in self.analysis_results]
        
        return {
            "total_analyses": len(self.analysis_results),
            "network_types": network_types,
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "total_clusters": total_clusters,
            "key_nodes": {
                "hubs": total_hubs,
                "bridges": total_bridges,
                "super_spreaders": total_super_spreaders
            },
            "performance": {
                "average_analysis_time": statistics.mean(analysis_times) if analysis_times else 0,
                "total_analysis_time": sum(analysis_times)
            }
        }
    
    def get_high_risk_networks(self) -> List[Dict]:
        """Get networks with high transmission risk."""
        
        high_risk_networks = []
        
        for result in self.analysis_results:
            risk_score = 0
            
            # High density networks
            if result.network_density > 0.4:
                risk_score += 2
            
            # Large super-spreader count
            if len(result.super_spreader_nodes) > 2:
                risk_score += 3
            
            # Large clusters
            large_clusters = [c for c in result.clusters_detected if c.cluster_size > 5]
            if large_clusters:
                risk_score += len(large_clusters)
            
            # High connectivity
            if result.average_degree > 3:
                risk_score += 1
            
            if risk_score >= 3:  # Threshold for high risk
                high_risk_networks.append({
                    'analysis_id': result.analysis_id,
                    'network_type': result.network_type.value,
                    'risk_score': risk_score,
                    'total_nodes': result.total_nodes,
                    'network_density': result.network_density,
                    'super_spreaders': len(result.super_spreader_nodes),
                    'large_clusters': len(large_clusters)
                })
        
        return sorted(high_risk_networks, key=lambda x: x['risk_score'], reverse=True)

# Mock data generator
def generate_mock_network_data():
    """Generate mock network data for testing."""
    
    base_date = datetime.now() - timedelta(days=30)
    base_lat = 40.7128
    base_lon = -74.0060
    
    # Generate animal data with clustering
    animal_data = []
    
    # Cluster 1: Large outbreak
    for i in range(15):
        lat_offset = random.uniform(-0.02, 0.02)
        lon_offset = random.uniform(-0.02, 0.02)
        
        animal_data.append({
            "animal_id": f"NETWORK_FARM_{i:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(1, 10))).isoformat(),
            "location_lat": base_lat + 0.1 + lat_offset,
            "location_lon": base_lon + 0.1 + lon_offset,
            "species": "poultry",
            "mortality_count": random.randint(8, 25),
            "farm_type": "commercial",
            "movement_history": random.choice([True, False])
        })
    
    # Cluster 2: Medium outbreak
    for i in range(8):
        lat_offset = random.uniform(-0.015, 0.015)
        lon_offset = random.uniform(-0.015, 0.015)
        
        animal_data.append({
            "animal_id": f"NETWORK_FARM_{i+15:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(5, 15))).isoformat(),
            "location_lat": base_lat - 0.08 + lat_offset,
            "location_lon": base_lon - 0.08 + lon_offset,
            "species": "swine",
            "mortality_count": random.randint(3, 12),
            "farm_type": "backyard",
            "movement_history": random.choice([True, False])
        })
    
    # Isolated cases
    for i in range(5):
        lat_offset = random.uniform(-0.3, 0.3)
        lon_offset = random.uniform(-0.3, 0.3)
        
        animal_data.append({
            "animal_id": f"NETWORK_FARM_{i+23:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(10, 20))).isoformat(),
            "location_lat": base_lat + lat_offset,
            "location_lon": base_lon + lon_offset,
            "species": "cattle",
            "mortality_count": random.randint(1, 4),
            "farm_type": "dairy",
            "movement_history": False
        })
    
    # Generate human data correlated with animal outbreaks
    human_data = []
    
    # Cases near animal cluster 1
    for i in range(12):
        lat_offset = random.uniform(-0.03, 0.03)
        lon_offset = random.uniform(-0.03, 0.03)
        
        human_data.append({
            "case_id": f"NETWORK_HUM_{i:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(3, 12))).isoformat(),
            "location_lat": base_lat + 0.1 + lat_offset,
            "location_lon": base_lon + 0.1 + lon_offset,
            "case_classification": "confirmed",
            "case_count": 1,
            "severity": random.choice(["mild", "moderate", "severe"]),
            "occupation": random.choice(["farmer", "veterinarian", "healthcare_worker", "other"]),
            "animal_contact": random.choice([True, False])
        })
    
    # Cases near animal cluster 2
    for i in range(6):
        lat_offset = random.uniform(-0.025, 0.025)
        lon_offset = random.uniform(-0.025, 0.025)
        
        human_data.append({
            "case_id": f"NETWORK_HUM_{i+12:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(7, 18))).isoformat(),
            "location_lat": base_lat - 0.08 + lat_offset,
            "location_lon": base_lon - 0.08 + lon_offset,
            "case_classification": "probable",
            "case_count": 1,
            "severity": random.choice(["mild", "moderate"]),
            "occupation": random.choice(["farmer", "veterinarian", "other"]),
            "animal_contact": True
        })
    
    # Scattered human cases
    for i in range(4):
        lat_offset = random.uniform(-0.2, 0.2)
        lon_offset = random.uniform(-0.2, 0.2)
        
        human_data.append({
            "case_id": f"NETWORK_HUM_{i+18:03d}",
            "timestamp": (base_date + timedelta(days=random.randint(12, 25))).isoformat(),
            "location_lat": base_lat + lat_offset,
            "location_lon": base_lon + lon_offset,
            "case_classification": "suspected",
            "case_count": 1,
            "severity": "mild",
            "occupation": "other",
            "animal_contact": False
        })
    
    return animal_data, human_data

def run_demonstration():
    """Run demonstration of network analysis system."""
    print("🕸️ One Health Network Analysis System - Demonstration")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OneHealthNetworkAnalyzer()
    
    # Generate mock network data
    animal_data, human_data = generate_mock_network_data()
    
    print(f"\n🔗 Network Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    
    # Run comprehensive network analysis
    print(f"\n🕸️ Running Comprehensive Network Analysis...")
    results = analyzer.comprehensive_network_analysis(animal_data, human_data)
    
    # Display network analysis results
    print(f"\n📊 Network Analysis Results ({len(results)} total):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Network Analysis - {result.analysis_id}")
        print(f"   Network Type: {result.network_type.value.replace('_', ' ').title()}")
        print(f"   Total Nodes: {result.total_nodes}")
        print(f"   Total Edges: {result.total_edges}")
        print(f"   Network Density: {result.network_density:.3f}")
        print(f"   Average Degree: {result.average_degree:.2f}")
        print(f"   Connected Components: {result.connected_components}")
        print(f"   Largest Component: {result.largest_component_size} nodes")
        
        if result.global_clustering_coefficient is not None:
            print(f"   Clustering Coefficient: {result.global_clustering_coefficient:.3f}")
        
        print(f"   Clusters Detected: {len(result.clusters_detected)}")
        
        # Show cluster details
        for j, cluster in enumerate(result.clusters_detected[:3], 1):  # Top 3
            print(f"     {j}. {cluster.cluster_id}")
            print(f"        Size: {cluster.cluster_size} nodes")
            print(f"        Cases: {cluster.total_cases}")
            print(f"        Density: {cluster.cluster_density:.3f}")
            if cluster.geographic_radius_km:
                print(f"        Geographic Radius: {cluster.geographic_radius_km:.2f} km")
            if cluster.cluster_duration_days:
                print(f"        Duration: {cluster.cluster_duration_days} days")
        
        print(f"   Hub Nodes: {len(result.hub_nodes)}")
        if result.hub_nodes:
            print(f"     Key Hubs: {', '.join(result.hub_nodes[:3])}")
        
        print(f"   Bridge Nodes: {len(result.bridge_nodes)}")
        if result.bridge_nodes:
            print(f"     Key Bridges: {', '.join(result.bridge_nodes[:3])}")
        
        print(f"   Super-Spreader Nodes: {len(result.super_spreader_nodes)}")
        if result.super_spreader_nodes:
            print(f"     Potential Super-Spreaders: {', '.join(result.super_spreader_nodes[:3])}")
        
        print(f"   Most Central Nodes:")
        for node_id, centrality in result.most_central_nodes[:3]:  # Top 3
            print(f"     {node_id}: {centrality:.3f}")
        
        print(f"   Analysis Duration: {result.analysis_duration_seconds:.3f}s")
        
        if result.key_findings:
            print(f"   Key Findings ({len(result.key_findings)}):")
            for finding in result.key_findings:
                print(f"     • {finding}")
        
        if result.risk_assessment:
            print(f"   Risk Assessment ({len(result.risk_assessment)}):")
            for risk in result.risk_assessment:
                print(f"     • {risk}")
        
        if result.intervention_recommendations:
            print(f"   Intervention Recommendations ({len(result.intervention_recommendations)}):")
            for rec in result.intervention_recommendations:
                print(f"     • {rec}")
    
    # Network analysis summary
    summary = analyzer.get_network_summary()
    print(f"\n📊 Network Analysis Summary:")
    if "message" in summary:
        print(f"  {summary['message']}")
    else:
        print(f"  Total Analyses: {summary['total_analyses']}")
        print(f"  Network Types: {', '.join(summary['network_types'])}")
        print(f"  Total Nodes: {summary['total_nodes']}")
        print(f"  Total Edges: {summary['total_edges']}")
        print(f"  Total Clusters: {summary['total_clusters']}")
        
        print(f"\n🔗 Key Nodes:")
        key_nodes = summary['key_nodes']
        print(f"  Hubs: {key_nodes['hubs']}")
        print(f"  Bridges: {key_nodes['bridges']}")
        print(f"  Super-Spreaders: {key_nodes['super_spreaders']}")
        
        print(f"\n⚡ Performance:")
        perf = summary['performance']
        print(f"  Average Analysis Time: {perf['average_analysis_time']:.3f}s")
        print(f"  Total Analysis Time: {perf['total_analysis_time']:.3f}s")
    
    # High-risk networks
    high_risk_networks = analyzer.get_high_risk_networks()
    if high_risk_networks:
        print(f"\n🚨 HIGH RISK Networks ({len(high_risk_networks)}):")
        for i, network in enumerate(high_risk_networks[:3], 1):  # Top 3
            print(f"  {i}. {network['network_type'].title()} Network")
            print(f"     Risk Score: {network['risk_score']}")
            print(f"     Nodes: {network['total_nodes']}")
            print(f"     Density: {network['network_density']:.3f}")
            print(f"     Super-Spreaders: {network['super_spreaders']}")
            print(f"     Large Clusters: {network['large_clusters']}")
    
    return analyzer

if __name__ == "__main__":
    analyzer = run_demonstration()
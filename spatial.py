"""
Geospatial Analysis Engine
==========================
Module 3: Analysis & Modeling Tools

Advanced geospatial analysis system for One Health surveillance, providing
spatial pattern detection, clustering analysis, and geographic risk assessment.

NIW Focus: Spatial intelligence revealing geographic disease transmission patterns.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
import itertools
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SpatialAnalysisType(Enum):
    """Types of spatial analysis."""
    HOTSPOT_DETECTION = "hotspot_detection"       # Disease hotspot identification
    CLUSTER_ANALYSIS = "cluster_analysis"         # Spatial clustering
    DISTANCE_ANALYSIS = "distance_analysis"       # Distance-based analysis
    INTERPOLATION = "interpolation"               # Spatial interpolation
    ACCESSIBILITY = "accessibility"               # Healthcare accessibility
    BUFFER_ANALYSIS = "buffer_analysis"           # Proximity analysis
    NETWORK_ANALYSIS = "network_analysis"         # Transportation network

class SpatialPattern(Enum):
    """Types of spatial patterns."""
    CLUSTERED = "clustered"                       # Clustered pattern
    DISPERSED = "dispersed"                       # Dispersed/random pattern
    UNIFORM = "uniform"                          # Uniform distribution
    LINEAR = "linear"                            # Linear pattern
    RADIAL = "radial"                           # Radial from center
    IRREGULAR = "irregular"                      # Irregular pattern

class ClusteringMethod(Enum):
    """Spatial clustering methods."""
    KMEANS = "kmeans"                           # K-means clustering
    DBSCAN = "dbscan"                          # Density-based clustering
    HIERARCHICAL = "hierarchical"               # Hierarchical clustering
    SPATIAL_SCAN = "spatial_scan"              # Spatial scan statistics
    LOCAL_MORANS_I = "local_morans_i"          # Local Moran's I
    GETIS_ORD = "getis_ord"                    # Getis-Ord Gi* statistic

@dataclass
class SpatialPoint:
    """Represents a spatial point with attributes."""
    point_id: str
    latitude: float
    longitude: float
    attributes: Dict[str, Any]
    timestamp: Optional[datetime] = None
    weight: Optional[float] = None
    
    def distance_to(self, other: 'SpatialPoint') -> float:
        """Calculate distance to another point in kilometers."""
        return SpatialAnalysisEngine.haversine_distance(
            self.latitude, self.longitude,
            other.latitude, other.longitude
        )

@dataclass
class SpatialCluster:
    """Represents a spatial cluster."""
    cluster_id: str
    cluster_method: ClusteringMethod
    center_lat: float
    center_lon: float
    radius_km: float
    points: List[SpatialPoint]
    
    # Cluster statistics
    point_count: int = 0
    total_weight: Optional[float] = None
    density: Optional[float] = None
    cohesion: Optional[float] = None
    
    # Statistical significance
    p_value: Optional[float] = None
    z_score: Optional[float] = None
    statistical_significance: bool = False
    
    # Temporal characteristics
    time_span_days: Optional[int] = None
    cluster_duration: Optional[timedelta] = None
    
    def __post_init__(self):
        """Calculate derived statistics."""
        self.point_count = len(self.points)
        
        if self.points:
            # Calculate total weight
            weights = [p.weight for p in self.points if p.weight is not None]
            self.total_weight = sum(weights) if weights else self.point_count
            
            # Calculate cluster cohesion (average distance to center)
            distances = [
                SpatialAnalysisEngine.haversine_distance(
                    p.latitude, p.longitude,
                    self.center_lat, self.center_lon
                ) for p in self.points
            ]
            self.cohesion = statistics.mean(distances) if distances else 0.0
            
            # Calculate density (points per square km)
            area = math.pi * (self.radius_km ** 2)
            self.density = self.point_count / area if area > 0 else 0.0
            
            # Calculate time span
            timestamps = [p.timestamp for p in self.points if p.timestamp]
            if len(timestamps) >= 2:
                timestamps.sort()
                self.cluster_duration = timestamps[-1] - timestamps[0]
                self.time_span_days = self.cluster_duration.days

@dataclass
class SpatialAnalysisResult:
    """Result of spatial analysis."""
    
    analysis_id: str
    analysis_type: SpatialAnalysisType
    analysis_timestamp: datetime
    
    # Input data characteristics
    total_points: int
    study_area_bounds: Tuple[float, float, float, float]  # (min_lat, max_lat, min_lon, max_lon)
    
    # Analysis results
    clusters_detected: List[SpatialCluster]
    hotspots_detected: List[Dict]
    spatial_pattern: Optional[SpatialPattern] = None
    
    # Statistical measures
    global_morans_i: Optional[float] = None
    spatial_autocorrelation: Optional[float] = None
    clustering_coefficient: Optional[float] = None
    nearest_neighbor_ratio: Optional[float] = None
    
    # Performance metrics
    analysis_duration_seconds: float = 0.0
    memory_usage_mb: Optional[float] = None
    
    # Geographic context
    administrative_regions: List[str] = None
    population_affected: Optional[int] = None
    area_affected_km2: Optional[float] = None
    
    # Interpretation
    key_findings: List[str] = None
    risk_areas: List[Dict] = None
    recommended_interventions: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.key_findings is None:
            self.key_findings = []
        if self.risk_areas is None:
            self.risk_areas = []
        if self.recommended_interventions is None:
            self.recommended_interventions = []
        if self.administrative_regions is None:
            self.administrative_regions = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['analysis_type'] = self.analysis_type.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        
        if self.spatial_pattern:
            data['spatial_pattern'] = self.spatial_pattern.value
        
        # Convert clusters to dictionaries
        data['clusters_detected'] = [
            {
                'cluster_id': c.cluster_id,
                'method': c.cluster_method.value,
                'center_lat': c.center_lat,
                'center_lon': c.center_lon,
                'radius_km': c.radius_km,
                'point_count': c.point_count,
                'density': c.density,
                'statistical_significance': c.statistical_significance,
                'time_span_days': c.time_span_days
            }
            for c in self.clusters_detected
        ]
        
        return data

class SpatialAnalysisEngine:
    """Main engine for spatial analysis operations."""
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great circle distance between two points in kilometers."""
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
    def calculate_study_area_bounds(points: List[SpatialPoint]) -> Tuple[float, float, float, float]:
        """Calculate bounding box of study area."""
        if not points:
            return (0.0, 0.0, 0.0, 0.0)
        
        lats = [p.latitude for p in points]
        lons = [p.longitude for p in points]
        
        return (min(lats), max(lats), min(lons), max(lons))
    
    @staticmethod
    def calculate_center_point(points: List[SpatialPoint]) -> Tuple[float, float]:
        """Calculate geographic center of points."""
        if not points:
            return (0.0, 0.0)
        
        center_lat = statistics.mean([p.latitude for p in points])
        center_lon = statistics.mean([p.longitude for p in points])
        
        return center_lat, center_lon

class HotspotDetector:
    """Detects disease hotspots using various methods."""
    
    @staticmethod
    def detect_kernel_density_hotspots(points: List[SpatialPoint],
                                      bandwidth_km: float = 5.0,
                                      threshold_percentile: float = 90.0) -> List[Dict]:
        """Detect hotspots using kernel density estimation."""
        
        if len(points) < 3:
            return []
        
        # Create grid for density calculation
        bounds = SpatialAnalysisEngine.calculate_study_area_bounds(points)
        min_lat, max_lat, min_lon, max_lon = bounds
        
        # Grid resolution (degrees)
        resolution = 0.01  # ~1km
        lat_steps = max(10, int((max_lat - min_lat) / resolution))
        lon_steps = max(10, int((max_lon - min_lon) / resolution))
        
        densities = []
        grid_points = []
        
        # Calculate density at each grid point
        for i in range(lat_steps):
            for j in range(lon_steps):
                grid_lat = min_lat + (i / lat_steps) * (max_lat - min_lat)
                grid_lon = min_lon + (j / lon_steps) * (max_lon - min_lon)
                
                # Calculate kernel density
                density = 0.0
                for point in points:
                    distance = SpatialAnalysisEngine.haversine_distance(
                        grid_lat, grid_lon, point.latitude, point.longitude
                    )
                    
                    # Gaussian kernel
                    if distance <= bandwidth_km * 3:  # 3-sigma cutoff
                        weight = point.weight if point.weight else 1.0
                        kernel_value = weight * math.exp(-0.5 * (distance / bandwidth_km) ** 2)
                        density += kernel_value
                
                densities.append(density)
                grid_points.append((grid_lat, grid_lon))
        
        if not densities:
            return []
        
        # Find hotspots above threshold
        if densities:
            sorted_densities = sorted(densities)
            threshold_index = int((threshold_percentile / 100.0) * len(sorted_densities))
            threshold_index = min(threshold_index, len(sorted_densities) - 1)
            threshold = sorted_densities[threshold_index]
        else:
            threshold = 0.0
        
        hotspots = []
        hotspot_id = 1
        
        for (lat, lon), density in zip(grid_points, densities):
            if density >= threshold:
                # Find nearby points
                nearby_points = []
                for point in points:
                    distance = SpatialAnalysisEngine.haversine_distance(
                        lat, lon, point.latitude, point.longitude
                    )
                    if distance <= bandwidth_km:
                        nearby_points.append(point)
                
                if nearby_points:
                    hotspots.append({
                        'hotspot_id': f"HOTSPOT_{hotspot_id}",
                        'center_lat': lat,
                        'center_lon': lon,
                        'density_score': density,
                        'threshold_ratio': density / threshold,
                        'radius_km': bandwidth_km,
                        'points_in_hotspot': len(nearby_points),
                        'significance': 'high' if density >= threshold * 1.5 else 'moderate'
                    })
                    hotspot_id += 1
        
        # Merge overlapping hotspots
        merged_hotspots = HotspotDetector._merge_overlapping_hotspots(hotspots, bandwidth_km)
        
        return merged_hotspots
    
    @staticmethod
    def detect_getis_ord_hotspots(points: List[SpatialPoint],
                                 distance_threshold_km: float = 10.0) -> List[Dict]:
        """Detect hotspots using Getis-Ord Gi* statistic."""
        
        if len(points) < 5:
            return []
        
        hotspots = []
        
        for i, focal_point in enumerate(points):
            # Find neighbors within distance threshold
            neighbors = []
            neighbor_weights = []
            
            for j, other_point in enumerate(points):
                if i != j:
                    distance = focal_point.distance_to(other_point)
                    if distance <= distance_threshold_km:
                        neighbors.append(other_point)
                        # Inverse distance weighting
                        weight = 1.0 / (1.0 + distance) if distance > 0 else 1.0
                        neighbor_weights.append(weight)
            
            if len(neighbors) < 3:
                continue
            
            # Calculate Getis-Ord Gi* statistic
            focal_weight = focal_point.weight if focal_point.weight else 1.0
            neighbor_weights_sum = sum([p.weight if p.weight else 1.0 for p in neighbors])
            
            # Calculate local sum and global statistics
            local_sum = focal_weight + neighbor_weights_sum
            global_weights = [p.weight if p.weight else 1.0 for p in points]
            global_mean = statistics.mean(global_weights)
            global_std = statistics.stdev(global_weights) if len(global_weights) > 1 else 1.0
            
            # Calculate standardized Gi* statistic
            n = len(neighbors) + 1  # Including focal point
            expected = global_mean * n
            
            if global_std > 0:
                variance = global_std**2 * (len(points) - n) / (len(points) - 1)
                std_error = math.sqrt(variance)
                
                if std_error > 0:
                    gi_star = (local_sum - expected) / std_error
                    
                    # Significant hotspot if Gi* > 1.96 (95% confidence)
                    if gi_star > 1.96:
                        hotspots.append({
                            'hotspot_id': f"GETIS_ORD_{i}",
                            'center_lat': focal_point.latitude,
                            'center_lon': focal_point.longitude,
                            'gi_star_statistic': gi_star,
                            'z_score': gi_star,
                            'p_value': HotspotDetector._calculate_p_value_from_z(gi_star),
                            'neighbor_count': len(neighbors),
                            'local_sum': local_sum,
                            'significance': 'high' if gi_star > 2.58 else 'moderate',
                            'radius_km': distance_threshold_km
                        })
        
        return hotspots
    
    @staticmethod
    def _merge_overlapping_hotspots(hotspots: List[Dict], merge_distance_km: float) -> List[Dict]:
        """Merge overlapping hotspots."""
        
        if len(hotspots) <= 1:
            return hotspots
        
        merged = []
        used = set()
        
        for i, hotspot1 in enumerate(hotspots):
            if i in used:
                continue
            
            # Start new merged hotspot
            merged_hotspot = hotspot1.copy()
            cluster_hotspots = [hotspot1]
            used.add(i)
            
            # Find overlapping hotspots
            for j, hotspot2 in enumerate(hotspots):
                if j <= i or j in used:
                    continue
                
                distance = SpatialAnalysisEngine.haversine_distance(
                    hotspot1['center_lat'], hotspot1['center_lon'],
                    hotspot2['center_lat'], hotspot2['center_lon']
                )
                
                if distance <= merge_distance_km:
                    cluster_hotspots.append(hotspot2)
                    used.add(j)
            
            # If multiple hotspots merged, recalculate center
            if len(cluster_hotspots) > 1:
                center_lat = statistics.mean([h['center_lat'] for h in cluster_hotspots])
                center_lon = statistics.mean([h['center_lon'] for h in cluster_hotspots])
                total_points = sum([h.get('points_in_hotspot', 1) for h in cluster_hotspots])
                
                merged_hotspot.update({
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'points_in_hotspot': total_points,
                    'merged_hotspots': len(cluster_hotspots)
                })
            
            merged.append(merged_hotspot)
        
        return merged
    
    @staticmethod
    def _calculate_p_value_from_z(z_score: float) -> float:
        """Calculate approximate p-value from z-score."""
        abs_z = abs(z_score)
        
        if abs_z > 3.29:
            return 0.001
        elif abs_z > 2.58:
            return 0.01
        elif abs_z > 1.96:
            return 0.05
        elif abs_z > 1.64:
            return 0.10
        else:
            return 0.20

class SpatialClusteringAnalyzer:
    """Performs spatial clustering analysis."""
    
    @staticmethod
    def kmeans_clustering(points: List[SpatialPoint], 
                         k: int = 3) -> List[SpatialCluster]:
        """Perform K-means spatial clustering."""
        
        if len(points) < k or k < 1:
            return []
        
        # Initialize random centroids
        random.seed(42)  # For reproducible results
        centroids = random.sample(points, k)
        centroid_coords = [(p.latitude, p.longitude) for p in centroids]
        
        max_iterations = 50
        tolerance = 0.001
        
        for iteration in range(max_iterations):
            # Assign points to closest centroids
            clusters = [[] for _ in range(k)]
            
            for point in points:
                distances = [
                    SpatialAnalysisEngine.haversine_distance(
                        point.latitude, point.longitude, lat, lon
                    )
                    for lat, lon in centroid_coords
                ]
                closest_cluster = distances.index(min(distances))
                clusters[closest_cluster].append(point)
            
            # Update centroids
            new_centroids = []
            converged = True
            
            for i, cluster_points in enumerate(clusters):
                if cluster_points:
                    new_lat = statistics.mean([p.latitude for p in cluster_points])
                    new_lon = statistics.mean([p.longitude for p in cluster_points])
                    
                    # Check convergence
                    old_lat, old_lon = centroid_coords[i]
                    distance_moved = SpatialAnalysisEngine.haversine_distance(
                        old_lat, old_lon, new_lat, new_lon
                    )
                    
                    if distance_moved > tolerance:
                        converged = False
                    
                    new_centroids.append((new_lat, new_lon))
                else:
                    # Keep old centroid if no points assigned
                    new_centroids.append(centroid_coords[i])
            
            centroid_coords = new_centroids
            
            if converged:
                break
        
        # Create cluster objects
        spatial_clusters = []
        
        for i, cluster_points in enumerate(clusters):
            if cluster_points:
                center_lat, center_lon = centroid_coords[i]
                
                # Calculate cluster radius (max distance to centroid)
                distances = [
                    SpatialAnalysisEngine.haversine_distance(
                        p.latitude, p.longitude, center_lat, center_lon
                    ) for p in cluster_points
                ]
                radius = max(distances) if distances else 0.0
                
                cluster = SpatialCluster(
                    cluster_id=f"KMEANS_CLUSTER_{i+1}",
                    cluster_method=ClusteringMethod.KMEANS,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    radius_km=radius,
                    points=cluster_points
                )
                
                spatial_clusters.append(cluster)
        
        return spatial_clusters
    
    @staticmethod
    def dbscan_clustering(points: List[SpatialPoint],
                         epsilon_km: float = 5.0,
                         min_points: int = 3) -> List[SpatialCluster]:
        """Perform DBSCAN spatial clustering."""
        
        if len(points) < min_points:
            return []
        
        # DBSCAN algorithm
        labels = [-1] * len(points)  # -1 = unassigned, -2 = noise
        cluster_id = 0
        
        for i, point in enumerate(points):
            if labels[i] != -1:  # Already processed
                continue
            
            # Find neighbors within epsilon distance
            neighbors = SpatialClusteringAnalyzer._find_neighbors(points, i, epsilon_km)
            
            if len(neighbors) < min_points:
                labels[i] = -2  # Mark as noise
                continue
            
            # Start new cluster
            labels[i] = cluster_id
            seed_set = neighbors[:]
            
            # Expand cluster
            j = 0
            while j < len(seed_set):
                neighbor_idx = seed_set[j]
                
                if labels[neighbor_idx] == -2:  # Change noise to border point
                    labels[neighbor_idx] = cluster_id
                
                if labels[neighbor_idx] != -1:  # Already processed
                    j += 1
                    continue
                
                labels[neighbor_idx] = cluster_id
                
                # Find neighbors of neighbor
                neighbor_neighbors = SpatialClusteringAnalyzer._find_neighbors(
                    points, neighbor_idx, epsilon_km
                )
                
                if len(neighbor_neighbors) >= min_points:
                    seed_set.extend(neighbor_neighbors)
                
                j += 1
            
            cluster_id += 1
        
        # Create cluster objects
        spatial_clusters = []
        
        for cid in range(cluster_id):
            cluster_points = [points[i] for i, label in enumerate(labels) if label == cid]
            
            if cluster_points:
                center_lat, center_lon = SpatialAnalysisEngine.calculate_center_point(cluster_points)
                
                # Calculate cluster radius
                distances = [
                    SpatialAnalysisEngine.haversine_distance(
                        p.latitude, p.longitude, center_lat, center_lon
                    ) for p in cluster_points
                ]
                radius = max(distances) if distances else epsilon_km
                
                cluster = SpatialCluster(
                    cluster_id=f"DBSCAN_CLUSTER_{cid+1}",
                    cluster_method=ClusteringMethod.DBSCAN,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    radius_km=radius,
                    points=cluster_points
                )
                
                spatial_clusters.append(cluster)
        
        return spatial_clusters
    
    @staticmethod
    def _find_neighbors(points: List[SpatialPoint], point_idx: int, 
                       epsilon_km: float) -> List[int]:
        """Find neighbors within epsilon distance."""
        
        neighbors = []
        query_point = points[point_idx]
        
        for i, other_point in enumerate(points):
            if i != point_idx:
                distance = query_point.distance_to(other_point)
                if distance <= epsilon_km:
                    neighbors.append(i)
        
        return neighbors

class SpatialPatternAnalyzer:
    """Analyzes overall spatial patterns."""
    
    @staticmethod
    def analyze_nearest_neighbor(points: List[SpatialPoint]) -> Dict[str, float]:
        """Analyze nearest neighbor patterns."""
        
        if len(points) < 2:
            return {}
        
        # Calculate nearest neighbor distances
        nn_distances = []
        
        for i, point1 in enumerate(points):
            min_distance = float('inf')
            
            for j, point2 in enumerate(points):
                if i != j:
                    distance = point1.distance_to(point2)
                    min_distance = min(min_distance, distance)
            
            nn_distances.append(min_distance)
        
        # Calculate statistics
        mean_nn_distance = statistics.mean(nn_distances)
        
        # Expected mean distance for random pattern
        bounds = SpatialAnalysisEngine.calculate_study_area_bounds(points)
        min_lat, max_lat, min_lon, max_lon = bounds
        
        # Approximate area calculation
        area_km2 = SpatialPatternAnalyzer._calculate_area_km2(bounds)
        density = len(points) / area_km2 if area_km2 > 0 else 0
        expected_nn_distance = 0.5 / math.sqrt(density) if density > 0 else 0
        
        # Nearest neighbor ratio
        nn_ratio = mean_nn_distance / expected_nn_distance if expected_nn_distance > 0 else 1.0
        
        # Interpret pattern
        if nn_ratio < 0.5:
            pattern = SpatialPattern.CLUSTERED
        elif nn_ratio > 1.5:
            pattern = SpatialPattern.DISPERSED
        else:
            pattern = SpatialPattern.UNIFORM
        
        return {
            'mean_nn_distance_km': mean_nn_distance,
            'expected_nn_distance_km': expected_nn_distance,
            'nn_ratio': nn_ratio,
            'spatial_pattern': pattern,
            'point_density_per_km2': density
        }
    
    @staticmethod
    def calculate_spatial_autocorrelation(points: List[SpatialPoint],
                                        distance_threshold_km: float = 10.0) -> Dict[str, float]:
        """Calculate Moran's I spatial autocorrelation."""
        
        if len(points) < 3:
            return {}
        
        # Extract weights (values)
        weights = [p.weight if p.weight else 1.0 for p in points]
        n = len(points)
        
        if statistics.stdev(weights) == 0:  # No variation
            return {'morans_i': 0.0, 'z_score': 0.0, 'p_value': 1.0}
        
        # Create spatial weights matrix
        w_matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                if i != j:
                    distance = points[i].distance_to(points[j])
                    weight = 1.0 if distance <= distance_threshold_km else 0.0
                else:
                    weight = 0.0
                row.append(weight)
            w_matrix.append(row)
        
        # Calculate total weights
        W = sum(sum(row) for row in w_matrix)
        
        if W == 0:
            return {'morans_i': 0.0, 'z_score': 0.0, 'p_value': 1.0}
        
        # Calculate Moran's I
        mean_weight = statistics.mean(weights)
        
        numerator = 0.0
        denominator = 0.0
        
        for i in range(n):
            for j in range(n):
                numerator += w_matrix[i][j] * (weights[i] - mean_weight) * (weights[j] - mean_weight)
            
            denominator += (weights[i] - mean_weight) ** 2
        
        morans_i = (n / W) * (numerator / denominator) if denominator > 0 else 0.0
        
        # Calculate expected value and variance (simplified)
        expected_i = -1.0 / (n - 1)
        
        # Simplified z-score calculation
        variance_i = 1.0 / (n - 1)  # Simplified
        z_score = (morans_i - expected_i) / math.sqrt(variance_i) if variance_i > 0 else 0.0
        
        # Approximate p-value
        p_value = HotspotDetector._calculate_p_value_from_z(z_score)
        
        return {
            'morans_i': morans_i,
            'expected_i': expected_i,
            'z_score': z_score,
            'p_value': p_value,
            'spatial_autocorrelation': 'positive' if morans_i > expected_i else 'negative'
        }
    
    @staticmethod
    def _calculate_area_km2(bounds: Tuple[float, float, float, float]) -> float:
        """Calculate approximate area in square kilometers."""
        min_lat, max_lat, min_lon, max_lon = bounds
        
        # Approximate calculation using lat/lon degrees
        lat_diff = max_lat - min_lat
        lon_diff = max_lon - min_lon
        
        # Convert to approximate kilometers (rough estimate)
        lat_km = lat_diff * 111.0  # ~111 km per degree latitude
        lon_km = lon_diff * 111.0 * math.cos(math.radians((min_lat + max_lat) / 2))
        
        return lat_km * lon_km

class OneHealthSpatialAnalyzer:
    """Main spatial analyzer for One Health surveillance."""
    
    def __init__(self):
        self.analysis_results: List[SpatialAnalysisResult] = []
        self.analysis_log: List[Dict] = []
        
        logger.info("One Health Spatial Analyzer initialized")
    
    def comprehensive_spatial_analysis(self, animal_data: List[Dict],
                                     human_data: List[Dict],
                                     environmental_data: List[Dict]) -> List[SpatialAnalysisResult]:
        """Perform comprehensive spatial analysis across all domains."""
        
        analysis_start = datetime.now()
        results = []
        
        logger.info(f"Starting comprehensive spatial analysis")
        
        # Convert data to spatial points
        domain_points = {
            "animal": self._extract_spatial_points(animal_data, "animal"),
            "human": self._extract_spatial_points(human_data, "human"),
            "environmental": self._extract_spatial_points(environmental_data, "environmental")
        }
        
        # Analyze each domain
        for domain, points in domain_points.items():
            if len(points) >= 3:
                try:
                    result = self._analyze_domain_spatial_patterns(points, domain)
                    if result:
                        results.append(result)
                        
                except Exception as e:
                    logger.error(f"Error in {domain} spatial analysis: {e}")
        
        # Combined cross-domain analysis
        all_points = []
        for points in domain_points.values():
            all_points.extend(points)
        
        if len(all_points) >= 5:
            try:
                combined_result = self._analyze_domain_spatial_patterns(all_points, "integrated")
                if combined_result:
                    results.append(combined_result)
                    
            except Exception as e:
                logger.error(f"Error in integrated spatial analysis: {e}")
        
        # Store results
        self.analysis_results.extend(results)
        
        # Log performance
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "analyses_completed": len(results),
            "total_points_analyzed": len(all_points),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            }
        })
        
        logger.info(f"Spatial analysis completed: {len(results)} analyses in {analysis_time:.2f}s")
        
        return results
    
    def _extract_spatial_points(self, data: List[Dict], domain: str) -> List[SpatialPoint]:
        """Extract spatial points from surveillance data."""
        
        points = []
        
        for record in data:
            lat = record.get('location_lat')
            lon = record.get('location_lon')
            timestamp_str = record.get('timestamp')
            
            if lat is not None and lon is not None:
                timestamp = None
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str[:19])
                    except ValueError:
                        pass
                
                # Determine weight based on domain
                if domain == "animal":
                    weight = record.get('mortality_count', record.get('morbidity_count', 1))
                elif domain == "human":
                    weight = record.get('case_count', 1)
                    # Adjust weight by severity
                    severity = record.get('severity', '').lower()
                    if severity == 'critical':
                        weight *= 3
                    elif severity == 'severe':
                        weight *= 2
                elif domain == "environmental":
                    weight = record.get('total_collected', record.get('value', 1))
                else:
                    weight = 1
                
                point = SpatialPoint(
                    point_id=record.get('animal_id', record.get('case_id', record.get('record_id', f"{domain}_{len(points)}"))),
                    latitude=float(lat),
                    longitude=float(lon),
                    attributes=record,
                    timestamp=timestamp,
                    weight=float(weight) if weight else 1.0
                )
                
                points.append(point)
        
        return points
    
    def _analyze_domain_spatial_patterns(self, points: List[SpatialPoint], 
                                       domain: str) -> Optional[SpatialAnalysisResult]:
        """Analyze spatial patterns for a specific domain."""
        
        if len(points) < 3:
            return None
        
        analysis_start = datetime.now()
        
        # Calculate study area bounds
        bounds = SpatialAnalysisEngine.calculate_study_area_bounds(points)
        
        # Hotspot detection
        hotspots_kernel = HotspotDetector.detect_kernel_density_hotspots(
            points, bandwidth_km=10.0, threshold_percentile=85.0
        )
        
        hotspots_getis = HotspotDetector.detect_getis_ord_hotspots(
            points, distance_threshold_km=15.0
        )
        
        all_hotspots = hotspots_kernel + hotspots_getis
        
        # Spatial clustering
        clusters_kmeans = SpatialClusteringAnalyzer.kmeans_clustering(points, k=min(5, len(points)//3))
        clusters_dbscan = SpatialClusteringAnalyzer.dbscan_clustering(points, epsilon_km=8.0, min_points=3)
        
        all_clusters = clusters_kmeans + clusters_dbscan
        
        # Spatial pattern analysis
        nn_analysis = SpatialPatternAnalyzer.analyze_nearest_neighbor(points)
        autocorr_analysis = SpatialPatternAnalyzer.calculate_spatial_autocorrelation(points)
        
        # Generate key findings
        key_findings = []
        
        if all_hotspots:
            high_significance_hotspots = [h for h in all_hotspots if h.get('significance') == 'high']
            key_findings.append(f"Detected {len(all_hotspots)} hotspots ({len(high_significance_hotspots)} high significance)")
        
        if all_clusters:
            significant_clusters = [c for c in all_clusters if c.statistical_significance]
            key_findings.append(f"Identified {len(all_clusters)} spatial clusters ({len(significant_clusters)} significant)")
        
        spatial_pattern = nn_analysis.get('spatial_pattern')
        if spatial_pattern:
            key_findings.append(f"Spatial pattern: {spatial_pattern.value}")
        
        morans_i = autocorr_analysis.get('morans_i')
        if morans_i is not None:
            autocorr_type = autocorr_analysis.get('spatial_autocorrelation', 'none')
            key_findings.append(f"Spatial autocorrelation: {autocorr_type} (I = {morans_i:.3f})")
        
        # Generate recommendations
        recommendations = []
        
        if len(all_hotspots) > 0:
            recommendations.append("Focus surveillance resources on identified hotspots")
        
        if spatial_pattern == SpatialPattern.CLUSTERED:
            recommendations.append("Investigate transmission sources in clustered areas")
        elif spatial_pattern == SpatialPattern.DISPERSED:
            recommendations.append("Implement broad-scale preventive measures")
        
        if autocorr_analysis.get('spatial_autocorrelation') == 'positive':
            recommendations.append("Strengthen regional coordination due to spatial clustering")
        
        # Calculate affected area
        if all_clusters:
            total_area = sum(math.pi * (c.radius_km ** 2) for c in all_clusters)
        else:
            # Approximate based on bounding box
            min_lat, max_lat, min_lon, max_lon = bounds
            total_area = SpatialPatternAnalyzer._calculate_area_km2(bounds)
        
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        
        result = SpatialAnalysisResult(
            analysis_id=f"SPATIAL_{domain.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            analysis_type=SpatialAnalysisType.CLUSTER_ANALYSIS,
            analysis_timestamp=analysis_start,
            total_points=len(points),
            study_area_bounds=bounds,
            clusters_detected=all_clusters,
            hotspots_detected=all_hotspots,
            spatial_pattern=spatial_pattern,
            global_morans_i=autocorr_analysis.get('morans_i'),
            spatial_autocorrelation=autocorr_analysis.get('morans_i'),
            nearest_neighbor_ratio=nn_analysis.get('nn_ratio'),
            analysis_duration_seconds=analysis_duration,
            area_affected_km2=total_area,
            key_findings=key_findings,
            recommended_interventions=recommendations
        )
        
        return result
    
    def get_spatial_summary(self) -> Dict:
        """Get summary of spatial analysis results."""
        
        if not self.analysis_results:
            return {"message": "No spatial analyses performed"}
        
        # Aggregate statistics
        total_hotspots = sum(len(r.hotspots_detected) for r in self.analysis_results)
        total_clusters = sum(len(r.clusters_detected) for r in self.analysis_results)
        total_points = sum(r.total_points for r in self.analysis_results)
        
        # Spatial pattern distribution
        pattern_counts = defaultdict(int)
        for result in self.analysis_results:
            if result.spatial_pattern:
                pattern_counts[result.spatial_pattern.value] += 1
        
        # Performance statistics
        analysis_times = [r.analysis_duration_seconds for r in self.analysis_results]
        
        return {
            "total_analyses": len(self.analysis_results),
            "total_points_analyzed": total_points,
            "total_hotspots_detected": total_hotspots,
            "total_clusters_detected": total_clusters,
            "spatial_patterns": dict(pattern_counts),
            "performance": {
                "average_analysis_time": statistics.mean(analysis_times) if analysis_times else 0,
                "total_analysis_time": sum(analysis_times)
            }
        }
    
    def get_high_risk_areas(self) -> List[Dict]:
        """Get areas identified as high risk."""
        
        high_risk_areas = []
        
        for result in self.analysis_results:
            # High-significance hotspots
            for hotspot in result.hotspots_detected:
                if hotspot.get('significance') == 'high':
                    high_risk_areas.append({
                        'type': 'hotspot',
                        'location': (hotspot['center_lat'], hotspot['center_lon']),
                        'risk_score': hotspot.get('density_score', 0),
                        'radius_km': hotspot.get('radius_km', 0),
                        'analysis_id': result.analysis_id
                    })
            
            # Significant clusters
            for cluster in result.clusters_detected:
                if cluster.statistical_significance and cluster.density > 1.0:  # High density threshold
                    high_risk_areas.append({
                        'type': 'cluster',
                        'location': (cluster.center_lat, cluster.center_lon),
                        'risk_score': cluster.density,
                        'radius_km': cluster.radius_km,
                        'point_count': cluster.point_count,
                        'analysis_id': result.analysis_id
                    })
        
        # Sort by risk score
        return sorted(high_risk_areas, key=lambda x: x['risk_score'], reverse=True)

# Mock data generator
def generate_mock_spatial_data():
    """Generate mock spatial data for testing."""
    
    # Base location (New York City area)
    base_lat = 40.7128
    base_lon = -74.0060
    
    # Generate animal data with spatial clusters
    animal_data = []
    
    # Cluster 1: High outbreak area
    for i in range(15):
        lat_offset = random.uniform(-0.02, 0.02)  # ~2km radius
        lon_offset = random.uniform(-0.02, 0.02)
        
        animal_data.append({
            "animal_id": f"SPATIAL_FARM_{i:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat(),
            "location_lat": base_lat + 0.1 + lat_offset,  # Cluster center offset
            "location_lon": base_lon + 0.1 + lon_offset,
            "species": "poultry",
            "mortality_count": random.randint(5, 20)
        })
    
    # Cluster 2: Medium outbreak area
    for i in range(10):
        lat_offset = random.uniform(-0.015, 0.015)
        lon_offset = random.uniform(-0.015, 0.015)
        
        animal_data.append({
            "animal_id": f"SPATIAL_FARM_{i+15:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 8))).isoformat(),
            "location_lat": base_lat - 0.08 + lat_offset,
            "location_lon": base_lon - 0.08 + lon_offset,
            "species": "cattle",
            "mortality_count": random.randint(2, 8)
        })
    
    # Scattered cases
    for i in range(8):
        lat_offset = random.uniform(-0.3, 0.3)
        lon_offset = random.uniform(-0.3, 0.3)
        
        animal_data.append({
            "animal_id": f"SPATIAL_FARM_{i+25:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 15))).isoformat(),
            "location_lat": base_lat + lat_offset,
            "location_lon": base_lon + lon_offset,
            "species": "swine",
            "mortality_count": random.randint(1, 3)
        })
    
    # Generate human data correlated with animal clusters
    human_data = []
    
    # Cases near animal cluster 1
    for i in range(8):
        lat_offset = random.uniform(-0.03, 0.03)
        lon_offset = random.uniform(-0.03, 0.03)
        
        human_data.append({
            "case_id": f"SPATIAL_HUM_{i:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 5))).isoformat(),
            "location_lat": base_lat + 0.1 + lat_offset,
            "location_lon": base_lon + 0.1 + lon_offset,
            "case_classification": "confirmed",
            "case_count": 1,
            "severity": random.choice(["moderate", "severe"])
        })
    
    # Cases near animal cluster 2
    for i in range(5):
        lat_offset = random.uniform(-0.025, 0.025)
        lon_offset = random.uniform(-0.025, 0.025)
        
        human_data.append({
            "case_id": f"SPATIAL_HUM_{i+8:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat(),
            "location_lat": base_lat - 0.08 + lat_offset,
            "location_lon": base_lon - 0.08 + lon_offset,
            "case_classification": "probable",
            "case_count": 1,
            "severity": "mild"
        })
    
    # Generate environmental data
    environmental_data = []
    
    # Environmental monitoring stations
    for i in range(12):
        lat_offset = random.uniform(-0.2, 0.2)
        lon_offset = random.uniform(-0.2, 0.2)
        
        environmental_data.append({
            "record_id": f"SPATIAL_ENV_{i:03d}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(1, 10))).isoformat(),
            "location_lat": base_lat + lat_offset,
            "location_lon": base_lon + lon_offset,
            "parameter": "temperature",
            "value": random.uniform(20, 35)
        })
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of spatial analysis system."""
    print("🗺️ One Health Geospatial Analysis Engine - Demonstration")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OneHealthSpatialAnalyzer()
    
    # Generate mock spatial data
    animal_data, human_data, env_data = generate_mock_spatial_data()
    
    print(f"\n📍 Spatial Analysis Data:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run comprehensive spatial analysis
    print(f"\n🗺️ Running Comprehensive Spatial Analysis...")
    results = analyzer.comprehensive_spatial_analysis(animal_data, human_data, env_data)
    
    # Display spatial analysis results
    print(f"\n📊 Spatial Analysis Results ({len(results)} total):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Spatial Analysis - {result.analysis_id}")
        print(f"   Analysis Type: {result.analysis_type.value.replace('_', ' ').title()}")
        print(f"   Total Points: {result.total_points}")
        print(f"   Study Area: {result.study_area_bounds}")
        
        if result.spatial_pattern:
            print(f"   Spatial Pattern: {result.spatial_pattern.value.upper()}")
        
        if result.global_morans_i is not None:
            print(f"   Moran's I: {result.global_morans_i:.3f}")
        
        if result.nearest_neighbor_ratio is not None:
            print(f"   Nearest Neighbor Ratio: {result.nearest_neighbor_ratio:.3f}")
        
        print(f"   Hotspots Detected: {len(result.hotspots_detected)}")
        
        # Show hotspot details
        for j, hotspot in enumerate(result.hotspots_detected[:3], 1):  # Top 3
            print(f"     {j}. {hotspot['hotspot_id']} at ({hotspot['center_lat']:.4f}, {hotspot['center_lon']:.4f})")
            print(f"        Significance: {hotspot.get('significance', 'unknown')}")
            if 'density_score' in hotspot:
                print(f"        Density Score: {hotspot['density_score']:.2f}")
        
        print(f"   Clusters Detected: {len(result.clusters_detected)}")
        
        # Show cluster details
        for j, cluster in enumerate(result.clusters_detected[:3], 1):  # Top 3
            print(f"     {j}. {cluster.cluster_id} ({cluster.cluster_method.value})")
            print(f"        Center: ({cluster.center_lat:.4f}, {cluster.center_lon:.4f})")
            print(f"        Points: {cluster.point_count}, Radius: {cluster.radius_km:.2f}km")
            print(f"        Density: {cluster.density:.2f} points/km²")
        
        if result.area_affected_km2:
            print(f"   Affected Area: {result.area_affected_km2:.1f} km²")
        
        print(f"   Analysis Duration: {result.analysis_duration_seconds:.3f}s")
        
        if result.key_findings:
            print(f"   Key Findings ({len(result.key_findings)}):")
            for finding in result.key_findings:
                print(f"     • {finding}")
        
        if result.recommended_interventions:
            print(f"   Recommendations ({len(result.recommended_interventions)}):")
            for rec in result.recommended_interventions:
                print(f"     • {rec}")
    
    # Display spatial analysis summary
    summary = analyzer.get_spatial_summary()
    print(f"\n📊 Spatial Analysis Summary:")
    if "message" in summary:
        print(f"  {summary['message']}")
    else:
        print(f"  Total Analyses: {summary['total_analyses']}")
        print(f"  Total Points: {summary['total_points_analyzed']}")
        print(f"  Hotspots Detected: {summary['total_hotspots_detected']}")
        print(f"  Clusters Detected: {summary['total_clusters_detected']}")
        
        if summary['spatial_patterns']:
            print(f"\n🗺️ Spatial Patterns:")
            for pattern, count in summary['spatial_patterns'].items():
                print(f"  {pattern.title()}: {count}")
        
        print(f"\n⚡ Performance:")
        perf = summary['performance']
        print(f"  Average Analysis Time: {perf['average_analysis_time']:.3f}s")
        print(f"  Total Analysis Time: {perf['total_analysis_time']:.3f}s")
    
    # High-risk areas
    high_risk_areas = analyzer.get_high_risk_areas()
    if high_risk_areas:
        print(f"\n🚨 HIGH RISK Areas ({len(high_risk_areas)}):")
        for i, area in enumerate(high_risk_areas[:5], 1):  # Top 5
            lat, lon = area['location']
            print(f"  {i}. {area['type'].title()} at ({lat:.4f}, {lon:.4f})")
            print(f"     Risk Score: {area['risk_score']:.2f}")
            print(f"     Radius: {area['radius_km']:.2f}km")
            if 'point_count' in area:
                print(f"     Point Count: {area['point_count']}")
    
    return analyzer

if __name__ == "__main__":
    analyzer = run_demonstration()
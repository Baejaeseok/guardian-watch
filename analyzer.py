"""
Cross-Species Analyzer
======================
Module 2: Essential Epidemiologic Tools

Advanced analytical engine for One Health surveillance data, performing cross-domain
correlation analysis, spatiotemporal pattern detection, and inter-species transmission analysis.

NIW Focus: Sophisticated analytics revealing hidden connections across health domains.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter
import itertools

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalysisType(Enum):
    """Types of cross-domain analysis."""
    CORRELATION = "correlation"
    CAUSALITY = "causality"
    CLUSTERING = "clustering"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    PATHOGEN_FLOW = "pathogen_flow"
    RISK_PROPAGATION = "risk_propagation"

class DataDomain(Enum):
    """Health surveillance data domains."""
    ANIMAL = "animal"
    HUMAN = "human"
    ENVIRONMENTAL = "environmental"
    VECTOR = "vector"
    LABORATORY = "laboratory"

class CorrelationType(Enum):
    """Types of correlation relationships."""
    POSITIVE = "positive"        # Variables move together
    NEGATIVE = "negative"        # Variables move opposite
    LAGGED = "lagged"           # Delayed relationship
    BIDIRECTIONAL = "bidirectional"  # Mutual influence
    THRESHOLD = "threshold"      # Step function relationship

@dataclass
class AnalysisResult:
    """Result of cross-domain analysis."""
    
    analysis_id: str
    analysis_type: AnalysisType
    domains: List[DataDomain]
    
    # Statistical measures
    correlation_coefficient: Optional[float] = None
    p_value: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None
    sample_size: int = 0
    
    # Temporal analysis
    time_lag_days: Optional[int] = None
    temporal_window: Optional[int] = None
    
    # Spatial analysis
    spatial_radius_km: Optional[float] = None
    geographic_clusters: Optional[List[Dict]] = None
    
    # Pathogen analysis
    shared_pathogens: Optional[List[str]] = None
    transmission_pathways: Optional[List[Dict]] = None
    
    # Interpretation
    relationship_strength: str = "unknown"  # "weak", "moderate", "strong"
    statistical_significance: bool = False
    practical_significance: str = "unknown"
    
    # Metadata
    analysis_date: datetime = None
    data_period_start: datetime = None
    data_period_end: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.analysis_date is None:
            self.analysis_date = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['analysis_type'] = self.analysis_type.value
        data['domains'] = [d.value for d in self.domains]
        data['analysis_date'] = self.analysis_date.isoformat()
        if self.data_period_start:
            data['data_period_start'] = self.data_period_start.isoformat()
        if self.data_period_end:
            data['data_period_end'] = self.data_period_end.isoformat()
        return data

class SpatioTemporalAnalyzer:
    """Analyzes spatial and temporal patterns across domains."""
    
    @staticmethod
    def calculate_spatial_correlation(domain1_data: List[Dict], 
                                    domain2_data: List[Dict],
                                    max_distance_km: float = 50) -> AnalysisResult:
        """Calculate spatial correlation between two domains."""
        
        # Extract location data
        locations1 = []
        locations2 = []
        
        for record in domain1_data:
            if record.get('location_lat') and record.get('location_lon'):
                locations1.append({
                    'lat': record['location_lat'],
                    'lon': record['location_lon'],
                    'timestamp': record.get('timestamp'),
                    'value': record.get('mortality_count', record.get('case_count', 1))
                })
        
        for record in domain2_data:
            if record.get('location_lat') and record.get('location_lon'):
                locations2.append({
                    'lat': record['location_lat'],
                    'lon': record['location_lon'],
                    'timestamp': record.get('timestamp'),
                    'value': record.get('case_count', record.get('total_collected', 1))
                })
        
        if not locations1 or not locations2:
            return AnalysisResult(
                analysis_id="SPATIAL_001",
                analysis_type=AnalysisType.SPATIAL,
                domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
                sample_size=0,
                relationship_strength="insufficient_data"
            )
        
        # Find spatially correlated events
        spatial_matches = []
        
        for loc1 in locations1:
            for loc2 in locations2:
                distance = SpatioTemporalAnalyzer._calculate_distance(
                    loc1['lat'], loc1['lon'], loc2['lat'], loc2['lon']
                )
                
                if distance <= max_distance_km:
                    spatial_matches.append({
                        'distance_km': distance,
                        'domain1_value': loc1['value'],
                        'domain2_value': loc2['value'],
                        'domain1_time': loc1['timestamp'],
                        'domain2_time': loc2['timestamp']
                    })
        
        # Calculate correlation
        if len(spatial_matches) >= 3:
            values1 = [m['domain1_value'] for m in spatial_matches]
            values2 = [m['domain2_value'] for m in spatial_matches]
            
            try:
                correlation = statistics.correlation(values1, values2)
                p_value = SpatioTemporalAnalyzer._estimate_p_value(correlation, len(spatial_matches))
                
            except statistics.StatisticsError:
                correlation = 0.0
                p_value = 1.0
        else:
            correlation = 0.0
            p_value = 1.0
        
        # Determine relationship strength
        strength = SpatioTemporalAnalyzer._classify_correlation_strength(correlation)
        significance = p_value < 0.05 if p_value else False
        
        return AnalysisResult(
            analysis_id="SPATIAL_001",
            analysis_type=AnalysisType.SPATIAL,
            domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
            correlation_coefficient=correlation,
            p_value=p_value,
            sample_size=len(spatial_matches),
            spatial_radius_km=max_distance_km,
            relationship_strength=strength,
            statistical_significance=significance,
            geographic_clusters=spatial_matches[:5]  # Top 5 matches
        )
    
    @staticmethod
    def calculate_temporal_lag_correlation(domain1_data: List[Dict],
                                         domain2_data: List[Dict],
                                         max_lag_days: int = 30) -> AnalysisResult:
        """Calculate temporal lag correlation between domains."""
        
        # Group data by date
        def group_by_date(data: List[Dict]) -> Dict[str, int]:
            date_counts = defaultdict(int)
            for record in data:
                timestamp_str = record.get('timestamp', '')
                if timestamp_str:
                    date_key = timestamp_str[:10]  # YYYY-MM-DD
                    count = record.get('mortality_count', 
                                     record.get('case_count', 
                                              record.get('total_collected', 1)))
                    date_counts[date_key] += count
            return dict(date_counts)
        
        dates1 = group_by_date(domain1_data)
        dates2 = group_by_date(domain2_data)
        
        if not dates1 or not dates2:
            return AnalysisResult(
                analysis_id="TEMPORAL_001",
                analysis_type=AnalysisType.TEMPORAL,
                domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
                sample_size=0,
                relationship_strength="insufficient_data"
            )
        
        # Test different lag periods
        best_correlation = 0.0
        best_lag = 0
        best_p_value = 1.0
        
        for lag_days in range(-max_lag_days, max_lag_days + 1):
            correlation, p_value = SpatioTemporalAnalyzer._test_lag_correlation(
                dates1, dates2, lag_days
            )
            
            if abs(correlation) > abs(best_correlation):
                best_correlation = correlation
                best_lag = lag_days
                best_p_value = p_value
        
        strength = SpatioTemporalAnalyzer._classify_correlation_strength(best_correlation)
        significance = best_p_value < 0.05
        
        return AnalysisResult(
            analysis_id="TEMPORAL_001",
            analysis_type=AnalysisType.TEMPORAL,
            domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
            correlation_coefficient=best_correlation,
            p_value=best_p_value,
            sample_size=len(dates1) + len(dates2),
            time_lag_days=best_lag,
            temporal_window=max_lag_days,
            relationship_strength=strength,
            statistical_significance=significance
        )
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers."""
        # Haversine formula
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2) 
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    @staticmethod
    def _test_lag_correlation(dates1: Dict[str, int], dates2: Dict[str, int], 
                            lag_days: int) -> Tuple[float, float]:
        """Test correlation with specific lag period."""
        
        # Adjust dates2 by lag
        adjusted_dates2 = {}
        for date_str, count in dates2.items():
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                adjusted_date = date_obj + timedelta(days=lag_days)
                adjusted_dates2[adjusted_date.strftime('%Y-%m-%d')] = count
            except ValueError:
                continue
        
        # Find common dates
        common_dates = set(dates1.keys()) & set(adjusted_dates2.keys())
        
        if len(common_dates) < 3:
            return 0.0, 1.0
        
        values1 = [dates1[date] for date in common_dates]
        values2 = [adjusted_dates2[date] for date in common_dates]
        
        try:
            correlation = statistics.correlation(values1, values2)
            p_value = SpatioTemporalAnalyzer._estimate_p_value(correlation, len(common_dates))
            return correlation, p_value
        except statistics.StatisticsError:
            return 0.0, 1.0
    
    @staticmethod
    def _estimate_p_value(correlation: float, sample_size: int) -> float:
        """Estimate p-value for correlation (simplified)."""
        if sample_size <= 2:
            return 1.0
        
        # t-test approximation for correlation
        t_stat = abs(correlation) * math.sqrt((sample_size - 2) / (1 - correlation**2))
        
        # Rough p-value estimation based on t-distribution
        if t_stat > 2.58:  # 99% confidence
            return 0.01
        elif t_stat > 1.96:  # 95% confidence  
            return 0.05
        elif t_stat > 1.64:  # 90% confidence
            return 0.10
        else:
            return 0.20
    
    @staticmethod
    def _classify_correlation_strength(correlation: float) -> str:
        """Classify correlation strength."""
        abs_corr = abs(correlation)
        
        if abs_corr >= 0.7:
            return "strong"
        elif abs_corr >= 0.3:
            return "moderate"
        elif abs_corr >= 0.1:
            return "weak"
        else:
            return "negligible"

class PathogenFlowAnalyzer:
    """Analyzes pathogen transmission patterns across species/domains."""
    
    @staticmethod
    def analyze_pathogen_transmission(animal_data: List[Dict],
                                    human_data: List[Dict],
                                    environmental_data: List[Dict]) -> AnalysisResult:
        """Analyze pathogen flow between domains."""
        
        # Extract pathogen data from each domain
        animal_pathogens = PathogenFlowAnalyzer._extract_pathogens(animal_data, 'animal')
        human_pathogens = PathogenFlowAnalyzer._extract_pathogens(human_data, 'human')
        env_pathogens = PathogenFlowAnalyzer._extract_pathogens(environmental_data, 'environmental')
        
        all_pathogens = animal_pathogens + human_pathogens + env_pathogens
        
        if not all_pathogens:
            return AnalysisResult(
                analysis_id="PATHOGEN_001",
                analysis_type=AnalysisType.PATHOGEN_FLOW,
                domains=[DataDomain.ANIMAL, DataDomain.HUMAN, DataDomain.ENVIRONMENTAL],
                sample_size=0,
                relationship_strength="no_pathogens"
            )
        
        # Find shared pathogens
        shared_pathogens = PathogenFlowAnalyzer._find_shared_pathogens(all_pathogens)
        
        # Analyze transmission pathways
        transmission_pathways = PathogenFlowAnalyzer._identify_transmission_pathways(
            all_pathogens, shared_pathogens
        )
        
        # Calculate cross-domain pathogen correlation
        correlation = PathogenFlowAnalyzer._calculate_pathogen_correlation(
            animal_pathogens, human_pathogens
        )
        
        return AnalysisResult(
            analysis_id="PATHOGEN_001",
            analysis_type=AnalysisType.PATHOGEN_FLOW,
            domains=[DataDomain.ANIMAL, DataDomain.HUMAN, DataDomain.ENVIRONMENTAL],
            correlation_coefficient=correlation,
            sample_size=len(all_pathogens),
            shared_pathogens=shared_pathogens,
            transmission_pathways=transmission_pathways,
            relationship_strength="moderate" if shared_pathogens else "weak"
        )
    
    @staticmethod
    def _extract_pathogens(data: List[Dict], domain: str) -> List[Dict]:
        """Extract pathogen information from domain data."""
        pathogens = []
        
        for record in data:
            pathogen_fields = ['pathogen_detected', 'confirmed_pathogen', 'suspected_pathogen']
            
            for field in pathogen_fields:
                if record.get(field):
                    pathogens.append({
                        'domain': domain,
                        'pathogen': record[field],
                        'timestamp': record.get('timestamp'),
                        'location_lat': record.get('location_lat'),
                        'location_lon': record.get('location_lon'),
                        'record_id': record.get('case_id', 
                                              record.get('animal_id', 
                                                        record.get('survey_id', 'unknown')))
                    })
                    break  # Only take first pathogen found
        
        return pathogens
    
    @staticmethod
    def _find_shared_pathogens(all_pathogens: List[Dict]) -> List[str]:
        """Find pathogens shared across multiple domains."""
        
        # Group by pathogen name
        pathogen_domains = defaultdict(set)
        
        for p in all_pathogens:
            pathogen_name = p['pathogen'].lower()
            # Normalize pathogen names
            if 'h5n1' in pathogen_name or 'avian' in pathogen_name:
                pathogen_name = 'h5n1'
            elif 'west_nile' in pathogen_name or 'wnv' in pathogen_name:
                pathogen_name = 'west_nile_virus'
            elif 'brucella' in pathogen_name:
                pathogen_name = 'brucella'
            
            pathogen_domains[pathogen_name].add(p['domain'])
        
        # Find pathogens in multiple domains
        shared = []
        for pathogen, domains in pathogen_domains.items():
            if len(domains) >= 2:
                shared.append(pathogen)
        
        return shared
    
    @staticmethod
    def _identify_transmission_pathways(all_pathogens: List[Dict], 
                                      shared_pathogens: List[str]) -> List[Dict]:
        """Identify potential transmission pathways."""
        
        pathways = []
        
        for shared_pathogen in shared_pathogens:
            # Find records of this pathogen across domains
            pathogen_records = [p for p in all_pathogens 
                              if shared_pathogen in p['pathogen'].lower()]
            
            # Group by domain
            domain_records = defaultdict(list)
            for record in pathogen_records:
                domain_records[record['domain']].append(record)
            
            # Analyze potential transmission directions
            domains = list(domain_records.keys())
            if len(domains) >= 2:
                for i, domain1 in enumerate(domains):
                    for domain2 in domains[i+1:]:
                        pathway = PathogenFlowAnalyzer._analyze_transmission_direction(
                            domain_records[domain1], 
                            domain_records[domain2],
                            shared_pathogen
                        )
                        
                        if pathway:
                            pathways.append(pathway)
        
        return pathways
    
    @staticmethod
    def _analyze_transmission_direction(records1: List[Dict], records2: List[Dict],
                                     pathogen: str) -> Optional[Dict]:
        """Analyze transmission direction between two domains."""
        
        # Simple temporal analysis - which appeared first?
        times1 = []
        times2 = []
        
        for record in records1:
            if record['timestamp']:
                try:
                    times1.append(datetime.fromisoformat(record['timestamp'][:19]))
                except ValueError:
                    pass
        
        for record in records2:
            if record['timestamp']:
                try:
                    times2.append(datetime.fromisoformat(record['timestamp'][:19]))
                except ValueError:
                    pass
        
        if not times1 or not times2:
            return None
        
        earliest1 = min(times1)
        earliest2 = min(times2)
        
        # Determine likely transmission direction
        if earliest1 < earliest2:
            source_domain = records1[0]['domain']
            target_domain = records2[0]['domain']
            time_diff = (earliest2 - earliest1).days
        else:
            source_domain = records2[0]['domain']
            target_domain = records1[0]['domain']
            time_diff = (earliest1 - earliest2).days
        
        return {
            'pathogen': pathogen,
            'source_domain': source_domain,
            'target_domain': target_domain,
            'time_difference_days': time_diff,
            'confidence': 'low' if time_diff > 30 else 'medium'
        }
    
    @staticmethod
    def _calculate_pathogen_correlation(animal_pathogens: List[Dict],
                                      human_pathogens: List[Dict]) -> float:
        """Calculate correlation between animal and human pathogen occurrences."""
        
        if not animal_pathogens or not human_pathogens:
            return 0.0
        
        # Group by date
        animal_dates = defaultdict(int)
        human_dates = defaultdict(int)
        
        for p in animal_pathogens:
            if p['timestamp']:
                date_key = p['timestamp'][:10]
                animal_dates[date_key] += 1
        
        for p in human_pathogens:
            if p['timestamp']:
                date_key = p['timestamp'][:10]
                human_dates[date_key] += 1
        
        # Find common dates
        all_dates = set(animal_dates.keys()) | set(human_dates.keys())
        
        if len(all_dates) < 3:
            return 0.0
        
        animal_counts = [animal_dates.get(date, 0) for date in all_dates]
        human_counts = [human_dates.get(date, 0) for date in all_dates]
        
        try:
            return statistics.correlation(animal_counts, human_counts)
        except statistics.StatisticsError:
            return 0.0

class ClusterAnalyzer:
    """Analyzes spatial and temporal clusters across domains."""
    
    @staticmethod
    def detect_cross_domain_clusters(domain1_data: List[Dict],
                                   domain2_data: List[Dict],
                                   spatial_threshold_km: float = 25,
                                   temporal_threshold_days: int = 14) -> AnalysisResult:
        """Detect clusters that appear across multiple domains."""
        
        # Extract events with locations and times
        events1 = ClusterAnalyzer._extract_events(domain1_data, 'domain1')
        events2 = ClusterAnalyzer._extract_events(domain2_data, 'domain2')
        
        all_events = events1 + events2
        
        if len(all_events) < 4:  # Need minimum events for clustering
            return AnalysisResult(
                analysis_id="CLUSTER_001",
                analysis_type=AnalysisType.CLUSTERING,
                domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
                sample_size=len(all_events),
                relationship_strength="insufficient_data"
            )
        
        # Find spatiotemporal clusters
        clusters = ClusterAnalyzer._find_spatiotemporal_clusters(
            all_events, spatial_threshold_km, temporal_threshold_days
        )
        
        # Filter to cross-domain clusters only
        cross_domain_clusters = []
        for cluster in clusters:
            domains_in_cluster = set(event['domain'] for event in cluster['events'])
            if len(domains_in_cluster) >= 2:
                cross_domain_clusters.append(cluster)
        
        # Calculate cluster strength
        if cross_domain_clusters:
            avg_cluster_size = statistics.mean([len(c['events']) for c in cross_domain_clusters])
            strength = "strong" if avg_cluster_size >= 5 else "moderate"
        else:
            strength = "weak"
        
        return AnalysisResult(
            analysis_id="CLUSTER_001",
            analysis_type=AnalysisType.CLUSTERING,
            domains=[DataDomain.ANIMAL, DataDomain.HUMAN],
            sample_size=len(all_events),
            spatial_radius_km=spatial_threshold_km,
            temporal_window=temporal_threshold_days,
            geographic_clusters=cross_domain_clusters,
            relationship_strength=strength,
            statistical_significance=len(cross_domain_clusters) > 0
        )
    
    @staticmethod
    def _extract_events(data: List[Dict], domain_label: str) -> List[Dict]:
        """Extract events with spatial and temporal information."""
        events = []
        
        for record in data:
            if (record.get('location_lat') and 
                record.get('location_lon') and 
                record.get('timestamp')):
                
                try:
                    timestamp = datetime.fromisoformat(record['timestamp'][:19])
                    events.append({
                        'domain': domain_label,
                        'lat': record['location_lat'],
                        'lon': record['location_lon'],
                        'timestamp': timestamp,
                        'record_id': record.get('case_id', 
                                              record.get('animal_id', 
                                                        record.get('survey_id', 'unknown')))
                    })
                except ValueError:
                    continue
        
        return events
    
    @staticmethod
    def _find_spatiotemporal_clusters(events: List[Dict],
                                    spatial_threshold_km: float,
                                    temporal_threshold_days: int) -> List[Dict]:
        """Find spatiotemporal clusters in events."""
        
        clusters = []
        used_events = set()
        
        for i, event in enumerate(events):
            if i in used_events:
                continue
            
            # Find nearby events in space and time
            cluster_events = [event]
            cluster_indices = {i}
            
            for j, other_event in enumerate(events):
                if j <= i or j in used_events:
                    continue
                
                # Check spatial proximity
                distance = SpatioTemporalAnalyzer._calculate_distance(
                    event['lat'], event['lon'],
                    other_event['lat'], other_event['lon']
                )
                
                # Check temporal proximity
                time_diff = abs((event['timestamp'] - other_event['timestamp']).days)
                
                if (distance <= spatial_threshold_km and 
                    time_diff <= temporal_threshold_days):
                    cluster_events.append(other_event)
                    cluster_indices.add(j)
            
            # Only consider clusters with multiple events
            if len(cluster_events) >= 2:
                clusters.append({
                    'cluster_id': f"CLUSTER_{len(clusters) + 1}",
                    'events': cluster_events,
                    'center_lat': statistics.mean([e['lat'] for e in cluster_events]),
                    'center_lon': statistics.mean([e['lon'] for e in cluster_events]),
                    'start_date': min(e['timestamp'] for e in cluster_events),
                    'end_date': max(e['timestamp'] for e in cluster_events),
                    'spatial_radius_km': spatial_threshold_km,
                    'temporal_span_days': temporal_threshold_days
                })
                
                used_events.update(cluster_indices)
        
        return clusters

class OneHealthAnalyzer:
    """Main analyzer for comprehensive One Health analysis."""
    
    def __init__(self):
        self.analysis_results: List[AnalysisResult] = []
        self.analysis_log: List[Dict] = []
        
        logger.info("One Health Analyzer initialized")
    
    def run_comprehensive_analysis(self, animal_data: List[Dict],
                                 human_data: List[Dict],
                                 environmental_data: List[Dict]) -> List[AnalysisResult]:
        """Run comprehensive cross-domain analysis."""
        
        start_time = datetime.now()
        results = []
        
        logger.info(f"Starting comprehensive analysis with {len(animal_data)} animal, "
                   f"{len(human_data)} human, {len(environmental_data)} environmental records")
        
        try:
            # Spatial correlation analysis
            spatial_result = SpatioTemporalAnalyzer.calculate_spatial_correlation(
                animal_data, human_data
            )
            results.append(spatial_result)
            logger.info(f"Spatial correlation: {spatial_result.correlation_coefficient:.3f}")
            
        except Exception as e:
            logger.error(f"Spatial analysis failed: {e}")
        
        try:
            # Temporal lag analysis
            temporal_result = SpatioTemporalAnalyzer.calculate_temporal_lag_correlation(
                animal_data, human_data
            )
            results.append(temporal_result)
            logger.info(f"Temporal correlation: {temporal_result.correlation_coefficient:.3f} "
                       f"(lag: {temporal_result.time_lag_days} days)")
            
        except Exception as e:
            logger.error(f"Temporal analysis failed: {e}")
        
        try:
            # Pathogen flow analysis
            pathogen_result = PathogenFlowAnalyzer.analyze_pathogen_transmission(
                animal_data, human_data, environmental_data
            )
            results.append(pathogen_result)
            logger.info(f"Pathogen analysis: {len(pathogen_result.shared_pathogens or [])} "
                       f"shared pathogens")
            
        except Exception as e:
            logger.error(f"Pathogen analysis failed: {e}")
        
        try:
            # Cluster analysis
            cluster_result = ClusterAnalyzer.detect_cross_domain_clusters(
                animal_data, human_data
            )
            results.append(cluster_result)
            logger.info(f"Cluster analysis: {len(cluster_result.geographic_clusters or [])} "
                       f"cross-domain clusters")
            
        except Exception as e:
            logger.error(f"Cluster analysis failed: {e}")
        
        # Store results
        self.analysis_results.extend(results)
        
        # Log performance
        analysis_time = (datetime.now() - start_time).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": start_time.isoformat(),
            "analysis_duration_seconds": analysis_time,
            "total_analyses": len(results),
            "data_inputs": {
                "animal_records": len(animal_data),
                "human_records": len(human_data),
                "environmental_records": len(environmental_data)
            }
        })
        
        logger.info(f"Comprehensive analysis completed in {analysis_time:.2f} seconds")
        
        return results
    
    def get_analysis_summary(self) -> Dict:
        """Get summary of all analyses performed."""
        
        if not self.analysis_results:
            return {"message": "No analyses performed"}
        
        # Group results by analysis type
        by_type = defaultdict(list)
        for result in self.analysis_results:
            by_type[result.analysis_type.value].append(result)
        
        # Calculate summary statistics
        significant_results = [r for r in self.analysis_results if r.statistical_significance]
        strong_relationships = [r for r in self.analysis_results 
                              if r.relationship_strength == "strong"]
        
        correlation_values = [r.correlation_coefficient for r in self.analysis_results 
                            if r.correlation_coefficient is not None]
        
        summary = {
            "total_analyses": len(self.analysis_results),
            "analysis_types": {atype: len(results) for atype, results in by_type.items()},
            "significant_results": len(significant_results),
            "strong_relationships": len(strong_relationships),
            "performance": {
                "total_analysis_runs": len(self.analysis_log),
                "average_duration": statistics.mean([log['analysis_duration_seconds'] 
                                                   for log in self.analysis_log]) if self.analysis_log else 0
            }
        }
        
        if correlation_values:
            summary["correlation_statistics"] = {
                "mean_correlation": statistics.mean(correlation_values),
                "max_correlation": max(correlation_values),
                "min_correlation": min(correlation_values)
            }
        
        # Key findings
        key_findings = []
        for result in self.analysis_results:
            if result.statistical_significance or result.relationship_strength in ["strong", "moderate"]:
                finding = {
                    "analysis_type": result.analysis_type.value,
                    "relationship_strength": result.relationship_strength,
                    "correlation": result.correlation_coefficient
                }
                
                if result.shared_pathogens:
                    finding["shared_pathogens"] = result.shared_pathogens
                
                if result.time_lag_days is not None:
                    finding["time_lag_days"] = result.time_lag_days
                
                key_findings.append(finding)
        
        summary["key_findings"] = key_findings
        
        return summary

# Mock data generator for testing
def generate_mock_analysis_data():
    """Generate mock data for cross-domain analysis testing."""
    
    # Mock animal data with coordinated outbreak
    animal_data = [
        {
            "animal_id": "FARM_001_COW_123",
            "timestamp": "2024-04-10T08:00:00",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "species": "cattle",
            "mortality_count": 8,
            "pathogen_detected": "H5N1"
        },
        {
            "animal_id": "FARM_002_PIG_456", 
            "timestamp": "2024-04-11T10:00:00",
            "location_lat": 40.7200,
            "location_lon": -74.0100,
            "species": "swine",
            "mortality_count": 3,
            "pathogen_detected": "Brucella"
        },
        {
            "animal_id": "POULTRY_003",
            "timestamp": "2024-04-12T14:00:00",
            "location_lat": 40.7050,
            "location_lon": -74.0080,
            "species": "poultry",
            "mortality_count": 15,
            "pathogen_detected": "H5N1"
        }
    ]
    
    # Mock human data with related cases
    human_data = [
        {
            "case_id": "HUM_001",
            "timestamp": "2024-04-12T18:00:00",
            "location_lat": 40.7150,
            "location_lon": -74.0070,
            "case_classification": "confirmed",
            "suspected_pathogen": "H5N1",
            "occupation": "farm_worker"
        },
        {
            "case_id": "HUM_002",
            "timestamp": "2024-04-13T09:00:00",
            "location_lat": 40.7180,
            "location_lon": -74.0090,
            "case_classification": "probable",
            "confirmed_pathogen": "H5N1"
        },
        {
            "case_id": "HUM_003",
            "timestamp": "2024-04-14T11:00:00",
            "location_lat": 40.7080,
            "location_lon": -74.0050,
            "case_classification": "confirmed",
            "suspected_pathogen": "Brucella"
        }
    ]
    
    # Mock environmental data
    environmental_data = [
        {
            "survey_id": "VEC_001",
            "timestamp": "2024-04-11T20:00:00",
            "location_lat": 40.7100,
            "location_lon": -74.0075,
            "parameter": "vector_count",
            "total_collected": 45,
            "pathogen_detected": "West_Nile_virus"
        },
        {
            "record_id": "CLIMATE_001",
            "timestamp": "2024-04-10T12:00:00",
            "location_lat": 40.7128,
            "location_lon": -74.0060,
            "parameter": "temperature",
            "value": 28.5
        }
    ]
    
    return animal_data, human_data, environmental_data

def run_demonstration():
    """Run demonstration of cross-domain analysis."""
    print("🔬 One Health Cross-Domain Analyzer - Demonstration")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OneHealthAnalyzer()
    
    # Generate mock data
    animal_data, human_data, env_data = generate_mock_analysis_data()
    
    print(f"\n📊 Analysis Data Summary:")
    print(f"  Animal Records: {len(animal_data)}")
    print(f"  Human Records: {len(human_data)}")
    print(f"  Environmental Records: {len(env_data)}")
    
    # Run comprehensive analysis
    print(f"\n🔬 Running Cross-Domain Analysis...")
    results = analyzer.run_comprehensive_analysis(animal_data, human_data, env_data)
    
    # Display results
    print(f"\n📈 Analysis Results ({len(results)} analyses):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.analysis_type.value.replace('_', ' ').title()} Analysis")
        print(f"   Analysis ID: {result.analysis_id}")
        print(f"   Domains: {[d.value for d in result.domains]}")
        print(f"   Sample Size: {result.sample_size}")
        
        if result.correlation_coefficient is not None:
            print(f"   Correlation: {result.correlation_coefficient:.3f}")
        
        if result.p_value is not None:
            print(f"   P-value: {result.p_value:.3f}")
        
        print(f"   Relationship Strength: {result.relationship_strength}")
        print(f"   Statistical Significance: {result.statistical_significance}")
        
        if result.time_lag_days is not None:
            print(f"   Time Lag: {result.time_lag_days} days")
        
        if result.shared_pathogens:
            print(f"   Shared Pathogens: {result.shared_pathogens}")
        
        if result.transmission_pathways:
            print(f"   Transmission Pathways: {len(result.transmission_pathways)}")
        
        if result.geographic_clusters:
            print(f"   Geographic Clusters: {len(result.geographic_clusters)}")
    
    # Analysis summary
    summary = analyzer.get_analysis_summary()
    print(f"\n📊 Analysis Summary:")
    print(f"  Total Analyses: {summary['total_analyses']}")
    print(f"  Significant Results: {summary['significant_results']}")
    print(f"  Strong Relationships: {summary['strong_relationships']}")
    
    if 'correlation_statistics' in summary:
        corr_stats = summary['correlation_statistics']
        print(f"  Mean Correlation: {corr_stats['mean_correlation']:.3f}")
        print(f"  Max Correlation: {corr_stats['max_correlation']:.3f}")
    
    # Key findings
    if summary['key_findings']:
        print(f"\n🔍 Key Findings ({len(summary['key_findings'])}):")
        for i, finding in enumerate(summary['key_findings'], 1):
            print(f"  {i}. {finding['analysis_type'].replace('_', ' ').title()}: "
                  f"{finding['relationship_strength']} relationship")
            if finding.get('correlation'):
                print(f"     Correlation: {finding['correlation']:.3f}")
            if finding.get('shared_pathogens'):
                print(f"     Shared Pathogens: {finding['shared_pathogens']}")
    
    print(f"\n⚡ Performance: {summary['performance']['average_duration']:.3f}s average")
    
    return analyzer

if __name__ == "__main__":
    analyzer = run_demonstration()
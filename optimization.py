"""
Optimization Algorithms System
==============================
Module 3: Analysis & Modeling Tools

Advanced optimization algorithms for One Health surveillance system enhancement,
providing resource allocation, parameter tuning, and response strategy optimization.

NIW Focus: Optimization intelligence maximizing surveillance efficiency and outbreak response.
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
import copy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizationType(Enum):
    """Types of optimization problems."""
    RESOURCE_ALLOCATION = "resource_allocation"     # Surveillance resource allocation
    PARAMETER_TUNING = "parameter_tuning"           # Model parameter optimization  
    NETWORK_DESIGN = "network_design"               # Surveillance network topology
    RESPONSE_STRATEGY = "response_strategy"         # Outbreak response optimization
    COST_MINIMIZATION = "cost_minimization"         # Cost-effective surveillance
    COVERAGE_MAXIMIZATION = "coverage_maximization" # Geographic coverage optimization

class OptimizationAlgorithm(Enum):
    """Optimization algorithms."""
    GENETIC_ALGORITHM = "genetic_algorithm"         # Evolutionary optimization
    PARTICLE_SWARM = "particle_swarm"               # Swarm intelligence
    SIMULATED_ANNEALING = "simulated_annealing"     # Probabilistic optimization
    GRADIENT_DESCENT = "gradient_descent"           # Gradient-based optimization
    RANDOM_SEARCH = "random_search"                 # Random sampling
    GRID_SEARCH = "grid_search"                     # Exhaustive parameter search
    BAYESIAN_OPTIMIZATION = "bayesian_optimization" # Probabilistic model-based

class ObjectiveType(Enum):
    """Optimization objectives."""
    MINIMIZE = "minimize"                           # Minimize objective
    MAXIMIZE = "maximize"                           # Maximize objective
    MULTI_OBJECTIVE = "multi_objective"             # Multiple objectives

class ConvergenceStatus(Enum):
    """Optimization convergence status."""
    CONVERGED = "converged"                         # Optimization converged
    MAX_ITERATIONS = "max_iterations"               # Reached iteration limit
    NO_IMPROVEMENT = "no_improvement"               # No improvement detected
    DIVERGED = "diverged"                           # Optimization diverged
    INTERRUPTED = "interrupted"                     # Optimization interrupted

@dataclass
class OptimizationParameter:
    """Single optimization parameter definition."""
    
    name: str
    value_type: str  # "float", "int", "categorical"
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    categories: Optional[List[str]] = None
    current_value: Optional[Union[float, int, str]] = None
    best_value: Optional[Union[float, int, str]] = None
    optimization_history: List[Union[float, int, str]] = field(default_factory=list)

@dataclass
class OptimizationConstraint:
    """Optimization constraint definition."""
    
    constraint_id: str
    constraint_type: str  # "equality", "inequality", "bound"
    constraint_function: str  # Description of constraint
    tolerance: float = 1e-6
    is_satisfied: bool = True
    violation_amount: float = 0.0

@dataclass
class OptimizationResult:
    """Result of optimization process."""
    
    optimization_id: str
    optimization_type: OptimizationType
    algorithm: OptimizationAlgorithm
    objective_type: ObjectiveType
    optimization_timestamp: datetime
    
    # Problem definition
    parameters: List[OptimizationParameter] = field(default_factory=list)
    constraints: List[OptimizationConstraint] = field(default_factory=list)
    
    # Optimization results
    best_objective_value: Optional[float] = None
    best_parameters: Dict[str, Union[float, int, str]] = field(default_factory=dict)
    objective_history: List[float] = field(default_factory=list)
    
    # Convergence information
    convergence_status: ConvergenceStatus = ConvergenceStatus.INTERRUPTED
    iterations_completed: int = 0
    max_iterations: int = 100
    convergence_tolerance: float = 1e-6
    improvement_threshold: float = 1e-8
    
    # Performance metrics
    optimization_duration_seconds: float = 0.0
    evaluations_count: int = 0
    convergence_rate: Optional[float] = None
    solution_quality: str = "unknown"  # "poor", "fair", "good", "excellent"
    
    # Statistical analysis
    objective_mean: Optional[float] = None
    objective_std: Optional[float] = None
    parameter_sensitivity: Dict[str, float] = field(default_factory=dict)
    
    # Key insights
    optimization_summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class ObjectiveFunction:
    """Base class for optimization objective functions."""
    
    def __init__(self, name: str, objective_type: ObjectiveType = ObjectiveType.MINIMIZE):
        self.name = name
        self.objective_type = objective_type
        self.evaluation_count = 0
        
    def evaluate(self, parameters: Dict[str, Union[float, int, str]]) -> float:
        """Evaluate objective function."""
        self.evaluation_count += 1
        return self._compute_objective(parameters)
    
    def _compute_objective(self, parameters: Dict[str, Union[float, int, str]]) -> float:
        """Compute objective value - to be implemented by subclasses."""
        raise NotImplementedError

class SurveillanceResourceObjective(ObjectiveFunction):
    """Objective function for surveillance resource allocation."""
    
    def __init__(self):
        super().__init__("surveillance_resource_allocation", ObjectiveType.MINIMIZE)
        
    def _compute_objective(self, parameters: Dict[str, Union[float, int, str]]) -> float:
        """Minimize cost while maximizing coverage."""
        # Resource allocation parameters
        human_resources = parameters.get("human_resources", 10)
        animal_resources = parameters.get("animal_resources", 8) 
        lab_resources = parameters.get("lab_resources", 5)
        geographic_coverage = parameters.get("geographic_coverage", 0.7)
        
        # Cost calculation (minimizing)
        resource_cost = (human_resources * 1000 + 
                        animal_resources * 800 + 
                        lab_resources * 1500)
        
        # Coverage penalty (maximize coverage = minimize negative coverage)
        coverage_penalty = (1.0 - geographic_coverage) * 10000
        
        # Detection efficiency bonus
        detection_efficiency = min(1.0, (human_resources + animal_resources) / 25)
        efficiency_bonus = (1.0 - detection_efficiency) * 5000
        
        total_cost = resource_cost + coverage_penalty + efficiency_bonus
        return total_cost

class OutbreakResponseObjective(ObjectiveFunction):
    """Objective function for outbreak response optimization."""
    
    def __init__(self):
        super().__init__("outbreak_response_optimization", ObjectiveType.MINIMIZE)
        
    def _compute_objective(self, parameters: Dict[str, Union[float, int, str]]) -> float:
        """Minimize response time and casualties."""
        # Response parameters
        response_time = parameters.get("response_time", 24)  # hours
        team_size = parameters.get("team_size", 5)
        equipment_level = parameters.get("equipment_level", 3)  # 1-5 scale
        coordination_score = parameters.get("coordination_score", 0.6)  # 0-1
        
        # Time penalty (earlier response is better)
        time_penalty = response_time * 100
        
        # Resource efficiency
        resource_efficiency = team_size * equipment_level * coordination_score
        efficiency_bonus = max(0, 100 - resource_efficiency) * 50
        
        # Coverage effectiveness
        coverage_effectiveness = min(1.0, team_size / 10) * coordination_score
        coverage_penalty = (1.0 - coverage_effectiveness) * 1000
        
        total_penalty = time_penalty + efficiency_bonus + coverage_penalty
        return total_penalty

class ParameterTuningObjective(ObjectiveFunction):
    """Objective function for model parameter tuning."""
    
    def __init__(self):
        super().__init__("parameter_tuning", ObjectiveType.MAXIMIZE)
        
    def _compute_objective(self, parameters: Dict[str, Union[float, int, str]]) -> float:
        """Maximize model performance metrics."""
        # Model parameters
        learning_rate = parameters.get("learning_rate", 0.01)
        regularization = parameters.get("regularization", 0.1)
        threshold = parameters.get("threshold", 0.5)
        ensemble_size = parameters.get("ensemble_size", 3)
        
        # Simulated model performance
        # Performance decreases if learning rate too high/low
        lr_factor = 1.0 - abs(learning_rate - 0.001) * 100
        
        # Regularization optimal around 0.1
        reg_factor = 1.0 - abs(regularization - 0.1) * 2
        
        # Threshold optimal around 0.5 for balanced classification
        threshold_factor = 1.0 - abs(threshold - 0.5) * 0.8
        
        # Ensemble benefits with diminishing returns
        ensemble_factor = min(1.0, ensemble_size / 5.0)
        
        # Combined performance score
        performance = (lr_factor * 0.3 + 
                      reg_factor * 0.3 + 
                      threshold_factor * 0.2 + 
                      ensemble_factor * 0.2)
        
        return max(0.0, min(1.0, performance))  # Bounded between 0 and 1

class GeneticAlgorithm:
    """Genetic algorithm implementation."""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1, 
                 crossover_rate: float = 0.8, elitism_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        
    def optimize(self, objective: ObjectiveFunction, parameters: List[OptimizationParameter],
                max_iterations: int = 100) -> OptimizationResult:
        """Run genetic algorithm optimization."""
        
        result = OptimizationResult(
            optimization_id=f"GA_{random.randint(100000, 999999)}",
            optimization_type=OptimizationType.PARAMETER_TUNING,
            algorithm=OptimizationAlgorithm.GENETIC_ALGORITHM,
            objective_type=objective.objective_type,
            optimization_timestamp=datetime.now(),
            parameters=copy.deepcopy(parameters),
            max_iterations=max_iterations
        )
        
        start_time = datetime.now()
        
        # Initialize population
        population = self._initialize_population(parameters)
        best_fitness = float('-inf') if objective.objective_type == ObjectiveType.MAXIMIZE else float('inf')
        best_individual = None
        no_improvement_count = 0
        
        for iteration in range(max_iterations):
            # Evaluate fitness
            fitness_scores = []
            for individual in population:
                params_dict = {p.name: individual[i] for i, p in enumerate(parameters)}
                fitness = objective.evaluate(params_dict)
                fitness_scores.append(fitness)
                
                # Track best solution
                is_better = (objective.objective_type == ObjectiveType.MAXIMIZE and fitness > best_fitness) or \
                           (objective.objective_type == ObjectiveType.MINIMIZE and fitness < best_fitness)
                
                if is_better:
                    best_fitness = fitness
                    best_individual = individual.copy()
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
            
            result.objective_history.append(best_fitness)
            result.iterations_completed = iteration + 1
            
            # Check convergence
            if no_improvement_count > 20:
                result.convergence_status = ConvergenceStatus.NO_IMPROVEMENT
                break
                
            # Selection, crossover, mutation
            new_population = []
            
            # Elitism - keep best individuals
            elite_count = int(self.population_size * self.elitism_rate)
            if elite_count > 0:
                sorted_pop = sorted(zip(population, fitness_scores), 
                                  key=lambda x: x[1], reverse=(objective.objective_type == ObjectiveType.MAXIMIZE))
                for i in range(elite_count):
                    new_population.append(sorted_pop[i][0])
            
            # Generate offspring
            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(population, fitness_scores, objective.objective_type)
                parent2 = self._tournament_selection(population, fitness_scores, objective.objective_type)
                
                if random.random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1.copy(), parent2.copy()
                
                if random.random() < self.mutation_rate:
                    child1 = self._mutate(child1, parameters)
                if random.random() < self.mutation_rate:
                    child2 = self._mutate(child2, parameters)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        if result.convergence_status == ConvergenceStatus.INTERRUPTED:
            result.convergence_status = ConvergenceStatus.MAX_ITERATIONS
            
        # Finalize results
        end_time = datetime.now()
        result.optimization_duration_seconds = (end_time - start_time).total_seconds()
        result.evaluations_count = objective.evaluation_count
        result.best_objective_value = best_fitness
        result.best_parameters = {p.name: best_individual[i] for i, p in enumerate(parameters)}
        
        if len(result.objective_history) > 1:
            result.objective_mean = statistics.mean(result.objective_history)
            result.objective_std = statistics.stdev(result.objective_history)
            
        # Solution quality assessment
        if objective.objective_type == ObjectiveType.MAXIMIZE:
            if best_fitness > 0.9:
                result.solution_quality = "excellent"
            elif best_fitness > 0.7:
                result.solution_quality = "good"
            elif best_fitness > 0.5:
                result.solution_quality = "fair"
            else:
                result.solution_quality = "poor"
        else:
            if best_fitness < 1000:
                result.solution_quality = "excellent"
            elif best_fitness < 5000:
                result.solution_quality = "good"
            elif best_fitness < 10000:
                result.solution_quality = "fair"
            else:
                result.solution_quality = "poor"
        
        result.optimization_summary = f"GA optimization completed in {result.iterations_completed} iterations"
        result.key_findings.append(f"Best objective value: {best_fitness:.3f}")
        result.key_findings.append(f"Convergence status: {result.convergence_status.value}")
        
        return result
    
    def _initialize_population(self, parameters: List[OptimizationParameter]) -> List[List[float]]:
        """Initialize random population."""
        population = []
        for _ in range(self.population_size):
            individual = []
            for param in parameters:
                if param.value_type == "float":
                    value = random.uniform(param.min_value, param.max_value)
                elif param.value_type == "int":
                    value = random.randint(int(param.min_value), int(param.max_value))
                else:  # categorical
                    value = random.choice(param.categories)
                individual.append(value)
            population.append(individual)
        return population
    
    def _tournament_selection(self, population: List[List[float]], fitness_scores: List[float],
                            objective_type: ObjectiveType) -> List[float]:
        """Tournament selection."""
        tournament_size = 3
        tournament_indices = random.sample(range(len(population)), tournament_size)
        
        best_idx = tournament_indices[0]
        best_fitness = fitness_scores[best_idx]
        
        for idx in tournament_indices[1:]:
            fitness = fitness_scores[idx]
            is_better = (objective_type == ObjectiveType.MAXIMIZE and fitness > best_fitness) or \
                       (objective_type == ObjectiveType.MINIMIZE and fitness < best_fitness)
            if is_better:
                best_idx = idx
                best_fitness = fitness
                
        return population[best_idx].copy()
    
    def _crossover(self, parent1: List[float], parent2: List[float]) -> Tuple[List[float], List[float]]:
        """Single-point crossover."""
        if len(parent1) <= 1:
            return parent1.copy(), parent2.copy()
            
        crossover_point = random.randint(1, len(parent1) - 1)
        
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2
    
    def _mutate(self, individual: List[float], parameters: List[OptimizationParameter]) -> List[float]:
        """Gaussian mutation."""
        mutated = individual.copy()
        
        for i, param in enumerate(parameters):
            if random.random() < 0.1:  # 10% chance per gene
                if param.value_type == "float":
                    mutation_strength = (param.max_value - param.min_value) * 0.1
                    mutated[i] += random.gauss(0, mutation_strength)
                    mutated[i] = max(param.min_value, min(param.max_value, mutated[i]))
                elif param.value_type == "int":
                    mutation_range = int((param.max_value - param.min_value) * 0.2)
                    mutated[i] += random.randint(-mutation_range, mutation_range)
                    mutated[i] = max(param.min_value, min(param.max_value, mutated[i]))
                else:  # categorical
                    mutated[i] = random.choice(param.categories)
        
        return mutated

class ParticleSwarmOptimizer:
    """Particle Swarm Optimization implementation."""
    
    def __init__(self, swarm_size: int = 30, inertia: float = 0.7, 
                 cognitive: float = 2.0, social: float = 2.0):
        self.swarm_size = swarm_size
        self.inertia = inertia
        self.cognitive = cognitive
        self.social = social
        
    def optimize(self, objective: ObjectiveFunction, parameters: List[OptimizationParameter],
                max_iterations: int = 100) -> OptimizationResult:
        """Run particle swarm optimization."""
        
        result = OptimizationResult(
            optimization_id=f"PSO_{random.randint(100000, 999999)}",
            optimization_type=OptimizationType.PARAMETER_TUNING,
            algorithm=OptimizationAlgorithm.PARTICLE_SWARM,
            objective_type=objective.objective_type,
            optimization_timestamp=datetime.now(),
            parameters=copy.deepcopy(parameters),
            max_iterations=max_iterations
        )
        
        start_time = datetime.now()
        
        # Initialize particles
        particles = self._initialize_swarm(parameters)
        velocities = [[0.0] * len(parameters) for _ in range(self.swarm_size)]
        personal_best_positions = [p.copy() for p in particles]
        personal_best_fitness = [float('-inf') if objective.objective_type == ObjectiveType.MAXIMIZE 
                               else float('inf')] * self.swarm_size
        
        global_best_position = None
        global_best_fitness = float('-inf') if objective.objective_type == ObjectiveType.MAXIMIZE else float('inf')
        
        no_improvement_count = 0
        
        for iteration in range(max_iterations):
            # Evaluate particles
            for i, particle in enumerate(particles):
                params_dict = {p.name: particle[j] for j, p in enumerate(parameters)}
                fitness = objective.evaluate(params_dict)
                
                # Update personal best
                is_better_personal = (objective.objective_type == ObjectiveType.MAXIMIZE and 
                                    fitness > personal_best_fitness[i]) or \
                                   (objective.objective_type == ObjectiveType.MINIMIZE and 
                                    fitness < personal_best_fitness[i])
                
                if is_better_personal:
                    personal_best_fitness[i] = fitness
                    personal_best_positions[i] = particle.copy()
                
                # Update global best
                is_better_global = (objective.objective_type == ObjectiveType.MAXIMIZE and 
                                  fitness > global_best_fitness) or \
                                 (objective.objective_type == ObjectiveType.MINIMIZE and 
                                  fitness < global_best_fitness)
                
                if is_better_global:
                    global_best_fitness = fitness
                    global_best_position = particle.copy()
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1
            
            result.objective_history.append(global_best_fitness)
            result.iterations_completed = iteration + 1
            
            # Check convergence
            if no_improvement_count > 25:
                result.convergence_status = ConvergenceStatus.NO_IMPROVEMENT
                break
            
            # Update velocities and positions
            for i in range(self.swarm_size):
                for j in range(len(parameters)):
                    r1, r2 = random.random(), random.random()
                    
                    # Velocity update
                    velocities[i][j] = (self.inertia * velocities[i][j] +
                                      self.cognitive * r1 * (personal_best_positions[i][j] - particles[i][j]) +
                                      self.social * r2 * (global_best_position[j] - particles[i][j]))
                    
                    # Position update
                    particles[i][j] += velocities[i][j]
                    
                    # Boundary constraints
                    param = parameters[j]
                    if param.value_type in ["float", "int"]:
                        particles[i][j] = max(param.min_value, min(param.max_value, particles[i][j]))
        
        if result.convergence_status == ConvergenceStatus.INTERRUPTED:
            result.convergence_status = ConvergenceStatus.MAX_ITERATIONS
            
        # Finalize results
        end_time = datetime.now()
        result.optimization_duration_seconds = (end_time - start_time).total_seconds()
        result.evaluations_count = objective.evaluation_count
        result.best_objective_value = global_best_fitness
        result.best_parameters = {p.name: global_best_position[i] for i, p in enumerate(parameters)}
        
        if len(result.objective_history) > 1:
            result.objective_mean = statistics.mean(result.objective_history)
            result.objective_std = statistics.stdev(result.objective_history)
            
        # Solution quality assessment
        if objective.objective_type == ObjectiveType.MAXIMIZE:
            if global_best_fitness > 0.9:
                result.solution_quality = "excellent"
            elif global_best_fitness > 0.7:
                result.solution_quality = "good"
            elif global_best_fitness > 0.5:
                result.solution_quality = "fair"
            else:
                result.solution_quality = "poor"
        else:
            if global_best_fitness < 1000:
                result.solution_quality = "excellent"
            elif global_best_fitness < 5000:
                result.solution_quality = "good"
            elif global_best_fitness < 10000:
                result.solution_quality = "fair"
            else:
                result.solution_quality = "poor"
        
        result.optimization_summary = f"PSO optimization completed in {result.iterations_completed} iterations"
        result.key_findings.append(f"Best objective value: {global_best_fitness:.3f}")
        result.key_findings.append(f"Convergence status: {result.convergence_status.value}")
        
        return result
    
    def _initialize_swarm(self, parameters: List[OptimizationParameter]) -> List[List[float]]:
        """Initialize random swarm."""
        swarm = []
        for _ in range(self.swarm_size):
            particle = []
            for param in parameters:
                if param.value_type == "float":
                    value = random.uniform(param.min_value, param.max_value)
                elif param.value_type == "int":
                    value = random.randint(int(param.min_value), int(param.max_value))
                else:  # categorical
                    value = random.choice(param.categories)
                particle.append(value)
            swarm.append(particle)
        return swarm

class OptimizationManager:
    """Central optimization management system."""
    
    def __init__(self):
        self.optimization_results: List[OptimizationResult] = []
        self.objective_functions: Dict[str, ObjectiveFunction] = {}
        self.algorithms: Dict[str, Any] = {
            "genetic_algorithm": GeneticAlgorithm(),
            "particle_swarm": ParticleSwarmOptimizer()
        }
        
        # Register default objective functions
        self._register_default_objectives()
        
        logger.info("One Health Optimization Manager initialized")
    
    def _register_default_objectives(self):
        """Register default objective functions."""
        self.objective_functions["surveillance_resource"] = SurveillanceResourceObjective()
        self.objective_functions["outbreak_response"] = OutbreakResponseObjective()
        self.objective_functions["parameter_tuning"] = ParameterTuningObjective()
    
    def run_optimization(self, optimization_type: str, algorithm_name: str,
                        parameters: List[OptimizationParameter], 
                        max_iterations: int = 100) -> OptimizationResult:
        """Run optimization with specified algorithm and parameters."""
        
        if optimization_type not in self.objective_functions:
            raise ValueError(f"Unknown optimization type: {optimization_type}")
        
        if algorithm_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        objective = self.objective_functions[optimization_type]
        algorithm = self.algorithms[algorithm_name]
        
        logger.info(f"Starting {algorithm_name} optimization for {optimization_type}")
        
        result = algorithm.optimize(objective, parameters, max_iterations)
        self.optimization_results.append(result)
        
        logger.info(f"Optimization completed: {result.optimization_id}")
        
        return result
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """Get comprehensive optimization summary."""
        
        if not self.optimization_results:
            return {"message": "No optimizations completed"}
        
        # Performance statistics
        durations = [r.optimization_duration_seconds for r in self.optimization_results]
        evaluations = [r.evaluations_count for r in self.optimization_results]
        
        # Quality distribution
        quality_dist = defaultdict(int)
        algorithm_dist = defaultdict(int)
        convergence_dist = defaultdict(int)
        
        for result in self.optimization_results:
            quality_dist[result.solution_quality] += 1
            algorithm_dist[result.algorithm.value] += 1
            convergence_dist[result.convergence_status.value] += 1
        
        # Best results per optimization type
        best_results = {}
        for result in self.optimization_results:
            opt_type = result.optimization_type.value
            if opt_type not in best_results:
                best_results[opt_type] = result
            else:
                current_best = best_results[opt_type]
                is_better = (result.objective_type == ObjectiveType.MAXIMIZE and 
                           result.best_objective_value > current_best.best_objective_value) or \
                          (result.objective_type == ObjectiveType.MINIMIZE and 
                           result.best_objective_value < current_best.best_objective_value)
                if is_better:
                    best_results[opt_type] = result
        
        return {
            "total_optimizations": len(self.optimization_results),
            "optimization_types": list(set(r.optimization_type.value for r in self.optimization_results)),
            "algorithms_used": list(set(r.algorithm.value for r in self.optimization_results)),
            "performance_stats": {
                "mean_duration": statistics.mean(durations),
                "total_duration": sum(durations),
                "mean_evaluations": statistics.mean(evaluations),
                "total_evaluations": sum(evaluations)
            },
            "quality_distribution": dict(quality_dist),
            "algorithm_distribution": dict(algorithm_dist),
            "convergence_distribution": dict(convergence_dist),
            "best_results_summary": [
                {
                    "optimization_type": opt_type,
                    "algorithm": result.algorithm.value,
                    "objective_value": result.best_objective_value,
                    "quality": result.solution_quality,
                    "optimization_id": result.optimization_id
                }
                for opt_type, result in best_results.items()
            ]
        }

def run_demonstration() -> OptimizationManager:
    """Run comprehensive optimization demonstration."""
    
    print("🔧 One Health Optimization System - Demonstration")
    print("=" * 60)
    
    manager = OptimizationManager()
    
    # Define optimization problems
    optimization_problems = [
        # Resource allocation optimization
        {
            "type": "surveillance_resource",
            "parameters": [
                OptimizationParameter("human_resources", "int", 5, 20),
                OptimizationParameter("animal_resources", "int", 3, 15),
                OptimizationParameter("lab_resources", "int", 2, 10),
                OptimizationParameter("geographic_coverage", "float", 0.3, 1.0)
            ],
            "algorithms": ["genetic_algorithm", "particle_swarm"],
            "max_iterations": 50
        },
        # Outbreak response optimization
        {
            "type": "outbreak_response",
            "parameters": [
                OptimizationParameter("response_time", "float", 1, 72),  # hours
                OptimizationParameter("team_size", "int", 3, 15),
                OptimizationParameter("equipment_level", "int", 1, 5),
                OptimizationParameter("coordination_score", "float", 0.3, 1.0)
            ],
            "algorithms": ["genetic_algorithm"],
            "max_iterations": 40
        },
        # Parameter tuning optimization  
        {
            "type": "parameter_tuning",
            "parameters": [
                OptimizationParameter("learning_rate", "float", 0.0001, 0.1),
                OptimizationParameter("regularization", "float", 0.01, 1.0),
                OptimizationParameter("threshold", "float", 0.1, 0.9),
                OptimizationParameter("ensemble_size", "int", 1, 10)
            ],
            "algorithms": ["particle_swarm"],
            "max_iterations": 60
        }
    ]
    
    print(f"\n📊 Optimization Problems:")
    for i, problem in enumerate(optimization_problems, 1):
        print(f"  Problem {i}: {problem['type']}")
        print(f"    Parameters: {len(problem['parameters'])}")
        print(f"    Algorithms: {', '.join(problem['algorithms'])}")
    
    print(f"\n🔧 Running Comprehensive Optimization...")
    
    # Run optimizations
    results = []
    for problem in optimization_problems:
        for algorithm in problem["algorithms"]:
            print(f"\n{len(results) + 1}. {algorithm.replace('_', ' ').title()} - {problem['type']}")
            
            result = manager.run_optimization(
                optimization_type=problem["type"],
                algorithm_name=algorithm,
                parameters=problem["parameters"],
                max_iterations=problem["max_iterations"]
            )
            results.append(result)
    
    return manager

def display_optimization_results(manager: OptimizationManager):
    """Display comprehensive optimization results."""
    
    results = manager.optimization_results
    
    print(f"\n📊 Optimization Results ({len(results)} total):")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.algorithm.value.replace('_', ' ').title()}")
        print(f"   Optimization Type: {result.optimization_type.value.replace('_', ' ').title()}")
        print(f"   Objective: {result.objective_type.value.title()}")
        print(f"   Best Value: {result.best_objective_value:.3f}")
        print(f"   Convergence: {result.convergence_status.value.replace('_', ' ').title()}")
        print(f"   Iterations: {result.iterations_completed}")
        print(f"   Quality: {result.solution_quality.upper()}")
        print(f"   Duration: {result.optimization_duration_seconds:.3f}s")
        print(f"   Evaluations: {result.evaluations_count}")
        
        if result.best_parameters:
            print(f"   Best Parameters:")
            for param_name, param_value in result.best_parameters.items():
                if isinstance(param_value, float):
                    print(f"     • {param_name}: {param_value:.3f}")
                else:
                    print(f"     • {param_name}: {param_value}")
        
        if result.key_findings:
            print(f"   Key Findings ({len(result.key_findings)}):")
            for finding in result.key_findings:
                print(f"     • {finding}")
    
    # Summary statistics
    summary = manager.get_optimization_summary()
    
    print(f"\n📊 Optimization Summary:")
    print(f"  Total Optimizations: {summary['total_optimizations']}")
    print(f"  Optimization Types: {', '.join(summary['optimization_types'])}")
    print(f"  Algorithms Used: {', '.join(summary['algorithms_used'])}")
    
    print(f"\n📈 Performance Stats:")
    perf = summary["performance_stats"]
    print(f"  Average Duration: {perf['mean_duration']:.3f}s")
    print(f"  Total Duration: {perf['total_duration']:.3f}s") 
    print(f"  Average Evaluations: {perf['mean_evaluations']:.0f}")
    print(f"  Total Evaluations: {perf['total_evaluations']}")
    
    print(f"\n🏆 Quality Distribution:")
    for quality, count in summary["quality_distribution"].items():
        print(f"  {quality.title()}: {count}")
    
    print(f"\n🔄 Convergence Status:")
    for status, count in summary["convergence_distribution"].items():
        print(f"  {status.replace('_', ' ').title()}: {count}")
    
    print(f"\n🏆 BEST PERFORMING Optimizations ({len(summary['best_results_summary'])}):")
    for i, best in enumerate(summary["best_results_summary"], 1):
        print(f"  {i}. {best['optimization_type'].replace('_', ' ').title()}")
        print(f"     Algorithm: {best['algorithm'].replace('_', ' ').title()}")
        print(f"     Best Value: {best['objective_value']:.3f}")
        print(f"     Quality: {best['quality'].title()}")
    
    print(f"\n⚡ Performance:")
    avg_time = perf['mean_duration']
    total_time = perf['total_duration']
    print(f"  Average Optimization Time: {avg_time:.3f}s")
    print(f"  Total Optimization Time: {total_time:.3f}s")

if __name__ == "__main__":
    # Run comprehensive demonstration
    optimization_manager = run_demonstration()
    display_optimization_results(optimization_manager)
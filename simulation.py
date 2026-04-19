"""
Monte Carlo Simulation Engine
============================
Module 3: Analysis & Modeling Tools

Advanced Monte Carlo simulation system for One Health surveillance, providing
epidemic scenario modeling, intervention assessment, and probabilistic forecasting.

NIW Focus: Simulation intelligence enabling scenario-based preparedness planning.
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

class SimulationType(Enum):
    """Types of simulations."""
    EPIDEMIC_SPREAD = "epidemic_spread"         # Disease spread simulation
    INTERVENTION_IMPACT = "intervention_impact" # Intervention effectiveness
    SCENARIO_COMPARISON = "scenario_comparison" # Multiple scenario comparison
    SENSITIVITY_ANALYSIS = "sensitivity_analysis" # Parameter sensitivity
    STOCHASTIC_MODEL = "stochastic_model"       # General stochastic modeling
    OUTBREAK_RESPONSE = "outbreak_response"     # Response strategy simulation

class ModelType(Enum):
    """Types of epidemic models."""
    SIR = "sir"                                # Susceptible-Infected-Recovered
    SEIR = "seir"                             # With Exposed compartment
    SIRD = "sird"                             # With Death compartment
    AGENT_BASED = "agent_based"               # Agent-based modeling
    METAPOPULATION = "metapopulation"         # Multi-population model
    NETWORK_BASED = "network_based"           # Network transmission model

class InterventionType(Enum):
    """Types of interventions."""
    QUARANTINE = "quarantine"                 # Quarantine measures
    VACCINATION = "vaccination"               # Vaccination campaign
    MOVEMENT_RESTRICTION = "movement_restriction" # Movement controls
    SURVEILLANCE_ENHANCEMENT = "surveillance_enhancement" # Enhanced monitoring
    CONTACT_TRACING = "contact_tracing"       # Contact tracing
    FARM_BIOSECURITY = "farm_biosecurity"     # Agricultural biosecurity
    CULLING = "culling"                       # Animal culling

@dataclass
class SimulationParameter:
    """Simulation parameter with uncertainty."""
    name: str
    base_value: float
    distribution: str                         # "normal", "uniform", "gamma", "beta"
    variance: Optional[float] = None          # For normal distribution
    min_value: Optional[float] = None         # For uniform/bounds
    max_value: Optional[float] = None
    shape_alpha: Optional[float] = None       # For beta/gamma distribution
    shape_beta: Optional[float] = None
    
    def sample(self) -> float:
        """Sample a value from the parameter distribution."""
        if self.distribution == "normal":
            std_dev = math.sqrt(self.variance) if self.variance else self.base_value * 0.1
            value = random.normalvariate(self.base_value, std_dev)
            
            # Apply bounds if specified
            if self.min_value is not None:
                value = max(value, self.min_value)
            if self.max_value is not None:
                value = min(value, self.max_value)
                
            return value
            
        elif self.distribution == "uniform":
            min_val = self.min_value if self.min_value is not None else self.base_value * 0.8
            max_val = self.max_value if self.max_value is not None else self.base_value * 1.2
            return random.uniform(min_val, max_val)
            
        elif self.distribution == "gamma":
            # Use method of moments to parameterize
            if self.variance and self.variance > 0:
                scale = self.variance / self.base_value
                shape = self.base_value / scale
                return random.gammavariate(shape, scale)
            else:
                return self.base_value
                
        elif self.distribution == "beta":
            if self.shape_alpha and self.shape_beta:
                return random.betavariate(self.shape_alpha, self.shape_beta)
            else:
                return self.base_value
        else:
            return self.base_value

@dataclass
class EpidemicState:
    """State of epidemic at a point in time."""
    day: int
    susceptible: int
    exposed: Optional[int] = None
    infected: int = 0
    recovered: int = 0
    dead: int = 0
    
    # Domain-specific states
    animal_susceptible: int = 0
    animal_infected: int = 0
    human_susceptible: int = 0
    human_infected: int = 0
    
    # Additional tracking
    new_infections: int = 0
    cumulative_infections: int = 0
    effective_reproduction_number: Optional[float] = None
    
    @property
    def total_population(self) -> int:
        """Total population size."""
        return self.susceptible + (self.exposed or 0) + self.infected + self.recovered + self.dead

@dataclass
class InterventionScenario:
    """Intervention scenario definition."""
    intervention_id: str
    intervention_type: InterventionType
    start_day: int
    end_day: Optional[int] = None
    
    # Intervention parameters
    coverage: float = 0.8                     # Population coverage (0-1)
    effectiveness: float = 0.7               # Intervention effectiveness (0-1)
    compliance: float = 0.9                  # Population compliance (0-1)
    
    # Specific parameters
    target_population: str = "all"           # "all", "animal", "human", "high_risk"
    geographic_coverage: float = 1.0         # Geographic coverage (0-1)
    
    # Cost and resources
    cost_per_day: Optional[float] = None
    resource_requirement: Optional[float] = None
    
    def get_effective_impact(self, day: int) -> float:
        """Get effective impact on given day."""
        if day < self.start_day:
            return 0.0
        
        if self.end_day and day > self.end_day:
            return 0.0
        
        return self.coverage * self.effectiveness * self.compliance

@dataclass
class SimulationResult:
    """Result of a single simulation run."""
    run_id: int
    simulation_type: SimulationType
    model_type: ModelType
    
    # Time series data
    epidemic_timeline: List[EpidemicState]
    intervention_scenarios: List[InterventionScenario]
    
    # Final outcomes
    total_infected: int
    peak_infected: int
    peak_day: int
    epidemic_duration_days: int
    attack_rate: float                        # Final attack rate
    
    # Reproduction numbers
    basic_reproduction_number: float          # R0
    effective_reproduction_number: float      # Rt (with interventions)
    
    # Intervention impact
    infections_averted: Optional[int] = None
    intervention_cost: Optional[float] = None
    cost_effectiveness: Optional[float] = None
    
    # Domain-specific outcomes
    animal_attack_rate: Optional[float] = None
    human_attack_rate: Optional[float] = None
    zoonotic_transmissions: Optional[int] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['simulation_type'] = self.simulation_type.value
        data['model_type'] = self.model_type.value
        
        # Convert timeline
        data['epidemic_timeline'] = [
            {
                'day': state.day,
                'susceptible': state.susceptible,
                'infected': state.infected,
                'recovered': state.recovered,
                'new_infections': state.new_infections,
                'cumulative_infections': state.cumulative_infections
            }
            for state in self.epidemic_timeline
        ]
        
        return data

@dataclass
class MonteCarloResults:
    """Results from Monte Carlo simulation ensemble."""
    
    analysis_id: str
    simulation_type: SimulationType
    analysis_timestamp: datetime
    
    # Simulation configuration
    total_runs: int
    model_type: ModelType
    simulation_days: int
    base_parameters: Dict[str, float]
    
    # Statistical results
    mean_attack_rate: float
    median_attack_rate: float
    attack_rate_ci_95: Tuple[float, float]    # 95% confidence interval
    
    mean_peak_infected: float
    peak_infected_ci_95: Tuple[float, float]
    
    mean_epidemic_duration: float
    duration_ci_95: Tuple[float, float]
    
    # Risk assessment
    probability_major_outbreak: float         # P(attack_rate > 0.1)
    probability_peak_exceeded: float          # P(peak > threshold)
    expected_total_cases: float
    
    # Performance metrics
    simulation_duration_seconds: float = 0.0
    convergence_achieved: bool = False
    
    # Intervention analysis
    intervention_effectiveness: Optional[Dict[str, float]] = None
    cost_effectiveness_ratios: Optional[Dict[str, float]] = None
    
    # Sensitivity analysis
    parameter_sensitivity: Optional[Dict[str, float]] = None
    
    # Key insights
    key_findings: List[str] = None
    risk_scenarios: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.key_findings is None:
            self.key_findings = []
        if self.risk_scenarios is None:
            self.risk_scenarios = []
        if self.recommendations is None:
            self.recommendations = []

class SIRSimulator:
    """SIR epidemic model simulator."""
    
    @staticmethod
    def _poisson_sample(lam: float) -> int:
        """Sample from Poisson distribution using Knuth's algorithm."""
        if lam <= 0:
            return 0
        if lam > 30:  # For large lambda, use normal approximation
            return max(0, int(random.normalvariate(lam, math.sqrt(lam))))
        
        # Knuth's algorithm for small lambda
        L = math.exp(-lam)
        k = 0
        p = 1.0
        
        while True:
            k += 1
            p *= random.random()
            if p <= L:
                return k - 1
    
    @staticmethod
    def run_sir_simulation(population: int,
                          initial_infected: int,
                          transmission_rate: float,
                          recovery_rate: float,
                          simulation_days: int,
                          interventions: List[InterventionScenario] = None) -> SimulationResult:
        """Run SIR epidemic simulation."""
        
        if interventions is None:
            interventions = []
        
        # Initialize state
        current_state = EpidemicState(
            day=0,
            susceptible=population - initial_infected,
            infected=initial_infected,
            recovered=0,
            cumulative_infections=initial_infected
        )
        
        timeline = [current_state]
        
        # Calculate basic reproduction number
        r0 = transmission_rate / recovery_rate
        
        # Run simulation
        for day in range(1, simulation_days + 1):
            # Calculate intervention effects
            intervention_effect = 0.0
            for intervention in interventions:
                intervention_effect += intervention.get_effective_impact(day)
            
            # Adjust transmission rate for interventions
            effective_transmission_rate = transmission_rate * (1 - min(intervention_effect, 0.95))
            
            # SIR equations with stochastic elements
            S = current_state.susceptible
            I = current_state.infected
            R = current_state.recovered
            N = S + I + R
            
            if N == 0 or I == 0:
                break
            
            # Calculate transition probabilities
            infection_prob = effective_transmission_rate * S * I / N
            recovery_prob = recovery_rate * I
            
            # Stochastic transitions using custom Poisson implementation
            new_infections = min(S, SIRSimulator._poisson_sample(infection_prob) if infection_prob > 0 else 0)
            new_recoveries = min(I, SIRSimulator._poisson_sample(recovery_prob) if recovery_prob > 0 else 0)
            
            # Update state
            new_state = EpidemicState(
                day=day,
                susceptible=S - new_infections,
                infected=I + new_infections - new_recoveries,
                recovered=R + new_recoveries,
                new_infections=new_infections,
                cumulative_infections=current_state.cumulative_infections + new_infections
            )
            
            # Calculate effective reproduction number
            if S > 0 and N > 0:
                new_state.effective_reproduction_number = effective_transmission_rate * S / (N * recovery_rate)
            
            timeline.append(new_state)
            current_state = new_state
        
        # Calculate final metrics
        final_state = timeline[-1]
        total_infected = final_state.cumulative_infections
        attack_rate = total_infected / population
        
        # Find peak
        peak_infected = max(state.infected for state in timeline)
        peak_day = next(i for i, state in enumerate(timeline) if state.infected == peak_infected)
        
        # Calculate epidemic duration (days with active infections)
        epidemic_duration = len([state for state in timeline if state.infected > 0])
        
        # Calculate intervention impact
        infections_averted = None
        if interventions:
            # Compare with baseline (no intervention) scenario
            baseline_result = SIRSimulator.run_sir_simulation(
                population, initial_infected, transmission_rate, recovery_rate, simulation_days, []
            )
            infections_averted = baseline_result.total_infected - total_infected
        
        return SimulationResult(
            run_id=0,
            simulation_type=SimulationType.EPIDEMIC_SPREAD,
            model_type=ModelType.SIR,
            epidemic_timeline=timeline,
            intervention_scenarios=interventions,
            total_infected=total_infected,
            peak_infected=peak_infected,
            peak_day=peak_day,
            epidemic_duration_days=epidemic_duration,
            attack_rate=attack_rate,
            basic_reproduction_number=r0,
            effective_reproduction_number=timeline[-1].effective_reproduction_number or r0,
            infections_averted=infections_averted
        )

class SEIRSimulator:
    """SEIR epidemic model simulator with exposed compartment."""
    
    @staticmethod
    def run_seir_simulation(population: int,
                           initial_exposed: int,
                           transmission_rate: float,
                           incubation_rate: float,
                           recovery_rate: float,
                           simulation_days: int,
                           interventions: List[InterventionScenario] = None) -> SimulationResult:
        """Run SEIR epidemic simulation."""
        
        if interventions is None:
            interventions = []
        
        # Initialize state
        current_state = EpidemicState(
            day=0,
            susceptible=population - initial_exposed,
            exposed=initial_exposed,
            infected=0,
            recovered=0,
            cumulative_infections=0
        )
        
        timeline = [current_state]
        
        # Calculate basic reproduction number
        r0 = transmission_rate / recovery_rate
        
        # Run simulation
        for day in range(1, simulation_days + 1):
            # Calculate intervention effects
            intervention_effect = 0.0
            for intervention in interventions:
                intervention_effect += intervention.get_effective_impact(day)
            
            # Adjust transmission rate for interventions
            effective_transmission_rate = transmission_rate * (1 - min(intervention_effect, 0.95))
            
            # SEIR equations
            S = current_state.susceptible
            E = current_state.exposed or 0
            I = current_state.infected
            R = current_state.recovered
            N = S + E + I + R
            
            if N == 0 or (I == 0 and E == 0):
                break
            
            # Calculate transition rates
            exposure_rate = effective_transmission_rate * S * I / N if N > 0 else 0
            infection_rate = incubation_rate * E
            recovery_rate_actual = recovery_rate * I
            
            # Stochastic transitions using custom Poisson implementation
            new_exposures = min(S, SIRSimulator._poisson_sample(exposure_rate) if exposure_rate > 0 else 0)
            new_infections = min(E, SIRSimulator._poisson_sample(infection_rate) if infection_rate > 0 else 0)
            new_recoveries = min(I, SIRSimulator._poisson_sample(recovery_rate_actual) if recovery_rate_actual > 0 else 0)
            
            # Update state
            new_state = EpidemicState(
                day=day,
                susceptible=S - new_exposures,
                exposed=E + new_exposures - new_infections,
                infected=I + new_infections - new_recoveries,
                recovered=R + new_recoveries,
                new_infections=new_infections,
                cumulative_infections=current_state.cumulative_infections + new_infections
            )
            
            # Calculate effective reproduction number
            if S > 0 and N > 0:
                new_state.effective_reproduction_number = effective_transmission_rate * S / (N * recovery_rate)
            
            timeline.append(new_state)
            current_state = new_state
        
        # Calculate final metrics
        final_state = timeline[-1]
        total_infected = final_state.cumulative_infections
        attack_rate = total_infected / population
        
        # Find peak
        peak_infected = max(state.infected for state in timeline)
        peak_day = next(i for i, state in enumerate(timeline) if state.infected == peak_infected)
        
        # Calculate epidemic duration
        epidemic_duration = len([state for state in timeline if state.infected > 0 or (state.exposed or 0) > 0])
        
        return SimulationResult(
            run_id=0,
            simulation_type=SimulationType.EPIDEMIC_SPREAD,
            model_type=ModelType.SEIR,
            epidemic_timeline=timeline,
            intervention_scenarios=interventions,
            total_infected=total_infected,
            peak_infected=peak_infected,
            peak_day=peak_day,
            epidemic_duration_days=epidemic_duration,
            attack_rate=attack_rate,
            basic_reproduction_number=r0,
            effective_reproduction_number=timeline[-1].effective_reproduction_number or r0
        )

class OneHealthSimulator:
    """One Health multi-domain epidemic simulator."""
    
    @staticmethod
    def run_zoonotic_simulation(animal_population: int,
                               human_population: int,
                               animal_transmission_rate: float,
                               zoonotic_transmission_rate: float,
                               human_transmission_rate: float,
                               recovery_rates: Dict[str, float],
                               simulation_days: int,
                               initial_animal_infected: int = 1) -> SimulationResult:
        """Run zoonotic disease simulation across animal and human populations."""
        
        # Initialize state
        current_state = EpidemicState(
            day=0,
            susceptible=animal_population + human_population - initial_animal_infected,
            infected=initial_animal_infected,
            recovered=0,
            animal_susceptible=animal_population - initial_animal_infected,
            animal_infected=initial_animal_infected,
            human_susceptible=human_population,
            human_infected=0,
            cumulative_infections=initial_animal_infected
        )
        
        timeline = [current_state]
        zoonotic_transmissions = 0
        
        # Run simulation
        for day in range(1, simulation_days + 1):
            AS = current_state.animal_susceptible
            AI = current_state.animal_infected
            AR = current_state.recovered - current_state.human_infected  # Animal recovered
            
            HS = current_state.human_susceptible
            HI = current_state.human_infected
            HR = current_state.recovered - (current_state.recovered - current_state.human_infected)  # Human recovered
            
            # Animal-to-animal transmission
            animal_new_infections = 0
            if AS > 0 and AI > 0:
                animal_infection_rate = animal_transmission_rate * AS * AI / (AS + AI + AR)
                animal_new_infections = min(AS, SIRSimulator._poisson_sample(animal_infection_rate) if animal_infection_rate > 0 else 0)
            
            # Zoonotic transmission (animal to human)
            zoonotic_new_infections = 0
            if HS > 0 and AI > 0:
                zoonotic_infection_rate = zoonotic_transmission_rate * HS * AI / animal_population
                zoonotic_new_infections = min(HS, SIRSimulator._poisson_sample(zoonotic_infection_rate) if zoonotic_infection_rate > 0 else 0)
                zoonotic_transmissions += zoonotic_new_infections
            
            # Human-to-human transmission
            human_new_infections = 0
            if HS > 0 and HI > 0:
                human_infection_rate = human_transmission_rate * HS * HI / (HS + HI + HR)
                human_new_infections = min(HS - zoonotic_new_infections, SIRSimulator._poisson_sample(human_infection_rate) if human_infection_rate > 0 else 0)
            
            # Recoveries
            animal_recoveries = min(AI, SIRSimulator._poisson_sample(recovery_rates.get('animal', 0.1) * AI) if AI > 0 else 0)
            human_recoveries = min(HI, SIRSimulator._poisson_sample(recovery_rates.get('human', 0.1) * HI) if HI > 0 else 0)
            
            # Update state
            new_AS = AS - animal_new_infections
            new_AI = AI + animal_new_infections - animal_recoveries
            new_HS = HS - zoonotic_new_infections - human_new_infections
            new_HI = HI + zoonotic_new_infections + human_new_infections - human_recoveries
            new_recovered = current_state.recovered + animal_recoveries + human_recoveries
            
            total_new_infections = animal_new_infections + zoonotic_new_infections + human_new_infections
            
            new_state = EpidemicState(
                day=day,
                susceptible=new_AS + new_HS,
                infected=new_AI + new_HI,
                recovered=new_recovered,
                animal_susceptible=new_AS,
                animal_infected=new_AI,
                human_susceptible=new_HS,
                human_infected=new_HI,
                new_infections=total_new_infections,
                cumulative_infections=current_state.cumulative_infections + total_new_infections
            )
            
            timeline.append(new_state)
            current_state = new_state
            
            # Stop if no active infections
            if new_AI == 0 and new_HI == 0:
                break
        
        # Calculate final metrics
        final_state = timeline[-1]
        total_infected = final_state.cumulative_infections
        attack_rate = total_infected / (animal_population + human_population)
        
        # Calculate domain-specific attack rates
        animal_attack_rate = (animal_population - final_state.animal_susceptible) / animal_population
        human_attack_rate = (human_population - final_state.human_susceptible) / human_population if human_population > 0 else 0
        
        # Find peak
        peak_infected = max(state.infected for state in timeline)
        peak_day = next(i for i, state in enumerate(timeline) if state.infected == peak_infected)
        
        # Calculate epidemic duration
        epidemic_duration = len([state for state in timeline if state.infected > 0])
        
        return SimulationResult(
            run_id=0,
            simulation_type=SimulationType.EPIDEMIC_SPREAD,
            model_type=ModelType.METAPOPULATION,
            epidemic_timeline=timeline,
            intervention_scenarios=[],
            total_infected=total_infected,
            peak_infected=peak_infected,
            peak_day=peak_day,
            epidemic_duration_days=epidemic_duration,
            attack_rate=attack_rate,
            basic_reproduction_number=max(animal_transmission_rate, human_transmission_rate) / min(recovery_rates.values()),
            effective_reproduction_number=max(animal_transmission_rate, human_transmission_rate) / min(recovery_rates.values()),
            animal_attack_rate=animal_attack_rate,
            human_attack_rate=human_attack_rate,
            zoonotic_transmissions=zoonotic_transmissions
        )

class MonteCarloEngine:
    """Monte Carlo simulation engine for epidemic modeling."""
    
    def __init__(self, random_seed: Optional[int] = None):
        if random_seed is not None:
            random.seed(random_seed)
        
        self.simulation_results: List[MonteCarloResults] = []
        self.analysis_log: List[Dict] = []
        
        logger.info("Monte Carlo Engine initialized")
    
    def run_monte_carlo_simulation(self, 
                                 base_parameters: Dict[str, float],
                                 parameter_distributions: Dict[str, SimulationParameter],
                                 simulation_type: SimulationType = SimulationType.EPIDEMIC_SPREAD,
                                 model_type: ModelType = ModelType.SIR,
                                 num_runs: int = 1000,
                                 simulation_days: int = 365,
                                 interventions: List[InterventionScenario] = None) -> MonteCarloResults:
        """Run Monte Carlo simulation ensemble."""
        
        analysis_start = datetime.now()
        simulation_runs = []
        
        logger.info(f"Starting Monte Carlo simulation with {num_runs} runs")
        
        if interventions is None:
            interventions = []
        
        # Run simulations
        for run_id in range(num_runs):
            try:
                # Sample parameters
                sampled_params = {}
                for param_name, param_obj in parameter_distributions.items():
                    sampled_params[param_name] = param_obj.sample()
                
                # Merge with base parameters
                run_params = {**base_parameters, **sampled_params}
                
                # Run simulation based on model type
                if model_type == ModelType.SIR:
                    result = SIRSimulator.run_sir_simulation(
                        population=int(run_params.get('population', 100000)),
                        initial_infected=int(run_params.get('initial_infected', 10)),
                        transmission_rate=run_params.get('transmission_rate', 0.3),
                        recovery_rate=run_params.get('recovery_rate', 0.1),
                        simulation_days=simulation_days,
                        interventions=interventions
                    )
                elif model_type == ModelType.SEIR:
                    result = SEIRSimulator.run_seir_simulation(
                        population=int(run_params.get('population', 100000)),
                        initial_exposed=int(run_params.get('initial_exposed', 20)),
                        transmission_rate=run_params.get('transmission_rate', 0.3),
                        incubation_rate=run_params.get('incubation_rate', 0.2),
                        recovery_rate=run_params.get('recovery_rate', 0.1),
                        simulation_days=simulation_days,
                        interventions=interventions
                    )
                elif model_type == ModelType.METAPOPULATION:
                    result = OneHealthSimulator.run_zoonotic_simulation(
                        animal_population=int(run_params.get('animal_population', 50000)),
                        human_population=int(run_params.get('human_population', 50000)),
                        animal_transmission_rate=run_params.get('animal_transmission_rate', 0.4),
                        zoonotic_transmission_rate=run_params.get('zoonotic_transmission_rate', 0.01),
                        human_transmission_rate=run_params.get('human_transmission_rate', 0.2),
                        recovery_rates={'animal': run_params.get('animal_recovery_rate', 0.15),
                                      'human': run_params.get('human_recovery_rate', 0.1)},
                        simulation_days=simulation_days,
                        initial_animal_infected=int(run_params.get('initial_animal_infected', 5))
                    )
                else:
                    # Default to SIR
                    result = SIRSimulator.run_sir_simulation(
                        population=int(run_params.get('population', 100000)),
                        initial_infected=int(run_params.get('initial_infected', 10)),
                        transmission_rate=run_params.get('transmission_rate', 0.3),
                        recovery_rate=run_params.get('recovery_rate', 0.1),
                        simulation_days=simulation_days,
                        interventions=interventions
                    )
                
                result.run_id = run_id
                simulation_runs.append(result)
                
            except Exception as e:
                logger.warning(f"Simulation run {run_id} failed: {e}")
                continue
        
        if not simulation_runs:
            raise ValueError("No successful simulation runs")
        
        # Analyze results
        analysis_results = self._analyze_monte_carlo_results(
            simulation_runs, simulation_type, model_type, base_parameters, analysis_start
        )
        
        # Store results
        self.simulation_results.append(analysis_results)
        
        # Log performance
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        self.analysis_log.append({
            "analysis_timestamp": analysis_start.isoformat(),
            "analysis_duration": analysis_time,
            "total_runs": len(simulation_runs),
            "simulation_type": simulation_type.value,
            "model_type": model_type.value
        })
        
        logger.info(f"Monte Carlo simulation completed: {len(simulation_runs)} runs in {analysis_time:.2f}s")
        
        return analysis_results
    
    def _analyze_monte_carlo_results(self, 
                                   simulation_runs: List[SimulationResult],
                                   simulation_type: SimulationType,
                                   model_type: ModelType,
                                   base_parameters: Dict[str, float],
                                   analysis_start: datetime) -> MonteCarloResults:
        """Analyze Monte Carlo simulation results."""
        
        # Extract key metrics
        attack_rates = [result.attack_rate for result in simulation_runs]
        peak_infected = [result.peak_infected for result in simulation_runs]
        epidemic_durations = [result.epidemic_duration_days for result in simulation_runs]
        total_infected = [result.total_infected for result in simulation_runs]
        
        # Calculate statistics
        mean_attack_rate = statistics.mean(attack_rates)
        median_attack_rate = statistics.median(attack_rates)
        attack_rate_ci = self._calculate_confidence_interval(attack_rates)
        
        mean_peak_infected = statistics.mean(peak_infected)
        peak_infected_ci = self._calculate_confidence_interval(peak_infected)
        
        mean_epidemic_duration = statistics.mean(epidemic_durations)
        duration_ci = self._calculate_confidence_interval(epidemic_durations)
        
        # Risk assessment
        major_outbreak_threshold = 0.1  # 10% attack rate
        probability_major_outbreak = len([ar for ar in attack_rates if ar > major_outbreak_threshold]) / len(attack_rates)
        
        peak_threshold = max(peak_infected) * 0.8  # 80% of maximum observed peak
        probability_peak_exceeded = len([pi for pi in peak_infected if pi > peak_threshold]) / len(peak_infected)
        
        expected_total_cases = statistics.mean(total_infected)
        
        # Generate insights
        key_findings = []
        key_findings.append(f"Mean attack rate: {mean_attack_rate:.1%}")
        key_findings.append(f"Peak infections: {int(mean_peak_infected):,} (95% CI: {int(peak_infected_ci[0]):,}-{int(peak_infected_ci[1]):,})")
        key_findings.append(f"Mean epidemic duration: {mean_epidemic_duration:.0f} days")
        
        risk_scenarios = []
        if probability_major_outbreak > 0.1:
            risk_scenarios.append(f"{probability_major_outbreak:.1%} probability of major outbreak (>10% attack rate)")
        
        if probability_peak_exceeded > 0.2:
            risk_scenarios.append(f"{probability_peak_exceeded:.1%} probability of exceeding peak capacity")
        
        recommendations = []
        if probability_major_outbreak > 0.3:
            recommendations.append("High outbreak risk - consider preventive interventions")
        
        if mean_epidemic_duration > 200:
            recommendations.append("Long epidemic duration expected - prepare for sustained response")
        
        if statistics.stdev(attack_rates) > 0.2:
            recommendations.append("High outcome variability - robust contingency planning needed")
        
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        
        return MonteCarloResults(
            analysis_id=f"MONTE_CARLO_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            simulation_type=simulation_type,
            analysis_timestamp=analysis_start,
            total_runs=len(simulation_runs),
            model_type=model_type,
            simulation_days=max(result.epidemic_duration_days for result in simulation_runs),
            base_parameters=base_parameters,
            mean_attack_rate=mean_attack_rate,
            median_attack_rate=median_attack_rate,
            attack_rate_ci_95=attack_rate_ci,
            mean_peak_infected=mean_peak_infected,
            peak_infected_ci_95=peak_infected_ci,
            mean_epidemic_duration=mean_epidemic_duration,
            duration_ci_95=duration_ci,
            probability_major_outbreak=probability_major_outbreak,
            probability_peak_exceeded=probability_peak_exceeded,
            expected_total_cases=expected_total_cases,
            simulation_duration_seconds=analysis_duration,
            convergence_achieved=len(simulation_runs) >= 500,  # Simple convergence criterion
            key_findings=key_findings,
            risk_scenarios=risk_scenarios,
            recommendations=recommendations
        )
    
    def _calculate_confidence_interval(self, data: List[float], confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for data."""
        
        if len(data) < 2:
            return (0.0, 0.0)
        
        # Use percentile method
        alpha = 1 - confidence_level
        lower_percentile = alpha / 2 * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        lower_index = int(lower_percentile / 100 * n)
        upper_index = int(upper_percentile / 100 * n)
        
        lower_index = max(0, min(lower_index, n - 1))
        upper_index = max(0, min(upper_index, n - 1))
        
        return (sorted_data[lower_index], sorted_data[upper_index])
    
    def compare_intervention_scenarios(self, 
                                     base_parameters: Dict[str, float],
                                     parameter_distributions: Dict[str, SimulationParameter],
                                     intervention_scenarios: List[List[InterventionScenario]],
                                     scenario_names: List[str],
                                     num_runs: int = 500) -> Dict[str, MonteCarloResults]:
        """Compare multiple intervention scenarios."""
        
        results = {}
        
        for i, (interventions, name) in enumerate(zip(intervention_scenarios, scenario_names)):
            logger.info(f"Running scenario: {name}")
            
            result = self.run_monte_carlo_simulation(
                base_parameters=base_parameters,
                parameter_distributions=parameter_distributions,
                simulation_type=SimulationType.SCENARIO_COMPARISON,
                num_runs=num_runs,
                interventions=interventions
            )
            
            results[name] = result
        
        return results
    
    def get_simulation_summary(self) -> Dict:
        """Get summary of simulation results."""
        
        if not self.simulation_results:
            return {"message": "No simulations performed"}
        
        # Aggregate statistics
        total_simulations = len(self.simulation_results)
        total_runs = sum(result.total_runs for result in self.simulation_results)
        
        # Model types used
        model_types = [result.model_type.value for result in self.simulation_results]
        
        # Performance statistics
        simulation_times = [result.simulation_duration_seconds for result in self.simulation_results]
        
        return {
            "total_simulations": total_simulations,
            "total_runs": total_runs,
            "model_types": list(set(model_types)),
            "convergence_rate": len([r for r in self.simulation_results if r.convergence_achieved]) / total_simulations,
            "performance": {
                "average_simulation_time": statistics.mean(simulation_times) if simulation_times else 0,
                "total_simulation_time": sum(simulation_times)
            }
        }

# Mock parameter generator
def generate_mock_simulation_parameters():
    """Generate mock simulation parameters for testing."""
    
    # Base parameters
    base_parameters = {
        'population': 100000,
        'animal_population': 50000,
        'human_population': 50000,
        'initial_infected': 10,
        'initial_exposed': 20,
        'initial_animal_infected': 5
    }
    
    # Parameter distributions with uncertainty
    parameter_distributions = {
        'transmission_rate': SimulationParameter(
            name='transmission_rate',
            base_value=0.3,
            distribution='normal',
            variance=0.01,
            min_value=0.1,
            max_value=0.8
        ),
        'recovery_rate': SimulationParameter(
            name='recovery_rate',
            base_value=0.1,
            distribution='gamma',
            variance=0.005
        ),
        'animal_transmission_rate': SimulationParameter(
            name='animal_transmission_rate',
            base_value=0.4,
            distribution='uniform',
            min_value=0.2,
            max_value=0.6
        ),
        'zoonotic_transmission_rate': SimulationParameter(
            name='zoonotic_transmission_rate',
            base_value=0.01,
            distribution='gamma',
            variance=0.0005
        ),
        'human_transmission_rate': SimulationParameter(
            name='human_transmission_rate',
            base_value=0.25,
            distribution='normal',
            variance=0.01,
            min_value=0.1,
            max_value=0.5
        ),
        'incubation_rate': SimulationParameter(
            name='incubation_rate',
            base_value=0.2,
            distribution='gamma',
            variance=0.01
        )
    }
    
    return base_parameters, parameter_distributions

def generate_mock_intervention_scenarios():
    """Generate mock intervention scenarios for testing."""
    
    # No intervention baseline
    no_intervention = []
    
    # Light intervention
    light_intervention = [
        InterventionScenario(
            intervention_id="surveillance_enhancement",
            intervention_type=InterventionType.SURVEILLANCE_ENHANCEMENT,
            start_day=30,
            coverage=0.6,
            effectiveness=0.3,
            compliance=0.8
        )
    ]
    
    # Moderate intervention
    moderate_intervention = [
        InterventionScenario(
            intervention_id="surveillance_enhancement",
            intervention_type=InterventionType.SURVEILLANCE_ENHANCEMENT,
            start_day=20,
            coverage=0.8,
            effectiveness=0.4,
            compliance=0.9
        ),
        InterventionScenario(
            intervention_id="contact_tracing",
            intervention_type=InterventionType.CONTACT_TRACING,
            start_day=25,
            coverage=0.7,
            effectiveness=0.6,
            compliance=0.8
        )
    ]
    
    # Aggressive intervention
    aggressive_intervention = [
        InterventionScenario(
            intervention_id="quarantine",
            intervention_type=InterventionType.QUARANTINE,
            start_day=10,
            end_day=100,
            coverage=0.9,
            effectiveness=0.8,
            compliance=0.9
        ),
        InterventionScenario(
            intervention_id="movement_restriction",
            intervention_type=InterventionType.MOVEMENT_RESTRICTION,
            start_day=15,
            end_day=80,
            coverage=0.95,
            effectiveness=0.7,
            compliance=0.85
        )
    ]
    
    return {
        'no_intervention': no_intervention,
        'light_intervention': light_intervention,
        'moderate_intervention': moderate_intervention,
        'aggressive_intervention': aggressive_intervention
    }

def run_demonstration():
    """Run demonstration of Monte Carlo simulation system."""
    print("🎲 One Health Monte Carlo Simulation Engine - Demonstration")
    print("=" * 60)
    
    # Initialize engine
    engine = MonteCarloEngine(random_seed=42)  # For reproducible results
    
    # Generate mock parameters
    base_params, param_distributions = generate_mock_simulation_parameters()
    intervention_scenarios = generate_mock_intervention_scenarios()
    
    print(f"\n⚙️ Simulation Configuration:")
    print(f"  Base Population: {base_params['population']:,}")
    print(f"  Animal Population: {base_params['animal_population']:,}")
    print(f"  Human Population: {base_params['human_population']:,}")
    print(f"  Parameter Uncertainty: {len(param_distributions)} parameters")
    
    # Run Monte Carlo simulations for different models
    print(f"\n🎲 Running Monte Carlo Simulations...")
    
    # 1. SIR Model simulation
    print(f"\n1. SIR Model Simulation (1000 runs)")
    sir_result = engine.run_monte_carlo_simulation(
        base_parameters=base_params,
        parameter_distributions={k: v for k, v in param_distributions.items() 
                               if k in ['transmission_rate', 'recovery_rate']},
        simulation_type=SimulationType.EPIDEMIC_SPREAD,
        model_type=ModelType.SIR,
        num_runs=1000,
        simulation_days=200
    )
    
    # 2. One Health zoonotic simulation
    print(f"\n2. One Health Zoonotic Model Simulation (500 runs)")
    zoonotic_result = engine.run_monte_carlo_simulation(
        base_parameters=base_params,
        parameter_distributions={k: v for k, v in param_distributions.items() 
                               if 'animal' in k or 'human' in k or 'zoonotic' in k},
        simulation_type=SimulationType.EPIDEMIC_SPREAD,
        model_type=ModelType.METAPOPULATION,
        num_runs=500,
        simulation_days=300
    )
    
    # 3. Intervention comparison
    print(f"\n3. Intervention Scenario Comparison (250 runs each)")
    scenario_comparison = engine.compare_intervention_scenarios(
        base_parameters=base_params,
        parameter_distributions={k: v for k, v in param_distributions.items() 
                               if k in ['transmission_rate', 'recovery_rate']},
        intervention_scenarios=[
            intervention_scenarios['no_intervention'],
            intervention_scenarios['moderate_intervention'],
            intervention_scenarios['aggressive_intervention']
        ],
        scenario_names=['Baseline', 'Moderate Intervention', 'Aggressive Intervention'],
        num_runs=250
    )
    
    # Display results
    print(f"\n📊 Monte Carlo Simulation Results:")
    
    # SIR results
    print(f"\n1. SIR Model Results:")
    print(f"   Total Runs: {sir_result.total_runs}")
    print(f"   Mean Attack Rate: {sir_result.mean_attack_rate:.1%}")
    print(f"   Attack Rate 95% CI: [{sir_result.attack_rate_ci_95[0]:.1%}, {sir_result.attack_rate_ci_95[1]:.1%}]")
    print(f"   Mean Peak Infected: {int(sir_result.mean_peak_infected):,}")
    print(f"   Peak 95% CI: [{int(sir_result.peak_infected_ci_95[0]):,}, {int(sir_result.peak_infected_ci_95[1]):,}]")
    print(f"   Mean Duration: {sir_result.mean_epidemic_duration:.0f} days")
    print(f"   Probability Major Outbreak: {sir_result.probability_major_outbreak:.1%}")
    print(f"   Expected Total Cases: {int(sir_result.expected_total_cases):,}")
    print(f"   Convergence: {'Yes' if sir_result.convergence_achieved else 'No'}")
    
    if sir_result.key_findings:
        print(f"   Key Findings ({len(sir_result.key_findings)}):")
        for finding in sir_result.key_findings:
            print(f"     • {finding}")
    
    # Zoonotic results
    print(f"\n2. One Health Zoonotic Results:")
    print(f"   Total Runs: {zoonotic_result.total_runs}")
    print(f"   Mean Attack Rate: {zoonotic_result.mean_attack_rate:.1%}")
    print(f"   Mean Peak Infected: {int(zoonotic_result.mean_peak_infected):,}")
    print(f"   Mean Duration: {zoonotic_result.mean_epidemic_duration:.0f} days")
    print(f"   Probability Major Outbreak: {zoonotic_result.probability_major_outbreak:.1%}")
    print(f"   Expected Total Cases: {int(zoonotic_result.expected_total_cases):,}")
    
    # Intervention comparison
    print(f"\n3. Intervention Comparison Results:")
    for scenario_name, result in scenario_comparison.items():
        print(f"   {scenario_name}:")
        print(f"     Attack Rate: {result.mean_attack_rate:.1%}")
        print(f"     Peak Infected: {int(result.mean_peak_infected):,}")
        print(f"     Duration: {result.mean_epidemic_duration:.0f} days")
        print(f"     Major Outbreak Risk: {result.probability_major_outbreak:.1%}")
    
    # Calculate intervention effectiveness
    baseline_cases = scenario_comparison['Baseline'].expected_total_cases
    for scenario_name, result in scenario_comparison.items():
        if scenario_name != 'Baseline':
            cases_averted = baseline_cases - result.expected_total_cases
            effectiveness = (cases_averted / baseline_cases) * 100
            print(f"   {scenario_name} Effectiveness: {effectiveness:.1f}% cases averted ({int(cases_averted):,} cases)")
    
    # Simulation summary
    summary = engine.get_simulation_summary()
    print(f"\n📊 Simulation Summary:")
    print(f"  Total Simulations: {summary['total_simulations']}")
    print(f"  Total Runs: {summary['total_runs']:,}")
    print(f"  Model Types: {', '.join(summary['model_types'])}")
    print(f"  Convergence Rate: {summary['convergence_rate']:.1%}")
    
    print(f"\n⚡ Performance:")
    perf = summary['performance']
    print(f"  Average Simulation Time: {perf['average_simulation_time']:.2f}s")
    print(f"  Total Simulation Time: {perf['total_simulation_time']:.2f}s")
    
    # Risk assessment across all simulations
    all_results = [sir_result, zoonotic_result] + list(scenario_comparison.values())
    high_risk_simulations = [r for r in all_results if r.probability_major_outbreak > 0.3]
    
    if high_risk_simulations:
        print(f"\n🚨 HIGH RISK Simulations ({len(high_risk_simulations)}):")
        for result in high_risk_simulations[:3]:  # Top 3
            print(f"  • {result.analysis_id}")
            print(f"    Major Outbreak Probability: {result.probability_major_outbreak:.1%}")
            print(f"    Expected Cases: {int(result.expected_total_cases):,}")
    
    return engine

if __name__ == "__main__":
    engine = run_demonstration()
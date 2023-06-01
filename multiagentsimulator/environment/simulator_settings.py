from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationSettings:
    infection_spread_rate_mean: float = 0.21

    infection_spread_rate_sigma: float = 0.1

    random_testing_rate: float = 0.02

    symp_testing_rate: float = 0.3

    critical_testing_rate: float = 1.

    testing_false_positive_rate: float = 0.001  # false positives are much more rare than negatives

    testing_false_negative_rate: float = 0.01

    retest_rate: float = 0.033

    sim_steps_per_regulation: int = 24

    use_contact_tracer: bool = True

    contact_tracer_history_size: int = 5

    infection_threshold: int = 50

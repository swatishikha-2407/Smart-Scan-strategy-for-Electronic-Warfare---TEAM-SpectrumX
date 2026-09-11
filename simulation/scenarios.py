"""
Predefined simulation scenarios.

These functions create RFEnvironment objects with different
simulated emitter behaviors.

All scenarios are software simulations only.
"""

from typing import Callable, Dict

from .config import (
    NUM_BANDS,
    SIMULATION_TIME_STEPS,
    DEFAULT_SEED,
    PERIODIC,
    RANDOM,
    FREQUENCY_CHANGING,
    INTERMITTENT,
)

from .emitter import Emitter
from .environment import RFEnvironment


def create_periodic_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a scenario containing periodic emitters.

    Periodic emitters become active according to fixed
    time patterns.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    emitter_1 = Emitter(
        emitter_id=1,
        band=2,
        behavior=PERIODIC,
        period=6,
        duration=2,
    )

    emitter_2 = Emitter(
        emitter_id=2,
        band=8,
        behavior=PERIODIC,
        period=10,
        duration=3,
    )

    environment.add_emitter(emitter_1)
    environment.add_emitter(emitter_2)

    return environment


def create_random_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a scenario containing randomly active emitters.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    emitter_1 = Emitter(
        emitter_id=1,
        band=4,
        behavior=RANDOM,
        activity_probability=0.4,
    )

    emitter_2 = Emitter(
        emitter_id=2,
        band=12,
        behavior=RANDOM,
        activity_probability=0.6,
    )

    environment.add_emitter(emitter_1)
    environment.add_emitter(emitter_2)

    return environment


def create_frequency_changing_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a scenario where simulated emitters change bands.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    emitter_1 = Emitter(
        emitter_id=1,
        band=3,
        behavior=FREQUENCY_CHANGING,
        frequency_change_probability=0.25,
    )

    emitter_2 = Emitter(
        emitter_id=2,
        band=15,
        behavior=FREQUENCY_CHANGING,
        frequency_change_probability=0.15,
    )

    environment.add_emitter(emitter_1)
    environment.add_emitter(emitter_2)

    return environment


def create_intermittent_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a scenario with intermittent activity.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    emitter_1 = Emitter(
        emitter_id=1,
        band=5,
        behavior=INTERMITTENT,
        intermittent_probability=0.35,
    )

    emitter_2 = Emitter(
        emitter_id=2,
        band=14,
        behavior=INTERMITTENT,
        intermittent_probability=0.55,
    )

    environment.add_emitter(emitter_1)
    environment.add_emitter(emitter_2)

    return environment


def create_mixed_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a mixed scenario containing multiple emitter types.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    periodic_emitter = Emitter(
        emitter_id=1,
        band=2,
        behavior=PERIODIC,
        period=8,
        duration=2,
    )

    random_emitter = Emitter(
        emitter_id=2,
        band=7,
        behavior=RANDOM,
        activity_probability=0.45,
    )

    changing_emitter = Emitter(
        emitter_id=3,
        band=13,
        behavior=FREQUENCY_CHANGING,
        frequency_change_probability=0.2,
    )

    intermittent_emitter = Emitter(
        emitter_id=4,
        band=17,
        behavior=INTERMITTENT,
        intermittent_probability=0.4,
    )

    environment.add_emitter(periodic_emitter)
    environment.add_emitter(random_emitter)
    environment.add_emitter(changing_emitter)
    environment.add_emitter(intermittent_emitter)

    return environment


def create_unknown_activity_scenario(
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a less predictable scenario.

    The scheduler does not receive prior information about
    which bands are likely to be active. Activity is generated
    using several changing/intermittent simulated emitters.
    """

    environment = RFEnvironment(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )

    emitter_1 = Emitter(
        emitter_id=1,
        band=1,
        behavior=INTERMITTENT,
        intermittent_probability=0.3,
    )

    emitter_2 = Emitter(
        emitter_id=2,
        band=9,
        behavior=FREQUENCY_CHANGING,
        frequency_change_probability=0.3,
    )

    emitter_3 = Emitter(
        emitter_id=3,
        band=16,
        behavior=RANDOM,
        activity_probability=0.35,
    )

    environment.add_emitter(emitter_1)
    environment.add_emitter(emitter_2)
    environment.add_emitter(emitter_3)

    return environment


# ============================================================
# SCENARIO REGISTRY
# ============================================================

SCENARIOS: Dict[str, Callable[..., RFEnvironment]] = {
    "periodic": create_periodic_scenario,
    "random": create_random_scenario,
    "frequency_changing": create_frequency_changing_scenario,
    "intermittent": create_intermittent_scenario,
    "mixed": create_mixed_scenario,
    "unknown_activity": create_unknown_activity_scenario,
}


def create_scenario(
    scenario_name: str,
    num_bands: int = NUM_BANDS,
    simulation_time_steps: int = SIMULATION_TIME_STEPS,
    seed: int = DEFAULT_SEED,
) -> RFEnvironment:
    """
    Create a scenario by name.

    Example
    -------
    environment = create_scenario("periodic")
    """

    if scenario_name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())

        raise ValueError(
            f"Unknown scenario '{scenario_name}'. "
            f"Available scenarios: {available}"
        )

    scenario_function = SCENARIOS[scenario_name]

    return scenario_function(
        num_bands=num_bands,
        simulation_time_steps=simulation_time_steps,
        seed=seed,
    )


def get_available_scenarios():
    """Return the names of all available scenarios."""

    return list(SCENARIOS.keys())

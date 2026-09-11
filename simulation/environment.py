"""
Simulated RF environment for the Smart Scan Strategy project.

This module maintains:
- Simulated frequency bands
- Simulated emitters
- Current simulation time
- Ground-truth activity

This environment does NOT interact with real RF hardware.
It is purely a software simulation for testing adaptive
scan scheduling algorithms.
"""

from typing import Dict, List, Optional
import random

from .config import (
    NUM_BANDS,
    SIMULATION_TIME_STEPS,
    DEFAULT_SEED,
)

from .emitter import Emitter


class RFEnvironment:
    """
    Simulated RF environment.

    The environment contains a fixed number of frequency bands.
    Simulated emitters create activity inside those bands.

    Other modules can ask:

        environment.get_band_state(band)

    or:

        environment.get_state()
    """

    def __init__(
        self,
        num_bands: int = NUM_BANDS,
        simulation_time_steps: int = SIMULATION_TIME_STEPS,
        seed: int = DEFAULT_SEED,
        emitters: Optional[List[Emitter]] = None,
    ):
        """
        Initialize the simulated environment.

        Parameters
        ----------
        num_bands:
            Number of simulated frequency bands.

        simulation_time_steps:
            Maximum number of simulation steps.

        seed:
            Random seed for reproducibility.

        emitters:
            Optional list of simulated emitters.
        """

        if num_bands <= 0:
            raise ValueError(
                "num_bands must be greater than zero."
            )

        if simulation_time_steps <= 0:
            raise ValueError(
                "simulation_time_steps must be greater than zero."
            )

        self.num_bands = num_bands
        self.simulation_time_steps = simulation_time_steps
        self.seed = seed

        # Main random generator for the environment.
        self.rng = random.Random(seed)

        # Current simulation time.
        self.current_time = 0

        # Store emitters by ID.
        self.emitters: Dict[int, Emitter] = {}

        # Ground truth:
        #
        # {
        #     band_id: True/False
        # }
        #
        # True means simulated activity exists in that band.
        self.band_states: Dict[int, bool] = {
            band: False
            for band in range(self.num_bands)
        }

        # Store ground truth history.
        self.ground_truth_history: List[dict] = []

        # Add initial emitters if provided.
        if emitters is not None:
            for emitter in emitters:
                self.add_emitter(emitter)

        # Initialize environment state.
        self._update_band_states()

    # ============================================================
    # RESET
    # ============================================================

    def reset(self):
        """
        Reset the simulation to its initial state.

        Returns
        -------
        dict
            Current environment state after reset.
        """

        self.current_time = 0

        self.rng = random.Random(self.seed)

        self.ground_truth_history.clear()

        # Reset emitter random generators.
        for emitter_id, emitter in self.emitters.items():

            emitter.rng = random.Random(
                self.seed + emitter_id + 1
            )

            emitter.active = False
            emitter.previous_band = emitter.band

        self.band_states = {
            band: False
            for band in range(self.num_bands)
        }

        self._update_band_states()

        return self.get_state()

    # ============================================================
    # STEP
    # ============================================================

    def step(self) -> dict:
        """
        Advance the environment by one simulation time step.

        Returns
        -------
        dict
            Current environment state.
        """

        # Prevent simulation from advancing beyond configured
        # duration.
        if self.current_time >= self.simulation_time_steps:
            return self.get_state()

        # Update all emitters.
        for emitter in self.emitters.values():
            emitter.update(
                current_time=self.current_time,
                num_bands=self.num_bands,
            )

        # Recalculate which bands contain simulated activity.
        self._update_band_states()

        # Save ground truth.
        self._record_ground_truth()

        # Move to next time step.
        self.current_time += 1

        return self.get_state()

    # ============================================================
    # INTERNAL STATE UPDATE
    # ============================================================

    def _update_band_states(self):
        """
        Recalculate activity for every band.

        A band is active if at least one emitter currently
        occupies that band and is active.
        """

        self.band_states = {
            band: False
            for band in range(self.num_bands)
        }

        for emitter in self.emitters.values():

            if emitter.active:

                band = emitter.get_band()

                if 0 <= band < self.num_bands:
                    self.band_states[band] = True

    # ============================================================
    # RECORD GROUND TRUTH
    # ============================================================

    def _record_ground_truth(self):
        """Store the current ground-truth state."""

        self.ground_truth_history.append(
            {
                "time": self.current_time,
                "band_states": self.band_states.copy(),
            }
        )

    # ============================================================
    # GET BAND STATE
    # ============================================================

    def get_band_state(self, band: int) -> dict:
        """
        Return the state of one simulated frequency band.

        IMPORTANT:
        This is one of the main interfaces shared with Member 2.

        Member 2 can call:

            environment.get_band_state(band)

        Parameters
        ----------
        band:
            Band ID.

        Returns
        -------
        dict
            Information about the selected band.
        """

        self._validate_band(band)

        active = self.band_states[band]

        active_emitters = []

        for emitter in self.emitters.values():

            if (
                emitter.active
                and emitter.get_band() == band
            ):
                active_emitters.append(
                    emitter.emitter_id
                )

        return {
            "band": band,
            "active": active,
            "time": self.current_time,
            "active_emitters": active_emitters,
        }

    # ============================================================
    # GET FULL STATE
    # ============================================================

    def get_state(self) -> dict:
        """
        Return the complete current environment state.

        IMPORTANT:
        This is another main interface shared with other
        team members.
        """

        return {
            "current_time": self.current_time,
            "num_bands": self.num_bands,
            "simulation_time_steps": (
                self.simulation_time_steps
            ),
            "band_states": self.band_states.copy(),
            "active_bands": self.get_active_bands(),
            "emitters": [
                emitter.get_state()
                for emitter in self.emitters.values()
            ],
        }

    # ============================================================
    # GET ACTIVE BANDS
    # ============================================================

    def get_active_bands(self) -> List[int]:
        """
        Return a list of currently active bands.
        """

        return [
            band
            for band, active in self.band_states.items()
            if active
        ]

    # ============================================================
    # GET GROUND TRUTH
    # ============================================================

    def get_ground_truth(self) -> dict:
        """
        Return the current ground-truth state.

        This is useful for evaluation and metrics.

        The receiver/scheduler should NOT directly use this
        to make decisions because it represents hidden truth.
        """

        return {
            "time": self.current_time,
            "band_states": self.band_states.copy(),
            "active_bands": self.get_active_bands(),
        }

    # ============================================================
    # GET CURRENT TIME
    # ============================================================

    def get_current_time(self) -> int:
        """Return the current simulation time."""

        return self.current_time

    # ============================================================
    # ADD EMITTER
    # ============================================================

    def add_emitter(self, emitter: Emitter):
        """
        Add a simulated emitter to the environment.
        """

        if emitter.emitter_id in self.emitters:
            raise ValueError(
                f"Emitter ID {emitter.emitter_id} already exists."
            )

        if emitter.band >= self.num_bands:
            raise ValueError(
                f"Emitter band {emitter.band} is outside "
                f"the available range 0-{self.num_bands - 1}."
            )

        # Give every emitter a deterministic random generator.
        emitter.rng = random.Random(
            self.seed + emitter.emitter_id + 1
        )

        self.emitters[emitter.emitter_id] = emitter

        self._update_band_states()

    # ============================================================
    # REMOVE EMITTER
    # ============================================================

    def remove_emitter(self, emitter_id: int):
        """
        Remove an emitter from the environment.
        """

        if emitter_id not in self.emitters:
            raise KeyError(
                f"Emitter ID {emitter_id} does not exist."
            )

        del self.emitters[emitter_id]

        self._update_band_states()

    # ============================================================
    # BAND VALIDATION
    # ============================================================

    def _validate_band(self, band: int):
        """Validate a band ID."""

        if not isinstance(band, int):
            raise TypeError(
                "Band ID must be an integer."
            )

        if band < 0 or band >= self.num_bands:
            raise ValueError(
                f"Invalid band {band}. "
                f"Valid range is 0-{self.num_bands - 1}."
            )

    # ============================================================
    # UTILITY METHODS
    # ============================================================

    def get_num_bands(self) -> int:
        """Return number of simulated bands."""

        return self.num_bands

    def get_emitters(self) -> List[Emitter]:
        """Return all simulated emitters."""

        return list(self.emitters.values())

    def get_ground_truth_history(self) -> List[dict]:
        """Return historical ground-truth states."""

        return list(self.ground_truth_history)

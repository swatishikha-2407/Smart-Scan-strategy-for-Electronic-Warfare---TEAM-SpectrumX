"""
Simulated emitter models for the Smart Scan Strategy project.

An emitter represents a simulated source of activity inside
the virtual RF environment.

Supported behaviors:
- Periodic
- Random
- Frequency-changing
- Intermittent
"""

from dataclasses import dataclass
from typing import Optional
import random

from .config import (
    PERIODIC,
    RANDOM,
    FREQUENCY_CHANGING,
    INTERMITTENT,
    DEFAULT_ACTIVITY_PROBABILITY,
    DEFAULT_FREQUENCY_CHANGE_PROBABILITY,
    DEFAULT_INTERMITTENT_PROBABILITY,
    DEFAULT_PERIOD,
    DEFAULT_DURATION,
)


@dataclass
class Emitter:
    """
    Represents one simulated emitter.

    Parameters
    ----------
    emitter_id:
        Unique identifier for the emitter.

    band:
        Current frequency-band ID.

    behavior:
        Behavior type of the emitter.

    period:
        Number of time steps between periodic transmissions.

    duration:
        Number of time steps for which a periodic emitter
        remains active.

    activity_probability:
        Probability of activity for random behavior.

    frequency_change_probability:
        Probability of changing band for frequency-changing behavior.

    intermittent_probability:
        Probability of being active for intermittent behavior.

    rng:
        Random number generator.
    """

    emitter_id: int
    band: int
    behavior: str

    period: int = DEFAULT_PERIOD
    duration: int = DEFAULT_DURATION

    activity_probability: float = DEFAULT_ACTIVITY_PROBABILITY
    frequency_change_probability: float = (
        DEFAULT_FREQUENCY_CHANGE_PROBABILITY
    )
    intermittent_probability: float = (
        DEFAULT_INTERMITTENT_PROBABILITY
    )

    rng: Optional[random.Random] = None

    # Internal state
    active: bool = False
    previous_band: Optional[int] = None

    def __post_init__(self):
        """Validate emitter configuration."""

        if self.rng is None:
            self.rng = random.Random()

        if self.band < 0:
            raise ValueError("Emitter band cannot be negative.")

        if self.period <= 0:
            raise ValueError("Period must be greater than zero.")

        if self.duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        self._validate_probability(
            self.activity_probability,
            "activity_probability",
        )

        self._validate_probability(
            self.frequency_change_probability,
            "frequency_change_probability",
        )

        self._validate_probability(
            self.intermittent_probability,
            "intermittent_probability",
        )

        if self.previous_band is None:
            self.previous_band = self.band

    @staticmethod
    def _validate_probability(value: float, name: str):
        """Ensure a probability is between 0 and 1."""

        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{name} must be between 0.0 and 1.0."
            )

    def update(self, current_time: int, num_bands: int):
        """
        Update the emitter state for the current simulation time.

        Parameters
        ----------
        current_time:
            Current simulation time step.

        num_bands:
            Total number of available bands.

        Returns
        -------
        bool
            True if the emitter is active during this time step.
        """

        if num_bands <= 0:
            raise ValueError("num_bands must be greater than zero.")

        if self.band >= num_bands:
            raise ValueError(
                f"Emitter {self.emitter_id} uses invalid band "
                f"{self.band} for {num_bands} bands."
            )

        # --------------------------------------------------------
        # PERIODIC BEHAVIOR
        # --------------------------------------------------------

        if self.behavior == PERIODIC:
            cycle_position = current_time % self.period

            self.active = cycle_position < self.duration

        # --------------------------------------------------------
        # RANDOM BEHAVIOR
        # --------------------------------------------------------

        elif self.behavior == RANDOM:
            self.active = (
                self.rng.random()
                < self.activity_probability
            )

        # --------------------------------------------------------
        # FREQUENCY-CHANGING BEHAVIOR
        # --------------------------------------------------------

        elif self.behavior == FREQUENCY_CHANGING:

            # The emitter may change its band.
            if (
                self.rng.random()
                < self.frequency_change_probability
            ):
                self.previous_band = self.band

                self.band = self.rng.randrange(num_bands)

            # Frequency-changing emitters are active during
            # each simulation step in this simplified model.
            self.active = True

        # --------------------------------------------------------
        # INTERMITTENT BEHAVIOR
        # --------------------------------------------------------

        elif self.behavior == INTERMITTENT:
            self.active = (
                self.rng.random()
                < self.intermittent_probability
            )

        else:
            raise ValueError(
                f"Unsupported emitter behavior: {self.behavior}"
            )

        return self.active

    def get_state(self) -> dict:
        """
        Return the current state of the emitter.

        Returns
        -------
        dict
            Serializable emitter state.
        """

        return {
            "emitter_id": self.emitter_id,
            "band": self.band,
            "behavior": self.behavior,
            "active": self.active,
            "previous_band": self.previous_band,
        }

    def is_active(self) -> bool:
        """Return whether the emitter is currently active."""

        return self.active

    def get_band(self) -> int:
        """Return the current band used by the emitter."""

        return self.band

    def set_band(self, band: int):
        """
        Manually change the emitter's simulated band.

        This is useful when creating scenarios.
        """

        if band < 0:
            raise ValueError("Band cannot be negative.")

        self.previous_band = self.band
        self.band = band

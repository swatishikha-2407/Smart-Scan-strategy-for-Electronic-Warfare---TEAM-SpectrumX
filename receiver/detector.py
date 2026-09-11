"""
Simulated detector for the virtual receiver.

This detector uses configurable mathematical probabilities
to simulate detection uncertainty.

It does NOT perform real signal processing.
"""

import random

from .noise_model import NoiseModel


class Detector:
    """
    Software-only simulated detector.

    Parameters
    ----------
    detection_probability : float
        Probability of detecting an active simulated band.

    false_alarm_probability : float
        Probability of reporting activity when the simulated
        band is inactive.

    noise_model : NoiseModel, optional
        Optional mathematical uncertainty model.

    seed : int, optional
        Random seed for reproducible simulations.
    """

    def __init__(
        self,
        detection_probability=0.90,
        false_alarm_probability=0.05,
        noise_model=None,
        seed=None,
    ):
        self._validate_probability(
            detection_probability,
            "detection_probability",
        )

        self._validate_probability(
            false_alarm_probability,
            "false_alarm_probability",
        )

        self.detection_probability = float(detection_probability)
        self.false_alarm_probability = float(false_alarm_probability)

        if noise_model is not None and not isinstance(
            noise_model,
            NoiseModel,
        ):
            raise TypeError(
                "noise_model must be a NoiseModel instance or None"
            )

        self.noise_model = noise_model

        self.random = random.Random(seed)

    @staticmethod
    def _validate_probability(value, name):
        """
        Validate that a probability is between 0 and 1.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")

        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{name} must be between 0.0 and 1.0"
            )

    def detect(self, actual_active):
        """
        Perform one simulated detection.

        Parameters
        ----------
        actual_active : bool
            Ground-truth state supplied by the simulation.

        Returns
        -------
        dict
            Detection result.

        Possible result values:

        HIT
            Activity was actually active and detected.

        MISS
            Activity was actually active but not detected.

        FALSE_ALARM
            Activity was inactive but detected.

        NO_SIGNAL
            Activity was inactive and not detected.
        """

        actual_active = bool(actual_active)

        if actual_active:
            probability = self.detection_probability

            if self.noise_model is not None:
                probability = (
                    self.noise_model.apply_detection_probability(
                        probability
                    )
                )

            detected = self.random.random() < probability

            if detected:
                result = "HIT"
            else:
                result = "MISS"

        else:
            probability = self.false_alarm_probability

            if self.noise_model is not None:
                probability = (
                    self.noise_model.apply_detection_probability(
                        probability
                    )
                )

            detected = self.random.random() < probability

            if detected:
                result = "FALSE_ALARM"
            else:
                result = "NO_SIGNAL"

        return {
            "detected": detected,
            "result": result,
        }

    def reset_seed(self, seed):
        """
        Reset the random generator with a new seed.

        This is useful for reproducible experiments.
        """

        self.random.seed(seed)

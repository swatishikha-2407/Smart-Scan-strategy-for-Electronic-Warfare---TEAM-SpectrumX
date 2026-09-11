"""
Simple mathematical uncertainty model for the virtual receiver.

This module does NOT model real RF noise or physical hardware.
It only provides a configurable mathematical adjustment to
detection probability.
"""


class NoiseModel:
    """
    Simple uncertainty model.

    The model applies a small configurable adjustment to a
    probability value.

    Parameters
    ----------
    adjustment : float
        Value added to the base probability.

        Example:
        adjustment = -0.05
        0.90 becomes 0.85

    The final probability is always limited to [0.0, 1.0].
    """

    def __init__(self, adjustment=0.0):
        if not isinstance(adjustment, (int, float)):
            raise TypeError("adjustment must be a number")

        self.adjustment = float(adjustment)

    def apply_detection_probability(self, base_probability):
        """
        Apply the uncertainty adjustment to a probability.

        Parameters
        ----------
        base_probability : float
            Probability between 0.0 and 1.0.

        Returns
        -------
        float
            Adjusted probability between 0.0 and 1.0.
        """

        if not isinstance(base_probability, (int, float)):
            raise TypeError("base_probability must be a number")

        if not 0.0 <= base_probability <= 1.0:
            raise ValueError(
                "base_probability must be between 0.0 and 1.0"
            )

        adjusted_probability = (
            float(base_probability) + self.adjustment
        )

        return max(0.0, min(1.0, adjusted_probability))

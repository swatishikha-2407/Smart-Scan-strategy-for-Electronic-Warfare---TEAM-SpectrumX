"""
Virtual receiver for the Smart Scan Strategy simulation.

The receiver:

1. Receives a band selected by the caller.
2. Gets the simulated ground-truth state from Member 1's environment.
3. Sends the state to the simulated detector.
4. Records the observation.
5. Returns a JSON-compatible dictionary.

The receiver does NOT decide which band to scan.
"""

from .detector import Detector


class VirtualReceiver:
    """
    Software-only virtual receiver.

    Parameters
    ----------
    environment
        Instance of the simulation environment.

    detector : Detector
        Simulated detector used to generate observations.
    """

    def __init__(self, environment, detector):
        if environment is None:
            raise ValueError("environment cannot be None")

        if not isinstance(detector, Detector):
            raise TypeError(
                "detector must be a Detector instance"
            )

        self.environment = environment
        self.detector = detector

        self.history = []

        self.total_scans = 0
        self.total_hits = 0
        self.total_misses = 0
        self.total_false_alarms = 0
        self.total_no_signal = 0

    def scan(self, band):
        """
        Scan one simulated band.

        The caller decides which band to scan.

        Example
        -------
        result = receiver.scan(7)

        Returns
        -------
        dict
            JSON-compatible observation dictionary.
        """

        # Get the ground-truth state from Member 1's environment.
        state = self.environment.get_band_state(band)

        actual_active = bool(state["active"])
        current_time = state["time"]

        # Ask the detector to simulate the observation.
        detection = self.detector.detect(actual_active)

        detected = bool(detection["detected"])
        result = detection["result"]

        observation = {
            "time": current_time,
            "band": band,
            "actual_active": actual_active,
            "detected": detected,
            "result": result,
        }

        # Save observation.
        self.history.append(observation)

        # Update statistics.
        self.total_scans += 1

        if result == "HIT":
            self.total_hits += 1

        elif result == "MISS":
            self.total_misses += 1

        elif result == "FALSE_ALARM":
            self.total_false_alarms += 1

        elif result == "NO_SIGNAL":
            self.total_no_signal += 1

        return observation

    def get_history(self):
        """
        Return all recorded scan observations.

        Returns a copy so external code cannot directly
        modify the receiver's internal history.
        """

        return list(self.history)

    def clear_history(self):
        """
        Clear scan history and reset statistics.
        """

        self.history.clear()

        self.total_scans = 0
        self.total_hits = 0
        self.total_misses = 0
        self.total_false_alarms = 0
        self.total_no_signal = 0

    def get_statistics(self):
        """
        Return receiver statistics.

        Returns
        -------
        dict
            JSON-compatible statistics dictionary.
        """

        return {
            "total_scans": self.total_scans,
            "hits": self.total_hits,
            "misses": self.total_misses,
            "false_alarms": self.total_false_alarms,
            "no_signal": self.total_no_signal,
        }

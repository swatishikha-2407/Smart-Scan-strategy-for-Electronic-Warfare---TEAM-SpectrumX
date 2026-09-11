"""
Unit tests for the virtual receiver and simulated detector.
"""

import unittest

from simulation.scenarios import create_scenario
from receiver.receiver import VirtualReceiver
from receiver.detector import Detector
from receiver.noise_model import NoiseModel


class TestNoiseModel(unittest.TestCase):
    """
    Tests for NoiseModel.
    """

    def test_probability_without_adjustment(self):
        noise = NoiseModel(adjustment=0.0)

        result = noise.apply_detection_probability(0.90)

        self.assertEqual(result, 0.90)

    def test_probability_with_adjustment(self):
        noise = NoiseModel(adjustment=-0.05)

        result = noise.apply_detection_probability(0.90)

        self.assertEqual(result, 0.85)

    def test_probability_does_not_go_below_zero(self):
        noise = NoiseModel(adjustment=-0.50)

        result = noise.apply_detection_probability(0.20)

        self.assertEqual(result, 0.0)

    def test_probability_does_not_go_above_one(self):
        noise = NoiseModel(adjustment=0.50)

        result = noise.apply_detection_probability(0.80)

        self.assertEqual(result, 1.0)


class TestDetector(unittest.TestCase):
    """
    Tests for the simulated detector.
    """

    def test_active_signal_with_certain_detection(self):
        detector = Detector(
            detection_probability=1.0,
            false_alarm_probability=0.0,
            seed=42,
        )

        result = detector.detect(True)

        self.assertTrue(result["detected"])
        self.assertEqual(result["result"], "HIT")

    def test_active_signal_with_zero_detection(self):
        detector = Detector(
            detection_probability=0.0,
            false_alarm_probability=0.0,
            seed=42,
        )

        result = detector.detect(True)

        self.assertFalse(result["detected"])
        self.assertEqual(result["result"], "MISS")

    def test_inactive_signal_without_false_alarm(self):
        detector = Detector(
            detection_probability=1.0,
            false_alarm_probability=0.0,
            seed=42,
        )

        result = detector.detect(False)

        self.assertFalse(result["detected"])
        self.assertEqual(result["result"], "NO_SIGNAL")

    def test_inactive_signal_with_certain_false_alarm(self):
        detector = Detector(
            detection_probability=1.0,
            false_alarm_probability=1.0,
            seed=42,
        )

        result = detector.detect(False)

        self.assertTrue(result["detected"])
        self.assertEqual(result["result"], "FALSE_ALARM")


class TestVirtualReceiver(unittest.TestCase):
    """
    Tests for VirtualReceiver using Member 1's simulation.
    """

    def setUp(self):
        self.environment = create_scenario("mixed")

        self.detector = Detector(
            detection_probability=1.0,
            false_alarm_probability=0.0,
            seed=42,
        )

        self.receiver = VirtualReceiver(
            environment=self.environment,
            detector=self.detector,
        )

        # Move simulation forward so the environment has
        # current activity information.
        self.environment.step()

    def test_scan_returns_dictionary(self):
        result = self.receiver.scan(2)

        self.assertIsInstance(result, dict)

    def test_scan_contains_required_fields(self):
        result = self.receiver.scan(2)

        required_fields = {
            "time",
            "band",
            "actual_active",
            "detected",
            "result",
        }

        self.assertTrue(
            required_fields.issubset(result.keys())
        )

    def test_active_band_returns_hit(self):
        # In the mixed scenario, band 2 is active at time 1.
        result = self.receiver.scan(2)

        self.assertTrue(result["actual_active"])
        self.assertTrue(result["detected"])
        self.assertEqual(result["result"], "HIT")

    def test_inactive_band_returns_no_signal(self):
        # With false alarm probability 0, inactive band
        # should produce NO_SIGNAL.
        result = self.receiver.scan(0)

        self.assertFalse(result["actual_active"])
        self.assertFalse(result["detected"])
        self.assertEqual(result["result"], "NO_SIGNAL")

    def test_history_is_recorded(self):
        self.receiver.scan(2)
        self.receiver.scan(0)

        history = self.receiver.get_history()

        self.assertEqual(len(history), 2)

    def test_statistics_are_updated(self):
        self.receiver.scan(2)
        self.receiver.scan(0)

        statistics = self.receiver.get_statistics()

        self.assertEqual(statistics["total_scans"], 2)
        self.assertEqual(statistics["hits"], 1)
        self.assertEqual(statistics["no_signal"], 1)

    def test_clear_history(self):
        self.receiver.scan(2)

        self.receiver.clear_history()

        self.assertEqual(
            len(self.receiver.get_history()),
            0,
        )

        statistics = self.receiver.get_statistics()

        self.assertEqual(statistics["total_scans"], 0)
        self.assertEqual(statistics["hits"], 0)
        self.assertEqual(statistics["misses"], 0)
        self.assertEqual(statistics["false_alarms"], 0)
        self.assertEqual(statistics["no_signal"], 0)

    def test_scan_count_matches_history(self):
        self.receiver.scan(2)
        self.receiver.scan(0)
        self.receiver.scan(7)

        self.assertEqual(
            self.receiver.total_scans,
            len(self.receiver.get_history()),
        )


if __name__ == "__main__":
    unittest.main()

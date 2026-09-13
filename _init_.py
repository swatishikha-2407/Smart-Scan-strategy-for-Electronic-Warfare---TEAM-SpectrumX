"""
Metrics package for the Smart Scan Strategy for Electronic Warfare project.

This package contains:
    - Metric calculation functions
    - Scheduler evaluation logic
    - Sequential vs Smart scheduler comparison
    - Experiment runner
"""

from .metrics import (
    calculate_detection_rate,
    calculate_false_alarm_rate,
    calculate_average_detection_delay,
    calculate_detection_interception_rate,
    calculate_average_reward,
    calculate_coverage,
    calculate_hit_count,
    calculate_miss_count,
    calculate_false_alarm_count,
    calculate_total_scans,
)

from .evaluation import evaluate_scheduler

from .comparison import compare_schedulers

__all__ = [
    "calculate_detection_rate",
    "calculate_false_alarm_rate",
    "calculate_average_detection_delay",
    "calculate_detection_interception_rate",
    "calculate_average_reward",
    "calculate_coverage",
    "calculate_hit_count",
    "calculate_miss_count",
    "calculate_false_alarm_count",
    "calculate_total_scans",
    "evaluate_scheduler",
    "compare_schedulers",
]

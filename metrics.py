"""
Metric calculation functions for the Smart Scan Strategy project.

All calculations in this file operate on simulated experiment data.

No real-world military or RF operational data is used.
"""

from typing import Iterable, List, Optional


def calculate_detection_rate(
    successful_detections: int,
    actual_transmission_opportunities: int,
) -> float:
    """
    Calculate the detection rate.

    Formula:
        detection_rate =
            successful_detections / actual_transmission_opportunities

    Parameters
    ----------
    successful_detections : int
        Number of simulated transmission events that were detected.

    actual_transmission_opportunities : int
        Total number of simulated transmission events.

    Returns
    -------
    float
        Detection rate between 0.0 and 1.0.

    If there are no transmission opportunities, the result is 0.0.
    """

    if actual_transmission_opportunities <= 0:
        return 0.0

    return successful_detections / actual_transmission_opportunities


def calculate_false_alarm_rate(
    false_alarm_count: int,
    inactive_band_scans: int,
) -> float:
    """
    Calculate the false alarm rate.

    Formula:
        false_alarm_rate =
            false_alarms / scans_of_inactive_bands

    Parameters
    ----------
    false_alarm_count : int
        Number of scans where the scheduler reported a detection
        even though the scanned band was inactive.

    inactive_band_scans : int
        Number of scans performed on inactive bands.

    Returns
    -------
    float
        False alarm rate between 0.0 and 1.0.
    """

    if inactive_band_scans <= 0:
        return 0.0

    return false_alarm_count / inactive_band_scans


def calculate_average_detection_delay(
    detection_delays: Iterable[float],
) -> float:
    """
    Calculate average detection delay.

    Detection delay is measured in simulation time steps.

    For each successfully detected simulated transmission:

        detection_delay =
            detection_time - activity_start_time

    Parameters
    ----------
    detection_delays : Iterable[float]
        Detection delays for successfully detected transmission events.

    Returns
    -------
    float
        Average detection delay.

    If there are no successful detections, returns 0.0.
    """

    delays: List[float] = list(detection_delays)

    if not delays:
        return 0.0

    return sum(delays) / len(delays)


def calculate_detection_interception_rate(
    detected_transmission_events: int,
    total_transmission_events: int,
) -> float:
    """
    Calculate the detection/interception rate.

    For this project, the PDF defines this metric in the simulation as:

        detected simulated transmission events /
        total simulated transmission events

    Parameters
    ----------
    detected_transmission_events : int
        Number of detected simulated transmission events.

    total_transmission_events : int
        Total simulated transmission events.

    Returns
    -------
    float
        Detection/interception rate between 0.0 and 1.0.
    """

    if total_transmission_events <= 0:
        return 0.0

    return detected_transmission_events / total_transmission_events


def calculate_average_reward(
    rewards: Iterable[float],
) -> float:
    """
    Calculate the average scheduler reward.

    Parameters
    ----------
    rewards : Iterable[float]
        Reward received by the scheduler at each simulation step.

    Returns
    -------
    float
        Average reward.

    If no rewards are available, returns 0.0.
    """

    reward_list: List[float] = list(rewards)

    if not reward_list:
        return 0.0

    return sum(reward_list) / len(reward_list)


def calculate_total_scans(
    scan_records: Iterable,
) -> int:
    """
    Count the total number of scans.

    Each item in scan_records represents one scanner action.

    Parameters
    ----------
    scan_records : Iterable
        Collection of scan records.

    Returns
    -------
    int
        Total number of scans.
    """

    return len(list(scan_records))


def calculate_hit_count(
    detected_transmission_events: int,
) -> int:
    """
    Return the number of successful detections (hits).

    A hit occurs when an actual simulated transmission is
    successfully detected.
    """

    return max(0, detected_transmission_events)


def calculate_miss_count(
    total_transmission_events: int,
    detected_transmission_events: int,
) -> int:
    """
    Calculate the number of missed transmission events.

    Formula:
        miss_count =
            total_transmission_events - detected_transmission_events
    """

    return max(
        0,
        total_transmission_events - detected_transmission_events,
    )


def calculate_false_alarm_count(
    false_alarm_events: Iterable,
) -> int:
    """
    Count false alarm events.

    Parameters
    ----------
    false_alarm_events : Iterable
        Collection of false alarm records.

    Returns
    -------
    int
        Number of false alarms.
    """

    return len(list(false_alarm_events))


def calculate_coverage(
    scanned_bands: Iterable,
    total_bands: int,
) -> float:
    """
    Calculate band coverage.

    Formula:
        coverage =
            number_of_unique_bands_explored / total_number_of_bands

    Parameters
    ----------
    scanned_bands : Iterable
        Band identifiers that were scanned.

    total_bands : int
        Total number of available simulated bands.

    Returns
    -------
    float
        Coverage between 0.0 and 1.0.
    """

    if total_bands <= 0:
        return 0.0

    unique_bands = set(scanned_bands)

    return min(
        1.0,
        len(unique_bands) / total_bands,
    )

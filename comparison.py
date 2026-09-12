"""
Comparison logic for Sequential and Smart schedulers.
"""

from typing import Dict, List


def compare_schedulers(
    sequential_result: Dict,
    smart_result: Dict,
) -> Dict:
    """
    Compare Sequential and Smart scheduler results.

    Both results must come from equivalent simulated scenarios.

    Parameters
    ----------
    sequential_result : dict
        Evaluation result for Sequential Scheduler.

    smart_result : dict
        Evaluation result for Smart Scheduler.

    Returns
    -------
    dict
        Comparison containing metric differences.
    """

    # ---------------------------------------------------------
    # Verify that both schedulers were tested fairly
    # ---------------------------------------------------------

    if sequential_result["scenario"] != smart_result["scenario"]:
        raise ValueError(
            "Sequential and Smart schedulers must use "
            "the same scenario."
        )

    if sequential_result["num_bands"] != smart_result["num_bands"]:
        raise ValueError(
            "Sequential and Smart schedulers must use "
            "the same number of bands."
        )

    if sequential_result["time_steps"] != smart_result["time_steps"]:
        raise ValueError(
            "Sequential and Smart schedulers must use "
            "the same simulation duration."
        )

    if sequential_result["seed"] != smart_result["seed"]:
        raise ValueError(
            "Sequential and Smart schedulers must use "
            "the same random seed for a fair comparison."
        )

    # ---------------------------------------------------------
    # Calculate differences
    # ---------------------------------------------------------

    detection_rate_difference = (
        smart_result["detection_rate"]
        - sequential_result["detection_rate"]
    )

    false_alarm_rate_difference = (
        smart_result["false_alarm_rate"]
        - sequential_result["false_alarm_rate"]
    )

    average_delay_difference = (
        smart_result["average_detection_delay"]
        - sequential_result["average_detection_delay"]
    )

    average_reward_difference = (
        smart_result["average_reward"]
        - sequential_result["average_reward"]
    )

    detection_interception_difference = (
        smart_result["detection_interception_rate"]
        - sequential_result["detection_interception_rate"]
    )

    coverage_difference = (
        smart_result["coverage"]
        - sequential_result["coverage"]
    )

    # ---------------------------------------------------------
    # Determine better scheduler for each metric
    # ---------------------------------------------------------

    if (
        smart_result["detection_rate"]
        > sequential_result["detection_rate"]
    ):
        detection_rate_winner = "smart"

    elif (
        smart_result["detection_rate"]
        < sequential_result["detection_rate"]
    ):
        detection_rate_winner = "sequential"

    else:
        detection_rate_winner = "tie"

    # Higher false alarm rate is worse.
    if (
        smart_result["false_alarm_rate"]
        < sequential_result["false_alarm_rate"]
    ):
        false_alarm_winner = "smart"

    elif (
        smart_result["false_alarm_rate"]
        > sequential_result["false_alarm_rate"]
    ):
        false_alarm_winner = "sequential"

    else:
        false_alarm_winner = "tie"

    # Lower detection delay is better.
    if (
        smart_result["average_detection_delay"]
        < sequential_result["average_detection_delay"]
    ):
        delay_winner = "smart"

    elif (
        smart_result["average_detection_delay"]
        > sequential_result["average_detection_delay"]
    ):
        delay_winner = "sequential"

    else:
        delay_winner = "tie"

    # Higher reward is better.
    if (
        smart_result["average_reward"]
        > sequential_result["average_reward"]
    ):
        reward_winner = "smart"

    elif (
        smart_result["average_reward"]
        < sequential_result["average_reward"]
    ):
        reward_winner = "sequential"

    else:
        reward_winner = "tie"

    # ---------------------------------------------------------
    # Return comparison
    # ---------------------------------------------------------

    return {
        "scenario": sequential_result["scenario"],
        "seed": sequential_result["seed"],

        "sequential": sequential_result,

        "smart": smart_result,

        "difference": {
            "detection_rate": detection_rate_difference,

            "false_alarm_rate": false_alarm_rate_difference,

            "average_detection_delay": (
                average_delay_difference
            ),

            "detection_interception_rate": (
                detection_interception_difference
            ),

            "average_reward": average_reward_difference,

            "coverage": coverage_difference,
        },

        "winner": {
            "detection_rate": detection_rate_winner,

            "false_alarm_rate": false_alarm_winner,

            "average_detection_delay": delay_winner,

            "average_reward": reward_winner,
        },
    }


def determine_overall_winner(
    comparisons: List[Dict],
) -> str:
    """
    Determine the overall better scheduler.

    This function does not assume that Smart is better.

    A simple metric-win count is used:

        - Higher detection rate = better
        - Lower false alarm rate = better
        - Lower detection delay = better
        - Higher average reward = better

    If both schedulers have the same number of wins,
    the result is "tie".
    """

    smart_wins = 0
    sequential_wins = 0

    for comparison in comparisons:

        winners = comparison["winner"]

        for metric in [
            "detection_rate",
            "false_alarm_rate",
            "average_detection_delay",
            "average_reward",
        ]:

            winner = winners[metric]

            if winner == "smart":
                smart_wins += 1

            elif winner == "sequential":
                sequential_wins += 1

    if smart_wins > sequential_wins:
        return "smart"

    if sequential_wins > smart_wins:
        return "sequential"

    return "tie"

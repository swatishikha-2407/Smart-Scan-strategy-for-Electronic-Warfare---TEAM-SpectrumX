"""
Simulation manager for the Smart Scan Strategy project.

This file is responsible for integrating the simulation environment,
receiver, scheduler and metrics components.

The backend is SOFTWARE-ONLY. It does not communicate with real RF
hardware or real-world electronic warfare systems.
"""

from typing import Any, Dict, List, Optional


class SimulationManager:
    """
    Controls and integrates the complete simulation.

    Components:
        environment -> represents the simulated RF environment
        receiver    -> scans a selected frequency band
        scheduler   -> decides which band should be scanned
        metrics     -> evaluates simulation performance
    """

    def __init__(
        self,
        environment: Any = None,
        receiver: Any = None,
        scheduler: Any = None,
        metrics: Any = None,
    ):
        """
        Initialize the simulation manager.

        Parameters
        ----------
        environment:
            Member 1's simulation environment.

        receiver:
            Member 2's virtual receiver.

        scheduler:
            Member 3's scheduler.

        metrics:
            Member 4's evaluation/metrics component.
        """

        self.environment = environment
        self.receiver = receiver
        self.scheduler = scheduler
        self.metrics = metrics

        # Simulation clock
        self.current_time: int = 0

        # Whether the simulation is currently running
        self.running: bool = False

        # Stores every scan observation
        self.history: List[Dict[str, Any]] = []

        # Internal storage for calculated metrics
        self._metrics: Dict[str, float] = {
            "detection_rate": 0.0,
            "false_alarm_rate": 0.0,
            "average_detection_delay": 0.0,
            "average_reward": 0.0,
        }

    # ============================================================
    # SIMULATION CONTROL
    # ============================================================

    def start(self) -> Dict[str, str]:
        """
        Start the simulation.

        Returns
        -------
        dict
            Simulation status.
        """

        self.running = True

        return {
            "status": "started"
        }

    def stop(self) -> Dict[str, str]:
        """
        Stop the simulation.

        Returns
        -------
        dict
            Simulation status.
        """

        self.running = False

        return {
            "status": "stopped"
        }

    def reset(self) -> Dict[str, str]:
        """
        Reset the complete simulation.

        This resets:
            - simulation time
            - running state
            - history
            - metrics
        """

        self.current_time = 0
        self.running = False
        self.history = []

        self._metrics = {
            "detection_rate": 0.0,
            "false_alarm_rate": 0.0,
            "average_detection_delay": 0.0,
            "average_reward": 0.0,
        }

        # Reset Member 1 environment if it provides reset()
        if self.environment is not None:
            reset_method = getattr(self.environment, "reset", None)

            if callable(reset_method):
                reset_method()

        # Reset Member 2 receiver if it provides reset()
        if self.receiver is not None:
            reset_method = getattr(self.receiver, "reset", None)

            if callable(reset_method):
                reset_method()

        # Reset Member 3 scheduler if it provides reset()
        if self.scheduler is not None:
            reset_method = getattr(self.scheduler, "reset", None)

            if callable(reset_method):
                reset_method()

        # Reset Member 4 metrics if it provides reset()
        if self.metrics is not None:
            reset_method = getattr(self.metrics, "reset", None)

            if callable(reset_method):
                reset_method()

        return {
            "status": "reset"
        }

    # ============================================================
    # ONE SIMULATION STEP
    # ============================================================

    def step(self) -> Dict[str, Any]:
        """
        Perform approximately one complete simulation cycle.

        The PDF specifies the following sequence:

        1. obtain current environment state
        2. scheduler chooses band
        3. receiver scans selected band
        4. receiver returns HIT/MISS
        5. scheduler updates
        6. store observation
        7. calculate/update metrics
        8. return result
        """

        if not self.running:
            raise RuntimeError("Simulation has not been started.")

        # --------------------------------------------------------
        # 1. Obtain current environment state
        # --------------------------------------------------------

        environment_state = self._get_environment_state()

        # --------------------------------------------------------
        # 2. Scheduler chooses a band
        # --------------------------------------------------------

        current_band = self._choose_band(environment_state)

        # --------------------------------------------------------
        # 3 & 4. Receiver scans selected band
        # --------------------------------------------------------

        receiver_result = self._scan_band(
            current_band,
            environment_state
        )

        # Convert receiver result into a standard format.
        detected = self._extract_detection(receiver_result)

        result = "HIT" if detected else "MISS"

        # --------------------------------------------------------
        # 5. Scheduler updates
        # --------------------------------------------------------

        self._update_scheduler(
            current_band=current_band,
            detected=detected,
            environment_state=environment_state,
        )

        # --------------------------------------------------------
        # 6. Store observation
        # --------------------------------------------------------

        observation = {
            "time": self.current_time,
            "band": current_band,
            "result": result,
            "detected": detected,
        }

        self.history.append(observation)

        # --------------------------------------------------------
        # 7. Calculate/update metrics
        # --------------------------------------------------------

        self._update_metrics()

        # Move simulation clock forward
        self.current_time += 1

        # --------------------------------------------------------
        # Select next band information
        # --------------------------------------------------------

        next_band = self._get_next_band()

        # --------------------------------------------------------
        # 8. Return result
        # --------------------------------------------------------

        return {
            "time": self.current_time,
            "current_band": current_band,
            "result": result,
            "detected": detected,
            "next_band": next_band,
        }

    # ============================================================
    # ENVIRONMENT
    # ============================================================

    def _get_environment_state(self) -> Any:
        """
        Obtain the current state of Member 1's environment.

        The exact API of Member 1 is not specified in the PDF.
        Therefore this method supports common get_state() / state
        interfaces and can be adapted once Member 1's code is added.
        """

        if self.environment is None:
            return {}

        get_state = getattr(
            self.environment,
            "get_state",
            None
        )

        if callable(get_state):
            return get_state()

        state = getattr(
            self.environment,
            "state",
            None
        )

        if state is not None:
            return state

        return {}

    # ============================================================
    # SCHEDULER
    # ============================================================

    def _choose_band(self, environment_state: Any) -> int:
        """
        Ask Member 3's scheduler to select a band.

        The exact scheduler API is not provided in the PDF.
        """

        if self.scheduler is None:
            return 0

        # Try choose_band()
        choose_band = getattr(
            self.scheduler,
            "choose_band",
            None
        )

        if callable(choose_band):
            band = choose_band(environment_state)

            return int(band)

        # Try select_band()
        select_band = getattr(
            self.scheduler,
            "select_band",
            None
        )

        if callable(select_band):
            band = select_band(environment_state)

            return int(band)

        # Try selected_band property
        selected_band = getattr(
            self.scheduler,
            "selected_band",
            None
        )

        if selected_band is not None:
            return int(selected_band)

        return 0

    def _update_scheduler(
        self,
        current_band: int,
        detected: bool,
        environment_state: Any,
    ) -> None:
        """
        Inform the scheduler about the result of the scan.
        """

        if self.scheduler is None:
            return

        update_method = getattr(
            self.scheduler,
            "update",
            None
        )

        if callable(update_method):
            update_method(
                current_band,
                detected,
                environment_state,
            )
            return

        update_method = getattr(
            self.scheduler,
            "update_after_scan",
            None
        )

        if callable(update_method):
            update_method(
                current_band,
                detected,
            )

    def _get_next_band(self) -> Optional[int]:
        """
        Obtain the scheduler's next selected band.
        """

        if self.scheduler is None:
            return None

        selected_band = getattr(
            self.scheduler,
            "selected_band",
            None
        )

        if selected_band is not None:
            return int(selected_band)

        return None

    # ============================================================
    # RECEIVER
    # ============================================================

    def _scan_band(
        self,
        band: int,
        environment_state: Any,
    ) -> Any:
        """
        Ask Member 2's virtual receiver to scan a band.

        The exact receiver API is not specified in the PDF.
        """

        if self.receiver is None:
            return False

        scan = getattr(
            self.receiver,
            "scan",
            None
        )

        if callable(scan):
            try:
                return scan(
                    band,
                    environment_state
                )
            except TypeError:
                return scan(band)

        scan_band = getattr(
            self.receiver,
            "scan_band",
            None
        )

        if callable(scan_band):
            try:
                return scan_band(
                    band,
                    environment_state
                )
            except TypeError:
                return scan_band(band)

        return False

    def _extract_detection(self, receiver_result: Any) -> bool:
        """
        Convert different receiver return formats into a boolean.

        Supported examples:

            True
            False

            {"detected": True}

            {"result": "HIT"}

            {"hit": True}
        """

        if isinstance(receiver_result, bool):
            return receiver_result

        if isinstance(receiver_result, dict):

            if "detected" in receiver_result:
                return bool(receiver_result["detected"])

            if "hit" in receiver_result:
                return bool(receiver_result["hit"])

            if "result" in receiver_result:
                return str(
                    receiver_result["result"]
                ).upper() == "HIT"

        if isinstance(receiver_result, str):
            return receiver_result.upper() == "HIT"

        return bool(receiver_result)

    # ============================================================
    # METRICS
    # ============================================================

    def _update_metrics(self) -> None:
        """
        Calculate metrics using Member 4 when available.

        If Member 4 has not yet been integrated, calculate the
        basic detection rate from the stored simulation history.
        """

        if self.metrics is not None:

            evaluate = getattr(
                self.metrics,
                "evaluate",
                None
            )

            if callable(evaluate):

                calculated = evaluate(
                    self.history
                )

                if isinstance(calculated, dict):
                    self._metrics.update(calculated)

                    return

        # Basic fallback calculation.
        # This is NOT a fake hard-coded result.
        # It is calculated from actual simulation history.

        if not self.history:
            self._metrics = {
                "detection_rate": 0.0,
                "false_alarm_rate": 0.0,
                "average_detection_delay": 0.0,
                "average_reward": 0.0,
            }

            return

        total_scans = len(self.history)

        hits = sum(
            1
            for item in self.history
            if item["result"] == "HIT"
        )

        detection_rate = hits / total_scans

        self._metrics["detection_rate"] = detection_rate

    # ============================================================
    # PUBLIC INFORMATION METHODS
    # ============================================================

    def get_state(self) -> Dict[str, Any]:
        """
        Return the current simulation state.
        """

        return {
            "current_time": self.current_time,
            "running": self.running,
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Return scan history.
        """

        return self.history

    def get_metrics(self) -> Dict[str, float]:
        """
        Return calculated simulation metrics.
        """

        return self._metrics

    def get_scheduler_info(self) -> Dict[str, Any]:
        """
        Return information explaining why the scheduler prefers
        particular simulated bands.
        """

        if self.scheduler is None:
            return {
                "selected_band": None,
                "scores": {},
            }

        selected_band = getattr(
            self.scheduler,
            "selected_band",
            None
        )

        scores = getattr(
            self.scheduler,
            "scores",
            {}
        )

        if scores is None:
            scores = {}

        # Convert dictionary keys to strings because the API example
        # in the PDF uses string keys.
        string_scores = {
            str(key): value
            for key, value in scores.items()
        }

        return {
            "selected_band": selected_band,
            "scores": string_scores,
        }

class VirtualReceiver:
    def __init__(self, environment):
        self.environment = environment
        self.scan_count = 0

    def scan(self, band):
        """
        Scan one simulated band and return a simple observation.
        """

        state = self.environment.get_band_state(band)

        self.scan_count += 1

        if state["active"]:
            result = "HIT"
        else:
            result = "MISS"

        return {
            "band": band,
            "time": state["time"],
            "result": result,
            "signal_detected": state["active"]
        }
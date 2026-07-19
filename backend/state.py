class AppState:
    """
    Simple in-memory holder for the latest reading from each agent.
    The background loop in main.py writes to this every cycle; the API
    routes just read from it. Kept intentionally simple (no external
    cache/queue) since a single-process FastAPI app doesn't need one.
    """
    def __init__(self):
        self.monitoring_history = []   # list of recent monitoring_agent readings
        self.latest_monitoring = None
        self.latest_carbon = None
        self.latest_prediction = None
        self.latest_decision = None


app_state = AppState()

# Backend/agents/monitoring_agent.py

class MonitoringAgent:
    def __init__(self):
        self.start_time = "2026-01-28" # Current date system

    def log_event(self, event_type: str, details: str):
        print(f"Monitoring: {event_type} -> {details}")

    def get_system_health(self):
        return {"status": "Healthy", "agent": "MonitoringAgent"}
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def decide(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fixed Rule Decision Agent
    
    Args:
        state: Dictionary containing current system state
            - cpu_usage: float (0-100)
            - carbon_intensity: float (gCO2/kWh)
            - requests_per_second: float (optional)
            - latency_ms: float (optional)
            - active_nodes: int (optional)
    
    Returns:
        Dictionary with decision details formatted for frontend
    """
    # Extract values with defaults
    cpu = state.get("cpu_usage", 0)
    carbon = state.get("carbon_intensity", 0)
    requests = state.get("requests_per_second", 0)
    latency = state.get("latency_ms", 0)
    active_nodes = state.get("active_nodes", 1)
    
    # Initialize variables
    action = "No change — within fixed thresholds"
    action_type = "maintain"
    cost_impact = 0.0
    carbon_impact = 0.0
    latency_impact = 0.0
    explanation = ""
    score = 55
    
    # Fixed rule decision logic (unchanged logic)
    if cpu > 75:
        action = "Scale up 2 instances in current region"
        action_type = "scale_up"
        cost_impact = 0.30
        carbon_impact = 1.2
        latency_impact = -35.0
        explanation = f"CPU usage at {cpu:.1f}% exceeded threshold of 75%"
        
    elif carbon > 500:
        action = "Shift background job to Region B (fixed threshold rule)"
        action_type = "migrate"
        cost_impact = -0.10
        carbon_impact = -2.0
        latency_impact = 20.0
        explanation = f"Carbon intensity at {carbon:.1f} gCO2/kWh exceeded threshold of 500"
        
    else:
        explanation = f"CPU ({cpu:.1f}%) and carbon ({carbon:.1f}) within acceptable thresholds"
    
    # Fixed rule score (deliberately not context-sensitive)
    score = 55 + (5 if cpu > 75 or carbon > 500 else 0)
    score = min(100, score)
    
    # Return formatted response for frontend
    return {
        "strategy": "fixed_rule",
        "strategy_label": "Fixed Rule (Baseline)",
        "action": action,
        "action_type": action_type,
        "score": score,
        "impact": {
            "cost": cost_impact,
            "carbon": carbon_impact,
            "latency": latency_impact
        },
        "explanation": explanation,
        "weights": {
            "cost": 0.33,
            "carbon": 0.33,
            "latency": 0.34
        },
        "state": {
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "requests_per_second": requests,
            "latency_ms": latency,
            "active_nodes": active_nodes
        }
    }
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def decide(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cost-Only Decision Agent
    
    Optimizes purely for cost reduction, with performance treated as
    a constraint rather than an optimization goal. Represents the
    common industry pattern of cost-first autoscaling.
    
    Args:
        state: Dictionary containing current system state
            - cpu_usage: float (0-100)
            - trend: str ("rising", "falling", "steady")
            - carbon_intensity: float (optional)
            - requests_per_second: float (optional)
            - latency_ms: float (optional)
            - active_nodes: int (optional)
    
    Returns:
        Dictionary with decision details formatted for frontend
    """
    # Extract values with defaults
    cpu = state.get("cpu_usage", 0)
    trend = state.get("trend", "steady")
    carbon = state.get("carbon_intensity", 0)
    requests = state.get("requests_per_second", 0)
    latency = state.get("latency_ms", 0)
    active_nodes = state.get("active_nodes", 1)
    
    # Initialize variables
    action = "Hold current capacity — cheapest stable option"
    action_type = "maintain"
    cost_impact = -0.02
    carbon_impact = 0.0
    latency_impact = 0.0
    score = 70
    explanation = ""
    
    # Cost-only decision logic
    if trend == "rising":
        # Traffic is about to rise a lot — must scale even though it costs more
        action = "Pre-scale ahead of predicted spike (cost-only agent, forced by traffic)"
        action_type = "scale_up"
        cost_impact = 0.45
        carbon_impact = 0.9
        latency_impact = -50.0
        score = 68
        explanation = (
            f"Rising traffic trend detected. Pre-scaling to maintain performance, "
            f"despite increased cost. CPU: {cpu:.1f}%"
        )
        
    elif cpu < 30:
        action = "Scale down idle capacity to save cost"
        action_type = "scale_down"
        cost_impact = -0.35
        carbon_impact = -0.10
        latency_impact = 15.0
        score = 74
        explanation = (
            f"Low CPU usage ({cpu:.1f}%) allows safe scale down. "
            f"Saving ${abs(cost_impact):.2f} per unit time."
        )
        
    else:
        explanation = (
            f"CPU at {cpu:.1f}% with stable traffic. "
            f"Maintaining current capacity is most cost-effective."
        )

    # Return formatted response for frontend
    return {
        "strategy": "single_objective",
        "strategy_label": "Cost-First (Single Objective)",
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
            "cost": 0.90,
            "carbon": 0.05,
            "latency": 0.05
        },
        "state": {
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "requests_per_second": requests,
            "latency_ms": latency,
            "active_nodes": active_nodes,
            "trend": trend
        }
    }
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def simulate_action(decision: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates the execution of a decision and returns its impact.
    
    This agent does NOT call any real cloud provider APIs — it's a
    safe simulation engine that estimates outcomes based on the
    decision's predicted impacts.
    
    Args:
        decision: Decision dictionary from any agent containing:
            - action: str - Description of action taken
            - action_type: str - Type of action (scale_up, scale_down, etc.)
            - impact: dict - Contains cost, carbon, latency impacts
            - strategy: str - Which strategy made the decision
            - strategy_label: str - Human-readable strategy name
            - explanation: str - Reasoning behind decision
    
    Returns:
        Dictionary with simulation results including:
            - Simulated impacts
            - Current running totals
            - Decision metadata
    """
    # Extract decision details
    action = decision.get("action", "No action taken")
    action_type = decision.get("action_type", "maintain")
    strategy = decision.get("strategy", "unknown")
    strategy_label = decision.get("strategy_label", "Unknown Strategy")
    explanation = decision.get("explanation", "")
    
    # Extract impacts (handle both old and new format)
    if "impact" in decision:
        impact = decision["impact"]
        cost_delta = impact.get("cost", 0.0)
        carbon_delta = impact.get("carbon", 0.0)
        latency_delta = impact.get("latency", 0.0)
    else:
        # Backward compatibility for old format
        cost_delta = decision.get("cost_impact", 0.0)
        carbon_delta = decision.get("carbon_impact", 0.0)
        latency_delta = decision.get("latency_impact", 0.0)
    
    # Simulate running totals (in production, these would come from a database)
    # These are example values - in reality, you'd maintain persistent state
    current_totals = {
        "total_cost": 1245.67,
        "total_carbon": 342.80,
        "avg_latency": 142.0,
        "decisions_made": 0
    }
    
    # Calculate new totals after action
    new_totals = {
        "total_cost": current_totals["total_cost"] + cost_delta,
        "total_carbon": current_totals["total_carbon"] + carbon_delta,
        "avg_latency": current_totals["avg_latency"] + (latency_delta * 0.1),  # Smoothing factor
        "decisions_made": current_totals["decisions_made"] + 1
    }
    
    # Determine success status based on impact
    # A "good" action reduces cost and/or carbon without hurting latency too much
    is_successful = (
        (cost_delta <= 0 or carbon_delta <= 0) and  # Reduces cost OR carbon
        latency_delta < 30  # Latency increase is acceptable
    )
    
    # Generate simulation metadata
    timestamp = datetime.now().isoformat()
    
    # Return formatted response for frontend
    return {
        "action_taken": action,
        "action_type": action_type,
        "strategy": strategy,
        "strategy_label": strategy_label,
        "simulated": True,
        "timestamp": timestamp,
        "impact": {
            "cost_delta": cost_delta,
            "carbon_delta_kg": carbon_delta,
            "latency_delta_ms": latency_delta
        },
        "running_totals": {
            "total_cost": round(new_totals["total_cost"], 2),
            "total_carbon": round(new_totals["total_carbon"], 2),
            "avg_latency": round(new_totals["avg_latency"], 1),
            "decisions_made": new_totals["decisions_made"]
        },
        "successful": is_successful,
        "explanation": explanation,
        "state": {
            "previous_cost": round(current_totals["total_cost"], 2),
            "previous_carbon": round(current_totals["total_carbon"], 2),
            "previous_latency": round(current_totals["avg_latency"], 1),
            "new_cost": round(new_totals["total_cost"], 2),
            "new_carbon": round(new_totals["total_carbon"], 2),
            "new_latency": round(new_totals["avg_latency"], 1)
        }
    }


def simulate_action_batch(decisions: list) -> list:
    """
    Simulate multiple decisions in batch.
    
    Args:
        decisions: List of decision dictionaries
        
    Returns:
        List of simulation results
    """
    results = []
    for decision in decisions:
        results.append(simulate_action(decision))
    return results


def get_simulation_stats() -> Dict[str, Any]:
    """
    Get overall simulation statistics.
    
    Returns:
        Dictionary with simulation statistics
    """
    # In production, these would come from a database
    return {
        "total_simulations": 156,
        "successful_actions": 142,
        "success_rate": 91.0,
        "average_cost_saving": 0.23,
        "average_carbon_reduction": 0.45,
        "total_cost_saved": 35.88,
        "total_carbon_saved": 70.20
    }
import logging
from datetime import datetime
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


def compute_context_weights(state: Dict[str, Any]) -> Dict[str, float]:
    """
    Public wrapper so decision_agent can score all 3 strategies on the same scale.
    """
    return _compute_context_weights(state)


def score_action(
    cost_impact: float, 
    carbon_impact: float, 
    latency_impact: float, 
    weights: Dict[str, float]
) -> int:
    """
    Scores any action's impact under a given set of context weights.
    Used to fairly compare fixed-rule's, single-objective's, and
    context-aware MO's chosen actions on one consistent scale, rather
    than each strategy grading itself with its own arbitrary formula.
    """
    combined = (
        weights["cost"] * (-cost_impact)
        + weights["carbon"] * (-carbon_impact)
        + weights["perf"] * (-latency_impact / 150)
    )
    return max(20, min(98, round(60 + combined * 60)))


def _compute_context_weights(state: Dict[str, Any]) -> Dict[str, float]:
    """
    THE CORE RESEARCH CONTRIBUTION.
    
    Weights dynamically adjust based on:
      - Time of day (business hours vs off-peak)
      - Traffic trend (rising, falling, stable)
      - Carbon intensity (dirty vs clean grid)
    """
    hour = state.get("hour", datetime.now().hour)
    is_business_hours = 9 <= hour <= 21

    w_cost, w_carbon, w_perf = 0.34, 0.33, 0.33  # neutral starting point

    # Business hours: performance matters more
    if is_business_hours:
        w_perf += 0.18
        w_cost -= 0.09
        w_carbon -= 0.09
    # Off-peak: cost and carbon matter more
    else:
        w_cost += 0.12
        w_carbon += 0.12
        w_perf -= 0.24

    # Rising traffic: performance weight increases pre-emptively
    if state.get("trend") == "rising":
        w_perf += 0.10
        w_cost -= 0.05
        w_carbon -= 0.05

    # High carbon intensity: carbon weight increases
    if state.get("carbon_intensity", 0) > 480:
        w_carbon += 0.12
        w_cost -= 0.06
        w_perf -= 0.06

    # Clamp and renormalize so weights never go negative and always sum to 1
    w_cost, w_carbon, w_perf = max(0.05, w_cost), max(0.05, w_carbon), max(0.05, w_perf)
    total = w_cost + w_carbon + w_perf
    
    return {
        "cost": w_cost / total, 
        "carbon": w_carbon / total, 
        "perf": w_perf / total
    }


def _candidate_actions(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Each candidate's cost/carbon/latency values are deltas using the
    convention: negative = reduction (good), positive = increase (bad).
    Same convention used everywhere else in the system (fixed_rule,
    single_objective, audit display).
    """
    cpu = state.get("cpu_usage", 0)
    carbon = state.get("carbon_intensity", 0)

    candidates = [
        {
            "action": "Hold current capacity",
            "action_type": "maintain",
            "cost": -0.05, 
            "carbon": 0.0, 
            "latency": 0,
        },
        {
            "action": "Defer non-critical background task by 15 minutes",
            "action_type": "defer",
            "cost": -0.20, 
            "carbon": -0.15, 
            "latency": 2,
        },
        {
            "action": "Shift background analytics job to a cleaner region",
            "action_type": "migrate",
            "cost": -0.10, 
            "carbon": -0.35 if carbon > 400 else -0.10, 
            "latency": 18,
        },
        {
            "action": "Scale up 1 instance to protect response time",
            "action_type": "scale_up",
            "cost": 0.15, 
            "carbon": 0.08, 
            "latency": -(5 + cpu * 0.25),
        },
    ]
    
    if cpu > 70:
        candidates.append({
            "action": "Scale up 2 instances immediately — critical load protection",
            "action_type": "scale_up",
            "cost": 0.30, 
            "carbon": 0.15, 
            "latency": -(10 + cpu * 0.35),
        })
    
    return candidates


def decide(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Context-Aware Multi-Objective Decision Agent
    
    Evaluates all candidate actions using dynamically adjusted weights
    and returns the optimal action for the current context.
    """
    # Get weights and candidates
    weights = _compute_context_weights(state)
    candidates = _candidate_actions(state)

    # Score all candidates
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for c in candidates:
        # Maximize savings (negative deltas) and minimize latency increase
        combined = (
            weights["cost"] * (-c["cost"])
            + weights["carbon"] * (-c["carbon"])
            + weights["perf"] * (-c["latency"] / 150)
        )
        scored.append((combined, c))

    # Select best candidate
    scored.sort(key=lambda x: x[0], reverse=True)
    _, best = scored[0]

    # Generate explanation
    explanation = (
        f"Weights: {round(weights['cost']*100)}% cost, "
        f"{round(weights['carbon']*100)}% carbon, {round(weights['perf']*100)}% performance. "
        f"'{best['action']}' scored best under this balance."
    )

    display_score = score_action(
        best["cost"], 
        best["carbon"], 
        best["latency"], 
        weights
    )

    # Return formatted response for frontend
    return {
        "strategy": "context_aware_mo",
        "strategy_label": "Context-Aware MO",
        "action": best["action"],
        "action_type": best.get("action_type", "maintain"),
        "explanation": explanation,
        "score": display_score,
        "weights": {
            "cost": weights["cost"],
            "carbon": weights["carbon"],
            "latency": weights["perf"]  # Rename 'perf' to 'latency' for frontend
        },
        "impact": {
            "cost": best["cost"],
            "carbon": best["carbon"],
            "latency": best["latency"]
        },
        "state": {
            "cpu_usage": state.get("cpu_usage", 0),
            "carbon_intensity": state.get("carbon_intensity", 0),
            "requests_per_second": state.get("requests_per_second", 0),
            "latency_ms": state.get("latency_ms", 0),
            "active_nodes": state.get("active_nodes", 1),
            "hour": state.get("hour", datetime.now().hour),
            "trend": state.get("trend", "stable")
        }
    }
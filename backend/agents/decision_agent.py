"""
decision_agent.py - Orchestrates all decision strategies and returns unified result.
"""

from datetime import datetime
from agents.decision_strategies.fixed_rule import decide as fixedrule_decide
from agents.decision_strategies.single_objective import decide as singleobjective_decide
from agents.decision_strategies.multi_objective import decide as multiobjective_decide
from agents.decision_strategies.multi_objective import compute_context_weights, score_action


def make_decision(monitoring: dict, carbon: dict, prediction: dict) -> dict:
    state = {
        "cpu_usage": monitoring.get("cpu_usage", 0),
        "carbon_intensity": carbon.get("carbonIntensity", 0),
        "requests_per_second": monitoring.get("requests_per_second", 0),
        "latency_ms": monitoring.get("latency_ms", 0),
        "active_nodes": monitoring.get("active_nodes", 1),
        "predicted_traffic": prediction.get("predicted_traffic", []),
        "trend": prediction.get("trend", "steady"),
        "hour": datetime.now().hour
    }
    
    fr = fixedrule_decide(state)
    so = singleobjective_decide(state)
    mo = multiobjective_decide(state)
    
    weights = compute_context_weights(state)
    
    fr_fair_score = score_action(fr["impact"]["cost"], fr["impact"]["carbon"], fr["impact"]["latency"], weights)
    so_fair_score = score_action(so["impact"]["cost"], so["impact"]["carbon"], so["impact"]["latency"], weights)
    mo_fair_score = mo["score"]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "chosen_strategy": "context_aware_mo",
        "chosen_label": "Context-Aware MO",
        "action": mo["action"],
        "action_type": mo.get("action_type", "maintain"),
        "explanation": mo["explanation"],
        "score": mo["score"],
        "scores": {
            "fixed_rule": fr_fair_score,
            "single_objective": so_fair_score,
            "context_aware_mo": mo_fair_score
        },
        "impact": mo["impact"],
        "weights": mo["weights"],
        "state": state,
        "all_strategies": {
            "fixed_rule": {
                "action": fr["action"],
                "action_type": fr.get("action_type", "maintain"),
                "score": fr_fair_score,
                "impact": fr["impact"]
            },
            "single_objective": {
                "action": so["action"],
                "action_type": so.get("action_type", "maintain"),
                "score": so_fair_score,
                "impact": so["impact"]
            },
            "context_aware_mo": {
                "action": mo["action"],
                "action_type": mo.get("action_type", "maintain"),
                "score": mo_fair_score,
                "impact": mo["impact"]
            }
        }
    }
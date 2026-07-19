import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from state import app_state
from agents import make_decision
from agents.monitoring_agent import get_monitoring_state
from agents.prediction_agent import predict_traffic

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/decision")
async def get_decision(
    strategy: Optional[str] = Query(None, description="Force specific strategy: baseline, cost, weighted")
):
    """
    Get current decision from the decision engine.
    
    Args:
        strategy: Optional strategy override (baseline, cost, weighted)
    
    Returns:
        Decision with strategy comparison and chosen action
    """
    try:
        # Get current monitoring state
        monitoring = get_monitoring_state()
        
        # Get carbon data
        carbon = app_state.latest_carbon or {
            "carbonIntensity": 420,
            "region": "IN"
        }
        
        # Get prediction (need history)
        history = app_state.monitoring_history or []
        prediction = predict_traffic(history, horizon=6)
        
        # Make decision
        decision = make_decision(monitoring, carbon, prediction)
        
        # If specific strategy requested, override
        if strategy:
            # Map strategy to decision
            strategy_map = {
                "baseline": "fixed_rule",
                "cost": "single_objective",
                "weighted": "context_aware_mo"
            }
            
            if strategy in strategy_map:
                target = strategy_map[strategy]
                # Find the strategy in all_strategies
                if target in decision.get("all_strategies", {}):
                    strategy_data = decision["all_strategies"][target]
                    # Override decision with specific strategy
                    decision["action"] = strategy_data["action"]
                    decision["action_type"] = strategy_data["action_type"]
                    decision["score"] = strategy_data["score"]
                    decision["impact"] = strategy_data["impact"]
                    decision["chosen_strategy"] = target
                    decision["chosen_label"] = strategy_data.get("strategy_label", target)
        
        # Store latest decision
        app_state.latest_decision = decision
        
        return {
            "status": "success",
            "data": decision
        }
        
    except Exception as e:
        logger.error(f"Error making decision: {e}")
        
        # Return warm-up response
        return {
            "status": "success",
            "data": app_state.latest_decision or {
                "chosen_strategy": "context_aware_mo",
                "chosen_label": "Context-Aware MO",
                "action": "Warming up — collecting initial data",
                "action_type": "maintain",
                "explanation": "The system needs a few monitoring cycles before it can make its first informed decision.",
                "score": 0,
                "scores": {
                    "fixed_rule": 0,
                    "single_objective": 0,
                    "context_aware_mo": 0
                },
                "impact": {
                    "cost": 0,
                    "carbon": 0,
                    "latency": 0
                },
                "weights": {
                    "cost": 0.33,
                    "carbon": 0.33,
                    "latency": 0.34
                },
                "state": {},
                "all_strategies": {}
            }
        }


@router.get("/decision/strategies")
async def get_strategy_comparison():
    """
    Get comparison of all strategies for current state.
    
    Returns:
        Comparison data for all strategies
    """
    try:
        # Get current monitoring state
        monitoring = get_monitoring_state()
        
        # Get carbon data
        carbon = app_state.latest_carbon or {
            "carbonIntensity": 420,
            "region": "IN"
        }
        
        # Get prediction
        history = app_state.monitoring_history or []
        prediction = predict_traffic(history, horizon=6)
        
        # Make decision (contains all strategies)
        decision = make_decision(monitoring, carbon, prediction)
        
        # Extract strategies comparison
        strategies_data = decision.get("all_strategies", {})
        
        # Format for frontend comparison chart
        names = []
        costs = []
        carbons = []
        latencies = []
        scores = []
        actions = []
        
        for key, data in strategies_data.items():
            label_map = {
                "fixed_rule": "Fixed Rule (Baseline)",
                "single_objective": "Cost-First",
                "context_aware_mo": "Context-Aware MO"
            }
            names.append(label_map.get(key, key))
            
            impact = data.get("impact", {})
            costs.append(impact.get("cost", 0))
            carbons.append(impact.get("carbon", 0))
            latencies.append(impact.get("latency", 0))
            scores.append(data.get("score", 0))
            actions.append(data.get("action", ""))
        
        return {
            "status": "success",
            "data": {
                "names": names,
                "cost": costs,
                "carbon": carbons,
                "latency": latencies,
                "scores": scores,
                "actions": actions,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting strategy comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decision/execute")
async def execute_decision():
    """
    Execute the current decision and simulate action.
    
    Returns:
        Simulation result of the executed decision
    """
    try:
        from agents import simulate_action
        from agents.audit_agent import record_decision
        
        # Get current decision
        decision_response = await get_decision()
        decision = decision_response.get("data", {})
        
        # Simulate action
        action_result = simulate_action(decision)
        
        # Record in audit
        conn = app_state.db_connection if hasattr(app_state, 'db_connection') else None
        if conn:
            audit_entry = record_decision(conn, decision, action_result)
        else:
            audit_entry = None
        
        return {
            "status": "success",
            "data": {
                "decision": decision,
                "simulation": action_result,
                "audit_entry": audit_entry,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error executing decision: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decision/state")
async def get_decision_state():
    """
    Get current decision state including weights and context.
    
    Returns:
        Current decision state with weights and context
    """
    try:
        # Get current decision
        decision_response = await get_decision()
        decision = decision_response.get("data", {})
        
        return {
            "status": "success",
            "data": {
                "chosen_strategy": decision.get("chosen_strategy", "context_aware_mo"),
                "chosen_label": decision.get("chosen_label", "Context-Aware MO"),
                "weights": decision.get("weights", {
                    "cost": 0.33,
                    "carbon": 0.33,
                    "latency": 0.34
                }),
                "state": decision.get("state", {}),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting decision state: {e}")
        raise HTTPException(status_code=500, detail=str(e))
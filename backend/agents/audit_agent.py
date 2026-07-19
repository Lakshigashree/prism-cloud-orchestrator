import logging
from datetime import datetime
from typing import Dict, Any, Optional

from database.db_connection import insert_audit_entry, insert_decision

logger = logging.getLogger(__name__)


def _fmt_signed(value: float, unit: str, decimals: int = 2) -> str:
    sign = "+" if value >= 0 else ""
    formatted_value = f"{sign}{round(value, decimals)}"
    return f"{formatted_value}{unit}"


def _fmt_currency(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}${round(abs(value), 2)}"


def record_decision(
    conn: Any,
    decision: Dict[str, Any],
    action_result: Dict[str, Any]
) -> Dict[str, Any]:
    now = datetime.now()
    
    strategy_label = decision.get("strategy_label", "Unknown Strategy")
    
    if "impact" in decision:
        impact = decision["impact"]
        cost_impact = impact.get("cost", 0.0)
        carbon_impact = impact.get("carbon", 0.0)
        latency_impact = impact.get("latency", 0.0)
    else:
        cost_impact = decision.get("cost_impact", 0.0)
        carbon_impact = decision.get("carbon_impact", 0.0)
        latency_impact = decision.get("latency_impact", 0.0)
    
    if action_result and "impact" in action_result:
        sim_impact = action_result["impact"]
        cost_impact = sim_impact.get("cost_delta", cost_impact)
        carbon_impact = sim_impact.get("carbon_delta_kg", carbon_impact)
        latency_impact = sim_impact.get("latency_delta_ms", latency_impact)
    
    audit_entry = {
        "id": None,
        "timestamp": now.isoformat(),
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "action": decision.get("action", "No action taken"),
        "action_type": decision.get("action_type", "maintain"),
        "strategy": decision.get("strategy", "unknown"),
        "strategy_label": strategy_label,
        "score": decision.get("score", 0),
        "explanation": decision.get("explanation", ""),
        "impact": {
            "cost": cost_impact,
            "carbon": carbon_impact,
            "latency": latency_impact
        },
        "impact_formatted": {
            "cost": _fmt_currency(cost_impact),
            "carbon": _fmt_signed(carbon_impact, " kg"),
            "latency": _fmt_signed(latency_impact, "ms", 0)
        },
        "weights": decision.get("weights", {
            "cost": 0.33,
            "carbon": 0.33,
            "latency": 0.34
        }),
        "state": decision.get("state", {})
    }
    
    try:
        # Insert into database
        decision_id = insert_decision(conn, decision)
        audit_entry["id"] = decision_id
        
        insert_audit_entry(conn, audit_entry)
        
        logger.info(f"Audit recorded: {strategy_label} - {decision.get('action', '')[:50]}...")
        
    except Exception as e:
        logger.error(f"Failed to record audit entry: {e}")
    
    return audit_entry


def record_decision_batch(
    conn: Any,
    decisions: list,
    action_results: list
) -> list:
    entries = []
    for decision, action_result in zip(decisions, action_results):
        entry = record_decision(conn, decision, action_result)
        entries.append(entry)
    
    logger.info(f"Batch recorded: {len(entries)} decisions")
    return entries


def get_audit_summary(entries: list) -> Dict[str, Any]:
    if not entries:
        return {
            "total_decisions": 0,
            "strategies_used": {},
            "average_score": 0,
            "total_cost_saved": 0,
            "total_carbon_saved": 0
        }
    
    strategies = {}
    total_score = 0
    total_cost = 0
    total_carbon = 0
    
    for entry in entries:
        strategy = entry.get("strategy_label", "Unknown")
        strategies[strategy] = strategies.get(strategy, 0) + 1
        
        total_score += entry.get("score", 0)
        
        impact = entry.get("impact", {})
        cost_impact = impact.get("cost", 0)
        carbon_impact = impact.get("carbon", 0)
        
        if cost_impact < 0:
            total_cost += abs(cost_impact)
        if carbon_impact < 0:
            total_carbon += abs(carbon_impact)
    
    return {
        "total_decisions": len(entries),
        "strategies_used": strategies,
        "average_score": round(total_score / len(entries), 1),
        "total_cost_saved": round(total_cost, 2),
        "total_carbon_saved": round(total_carbon, 2)
    }


def format_for_audit_page(entries: list, limit: int = 50) -> Dict[str, Any]:
    sorted_entries = sorted(
        entries,
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )
    
    limited_entries = sorted_entries[:limit]
    
    return {
        "entries": limited_entries,
        "total": len(entries),
        "returned": len(limited_entries),
        "has_more": len(entries) > limit
    }
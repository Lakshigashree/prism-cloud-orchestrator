import json
import os
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

# Path to results file
RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), 
    "..", 
    "experiments", 
    "results", 
    "latest_results.json"
)


@router.get("/results")
async def get_experiment_results():
    """
    Get experiment results comparing all strategies across scenarios.
    
    Returns:
        Comparison data for all strategies across three scenarios
    """
    try:
        # Check if results file exists
        if os.path.exists(RESULTS_PATH):
            with open(RESULTS_PATH, "r") as f:
                data = json.load(f)
                return {
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
        
        # Return placeholder data
        return {
            "status": "success",
            "data": _get_placeholder_results(),
            "timestamp": datetime.now().isoformat(),
            "note": "Run experiments/run_experiments.py to generate real results"
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing results JSON: {e}")
        raise HTTPException(status_code=500, detail="Invalid results file format")
        
    except Exception as e:
        logger.error(f"Error fetching experiment results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/summary")
async def get_results_summary():
    """
    Get summary of experiment results with key findings.
    
    Returns:
        Summary statistics and key findings
    """
    try:
        # Get full results
        results_response = await get_experiment_results()
        data = results_response.get("data", {})
        
        # Extract strategies
        strategies = data.get("strategies", [])
        scenarios = data.get("scenarios", ["Normal Day", "Traffic Spike", "Low-Traffic Night"])
        
        # Calculate summary
        summary = {
            "scenarios": scenarios,
            "strategies": [],
            "best_overall": "",
            "best_cost": "",
            "best_carbon": "",
            "best_latency": ""
        }
        
        for strategy in strategies:
            name = strategy.get("name", "Unknown")
            cost_saved = strategy.get("costSaved", [0, 0, 0])
            carbon_saved = strategy.get("carbonSaved", [0, 0, 0])
            latency_penalty = strategy.get("latencyPenalty", [0, 0, 0])
            
            # Calculate averages
            avg_cost = sum(cost_saved) / len(cost_saved) if cost_saved else 0
            avg_carbon = sum(carbon_saved) / len(carbon_saved) if carbon_saved else 0
            avg_latency = sum(latency_penalty) / len(latency_penalty) if latency_penalty else 0
            
            summary["strategies"].append({
                "name": name,
                "avg_cost_saved": round(avg_cost, 2),
                "avg_carbon_saved": round(avg_carbon, 2),
                "avg_latency_penalty": round(avg_latency, 2),
                "cost_saved": cost_saved,
                "carbon_saved": carbon_saved,
                "latency_penalty": latency_penalty
            })
        
        # Determine best overall (highest combined savings)
        if summary["strategies"]:
            best = max(summary["strategies"], key=lambda x: x["avg_cost_saved"] + x["avg_carbon_saved"] - x["avg_latency_penalty"] / 100)
            summary["best_overall"] = best["name"]
            summary["best_cost"] = max(summary["strategies"], key=lambda x: x["avg_cost_saved"])["name"]
            summary["best_carbon"] = max(summary["strategies"], key=lambda x: x["avg_carbon_saved"])["name"]
            summary["best_latency"] = min(summary["strategies"], key=lambda x: x["avg_latency_penalty"])["name"]
        
        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting results summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/scenario/{scenario_name}")
async def get_scenario_results(scenario_name: str):
    """
    Get results for a specific scenario.
    
    Args:
        scenario_name: Name of the scenario (Normal Day, Traffic Spike, Low-Traffic Night)
    
    Returns:
        Results for the specified scenario
    """
    try:
        # Get full results
        results_response = await get_experiment_results()
        data = results_response.get("data", {})
        
        scenarios = data.get("scenarios", [])
        strategies = data.get("strategies", [])
        
        # Find scenario index
        try:
            scenario_index = scenarios.index(scenario_name)
        except ValueError:
            raise HTTPException(
                status_code=404, 
                detail=f"Scenario '{scenario_name}' not found. Available: {scenarios}"
            )
        
        # Extract data for this scenario
        scenario_results = []
        for strategy in strategies:
            scenario_results.append({
                "name": strategy.get("name", "Unknown"),
                "cost_saved": strategy.get("costSaved", [0, 0, 0])[scenario_index],
                "carbon_saved": strategy.get("carbonSaved", [0, 0, 0])[scenario_index],
                "latency_penalty": strategy.get("latencyPenalty", [0, 0, 0])[scenario_index]
            })
        
        return {
            "status": "success",
            "data": {
                "scenario": scenario_name,
                "results": scenario_results,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting scenario results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/results/update")
async def update_experiment_results(results_data: dict):
    """
    Update experiment results (called after running experiments).
    
    Args:
        results_data: New experiment results data
    
    Returns:
        Confirmation message
    """
    try:
        # Validate required fields
        required_fields = ["scenarios", "strategies"]
        for field in required_fields:
            if field not in results_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
        
        # Write to file
        with open(RESULTS_PATH, "w") as f:
            json.dump(results_data, f, indent=2)
        
        logger.info(f"Experiment results updated at {RESULTS_PATH}")
        
        return {
            "status": "success",
            "message": "Results updated successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating experiment results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/export")
async def export_results(
    format: str = Query("json", enum=["json", "csv"], description="Export format")
):
    """
    Export experiment results in various formats.
    
    Args:
        format: Export format (json or csv)
    
    Returns:
        Exported results
    """
    try:
        # Get full results
        results_response = await get_experiment_results()
        data = results_response.get("data", {})
        
        if format == "csv":
            # Return CSV format
            import csv
            from io import StringIO
            
            output = StringIO()
            
            # Flatten data for CSV
            rows = []
            strategies = data.get("strategies", [])
            scenarios = data.get("scenarios", ["Normal Day", "Traffic Spike", "Low-Traffic Night"])
            
            for strategy in strategies:
                name = strategy.get("name", "Unknown")
                for i, scenario in enumerate(scenarios):
                    rows.append({
                        "Strategy": name,
                        "Scenario": scenario,
                        "Cost Saved": strategy.get("costSaved", [0, 0, 0])[i],
                        "Carbon Saved": strategy.get("carbonSaved", [0, 0, 0])[i],
                        "Latency Penalty": strategy.get("latencyPenalty", [0, 0, 0])[i]
                    })
            
            if rows:
                writer = csv.DictWriter(output, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
                
                return {
                    "status": "success",
                    "format": "csv",
                    "data": output.getvalue()
                }
            else:
                return {
                    "status": "success",
                    "format": "csv",
                    "data": "No data available"
                }
        
        # Default: JSON
        return {
            "status": "success",
            "format": "json",
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_placeholder_results():
    """
    Generate placeholder results when no real results exist.
    
    Returns:
        Placeholder results data
    """
    return {
        "scenarios": ["Normal Day", "Traffic Spike", "Low-Traffic Night"],
        "strategies": [
            {
                "name": "Fixed Rule (Baseline)",
                "costSaved": [0, 0, 0],
                "carbonSaved": [0, 0, 0],
                "latencyPenalty": [0, 0, 0]
            },
            {
                "name": "Cost-First (Single Objective)",
                "costSaved": [15, 5, 20],
                "carbonSaved": [5, 2, 8],
                "latencyPenalty": [10, 25, 5]
            },
            {
                "name": "Context-Aware MO",
                "costSaved": [12, 8, 18],
                "carbonSaved": [20, 15, 25],
                "latencyPenalty": [5, 10, 3]
            }
        ],
        "note": "Run experiments/run_experiments.py to generate real results."
    }
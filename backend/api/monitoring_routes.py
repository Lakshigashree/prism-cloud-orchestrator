import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from state import app_state
from agents.monitoring_agent import (
    collect_live_metrics,
    get_monitoring_state,
    get_traffic_data,
    get_carbon_data
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/monitoring/live")
async def get_live_monitoring():
    """
    Get current live monitoring metrics.
    
    Returns:
        Current system metrics including CPU, memory, requests, latency
    """
    try:
        # Try to get fresh metrics
        metrics = collect_live_metrics()
        
        # Update app state
        app_state.latest_monitoring = metrics
        
        return {
            "status": "success",
            "data": metrics
        }
        
    except Exception as e:
        logger.error(f"Error fetching live monitoring: {e}")
        
        # Return cached data or defaults
        cached = app_state.latest_monitoring or {
            "cpu_usage": 0,
            "memory_usage": 0,
            "requests_per_second": 0,
            "latency_ms": 0,
            "carbon_intensity": 0,
            "active_nodes": 0,
            "timestamp": datetime.now().isoformat(),
            "source": "cached"
        }
        
        return {
            "status": "success",
            "data": cached,
            "warning": "Using cached data - live fetch failed"
        }


@router.get("/monitoring/state")
async def get_monitoring_state_endpoint():
    """
    Get complete monitoring state for decision agents.
    
    Returns:
        Complete system state including trend and predictions
    """
    try:
        state = get_monitoring_state()
        
        return {
            "status": "success",
            "data": state
        }
        
    except Exception as e:
        logger.error(f"Error fetching monitoring state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/history")
async def get_monitoring_history(
    limit: int = Query(100, ge=1, le=500, description="Number of history entries")
):
    """
    Get historical monitoring data for charts.
    
    Args:
        limit: Number of history entries to return
    
    Returns:
        Historical monitoring data
    """
    try:
        # Get from app state or generate sample
        history = app_state.monitoring_history or []
        
        if history:
            # Return last N entries
            limited_history = history[-limit:]
            return {
                "status": "success",
                "data": limited_history,
                "total": len(history),
                "returned": len(limited_history)
            }
        
        # Generate sample history for initial display
        from agents.traffic_simulator import generate_traffic_logs
        
        sample_history = generate_traffic_logs(count=min(limit, 100), interval_seconds=5)
        
        return {
            "status": "success",
            "data": sample_history,
            "total": len(sample_history),
            "returned": len(sample_history),
            "note": "Sample data generated - no real history available"
        }
        
    except Exception as e:
        logger.error(f"Error fetching monitoring history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/traffic")
async def get_traffic_data_endpoint(
    limit: int = Query(100, ge=10, le=500, description="Number of data points")
):
    """
    Get traffic data for live traffic chart.
    
    Args:
        limit: Number of data points to return
    
    Returns:
        Traffic data with timestamps, CPU, requests, latency
    """
    try:
        data = get_traffic_data(limit=limit)
        
        return {
            "status": "success",
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Error fetching traffic data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/traffic")
async def get_traffic_legacy(
    limit: int = Query(100, ge=10, le=500, description="Number of data points")
):
    """
    Legacy endpoint for traffic data (used by frontend).
    Redirects to /monitoring/traffic.
    """
    try:
        data = get_traffic_data(limit=limit)
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error fetching traffic data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/carbon")
async def get_carbon_endpoint():
    """
    Get current carbon intensity data.
    
    Returns:
        Current carbon intensity with region and metadata
    """
    try:
        data = get_carbon_data()
        
        return {
            "status": "success",
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Error fetching carbon data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/monitoring/update")
async def update_monitoring_data(metrics: dict):
    """
    Update monitoring data (called by background agent).
    
    Args:
        metrics: Dictionary with monitoring metrics
    
    Returns:
        Confirmation message
    """
    try:
        # Validate required fields
        required_fields = ["cpu_usage", "requests_per_second"]
        for field in required_fields:
            if field not in metrics:
                logger.warning(f"Missing optional field: {field}")
        
        # Add timestamp if not provided
        if "timestamp" not in metrics:
            metrics["timestamp"] = datetime.now().isoformat()
        
        # Update app state
        app_state.latest_monitoring = metrics
        
        # Add to history
        if not hasattr(app_state, 'monitoring_history'):
            app_state.monitoring_history = []
        
        app_state.monitoring_history.append(metrics)
        
        # Keep history at reasonable size
        if len(app_state.monitoring_history) > 1000:
            app_state.monitoring_history = app_state.monitoring_history[-500:]
        
        logger.info(f"Monitoring data updated: CPU {metrics.get('cpu_usage', 0)}%")
        
        return {
            "status": "success",
            "message": "Monitoring data updated",
            "timestamp": metrics["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"Error updating monitoring data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/monitoring/summary")
async def get_monitoring_summary():
    """
    Get summary of current monitoring state.
    
    Returns:
        Summary statistics for dashboard
    """
    try:
        metrics = app_state.latest_monitoring or {}
        
        # Calculate trend from history
        history = app_state.monitoring_history or []
        trend = "stable"
        
        if len(history) >= 5:
            recent = history[-5:]
            cpu_values = [h.get("cpu_usage", 0) for h in recent]
            avg_start = sum(cpu_values[:3]) / 3
            avg_end = sum(cpu_values[-3:]) / 3
            
            if avg_end > avg_start * 1.1:
                trend = "rising"
            elif avg_end < avg_start * 0.9:
                trend = "falling"
        
        return {
            "status": "success",
            "data": {
                "current": {
                    "cpu_usage": metrics.get("cpu_usage", 0),
                    "requests_per_second": metrics.get("requests_per_second", 0),
                    "latency_ms": metrics.get("latency_ms", 0),
                    "carbon_intensity": metrics.get("carbon_intensity", 0),
                    "active_nodes": metrics.get("active_nodes", 0)
                },
                "trend": trend,
                "history_count": len(history),
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting monitoring summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
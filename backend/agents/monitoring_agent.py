import os
import logging
from datetime import datetime
from typing import Dict, Any

import requests

from .traffic_simulator import generate_traffic_log

logger = logging.getLogger(__name__)

MONITORED_APP_URL = os.getenv("MONITORED_APP_URL", "")


def collect_live_metrics() -> Dict[str, Any]:
    """
    Collects live metrics from real app or falls back to simulator.
    
    Returns:
        Dictionary with metrics including:
            - cpu_usage: float (0-100)
            - carbon_intensity: float (gCO2/kWh)
            - requests_per_second: float
            - latency_ms: float
            - active_nodes: int
            - timestamp: str
            - source: str ("real" or "simulated")
    """
    # Try real app first
    if MONITORED_APP_URL:
        try:
            resp = requests.get(f"{MONITORED_APP_URL}/metrics", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                
                # Ensure all required fields exist
                metrics = {
                    "cpu_usage": data.get("cpu_usage", 0),
                    "carbon_intensity": data.get("carbon_intensity", 0),
                    "requests_per_second": data.get("requests_per_sec", data.get("requests_per_second", 0)),
                    "latency_ms": data.get("response_time_ms", data.get("latency_ms", 0)),
                    "active_nodes": data.get("active_nodes", 1),
                    "timestamp": datetime.now().isoformat(),
                    "source": "real"
                }
                
                logger.info(f"Real metrics collected from {MONITORED_APP_URL}")
                return metrics
                
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch real metrics: {e}")
        except Exception as e:
            logger.error(f"Error parsing metrics: {e}")
    
    # Fallback to simulator
    log = generate_traffic_log()
    log["source"] = "simulated"
    log["timestamp"] = datetime.now().isoformat()
    
    logger.info("Using simulated metrics (fallback)")
    return log


def get_monitoring_state() -> Dict[str, Any]:
    """
    Get current monitoring state in format expected by decision agents.
    
    Returns:
        Dictionary with complete system state
    """
    metrics = collect_live_metrics()
    
    return {
        "cpu_usage": metrics.get("cpu_usage", 0),
        "carbon_intensity": metrics.get("carbon_intensity", 0),
        "requests_per_second": metrics.get("requests_per_second", 0),
        "latency_ms": metrics.get("latency_ms", 0),
        "active_nodes": metrics.get("active_nodes", 1),
        "timestamp": metrics.get("timestamp", datetime.now().isoformat()),
        "source": metrics.get("source", "simulated")
    }


def get_traffic_data(limit: int = 100) -> Dict[str, Any]:
    """
    Get historical traffic data for charts.
    
    Args:
        limit: Number of data points to return
    
    Returns:
        Dictionary with timestamps, cpu, requests, latency arrays
    """
    # In production, this would query a database
    # For now, generate sample data
    
    import random
    from datetime import datetime, timedelta
    
    timestamps = []
    cpu_data = []
    requests_data = []
    latency_data = []
    
    now = datetime.now()
    
    for i in range(limit):
        t = now - timedelta(minutes=limit - i)
        timestamps.append(t.isoformat())
        
        # Generate realistic-looking data with some randomness
        base_cpu = 40 + 30 * (i / limit) + 10 * (1 if i % 20 < 10 else 0)
        cpu_data.append(round(base_cpu + random.uniform(-5, 5), 1))
        
        base_requests = 100 + 80 * (i / limit) + 20 * (1 if i % 15 < 5 else 0)
        requests_data.append(round(base_requests + random.uniform(-10, 10), 1))
        
        base_latency = 100 + 50 * (i / limit) + 30 * (1 if i % 25 < 8 else 0)
        latency_data.append(round(base_latency + random.uniform(-10, 10), 0))
    
    return {
        "timestamps": timestamps,
        "cpu": cpu_data,
        "requests": requests_data,
        "latency": latency_data
    }


def get_carbon_data() -> Dict[str, Any]:
    """
    Get current carbon intensity data.
    
    Returns:
        Dictionary with carbon intensity and related metrics
    """
    metrics = collect_live_metrics()
    
    return {
        "carbonIntensity": metrics.get("carbon_intensity", 0),
        "timestamp": metrics.get("timestamp", datetime.now().isoformat()),
        "source": metrics.get("source", "simulated"),
        "unit": "gCO2/kWh"
    }
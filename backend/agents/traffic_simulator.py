import random
import math
import time
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

_start_time = time.time()


def generate_traffic_log() -> Dict[str, Any]:
    """
    Generates a realistic traffic reading using smooth wave pattern.
    
    Simulates daily traffic cycles with:
    - Rise and fall like real user activity
    - Random variations for realism
    - All metrics correlated (high traffic = high CPU = higher latency)
    
    Returns:
        Dictionary with realistic traffic metrics
    """
    elapsed_minutes = (time.time() - _start_time) / 60
    
    # Create smooth wave pattern (oscillates 0..1 over time)
    wave = (math.sin(elapsed_minutes / 3) + 1) / 2
    
    # Add some daily cycle variation (simulate business hours)
    hour = datetime.now().hour
    if 9 <= hour <= 18:  # Business hours
        day_factor = 1.2
    elif 18 <= hour <= 22:  # Evening
        day_factor = 0.8
    else:  # Night
        day_factor = 0.3
    
    # Generate base values with wave + random noise
    base_requests = 80 + wave * 350 * day_factor
    requests_per_sec = int(base_requests + random.uniform(-20, 20))
    
    cpu_usage = round(15 + wave * 65 * day_factor + random.uniform(-5, 5), 2)
    
    # Latency increases with CPU usage (correlated)
    latency_base = 60 + (cpu_usage / 100) * 200
    response_time = round(latency_base + random.uniform(-15, 15), 2)
    
    # Carbon intensity varies with grid conditions
    carbon_intensity = round(150 + wave * 350 + random.uniform(-50, 50), 2)
    
    # Active nodes scale with traffic
    active_nodes = max(1, round(3 + wave * 8 * day_factor))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": max(0, min(100, cpu_usage)),
        "memory_usage": round(max(0, min(100, cpu_usage * 0.8 + random.uniform(-5, 5))), 2),
        "requests_per_second": max(0, requests_per_sec),
        "latency_ms": max(20, response_time),
        "carbon_intensity": max(50, carbon_intensity),
        "active_nodes": active_nodes,
        "source": "simulator"
    }


def generate_traffic_logs(count: int = 100, interval_seconds: int = 5) -> list:
    """
    Generate multiple traffic logs for historical data.
    
    Args:
        count: Number of logs to generate
        interval_seconds: Time between logs (for realistic timestamps)
    
    Returns:
        List of traffic logs
    """
    logs = []
    current_time = datetime.now()
    
    for i in range(count):
        # Generate a log
        log = generate_traffic_log()
        
        # Adjust timestamp to go backwards in time (older first)
        adjusted_time = current_time - timedelta(seconds=interval_seconds * (count - i))
        log["timestamp"] = adjusted_time.isoformat()
        
        logs.append(log)
    
    return logs


def get_current_state() -> Dict[str, Any]:
    """
    Get current state in format expected by decision agents.
    
    Returns:
        Dictionary with current system state
    """
    log = generate_traffic_log()
    
    return {
        "cpu_usage": log.get("cpu_usage", 0),
        "carbon_intensity": log.get("carbon_intensity", 0),
        "requests_per_second": log.get("requests_per_second", 0),
        "latency_ms": log.get("latency_ms", 0),
        "active_nodes": log.get("active_nodes", 1),
        "timestamp": log.get("timestamp", datetime.now().isoformat()),
        "trend": "steady",  # Will be updated by prediction agent
        "source": "simulated"
    }


def get_traffic_history(limit: int = 50) -> list:
    """
    Get historical traffic data for testing.
    
    Args:
        limit: Number of history entries to return
    
    Returns:
        List of historical traffic logs
    """
    return generate_traffic_logs(count=limit, interval_seconds=5)


# Import for timedelta
from datetime import timedelta
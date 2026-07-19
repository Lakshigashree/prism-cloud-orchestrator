import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from state import app_state

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/carbon")
async def get_carbon():
    """
    Get current carbon intensity data.
    
    Returns:
        Current carbon intensity with region and metadata
    """
    try:
        # Return latest carbon data from app state
        if app_state.latest_carbon:
            return {
                "status": "success",
                "data": app_state.latest_carbon
            }
        
        # Fallback default data
        return {
            "status": "success",
            "data": {
                "region": "IN",
                "carbonIntensity": 420.0,
                "unit": "gCO2eq/kWh",
                "timestamp": datetime.now().isoformat(),
                "source": "default"
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching carbon data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carbon/history")
async def get_carbon_history(
    limit: int = Query(24, ge=1, le=168, description="Number of hours of history")
):
    """
    Get historical carbon intensity data for charts.
    
    Args:
        limit: Number of hours of historical data to return
    
    Returns:
        Historical carbon intensity data with timestamps
    """
    try:
        # In production, this would query a database
        # For now, generate sample historical data
        
        import random
        from datetime import datetime, timedelta
        
        timestamps = []
        values = []
        
        now = datetime.now()
        
        for i in range(limit):
            t = now - timedelta(hours=limit - i)
            timestamps.append(t.isoformat())
            
            # Generate realistic carbon values with daily pattern
            hour = t.hour
            # Higher carbon during peak hours, lower at night
            base = 350 + 100 * (1 if 8 <= hour <= 20 else 0)
            values.append(round(base + random.uniform(-50, 50), 1))
        
        return {
            "status": "success",
            "data": {
                "timestamps": timestamps,
                "values": values,
                "unit": "gCO2eq/kWh",
                "region": "IN"
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching carbon history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carbon/regions")
async def get_carbon_regions():
    """
    Get available regions with their carbon intensities.
    
    Returns:
        List of regions with carbon intensity data
    """
    try:
        # In production, this would come from a database or API
        regions = [
            {"region": "IN", "name": "India", "carbonIntensity": 420},
            {"region": "US-EAST", "name": "US East", "carbonIntensity": 380},
            {"region": "US-WEST", "name": "US West", "carbonIntensity": 250},
            {"region": "EU", "name": "Europe", "carbonIntensity": 180},
            {"region": "APAC", "name": "Asia Pacific", "carbonIntensity": 450},
            {"region": "LATAM", "name": "Latin America", "carbonIntensity": 200}
        ]
        
        return {
            "status": "success",
            "data": regions
        }
        
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/carbon/update")
async def update_carbon_data(carbon_data: dict):
    """
    Update current carbon data (called by monitoring agent).
    
    Args:
        carbon_data: Dictionary with carbon intensity data
    
    Returns:
        Confirmation message
    """
    try:
        # Validate data
        if not carbon_data.get("carbonIntensity"):
            raise HTTPException(
                status_code=400, 
                detail="Missing required field: carbonIntensity"
            )
        
        # Update app state
        app_state.latest_carbon = {
            "region": carbon_data.get("region", "IN"),
            "carbonIntensity": carbon_data["carbonIntensity"],
            "unit": carbon_data.get("unit", "gCO2eq/kWh"),
            "timestamp": datetime.now().isoformat(),
            "source": carbon_data.get("source", "api_update")
        }
        
        logger.info(f"Carbon data updated: {app_state.latest_carbon['carbonIntensity']} gCO2eq/kWh")
        
        return {
            "status": "success",
            "message": "Carbon data updated successfully",
            "data": app_state.latest_carbon
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating carbon data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carbon/forecast")
async def get_carbon_forecast(
    hours: int = Query(6, ge=1, le=24, description="Forecast horizon in hours")
):
    """
    Get carbon intensity forecast (future predictions).
    
    Args:
        hours: Number of hours to forecast
    
    Returns:
        Carbon intensity forecast
    """
    try:
        # In production, this would use a forecasting model
        # For now, generate forecast based on historical patterns
        
        import random
        from datetime import datetime, timedelta
        
        timestamps = []
        values = []
        
        now = datetime.now()
        
        for i in range(hours):
            t = now + timedelta(hours=i + 1)
            timestamps.append(t.isoformat())
            
            # Simple forecast based on time of day
            hour = t.hour
            base = 350 + 100 * (1 if 8 <= hour <= 20 else 0)
            values.append(round(base + random.uniform(-30, 30), 1))
        
        return {
            "status": "success",
            "data": {
                "timestamps": timestamps,
                "values": values,
                "unit": "gCO2eq/kWh",
                "region": app_state.latest_carbon.get("region", "IN") if app_state.latest_carbon else "IN"
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching carbon forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))
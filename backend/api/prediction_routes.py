import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from state import app_state
from agents.prediction_agent import predict_traffic, get_prediction_summary
from agents.monitoring_agent import get_monitoring_state

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/prediction")
async def get_prediction(
    horizon: int = Query(6, ge=1, le=24, description="Number of steps to forecast (5-min steps)")
):
    """
    Get traffic prediction for the next N steps.
    
    Args:
        horizon: Number of 5-minute steps to forecast (default: 6 = 30 minutes)
    
    Returns:
        Prediction data with historical and future values
    """
    try:
        # Get monitoring history
        history = app_state.monitoring_history or []
        
        if not history:
            # Return warm-up response
            return {
                "status": "success",
                "data": {
                    "horizon_minutes": horizon * 5,
                    "steps": horizon,
                    "predicted_traffic": [],
                    "trend": "steady",
                    "method": "waiting",
                    "historical_values": [],
                    "historical_timestamps": [],
                    "future_timestamps": [],
                    "current_value": 0,
                    "timestamp": datetime.now().isoformat(),
                    "note": "Collecting data for prediction..."
                }
            }
        
        # Get prediction
        prediction = predict_traffic(history, horizon=horizon)
        
        # Store latest prediction
        app_state.latest_prediction = prediction
        
        return {
            "status": "success",
            "data": prediction
        }
        
    except Exception as e:
        logger.error(f"Error getting prediction: {e}")
        
        # Return cached or default
        cached = app_state.latest_prediction or {
            "horizon_minutes": horizon * 5,
            "steps": horizon,
            "predicted_traffic": [],
            "trend": "steady",
            "method": "error",
            "historical_values": [],
            "historical_timestamps": [],
            "future_timestamps": [],
            "current_value": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "data": cached,
            "warning": "Using cached prediction - error occurred"
        }


@router.get("/prediction/summary")
async def get_prediction_summary_endpoint(
    horizon: int = Query(6, ge=1, le=24, description="Number of steps to forecast")
):
    """
    Get summarized prediction for dashboard display.
    
    Args:
        horizon: Number of 5-minute steps to forecast
    
    Returns:
        Prediction summary with current, predicted, and peak values
    """
    try:
        # Get monitoring history
        history = app_state.monitoring_history or []
        
        if not history:
            return {
                "status": "success",
                "data": {
                    "current": 0,
                    "predicted": [],
                    "trend": "steady",
                    "method": "waiting",
                    "next_value": 0,
                    "peak_value": 0,
                    "peak_time": None,
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        # Get prediction summary
        summary = get_prediction_summary(history, horizon=horizon)
        
        return {
            "status": "success",
            "data": summary
        }
        
    except Exception as e:
        logger.error(f"Error getting prediction summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prediction/history")
async def get_prediction_history(
    limit: int = Query(50, ge=1, le=200, description="Number of historical predictions")
):
    """
    Get historical predictions for accuracy tracking.
    
    Args:
        limit: Number of historical predictions to return
    
    Returns:
        Historical predictions with actual values for comparison
    """
    try:
        # In production, this would come from a database
        # For now, return sample data
        from datetime import datetime, timedelta
        import random
        
        predictions = []
        now = datetime.now()
        
        for i in range(limit):
            t = now - timedelta(minutes=5 * i)
            predictions.append({
                "timestamp": t.isoformat(),
                "predicted": round(150 + random.uniform(-30, 30), 1),
                "actual": round(145 + random.uniform(-35, 35), 1),
                "error": round(random.uniform(-10, 10), 1)
            })
        
        return {
            "status": "success",
            "data": predictions,
            "total": len(predictions)
        }
        
    except Exception as e:
        logger.error(f"Error getting prediction history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prediction/accuracy")
async def get_prediction_accuracy():
    """
    Get prediction accuracy metrics.
    
    Returns:
        Accuracy metrics including MAE, RMSE, and trend accuracy
    """
    try:
        # In production, this would be calculated from historical data
        # For now, return sample metrics
        return {
            "status": "success",
            "data": {
                "mae": 12.5,  # Mean Absolute Error
                "rmse": 18.3,  # Root Mean Square Error
                "trend_accuracy": 78.5,  # Percentage of correct trend predictions
                "samples": 156,
                "last_updated": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting prediction accuracy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prediction/update")
async def update_prediction_data(prediction_data: dict):
    """
    Update prediction data (called by background agent).
    
    Args:
        prediction_data: Dictionary with prediction data
    
    Returns:
        Confirmation message
    """
    try:
        # Validate required fields
        if "predicted_traffic" not in prediction_data:
            raise HTTPException(
                status_code=400,
                detail="Missing required field: predicted_traffic"
            )
        
        # Add timestamp if not provided
        if "timestamp" not in prediction_data:
            prediction_data["timestamp"] = datetime.now().isoformat()
        
        # Update app state
        app_state.latest_prediction = prediction_data
        
        logger.info(f"Prediction updated: {len(prediction_data.get('predicted_traffic', []))} steps")
        
        return {
            "status": "success",
            "message": "Prediction updated successfully",
            "timestamp": prediction_data["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
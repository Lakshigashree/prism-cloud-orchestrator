"""
audit_routes.py - API Routes for Audit History
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from database.db_connection import get_audit_entries, get_audit_stats, clear_audit_table

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/audit/history")
async def get_audit_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    strategy: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    try:
        start_datetime = None
        end_datetime = None
        
        if start_date:
            start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        entries = get_audit_entries(
            limit=limit,
            offset=offset,
            strategy=strategy,
            start_date=start_datetime,
            end_date=end_datetime
        )
        
        return {
            "status": "success",
            "data": {
                "entries": entries,
                "total": len(entries),
                "returned": len(entries),
                "has_more": len(entries) >= limit
            }
        }
        
    except Exception as e:
        logger.error(f"Error fetching audit history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audit/stats")
async def get_audit_statistics():
    try:
        stats = get_audit_stats()
        
        return {
            "status": "success",
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"Error fetching audit stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
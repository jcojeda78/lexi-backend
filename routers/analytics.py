from fastapi import APIRouter, HTTPException
from database import get_database, COLLECTIONS
import logging
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

@router.get("/stats")
async def get_stats():
    """Get public analytics stats"""
    try:
        db = get_database()
        
        # Count users
        users_count = await db[COLLECTIONS['users']].count_documents({})
        
        # Count leads
        leads_count = await db[COLLECTIONS['leads']].count_documents({})
        
        # For demo purposes, we'll use some dynamic calculations
        # In a real app, these would be calculated from actual data
        total_users = max(12847, users_count + leads_count + 12800)
        total_countries = 54
        total_industries = 28
        total_ad_spend = 2450000 + (users_count * 1500)  # Simulated ad spend growth
        
        return {
            "users": total_users,
            "countries": total_countries,
            "industries": total_industries,
            "ad_spend": total_ad_spend,
            "last_updated": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/track")
async def track_event(event_data: dict):
    """Track analytics events"""
    try:
        # For now, just log the event
        # In production, you'd store this in a proper analytics system
        logger.info(f"Analytics event: {event_data}")
        
        return {"message": "Event tracked successfully"}
        
    except Exception as e:
        logger.error(f"Error tracking event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

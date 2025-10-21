from fastapi import APIRouter, HTTPException, Request
from models.lead import Lead, LeadCreate, LeadResponse
from database import get_database, COLLECTIONS
from typing import List
from datetime import datetime
import logging

router = APIRouter(prefix="/leads", tags=["Leads"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=dict)
async def create_lead(lead_data: LeadCreate, request: Request):
    """Create a new lead from trial signup"""
    try:
        db = get_database()
        leads_collection = db[COLLECTIONS['leads']]
        
        # Check if lead already exists with same email
        existing_lead = await leads_collection.find_one({"email": lead_data.email})
        if existing_lead:
            # Update existing lead with new information
            update_data = {k: v for k, v in lead_data.dict().items() if v is not None}
            update_data["updated_at"] = datetime.utcnow()
            
            await leads_collection.update_one(
                {"email": lead_data.email},
                {"$set": update_data}
            )
            
            return {
                "message": "Lead information updated successfully",
                "lead_id": existing_lead["id"]
            }
        
        # Extract UTM parameters from request if available
        utm_params = {}
        for param in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']:
            value = request.query_params.get(param)
            if value:
                utm_params[param] = value
        
        # Create new lead with UTM data
        lead_data_dict = lead_data.dict()
        lead_data_dict['utm'] = utm_params
        
        lead = Lead(**lead_data_dict)
        
        # Insert to database
        lead_dict = lead.dict() if hasattr(lead, 'dict') else lead.model_dump()
        await leads_collection.insert_one(lead_dict)
        
        logger.info(f"New lead created: {lead.email} from {lead.source}")
        
        return {
            "message": "Lead created successfully",
            "lead_id": lead.id
        }
        
    except Exception as e:
        logger.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[LeadResponse])
async def get_leads():
    """Get all leads (admin endpoint)"""
    try:
        db = get_database()
        leads_collection = db[COLLECTIONS['leads']]
        
        cursor = leads_collection.find({}).sort("created_at", -1).limit(100)
        
        leads = []
        async for doc in cursor:
            leads.append(LeadResponse(**doc))
        
        return leads
        
    except Exception as e:
        logger.error(f"Error fetching leads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

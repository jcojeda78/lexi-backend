from fastapi import APIRouter, HTTPException
from models.contact import Contact, ContactCreate, ContactResponse
from database import get_database, COLLECTIONS
from typing import List
import logging

router = APIRouter(prefix="/contact", tags=["Contact"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=dict)
async def create_contact(contact_data: ContactCreate):
    """Create a new contact message"""
    try:
        db = get_database()
        contacts_collection = db[COLLECTIONS['contacts']]
        
        # Create new contact
        contact = Contact(**contact_data.dict())
        
        # Insert to database
        contact_dict = contact.dict()
        await contacts_collection.insert_one(contact_dict)
        
        logger.info(f"New contact message from: {contact.email}")
        
        return {
            "message": "Contact message sent successfully",
            "contact_id": contact.id
        }
        
    except Exception as e:
        logger.error(f"Error creating contact message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[ContactResponse])
async def get_contacts():
    """Get all contact messages (admin endpoint)"""
    try:
        db = get_database()
        contacts_collection = db[COLLECTIONS['contacts']]
        
        cursor = contacts_collection.find({}).sort("created_at", -1).limit(100)
        
        contacts = []
        async for doc in cursor:
            contacts.append(ContactResponse(**doc))
        
        return contacts
        
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

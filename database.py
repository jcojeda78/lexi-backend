from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = MongoDB()

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.environ.get('MONGO_URL')
    db_name = os.environ.get('DB_NAME', 'lexi_db')
    
    if not mongo_url:
        raise Exception("MONGO_URL environment variable is not set")
    
    try:
        db.client = AsyncIOMotorClient(mongo_url)
        db.database = db.client[db_name]
        
        # Test the connection
        await db.client.admin.command('ping')
        logger.info(f"Connected to MongoDB database: {db_name}")
        
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("Disconnected from MongoDB")

def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if db.database is None:
        raise Exception("Database not initialized")
    return db.database

# Collection names
COLLECTIONS = {
    'users': 'users',
    'leads': 'leads',
    'testimonials': 'testimonials',
    'faqs': 'faqs',
    'contacts': 'contacts',
    'analytics': 'analytics',
}




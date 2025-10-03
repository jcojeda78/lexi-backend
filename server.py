from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from database import connect_to_mongo, close_mongo_connection
from services.data_service import DataService

# Import routes
from routes.auth import router as auth_router
from routes.leads import router as leads_router
from routes.content import router as content_router
from routes.contact import router as contact_router
from routes.analytics import router as analytics_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Lexi API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Lexi API is running", "status": "healthy"}

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(leads_router)
api_router.include_router(content_router)
api_router.include_router(contact_router)
api_router.include_router(analytics_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection and seed data"""
    try:
        await connect_to_mongo()
        await DataService.seed_initial_data()
        logger.info("Database initialized and seeded successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    await close_mongo_connection()

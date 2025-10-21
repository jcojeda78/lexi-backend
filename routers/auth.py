from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from models.user import User, UserCreate, UserLogin, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_user
from database import get_database, COLLECTIONS
from datetime import datetime, timedelta
import logging

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        db = get_database()
        users_collection = db[COLLECTIONS['users']]
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        
        # Set trial end date (7 days from now)
        trial_ends_at = datetime.utcnow() + timedelta(days=7)
        
        user = User(
            **user_data.dict(exclude={"password"}),
            password=hashed_password,
            trial_ends_at=trial_ends_at
        )
        
        # Insert user to database
        user_dict = user.dict()
        await users_collection.insert_one(user_dict)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(**user.dict())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login user"""
    try:
        db = get_database()
        users_collection = db[COLLECTIONS['users']]
        
        # Find user by email
        user_doc = await users_collection.find_one({"email": credentials.email})
        if not user_doc:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(credentials.password, user_doc['password']):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = User(**user_doc)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(**user.dict())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    try:
        db = get_database()
        users_collection = db[COLLECTIONS['users']]
        
        user_doc = await users_collection.find_one({"id": current_user["user_id"]})
        if not user_doc:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = User(**user_doc)
        return UserResponse(**user.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}

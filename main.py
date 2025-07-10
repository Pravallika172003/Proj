from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, Response
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables early
load_dotenv()

# Import routers
from backend.routes import auth_router, shipment_router, device_router, admin_router
from backend.database import users_collection

# Initialize FastAPI app
app = FastAPI(
    title="SCM Xpert Lite API",
    description="API for Supply Chain Management Xpert Lite application.",
    version="0.1.0",
)

# Configure CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Mount frontend static files (your HTML, JS, CSS)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Optional: serve a default favicon to avoid 404 error
@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon")

# Root redirect to login page
@app.get("/")
def root():
    return RedirectResponse("/frontend/login.html")

# Include all routers with prefixes
app.include_router(auth_router, prefix="/auth")
app.include_router(shipment_router, prefix="/shipments")
app.include_router(device_router, prefix="/device")
app.include_router(admin_router, prefix="/admin")

# 🔓 Unsafe user list (public, unauthenticated — for testing only!)
@app.get("/users")
async def get_all_public_users_data():
    """
    WARNING: This endpoint exposes user data without auth!
    DO NOT USE IN PRODUCTION. Use only for testing.
    """
    try:
        users = list(users_collection.find({}, {"password": 0}))
        for user in users:
            user["_id"] = str(user["_id"])
            if isinstance(user.get("created_at"), datetime):
                user["created_at"] = user["created_at"].isoformat()
        return {"users": users}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve public user data: {str(e)}"
        )

from fastapi import APIRouter

from app.routes.freelancer import freelancer_router
from app.routes.cro import cro_router

# Create the main API router
api_router = APIRouter()

# Include routers from different modules with versioning and tags
api_router.include_router(
    freelancer_router,
    prefix="/freelancers",  # Prefix to namespace the routes
    tags=["freelancers"],  # Tags for API documentation
    responses={404: {"description": "Not found"}},  # Default response for 404 errors
)

api_router.include_router(
    cro_router,
    prefix="/cros",  # Prefix to namespace the routes
    tags=["cros"],  # Tags for API documentation
    responses={404: {"description": "Not found"}},  # Default response for 404 errors
)



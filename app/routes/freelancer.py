import json
from fastapi import APIRouter, HTTPException
from app.schema.schema import FreelancerQuery
from app.controllers.freelancer import get_freelancer_response
freelancer_router = APIRouter()

# Define the input schema


@freelancer_router.get("/")
def get_freelancers(query: str):
    try:
        # Call the controller function which handles business logic
        reply = get_freelancer_response(query)
        return {"reply": json.loads(reply)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import json
from fastapi import APIRouter, HTTPException
from app.schema.schema import FreelancerQuery
from app.controllers.cro import get_cro_response
cro_router = APIRouter()

# Define the input schema


@cro_router.get("/")
def get_cro(query: str):
    try:
        # Call the controller function which handles business logic
        reply = get_cro_response(query)
        return {"reply": json.loads(reply)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
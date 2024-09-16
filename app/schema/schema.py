from pydantic import BaseModel

class FreelancerQuery(BaseModel):
    query: str
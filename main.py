import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.route import api_router

# Initialize FastAPI app
app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


# Configure CORS
origins = ["*"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define ping endpoint
@app.get("/api/v1/ping")
async def ping():
    return "pong"


# Run the FastAPI app using Uvicorn server
#if __name__ == "__main__":
    #uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)

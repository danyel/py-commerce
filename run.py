from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.routes import router  # Import your routes module, assuming you have defined routes in app/routes.py
import uvicorn

app = FastAPI()  # Create an instance of the FastAPI application

# Include your routers here
app.include_router(router)

# Define a root endpoint (optional, for testing)
@app.get("/")
async def read_root():
    return {"message": "Welcome to my API!"}

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1337)
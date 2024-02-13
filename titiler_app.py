import uvicorn
from fastapi import FastAPI
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.core.factory import TilerFactory

app = FastAPI()

# Create a TilerFactory
endpoints = TilerFactory()

# Register the endpoints
app.include_router(endpoints.router, tags=["Cloud Optimized GeoTIFF"])
add_exception_handlers(app, DEFAULT_STATUS_CODES)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")

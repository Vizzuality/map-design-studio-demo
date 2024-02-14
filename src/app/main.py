import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from tipg.collections import register_collection_catalog
from tipg.database import close_db_connection, connect_to_db
from tipg.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from tipg.factory import OGCTilesFactory
from tipg.settings import PostgresSettings

# from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.core.factory import TilerFactory

from app.routes import router

# Load the environment variables from the .env file
load_dotenv()


# Connect to the Postgres database
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan

    - Create DB connection POOL and `register` the custom tipg SQL function within `pg_temp`
    - Create the collection_catalog
    - Close the connection pool when closing the application

    """
    await connect_to_db(
        app,
        settings=PostgresSettings(database_url=os.environ.get("DATABASE_URL")),
        schemas=["public"],
    )
    await register_collection_catalog(app, schemas=["public"])

    yield

    await close_db_connection(app)


app = FastAPI(name="Design Studio", lifespan=lifespan)

# Add main router
app.include_router(router, tags=["Design Studio API"])

# Create a TilerFactory
raster_tiler = TilerFactory(router_prefix="/tiler/cog")
app.include_router(raster_tiler.router, tags=["TiTiler Raster Tiles Server"], prefix="/tiler/cog")

# Create a TiPgFactory
vector_tiler = OGCTilesFactory(
    with_common=False,
    with_viewer=False,
    router_prefix="/tiler/features",
)
app.include_router(vector_tiler.router, tags=["TiPG Vector Tiles Server"], prefix="/tiler/features")

# Add exception handlers
add_exception_handlers(app, DEFAULT_STATUS_CODES)

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")
# python -m uvicorn app.main:app

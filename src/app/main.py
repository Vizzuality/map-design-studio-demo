import os
from contextlib import asynccontextmanager

import jinja2
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette_cramjam.middleware import CompressionMiddleware
from tipg.collections import register_collection_catalog
from tipg.database import close_db_connection, connect_to_db
from tipg.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from tipg.factory import OGCTilesFactory
from tipg.middleware import CacheControlMiddleware, CatalogUpdateMiddleware
from tipg.settings import CustomSQLSettings, DatabaseSettings, PostgresSettings
from titiler.core.factory import TilerFactory

from app.routes import router

# Load the environment variables from the .env file
load_dotenv()

# Create a PostgresSettings object
postgres_settings = PostgresSettings(database_url=os.environ.get("DATABASE_URL"))
db_settings = DatabaseSettings()
custom_sql_settings = CustomSQLSettings()


# Connect to the Postgres database
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#    """FastAPI Lifespan
#    - Create DB connection POOL and `register` the custom tipg SQL function within `pg_temp`
#    - Create the collection_catalog
#    - Close the connection pool when closing the application
#    """
#    await connect_to_db(
#        app,
#        settings=postgres_settings,
#        schemas=["public"],
#    )
#    await register_collection_catalog(app, schemas=["public"])
#    yield
#    await close_db_connection(app)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan."""
    # Create Connection Pool
    await connect_to_db(
        app,
        settings=postgres_settings,
        schemas=db_settings.schemas,
        user_sql_files=custom_sql_settings.sql_files,
    )

    # Register Collection Catalog
    await register_collection_catalog(
        app,
        schemas=db_settings.schemas,
        tables=db_settings.tables,
        exclude_tables=db_settings.exclude_tables,
        exclude_table_schemas=db_settings.exclude_table_schemas,
        functions=db_settings.functions,
        exclude_functions=db_settings.exclude_functions,
        exclude_function_schemas=db_settings.exclude_function_schemas,
        spatial=db_settings.only_spatial_tables,
    )

    yield

    # Close the Connection Pool
    await close_db_connection(app)


app = FastAPI(name="Design Studio", lifespan=lifespan)

# Add main router
app.include_router(router, tags=["Design Studio API"])

# Create a TilerFactory
raster_tiler = TilerFactory()
app.include_router(raster_tiler.router, tags=["TiTiler Raster Tiles Server"])

# Create a TiPgFactory
templates = Jinja2Templates(
    directory="directoy",  # we need to set a dummy directory variable, see https://github.com/encode/starlette/issues/1214
    loader=jinja2.ChoiceLoader([jinja2.PackageLoader("tipg", "templates")]),
)  # type: ignore

vector_tiler = OGCTilesFactory(
    templates=templates,
    with_common=True,
    with_viewer=True,
)
app.include_router(vector_tiler.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.add_middleware(CacheControlMiddleware, cachecontrol="public, max-age=3600")
app.add_middleware(CompressionMiddleware)
app.add_middleware(
    CatalogUpdateMiddleware,
    func=register_collection_catalog,
    ttl=300,
    schemas=db_settings.schemas,
    tables=db_settings.tables,
    exclude_tables=db_settings.exclude_tables,
    exclude_table_schemas=db_settings.exclude_table_schemas,
    functions=db_settings.functions,
    exclude_functions=db_settings.exclude_functions,
    exclude_function_schemas=db_settings.exclude_function_schemas,
    spatial=db_settings.only_spatial_tables,
)

add_exception_handlers(app, DEFAULT_STATUS_CODES)

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")
# python -m uvicorn app.main:app

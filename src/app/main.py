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
# database_url=f'postgresql://{os.environ.get("POSTGRES_USERNAME")}:{os.environ.get("POSTGRES_PASSWORD")}@localhost:5433/postgis',
postgres_settings = PostgresSettings(
    user=os.environ.get("POSTGRES_USERNAME"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    database="postgis",
    host="postgresql",
    port=5433,
)
db_settings = DatabaseSettings()
custom_sql_settings = CustomSQLSettings()


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

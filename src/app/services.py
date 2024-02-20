import os

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel

# Load the environment variables from the .env file
load_dotenv()

API_BASE_URL = os.environ.get("API_BASE_URL")


class RasterTile(BaseModel):
    """
    Represents the information of a raster tile.
    """

    url: str


class VectorTile(BaseModel):
    """
    Represents the information of a vector tile.
    """

    url: str
    layer_name: str


class TileParams(BaseModel):
    """
    Represents the parameters of a tile.
    """

    url: str
    bidx: str
    colormap: str


async def get_titiler_api_response(params: TileParams) -> RasterTile:
    """
    Get raster tiles
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/tilejson.json", params=params.model_dump())
        tile_json = response.json()

    raster_tile = RasterTile(url=tile_json["tiles"][0])

    return raster_tile


async def get_tipg_api_response(collection: str) -> VectorTile:
    """
    Get raster tiles
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/collections/{collection}/tilejson.json")
        tile_json = response.json()

    vector_tile = VectorTile(
        url=tile_json["tiles"][0], layer_name=tile_json.get("vector_layers")[0].get("id")
    )

    return vector_tile

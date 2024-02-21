import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status
from starlette.responses import RedirectResponse

from app.services import get_tipg_api_response, get_titiler_api_response

router = APIRouter()


class RasterData(BaseModel):
    """
    Represents the data of a raster layer.
    """

    id: int
    styles: dict


class VectorData(BaseModel):
    """
    Represents the data of a vector layer.
    """

    id: int


class TileParams(BaseModel):
    """
    Represents the parameters of a tile.
    """

    url: str
    bidx: str
    colormap: str


class RasterLayerInfo(BaseModel):
    """
    Represents the information of a raster layer.
    """

    url: str
    info: dict


class VectorLayerInfo(BaseModel):
    """
    Represents the information of a vector layer.
    """

    url: str
    layer_name: str
    info: dict


@router.get("/layers")
async def get_layer_list(request: Request):
    """
    Get the list of layers.
    """
    async with request.app.state.pool.acquire() as conn:
        response_body = await conn.fetch("SELECT * FROM public.layers")

    return JSONResponse(content=jsonable_encoder(response_body))


@router.get("/raster_tiles")
async def get_raster_tiles(raster_data: RasterData, request: Request):
    """
    Get the raster tiles url from the layer.
    """
    async with request.app.state.pool.acquire() as conn:
        record = await conn.fetchrow("SELECT * FROM public.layers WHERE id = $1", raster_data.id)

    if not record:
        raise HTTPException(status_code=404, detail="Layer not found")

    # Get the raster layer info
    layer_info = dict(record)

    # Get raster layer tiles
    tile_params = TileParams(
        url=layer_info["url"], bidx="1", colormap=json.dumps(raster_data.styles)
    )
    raster_tile = await get_titiler_api_response(tile_params)

    raster_layer_info = RasterLayerInfo(**{**raster_tile.model_dump(), "info": layer_info})

    return raster_layer_info.model_dump()


@router.get("/vector_tiles")
async def get_vector_tiles(vector_data: VectorData, request: Request):
    """
    Get the vector tiles url from the layer.
    """
    async with request.app.state.pool.acquire() as conn:
        record = await conn.fetchrow("SELECT * FROM public.layers WHERE id = $1", vector_data.id)

    if not record:
        raise HTTPException(status_code=404, detail="Layer not found")

    # Get the raster layer info
    layer_info = dict(record)

    # Get vector layer tiles
    vector_tile = await get_tipg_api_response(collection=layer_info["collection"])

    vector_layer_info = VectorLayerInfo(**{**vector_tile.model_dump(), "info": layer_info})

    return vector_layer_info.model_dump()


@router.get("/")
def root_redirect():
    """Landing page"""
    return RedirectResponse("/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)

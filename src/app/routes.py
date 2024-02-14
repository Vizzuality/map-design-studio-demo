from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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


@router.get("/layers")
async def get_layer_list(request: Request):
    """
    Get the list of layers.
    """
    async with request.app.state.pool.acquire() as conn:
        response_body = await conn.fetch("SELECT * FROM public.layers")
    return JSONResponse(content=jsonable_encoder(response_body))


@router.get("/raster_tiles")
async def get_raster_tiles(raster_data: RasterData):
    """
    Get the raster tiles url from the layer.
    """
    raster_layer_info = await get_titiler_api_response(raster_data)
    return raster_layer_info.model_dump()


@router.get("/vector_tiles")
async def get_vector_tiles(vector_data: VectorData):
    """
    Get the vector tiles url from the layer.
    """
    vector_layer_info = await get_tipg_api_response(vector_data)
    return vector_layer_info.model_dump()

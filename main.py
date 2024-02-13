import sys

# Add the 'studio' directory to the Python path
sys.path.append("src/studio")

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from src.services import get_tipg_api_response, get_titiler_api_response

app = FastAPI()


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


@app.get("/raster_tiles")
async def get_raster_tiles(raster_data: RasterData):
    """
    Get the raster tiles url from the layer.
    """
    raster_layer_info = await get_titiler_api_response(raster_data)
    return raster_layer_info.model_dump()


@app.get("/vector_tiles")
async def get_vector_tiles(vector_data: VectorData):
    """
    Get the vector tiles url from the layer.
    """
    vector_layer_info = await get_tipg_api_response(vector_data)
    return vector_layer_info.model_dump()


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8088, log_level="info")

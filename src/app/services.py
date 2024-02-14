from pydantic import BaseModel

from app.studio.layers import Layer


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


async def get_titiler_api_response(data) -> RasterLayerInfo:
    """
    Get the raster tiles url from the layer.

    Args:
        id: The ID of the layer.
        styles: The styles of the layer.
        opacity: The opacity of the layer.

    Returns:
        str: The url of the tiles.
    """
    # Create a Layer object.
    layer = Layer(data.id, data.styles)
    # Get the tile json from the layer.
    try:
        tile_json = layer.get_tile_json()
    except Exception as e:
        return {"error": str(e)}

    # Get the url of the tiles.
    url = tile_json["tiles"][0]

    raster_layer_info = RasterLayerInfo(url=url, info=layer.info)

    return raster_layer_info


async def get_tipg_api_response(data) -> VectorLayerInfo:
    """
    Get the vector tiles url from the layer.

    Args:
        id: The ID of the layer.

    Returns:
        str: The url of the tiles.
    """
    # Create a Layer object.
    layer = Layer(data.id)
    # Get the tile json from the layer.
    try:
        tile_json = layer.get_tile_json()
    except Exception as e:
        return {"error": str(e)}

    # Get the url of the tiles.
    url = tile_json["tiles"][0]
    # Get vector layer name.
    layer_name = tile_json.get("vector_layers")[0].get("id")

    vector_layer_info = VectorLayerInfo(url=url, layer_name=layer_name, info=layer.info)

    return vector_layer_info

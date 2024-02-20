import json
import os

import httpx
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the service endpoint from the environment variables
service_endpoint = os.environ.get("API_BASE_URL")


class _TileSystem:
    def __init__(self):
        self._tile_types = {
            "raster": RasterTile,
            "vector": VectorTile,
        }

    def get_tile_type(self, type_id):
        tile_type = self._tile_types.get(type_id)
        if not type:
            raise ValueError("invalid type_name")
        return tile_type()


class RasterTile:
    """
    This class is responsible for getting tiles from a raster layer.
    """

    def get_tile_json(self, layer_info):
        """
        Get tiles from a raster layer.

        Args:
            layer: The raster layer.

        Returns:
            The tiles obtained from the raster layer.
        """
        url = layer_info["url"]
        styles = layer_info["styles"]

        try:
            r = httpx.get(
                f"{service_endpoint}/tilejson.json",
                params={
                    "url": url,
                    "bidx": "1",
                    "colormap": json.dumps(styles),
                },
            ).json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return r


class VectorTile:
    """
    This class is responsible for getting tiles from a vector layer.
    """

    def get_tile_json(self, layer_info):
        """
        Get tiles from a vector layer.

        Args:
            layer: The vector layer.

        Returns:
            The tiles obtained from the vector layer.
        """
        collection = layer_info["collection"]
        try:
            r = httpx.get(f"{service_endpoint}/collections/{collection}/tilejson.json").json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return r


_tile_system = _TileSystem()


def get_tile_type(type_id):
    """
    Get the tile type based on the given type ID.

    Args:
        type_id: The ID of the tile type.

    Returns:
        The tile type object.
    """
    return _tile_system.get_tile_type(type_id)

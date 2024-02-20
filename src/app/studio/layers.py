import os

import httpx
from dotenv import load_dotenv

from app.studio.tiles import get_tile_type

# Load the environment variables from the .env file
load_dotenv()

# Get the service endpoint from the environment variables
service_endpoint = os.environ.get("API_BASE_URL")


class _LayerDatabase:
    def __init__(self):
        try:
            response_body = httpx.get(
                f"{service_endpoint}/layers",
            ).json()

            self._layers = {
                item["id"]: {key: value for key, value in item.items() if key != "id"}
                for item in response_body
            }
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_layer_info(self, layer_id):
        info = self._layers.get(layer_id)
        if not info:
            raise ValueError("invalid layer_id")
        return info


class Layer:
    """
    Represents a layer in the map design studio.
    """

    def __init__(self, id, styles=None, opacity=1):
        """
        Initialize a Layer object.

        Args:
            id (int): The ID of the layer.

        """
        self.id = id
        self.styles = styles
        self.opacity = opacity
        self.info = layer_database.get_layer_info(self.id)
        self.info["styles"] = self.styles
        self.name = self.info["name"]
        self._tile_type = get_tile_type(self.info["type"])

    def get_tile_json(self):
        """
        Get tiles from the layer.
        """
        return self._tile_type.get_tile_json(self.info)


layer_database = _LayerDatabase()

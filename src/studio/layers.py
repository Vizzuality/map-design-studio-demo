from tiles import get_tile_type


class _LayerDatabase:
    def __init__(self):
        self._layers = {
            1: {
                "name": "Landscape Capital Index",
                "type": "raster",
                "colormap_type": "continuous",
                "path": "../data/raw/raster_data/final_lci.tif",
            },
            2: {
                "name": "Land Cover",
                "type": "raster",
                "colormap_type": "categorical",
                "path": "../data/raw/raster_data/land_cover.tif",
            },
            3: {
                "name": "Country Boundaries",
                "type": "vector",
                "colormap_type": "categorical",
                "collection": "public.countries",
            },
        }

    def get_layer_info(self, layer_id):
        info = self._layers.get(layer_id)
        if not info:
            raise ValueError("invalid employee_id")
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

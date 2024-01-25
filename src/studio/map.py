import folium
from folium.plugins import VectorGridProtobuf
from layers import Layer


class FoliumMap(folium.Map):
    """
    A custom Map class that can display Google Earth Engine tiles.

    Inherits from folium.Map class.
    """

    def __init__(self, center: tuple[float] = (25.0, 55.0), zoom: int = 3, **kwargs):
        """
        Constructor for MapGEE class.

        Parameters:
        center: list, default [25.0, 55.0]
            The current center of the map.
        zoom: int, default 3
            The current zoom value of the map.
        **kwargs: Additional arguments that are passed to the parent constructor.
        """
        self.center = list(center)
        self.zoom = zoom
        self.geometry = None
        super().__init__(location=self.center, zoom_start=self.zoom, control_scale=True, **kwargs)

    def add_raster_layer(self, layer: Layer):
        """
        Add a raster layer to the map.

        Args:
            layer: The raster layer.
        """
        # Get the tile json from the layer.
        tile_json = layer.get_tile_json()
        # Get the url of the tiles.
        url = tile_json["tiles"][0]

        tile_layer = folium.TileLayer(
            tiles=url,
            name=layer.name,
            attr=" ",
            overlay=True,
            control=True,
            opacity=layer.opacity,
        )

        tile_layer.add_to(self)

    def add_vector_layer(self, layer: Layer):
        """
        Add a vector layer to the map.

        Args:
            layer: The vector layer.
        """
        # Get the tile json from the layer.
        tile_json = layer.get_tile_json()
        # Get the url of the tiles.
        url = tile_json["tiles"][0]
        # Get the styles of the layer.
        layer_info = layer.info
        if layer_info.get("styles"):
            layer_name = tile_json.get("vector_layers")[0].get("id")
            vector_tile_layer_styles = {}
            vector_tile_layer_styles[layer_name] = layer_info.get("styles")

            options = {"vectorTileLayerStyles": vector_tile_layer_styles}
        else:
            options = None

        tile_layer = VectorGridProtobuf(
            url=url,
            name=layer.name,
            options=options,
            overlay=True,
            control=True,
        )

        tile_layer.add_to(self)

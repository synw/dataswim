import folium


class Map():

    def __init__(self):
        """
        Initialize
        """
        self.dsmap = None

    def marker(self, lat, long, text, color="darkslategrey", icon=None):
        """
        Adds a marker to the default map
        """
        try:
            xicon = folium.Icon(color=color, icon=icon)
            folium.Marker([lat, long], popup=text,
                          icon=xicon).add_to(self.dsmap)
        except Exception as e:
            self.err(e, self.marker, "Can not get marker")

    def marker_(self, lat, long, text, xmap,
                icon=None, color=None):
        """
        Adds a marker to a map
        """
        kwargs = {}
        xicon = None
        if icon is not None:
            kwargs["icon"] = icon
        if color is not None:
            kwargs["color"] = color
        if len(kwargs) > 0:
            xicon = folium.Icon(**kwargs)
        try:
            kwargs = dict()
            if xicon is not None:
                kwargs["icon"] = xicon
            folium.Marker([lat, long], popup=text, **kwargs).add_to(xmap)
            return xmap
        except Exception as e:
            self.err(e, self.marker, "Can not get marker")

    def map_(self, lat, long, zoom=10, tiles="map"):
        """
        Returns a map
        """
        try:
            return self._map(lat, long, zoom, tiles)
        except Exception as e:
            self.err(e, self.map_, "Can not get map")

    def map(self, lat, long, zoom=10, tiles="map"):
        """
        Sets a map
        """
        try:
            self.map = self._map(lat, long, zoom, tiles)
        except Exception as e:
            self.err(e, self.map, "Can not get map")

    def _map(self, lat, long, zoom=10, tiles="map"):
        """
        Returns a map
        """
        if tiles == "map":
            tiles = "OpenStreetMap"
        elif tiles == "terrain":
            tiles = "Stamen Terrain"
        elif tiles == "basic":
            tiles = "Stamen Toner"
        try:
            map = folium.Map(
                location=[lat, long],
                tiles=tiles,
                zoom_start=zoom
            )
            return map
        except Exception as e:
            self.err(e, self._map, "Can not make map")

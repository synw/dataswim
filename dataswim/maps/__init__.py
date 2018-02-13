import folium
from folium.features import DivIcon


class Map():

    def __init__(self):
        """
        Initialize
        """
        self.dsmap = None

    def tmarker(self, lat, long, text, color=None, icon=None, style=None):
        """
        Returns the map with a text marker to the default map
        """
        try:
            self.dsmap = self._marker(
                lat, long, text, self.dsmap, color, icon, True, style)
            return self.dsmap
        except Exception as e:
            self.err(e, self.tmarker, "Can not get text marker")

    def tmarker_(self, lat, long, text, pmap,
                 color=None, icon=None, style=None):
        """
        Returns the map with a text marker to the default map
        """
        try:
            xmap = self._marker(
                lat, long, text, pmap, color, icon, True, style)
            return xmap
        except Exception as e:
            self.err(e, self.tmarker_, "Can not get text marker")

    def marker_(self, lat, long, text, pmap, color=None, icon=None):
        """
        Returns the map with a marker to the default map
        """
        try:
            xmap = self._marker(lat, long, text, pmap, color, icon)
            return xmap
        except Exception as e:
            self.err(e, self.marker_, "Can not get marker")

    def marker(self, lat, long, text, color=None, icon=None):
        """
        Set the main map with a marker to the default map
        """
        try:
            self.dsmap = self._marker(lat, long, text, self.dsmap, color, icon)
            return self.dsmap
        except Exception as e:
            self.err(e, self.marker, "Can not get marker")

    def _marker(self, lat, long, text, xmap, color=None, icon=None,
                text_mark=False, style=None):
        """
        Adds a marker to the default map
        """
        kwargs = {}
        if icon is not None:
            kwargs["icon"] = icon
        if color is not None:
            kwargs["color"] = color
        if style is None:
            style = "font-size:18pt;font-weight:bold;" + \
                "color:black;border-radius:0.5"
        try:
            xicon1 = folium.Icon(**kwargs)
            if text_mark is True:
                xicon = DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
                    html='<div style="' + style + '">' + text + '</div>',
                )
                folium.Marker([lat, long], popup=text,
                              icon=xicon).add_to(xmap)
            folium.Marker([lat, long], popup=text,
                          icon=xicon1).add_to(xmap)
            return xmap
        except Exception as e:
            self.err(e, self._marker, "Can not get marker")

    def map_(self, lat, long, zoom=13, tiles="map"):
        """
        Returns a map
        """
        try:
            return self._map(lat, long, zoom, tiles)
        except Exception as e:
            self.err(e, self.map_, "Can not get map")

    def map(self, lat, long, zoom=13, tiles="map"):
        """
        Sets a map
        """
        try:
            self.dsmap = self._map(lat, long, zoom, tiles)
        except Exception as e:
            self.err(e, self.map, "Can not get map")

    def _map(self, lat, long, zoom, tiles):
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
            xmap = folium.Map(
                location=[lat, long],
                tiles=tiles,
                zoom_start=zoom
            )
            return xmap
        except Exception as e:
            self.err(e, self._map, "Can not make map")

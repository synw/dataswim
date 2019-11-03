import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
#import scipy.spatial as spatial
#from scipy.spatial import ConvexHull
from ..base import DsBase


class Map(DsBase):

    def __init__(self):
        """
        Initialize
        """
        self.dsmap = None

    """def polygon(self, list_of_points, layer_name="Polygons", line_color="lightblue",
                fill_color="royalblue", weight=5, text=""):
        ""
        Draw a polygon on the map
        ""
        if len(list_of_points) < 3:
            self.err(self.polygon,
                     "The list of points must contain at least 3 entries")
            return
        try:
            form = [list_of_points[i]
                    for i in spatial.ConvexHull(list_of_points).vertices]
            fg = folium.FeatureGroup(name=layer_name)
            fg.add_child(folium.vector_layers.Polygon(
                locations=form, color=line_color, fill_color=fill_color,
                weight=weight, popup=(folium.Popup(text))))
            self.dsmap.add_child(fg)
        except Exception as e:
            self.err(e, self.polygon, "Can not draw polygon on map")"""

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

    def amap(self, lat, long, zoom=13, tiles="map"):
        """
        Sets a map
        """
        try:
            self.dsmap = self._map(lat, long, zoom, tiles)
        except Exception as e:
            self.err(e, self.amap, "Can not get map")

    def mcluster(self, lat_col: str, lon_col: str):
        """
        Add a markers cluster to the map
        """
        try:
            mc = MarkerCluster()
            rows = []
            for _, v in self.df.iterrows():
                tup = (v[lat_col], v[lon_col])
                rows.append(tup)
            for el in rows:
                mc.add_child(folium.Marker([el[0], el[1]]))
            self.dsmap.add_child(mc)
        except Exception as e:
            self.err(e, "Can not add marker cluster")

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

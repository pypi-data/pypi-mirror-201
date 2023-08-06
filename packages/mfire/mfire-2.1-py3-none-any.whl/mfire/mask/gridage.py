"""
create mask on grid from geometry

a offset of 0.5 is applied on xy coordinates
in order to balance the fact that
coordinates are truncated ( instead of rounded) by draw function
thus 0.9 is interpreted as 0 by draw
and 0.9 + 0.5 = 1.4 is interpreted as 1 by draw
"""
import numpy as np
import xarray as xr
from shapely.geometry import mapping as SHAmapping
from PIL.Image import new as PILnew
from PIL.ImageDraw import Draw as PILdraw
from PIL.ImageChops import logical_or as PILor

from shapely import geometry as shp_geom
import json
from typing import Union

Shape = Union[
    shp_geom.Point,
    shp_geom.MultiPoint,
    shp_geom.LineString,
    shp_geom.MultiLineString,
    shp_geom.Polygon,
    shp_geom.MultiPolygon,
]


class GeoTypeException(Exception):
    """
    Exception on geometry Type
    """

    def __init__(self, key):
        self.message = "This geometry type is not managed : " + str(key)


class GeoDraw:
    """
    Draw geometry from json to image as mask
    """

    def __init__(self, gridinfo):
        """
        drawer : link to image to draw
        grid : specification of grid represent by image
        """
        self.grid = gridinfo
        self._set_image(
            PILnew("1", (self.grid["nb_c"], self.grid["nb_l"]))
        )  # actual image
        # link a type of geometry with action to do
        self.geoType_geoAction = {
            "Polygon": self._geopolygon,
            "MultiPolygon": self._geomultipolygon,
            "LineString": self._geoline,
            "MultiLineString": self._geomultiline,
            "Point": self._geopoint,
            "MultiPoint": self._geomultipoint,
        }

    def _set_image(self, image_in):
        self.image = image_in
        self.drawer = PILdraw(self.image)  # operator over image

    def get_image(self):
        return self.image

    def _lonlat2xy(self, coordinates):
        """
        convert latitude/longitude coordinates
        to list of x,y coordinates relative to grid
        Args :
        coordinates : list of points in geo coordinates
        Return :
        list of points in grid coordinates
        """
        LL = np.array(coordinates)
        A = self.grid["conversion_slope"]
        B = self.grid["conversion_offset"]
        X = A * LL + B
        # get all in one list
        return sum(X.tolist(), [])

    def draw_geo(self, geo):
        """
        manage the geometry of a geo
        select action to do by geometry type
        and apply it to the coordinate of the geometry
        """
        try:
            drawing = self.geoType_geoAction[geo["type"]]
        except KeyError:
            raise GeoTypeException(geo["type"])
        drawing(geo["coordinates"])

    def draw_shape(self, shape):
        """
        Entry point to manage the geometry of a shape
        """
        geo = json.loads(json.dumps(SHAmapping(shape)))
        self.draw_geo(geo)

    """
    All action available (one by geometry ttype known)
    """

    def _geopolygon(self, lines):
        """
        Draw a polygon
        first line is the contour of poylgon
        other lines are inner holes of polygon (option)
        """
        contour = lines.pop(0)
        if len(lines) == 0:
            # draw a simple polygon
            self.drawer.polygon(self._lonlat2xy(contour), fill=1)
        else:
            # draw a polygon with inner holes
            # first working on a different image
            image_holes = PILnew("1", (self.grid["nb_c"], self.grid["nb_l"]))
            draw_holes = PILdraw(image_holes)
            # draw the outer polygon
            draw_holes.polygon(self._lonlat2xy(contour), fill=1)
            # remove inner holes with fill=0
            [draw_holes.polygon(self._lonlat2xy(inner), fill=0) for inner in lines]
            # merge the previous image and the one with this polygon
            self._set_image(PILor(self.image, image_holes))

    def _geoline(self, line):
        """
        Draw a line
        """
        self.drawer.line(self._lonlat2xy(line), fill=1)

    def _geopoint(self, point):
        """
        Draw a point as a list of (unique) points
        """
        self.drawer.point(self._lonlat2xy([point]), fill=1)

    def _geomultipolygon(self, geos):
        """
        Draw multipolygon, one by one as polygon
        """
        [self._geopolygon(geo) for geo in geos]

    def _geomultiline(self, geos):
        """
        Draw multiline, one by one as line
        """
        [self._geoline(geo) for geo in geos]

    def _geomultipoint(self, geos):
        """
        Draw multipoint, at once
        """
        self.drawer.point(self._lonlat2xy(geos), fill=1)


def get_gridinfo(grid_da: xr.DataArray) -> dict:
    """Return grid's metadata.

    Args:
        grid_da (xr.DataArray): We will use only the lat/lon grid
            The grid should have latitude and longitude dimension.

    Returns:
        limited info about this grid (dict)
    """
    first_lat = grid_da.latitude[0].values.round(5)
    last_lat = grid_da.latitude[-1].values.round(5)
    nb_l = grid_da.latitude.size
    first_lon = grid_da.longitude[0].values.round(5)
    last_lon = grid_da.longitude[-1].values.round(5)
    nb_c = grid_da.longitude.size
    # xy / lonlat transform
    # compute matrix of transformation
    # nc -1 [nb_l -1] because grid start from 0
    # + 1 /2 for recentre
    a_x = (nb_c - 1) / (last_lon - first_lon)
    b_x = -first_lon * a_x + 0.5
    a_y = (nb_l - 1) / (last_lat - first_lat)
    b_y = -first_lat * a_y + 0.5
    A = np.array([a_x, a_y])
    B = np.array([b_x, b_y])
    info = {"conversion_slope": A, "conversion_offset": B, "nb_c": nb_c, "nb_l": nb_l}
    return info


def create_mask_PIL(poly: Shape, gridinfo: dict) -> xr.Dataset:
    geodraw = GeoDraw(gridinfo)
    geodraw.draw_shape(poly)
    img = geodraw.get_image()
    ds = xr.Dataset()
    for x in list(gridinfo["dims"]):
        ds.coords[x] = gridinfo[x]
    ds[gridinfo["name"]] = (gridinfo["dims"], np.array(img))
    # remove all unneeded coord
    ds = (
        ds.where(ds[gridinfo["name"]] > 0)
        .dropna(dim=gridinfo["dims"][0], how="all")
        .dropna(dim=gridinfo["dims"][1], how="all")
    )
    # to reduce time with computing operations
    ds[gridinfo["name"]] = ds[gridinfo["name"]].astype("int8").astype("bool")
    return ds

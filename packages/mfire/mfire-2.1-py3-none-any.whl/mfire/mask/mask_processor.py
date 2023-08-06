"""
This module should do mask preprocessing and transform geojson to netcdf.

History :
    (Vincent Chabot ) : Forcing small polygon to be represented as point or line.
    (Vincent Chabot) February 2021 :
        Adding splitting by
            - compass direction
            - altitude
    (Gaston Leroux) december 2022:
        - Optimizing code by using boolean
        - refactoring code
"""
from pathlib import Path
from typing import Tuple

from shapely import geometry as shp_geom
from geojson import Feature

import mfire.utils.hash as hashmod
from mfire.utils.xr_utils import ArrayLoader, from_0_360, from_center_to_0_360
from mfire.mask.north_south_mask import get_cardinal_masks
from mfire.mask.manage_merge import ManageMerge, MergeArea
from mfire.mask.gridage import create_mask_PIL, Shape
from mfire.mask.grids import get_info as GRIDget_info
from mfire.mask.altitude_mask import generate_mask_by_altitude
from mfire.mask.fusion import extract_areaName, perform_zone_fusion
import xarray as xr
from mfire.settings import get_logger, Settings

# Logging
LOGGER = get_logger(name="mask_processor", bind="mask")
# xarray settings
xr.set_options(keep_attrs=True)


class FileMask:
    def __init__(self, data, kwargs, grid_names):
        self.grid_names = grid_names
        if "mask_hash" in data:
            self.current_hash = data.get("mask_hash")
        else:
            handler = hashmod.MD5(data["geos"])
            self.current_hash = handler.hash
        # Pour chaque msb on va creer un nouveau fichier
        if "file" in data:
            self.fout = Path(data["file"])
        elif "uid" in data:
            self.fout = Path(kwargs.get("output_dir", "./") + data["uid"] + ".nc")
        else:
            raise ValueError(
                "You should have in the file something to name the output."
            )
        output_dir = self.fout.parent
        output_dir.mkdir(parents=True, exist_ok=True)

    def to_file(self, managemask):
        dmask = managemask.get_merge()
        # reduce netcdf size if possible
        for grid_name in self.grid_names:
            dmask[grid_name] = dmask[grid_name].astype("int8").astype("bool")
        dmask = dmask.drop_vars("is_polygon")  # remove tempo variable
        dmask.attrs["md5sum"] = self.current_hash
        dmask.to_netcdf(self.fout)


class MaskProcessor:
    """
    Permet de créer les masques géographiques sur les data array
    """

    def __init__(self, config_dict: dict, **kwargs):
        """
        Args:
            config_dict (dict): Dictionnaire de configuration de la production
                contenant au moins la clé 'geos'.
        Kwargs :
            output_dir : utilisé si pas de file dans le dictionnaire
        """
        self.data = config_dict
        self.change_geometry()
        self.kwargs = kwargs

    @property
    def grid_names(self) -> Tuple[str]:
        return tuple(
            p.name.split(".nc")[0] for p in Settings().altitudes_dirname.iterdir()
        )

    def get_grid_da(self, grid_name: str) -> xr.DataArray:
        return ArrayLoader(
            filename=Settings().altitudes_dirname / f"{grid_name}.nc"
        ).load()

    def change_geometry(self):
        """
        smooths line by rounding borders
        """
        for i, area in enumerate(self.data["geos"]["features"]):
            if shp_geom.shape(area["geometry"]).geometryType() in [
                "Polygon",
                "MultiPolygon",
                "LineString",
                "MultiLineString",
            ]:
                x = shp_geom.shape(area["geometry"]).buffer(1e-5)  # .buffer(-1e-5)
                self.data["geos"]["features"][i]["geometry"] = Feature(geometry=x)[
                    "geometry"
                ]

    def get_mask(self, grid_name: str, poly: Shape) -> xr.Dataset:
        """get_mask

        Args:
            grid_name (str): The grid name.
            poly (shapely.geometry.shape): The shape to transform in netcdf.

        Returns:
            xr.Dataset: The mask dataset.
        """
        grid_da = self.get_grid_da(grid_name)
        change_longitude = False
        if grid_da.longitude.max() > 180:
            change_longitude = True
            grid_da = from_0_360(grid_da)
        dout = create_mask_PIL(poly=poly, gridinfo=GRIDget_info(grid_da))
        if change_longitude:
            dout = from_center_to_0_360(dout)
        return dout.rename(
            {"latitude": f"latitude_{grid_name}", "longitude": f"longitude_{grid_name}"}
        )

    @staticmethod
    def is_axe(feature: dict) -> bool:
        """checks if mask's geojson description represents an axis.

        Args:
            feature (_type_): the geojson feature

        Returns:
            Bool: True if its an Axis, False otherwise
        """
        return feature["properties"].get("is_axe", False)

    def area_mask(self, area):
        """
        operation to be done for each area
        """
        area_id = area["id"]
        # Introduire ici le truc sur le hash
        poly = shp_geom.shape(area["geometry"])
        dmask = xr.Dataset()
        for grid_name in self.grid_names:
            dtemp = self.get_mask_on_grid(grid_name, poly, area_id, area["properties"])
            try:
                dmask = xr.merge([dmask, dtemp])
            except Exception as excpt:
                LOGGER.warning(f"Le merge partiel {dtemp}")
                LOGGER.warning(
                    "Failed to merge masks.",
                    dmask=dmask,
                    dtemp=dtemp,
                    area_id=area_id,
                    grid_name=grid_name,
                    func="area_masks",
                )
                raise excpt
        return (poly, dmask)

    def generate_alticompas(self, area_id, poly, managemask, dtemp):
        """
        generate altitude and cardinal zones
        """
        for grid_name in self.grid_names:
            LOGGER.debug(
                "Creating altitude and geographical mask",
                area_id=area_id,
                grid_name=grid_name,
                func="create_masks",
            )
            try:
                ds_mask_compass = self.get_compass_area(grid_name, poly, area_id)
                if ds_mask_compass and ds_mask_compass.id.size > 1:
                    managemask.merge(ds_mask_compass)
                ds_mask_alti = generate_mask_by_altitude(
                    dtemp[grid_name], self.get_grid_da(grid_name), area_id + "_alt_"
                )
                if ds_mask_alti is not None:
                    managemask.merge(ds_mask_alti)
            except Exception as excpt:
                LOGGER.warning(
                    "Failed to partial merge masks",
                    f"{ds_mask_compass} or {ds_mask_alti}",
                    dmask=managemask.get_merge(),
                    dtemp=dtemp,
                    area_id=area_id,
                    grid_name=grid_name,
                    func="create_masks",
                )
                raise excpt

    def generate_fusion(self, managemask, merged_list):
        """
        doing the actual creation and merging
        of already prepared fusionned zones
        """
        for grid_name in self.grid_names:
            dgrid = managemask.get_merge()[grid_name]
            managedout = ManageMerge()
            mergearea = MergeArea(dgrid, managedout)
            [mergearea.compute(new_zone) for new_zone in merged_list]
            dout = managedout.get_merge()
            if len(dout.data_vars) > 0:
                dout = dout.reset_coords(["areaName", "areaType"])
                managemask.merge(dout)

    def create_masks(self):
        """
        create_masks
        This function create all the mask from a geojson dictionnary.
        The creation is performed only if the output file is not present.
        """

        filemask = FileMask(self.data, self.kwargs, self.grid_names)
        # On tri les zones pour mettre les axes en dernier
        self.data["geos"]["features"].sort(key=self.is_axe)

        managemask = ManageMerge()  # to store all areas
        managealticompas = ManageMerge()
        merged_list = []  # to prepare fusionned areas
        for area in self.data["geos"]["features"]:
            """
            operation for every area
            """
            poly, dtemp = self.area_mask(area)
            managemask.merge(dtemp)
            # On recupere les infos qui nous interessent
            area_id = area["id"]
            if self.is_axe(area) and dtemp["is_polygon"]:
                """
                operation only for polygonal axis
                """
                # prepare set of couple of zones
                merged_list.extend(perform_zone_fusion(managemask.get_merge(), area_id))
                # adding altitude and cardinal zones
                self.generate_alticompas(area_id, poly, managealticompas, dtemp)

        LOGGER.info(f"{self.data['name']} Adding {len(merged_list)} fused zones")
        managemask.merge(managealticompas.get_merge())
        self.generate_fusion(managemask, merged_list)
        # save to disk
        filemask.to_file(managemask)

    def get_compass_area(self, grid_name: str, poly: Shape, area_id: str) -> xr.Dataset:
        """Effectue la découpe selon les points cardinaux

        Args:
            grid_name (str): Nom de la grille sur laquelle on veut projeter le JSON
            poly (shape): Le shape de la zone a découper
            area_id (str): L'identifiant original de la zone

        Returns:
            Dataset : Un dataset de la découpe
        """
        dmask = xr.Dataset()
        geo_B = get_cardinal_masks(poly, parent_id=area_id + "_compass_")
        for area in geo_B["features"]:
            compass_poly = shp_geom.shape(area["geometry"])
            compass_id = area["id"]
            area["properties"]["type"] = "compass"
            dtemp = self.get_mask_on_grid(
                grid_name, compass_poly, compass_id, area["properties"]
            )
            try:
                dmask = xr.merge([dmask, dtemp])
            except Exception as excpt:
                LOGGER.warning(
                    "Failed to merge masks.",
                    dmask=dmask,
                    dtemp=dtemp,
                    area_id=area_id,
                    grid_name=grid_name,
                    func="get_compass_area",
                )
                raise excpt
        return dmask

    def get_mask_on_grid(
        self, grid_name: str, poly: Shape, area_id: str, properties: dict
    ) -> xr.Dataset:
        """
        Args:
            grid_name (str): La grille d'intérêt
            poly (shape): The shape we will transfer to netcdf
            area_id (str): Id
            properties (dict): Dictionnary of properties
        """
        areaType = properties.get("type", "")
        if properties.get("is_axe", False):
            areaType = "Axis"

        areaName = extract_areaName(properties)
        dtemp = self.get_mask(grid_name, poly)
        dtemp = dtemp.expand_dims(dim="id").assign_coords(id=[area_id])
        dtemp["areaName"] = (("id",), [areaName])
        dtemp["areaType"] = (("id",), [areaType])
        # create tempo varaible needed for fusion
        dtemp["is_polygon"] = (
            ("id",),
            [poly.geometryType() in ["Polygon", "MultiPolygon"]],
        )
        return dtemp

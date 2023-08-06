from xarray import Dataset
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="mask_processor", bind="fusion")


def extract_areaName(properties: dict) -> str:
    """This enables to extract the name of the area from the configurations

    Args:
        properties ([dict]): The properties dictionnary.
        This dictionnary may contain "label", "alt_label", "name"

    Raises:
        ValueError: If we are not able to name the area we raise an error

    Returns:
        [str]: The areaName
    """
    for key in ("name", "label", "alt_label", "areaName", "area_name"):
        if key in properties and properties.get(key):
            return properties[key]
    raise ValueError(
        " Name was not found. Label cannot be split using '_' in 1 "
        "or 4 elements.  alt_label was empty."
    )


class CheckZone:
    """
    check if the union of 2 zones differs enough
    from already knonw zones
    """

    def __init__(self, dmask: Dataset, gmask: Dataset, list_poss: list, dims):
        """
        Args:
        dmask : entire set of zones
        gmask : set of zones to explore
        dims : variable used as dimensioins (lat, lon generally)
        """
        self.dmask = dmask
        self.gmask = gmask
        self.list_poss = list_poss
        self.dims = dims

    def compute(self, id1: str, id2: str):
        """
        check zones known as id1, id2
        return : True if the union is useful
        """
        z1 = self.gmask.sel(id=id1)
        z2 = self.gmask.sel(id=id2)
        my_zone = z1 + z2
        res = True
        for zone_id in self.list_poss:
            if not self.dmask["is_polygon"].sel(id=zone_id).values:
                LOGGER.info(f"Geometry {zone_id['geo_type']}")
                continue
            zone = self.gmask.sel(id=zone_id)
            inter_zone = (zone * my_zone).sum(self.dims).values
            if inter_zone == 0:
                continue
            union_zone = (zone + my_zone).sum(self.dims).values
            iou = inter_zone / union_zone
            if iou > 0.9:
                # Si la zone n'est pas assez différente d'une des zones descriptive
                res = False
                zone_name = self.dmask["areaName"].sel(id=zone_id).values
                LOGGER.info(f"Zone similaire : {zone_name}")
                break

        return res


class CoverZone:
    """
    check if zones differ enough from each other
    """

    def __init__(self, gmask, dims):
        """
         Args:
        gmask : set of zones to explore
        dims : variable used as dimensioins (lat, lon generally)
        """
        self.gmask = gmask
        self.dims = dims

    def compute(self, id1, id2):
        """
        check if zones (refer as id1, id2) differ
        Return : true if zones differ
        """
        z1 = self.gmask.sel(id=id1)
        z2 = self.gmask.sel(id=id2)
        inter_zones = (z1 * z2).sum(self.dims)
        return (
            inter_zones / z1.sum(self.dims) < 0.1
            and inter_zones / z2.sum(self.dims) < 0.1
        )


class FusionZone:
    """
    keep info needed to create fusion later
    """

    def __init__(self, dmask, parent_id):
        """
        Args
        dmask : entire set of zones
        parent_id : axis that integrate fusionned zones
            in order to generate id
        """
        self.dmask = dmask
        self.parent_id = parent_id

    def compute(self, id1, id2):
        """
        create a dico to prepare fusion
        Args:
        id1,id2 : reference to 2 zones to fusion
        return : dico that store info needed to fusion
        """
        areaName1 = self.dmask["areaName"].sel(id=id1).values
        areaName2 = self.dmask["areaName"].sel(id=id2).values
        name = str(areaName1) + " et " + str(areaName2)
        new_id = "__".join([self.parent_id, id1, id2])
        LOGGER.debug(f"On ajout a la liste {name} avec comme id {new_id}")
        descript = {
            "name": name,
            "base": [id1, id2],
            "id": new_id,
            "areaType": "fusion2",
        }
        return descript


def finest_grid_name(dmask) -> str:
    """
    choose the finest resolution by longitude
    in dmask dataset that contains all
    lat/lon possibility in coordinates
    """
    grid_ref = ""
    grid_points = 0
    for key in dmask.coords.keys():
        if dmask[key].name.startswith("longitude_"):
            points = len(dmask[key].values)
            if points > grid_points:
                grid_points = points
                grid_ref = dmask[key].name.replace("longitude_", "")
    return grid_ref


def perform_zone_fusion(dmask, area_id: str) -> list:
    """
    explore all zone from axis to create couple of zones to fusion
    Args:
    dmask : set of zones in touch with axis
    area_id : reference to axis
    return  : list of dico that contains info from 2 zones to fusion
    """
    inside = 0.9
    differ = 0.97
    grid_ref = finest_grid_name(dmask)
    dims = ("latitude_" + grid_ref, "longitude_" + grid_ref)
    gmask = dmask[grid_ref].astype("int8").astype("bool")
    axe = gmask.sel(id=area_id)
    axe_area = axe.sum(dims)
    l_poss = []  # id des zones possibles
    for zone_id in dmask["id"].values:
        zone = gmask.sel(id=zone_id)
        inter_zone_axe = (axe * zone).sum(dims)
        zone_area = zone.sum(dims)
        if (
            zone.sum(dims) > 0
            and inter_zone_axe / zone_area > inside
            and inter_zone_axe / axe_area < differ
        ):
            l_poss.append(zone_id)
    fus_loc = FusionZone(dmask, area_id)
    cov_loc = CoverZone(gmask, dims)
    chk_loc = CheckZone(dmask, gmask, l_poss, dims)
    l_fus = [
        fus_loc.compute(zoneid1, zoneid2)
        for i, zoneid1 in enumerate(l_poss[:-1])
        for zoneid2 in l_poss[i + 1 :]
        if (cov_loc.compute(zoneid1, zoneid2) and chk_loc.compute(zoneid1, zoneid2))
    ]
    return l_fus

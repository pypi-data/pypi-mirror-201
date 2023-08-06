"""Create divisions along cardinal points of a shapefile"""
from shapely import geometry as shp_geom
from shapely import affinity
from geojson import Feature, FeatureCollection

from mfire.settings import get_logger

LOGGER = get_logger(name="masks.processor.cardinals", bind="masks.processor")

PERCENT_ONE = 0.5  # pourcentage d'une zone (N, S, E, O) par rapport à l'ensemble
PERCENT_SMALL = 0.35  # pourcentage d'une zone "petite"
MIN_AREA = 0.1  # pourcentage minimal de la zone initiale pour conserver un découpage
MAX_AREA = 0.8  # pourcentage maximal
PERCENT_UNICITY = (
    0.85  # correspondance maximale entre deux zones (sinon on n'en conserve qu'une)
)

BUFFER_SIZE = 0.01  # pourcentage de simplification du découpage (par agrandissement)

# inutilisés dans cette version du module
# à supprimer après tests
PERCENT_BIG = 0.65
PERCENT_X = 0.8


class CardinalMasks:
    """Crée les masques selon les points cardinaux."""

    def __init__(self, geo, area_id, cards=None):
        """
        args:
            geo(shape) : la zone à découper
            cards(list) : liste des découpages voulus (défaut à tous)
        """
        self.name_template = "dans {}{}"
        self.name_size = "une {} partie "

        self.l_result = []  # keep only unique geo (nearby PERCENT_UNICITY)
        self.l_feat = []  # keep list as feature
        self.geo = geo
        self.area_id = area_id
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = self.geo.bounds
        self.delta_lat = self.max_lat - self.min_lat
        self.mid_lat = (self.max_lat + self.min_lat) / 2
        self.delta_lon = self.max_lon - self.min_lon
        self.mid_lon = (self.max_lon + self.min_lon) / 2

        self.bounding_rect = shp_geom.Polygon(
            [
                (self.min_lon, self.min_lat),
                (self.min_lon, self.max_lat),
                (self.max_lon, self.max_lat),
                (self.max_lon, self.min_lat),
            ]
        )

        self.cards = [
            "Nord",
            "Sud",
            "Est",
            "Ouest",
            "Sud-Est",
            "Sud-Ouest",
            "Nord-Est",
            "Nord-Ouest",
        ]
        if cards is not None:
            if any(x for x in cards if x not in self.cards):
                LOGGER.critical(
                    "une orientation du découpage demandée n'est pas configurée"
                )
                raise ValueError("bad parameter for the list of splits (cards)")
            self.cards = cards

        # nom du découpage associé
        # - aux arguments de transformation scalaire
        #               [x, y, (origin_x, origin_y] ('change_me' = proportions)
        # - au déterminant employé
        self.inputs = {
            "Nord": [(1, "change_me", (self.min_lon, self.max_lat)), "le "],
            "Sud": [(1, "change_me", (self.min_lon, self.min_lat)), "le "],
            "Est": [("change_me", 1, (self.max_lon, self.max_lat)), "l'"],
            "Ouest": [("change_me", 1, (self.min_lon, self.max_lat)), "l'"],
            "Sud-Est": [
                ("change_me", "change_me", (self.max_lon, self.min_lat)),
                "le ",
            ],
            "Sud-Ouest": [
                ("change_me", "change_me", (self.min_lon, self.min_lat)),
                "le ",
            ],
            "Nord-Est": [
                ("change_me", "change_me", (self.max_lon, self.max_lat)),
                "le ",
            ],
            "Nord-Ouest": [
                ("change_me", "change_me", (self.min_lon, self.max_lat)),
                "le ",
            ],
        }

        # possible utilisation de matrices avec affinity.affine_transform
        # mNorth = [1, 0, 0, x, 0, self.max_lat / 2]
        # mSouth = [1, 0, 0, 0.5, 0, self.min_lat / 2]
        # mEast = [0.5, 0, 0, 1, self.max_lon / 2, 0]
        # mWest = [0.5, 0, 0, 1, self.min_lon / 2, 0]

    def test_area(self, sub, min_area, max_area):
        """
        Test si la nouvelle zone est bien "assez grande" mais "pas trop grande"
        par rapport à sa zone d'origine.
        et que la découpe proposée ne ressemble pas trop à une déjà faite.

        Args:
            sub (shape): Découpe
            min_area (int): Pourcentage minimum de l'aire geographique
                (vis à vis de la zone d'origine)
            max_area (int): Pourcentage maximum de l'aire géographique
                (vis à vis de la zone d'origine)
        Using also:
            self.l_result : liste des découpes déjà retenues
            self.geo (shape): Zone géographique d'origine

        Returns:
            bool
        """
        if self.geo.geometryType not in ["Polygon"]:
            geo_t = self.geo.buffer(BUFFER_SIZE)
            sub_t = sub.buffer(BUFFER_SIZE)
        else:
            geo_t = self.geo
            sub_t = sub
        if (sub_t.area > geo_t.area * min_area) and (
            sub_t.area < geo_t.area * max_area
        ):
            if sub.geometryType not in ["Polygon"]:
                buffering = True
                sub_t = sub.buffer(BUFFER_SIZE)
            for tested in self.l_result:
                other_geo = tested
                if buffering:
                    other_geo = other_geo.buffer(BUFFER_SIZE)
                if (
                    sub_t.intersection(other_geo).area / other_geo.union(sub_t).area
                ) > PERCENT_UNICITY:
                    break
            else:
                self.l_result.append(sub)
                return True
        return False

    def get_rect_mask(self, lon_scale, lat_scale, origin):
        """Returns a part of the bounding rectangle

        Args:
            lon_scale (float): scalar used to multiple longitude values
            lat_scale (float): scalar used to multiple latitude values
            origin (tuple): center point (lon, lat) of the transformation

        Returns:
            (shapefile) bounding rectangle transformed
        """
        return affinity.scale(self.bounding_rect, lon_scale, lat_scale, origin=origin)

    def get_central_squares(self):
        """Returns two lozenges in the center of the self.geo"""
        big_one = shp_geom.Polygon(
            [
                (self.mid_lon, self.mid_lat + self.delta_lat / 2 * PERCENT_ONE),
                (self.mid_lon + self.delta_lon / 2 * PERCENT_ONE, self.mid_lat),
                (self.mid_lon, self.mid_lat - self.delta_lat / 2 * PERCENT_ONE),
                (self.mid_lon - self.delta_lon / 2 * PERCENT_ONE, self.mid_lat),
            ]
        )
        # unused, but in case of
        small_one = affinity.scale(big_one, 0.5, 0.5)
        return big_one, small_one

    def make_name(self, card):
        """Create a geo mask descriptive name from templates
            ...in French...

        Args:
            card(string): compact cardinal mask name

        Returns:
            (string) name
        """
        if card.startswith("Small"):
            return self.name_template.format(self.name_size.format("petite"), card[5:])
        return self.name_template.format(self.inputs[card][1], card)

    def make_all_masks(self, cardinal_point):
        """Make the masks according to cardinal points

        Returns:
            l_feat(FeatureCollection): geojsons
        """
        inpt = self.inputs[cardinal_point]
        for card_name, size in {
            cardinal_point: PERCENT_ONE,
            "Small" + cardinal_point: PERCENT_SMALL,
        }.items():
            scaling = [x if x != "change_me" else size for x in inpt[0]]
            rect_mask = self.get_rect_mask(*scaling)
            geo_mask = self.geo.intersection(rect_mask)
            if "-" in cardinal_point:
                # we remove the center for intercardinals
                big_square, _ = self.get_central_squares()
                geo_mask = geo_mask.difference(big_square)
            if self.test_area(geo_mask, MIN_AREA, MAX_AREA):
                geo_buf = geo_mask.buffer(BUFFER_SIZE)
                name = self.make_name(card_name)
                self.l_feat.append(
                    Feature(
                        geometry=geo_buf,
                        id=self.area_id
                        + "_"
                        + card_name,  # vérif si le "-" est à enlever
                        properties={"name": name},
                    )
                )


def get_cardinal_masks(geo, parent_id="", cards=None):
    """Renvoi la liste des découpages géographique
    via la classe"""

    cm = CardinalMasks(geo, parent_id, cards)
    [cm.make_all_masks(cardinal_point) for cardinal_point in cm.cards]
    return FeatureCollection(cm.l_feat)

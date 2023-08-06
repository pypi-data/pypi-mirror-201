"""
grid manipulation
"""
import xarray as xr
import numpy as np


def _get_gridinfo(grid_da: xr.DataArray) -> dict:
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

    info = {
        "name": grid_da.name,
        "dims": grid_da.dims,
        "conversion_slope": A,
        "conversion_offset": B,
        "nb_c": nb_c,
        "nb_l": nb_l,
    }
    for x in list(info["dims"]):
        info[x] = grid_da[x].values
    return info


grids_ = {}


def _add(grid_da: xr.DataArray):
    """
    Store the metadata
    """
    grid_name = grid_da.name
    grids_[grid_name] = _get_gridinfo(grid_da)


def get_info(grid_da: xr.DataArray):
    """
    give metadata
    first compute it if necessary
    """
    grid_name = grid_da.name
    try:
        return grids_[grid_name]
    except KeyError:
        _add(grid_da)
        return grids_[grid_name]

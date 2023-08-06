"""
Module permettant de gérer la génération de textes de synthèses.
C'est dans ce module qu'on va décider vers quel module
de génération de texte de synthèse on va s'orienter.
"""

from mfire.settings import get_logger

from mfire.text.base import BaseDirector
from mfire.text.wind import WindReducer, WindBuilder


# Logging
LOGGER = get_logger(name="wind_director.mod", bind="wind_director")


class WindDirector(BaseDirector):
    """Module permettant de gérer la génération de textes de synthèse."""

    reducer: WindReducer = WindReducer()
    builder: WindBuilder = WindBuilder()

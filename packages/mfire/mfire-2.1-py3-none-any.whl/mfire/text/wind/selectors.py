from mfire.settings import get_logger
from mfire.text.base import BaseSelector

# Logging
LOGGER = get_logger(name="wind_selector.mod", bind="wind_selector")


class WindSelector(BaseSelector):
    """WindSelector spécifique pour la wind"""

    def compute(self, reduction: dict) -> str:
        """génération du dictionnaire de choix, recherche dans la matrice
        du texte de synthèse pour le température pour détermier la clé du template
        en fonction du paramètre
        """

        LOGGER.info(f"reduction {reduction}")
        key = "P1_Z0"
        return key

from mfire.settings import get_logger
from mfire.text.base import BaseBuilder
from mfire.text.common import (
    SynonymeBuilder,
    ZoneBuilder,
    PeriodBuilder,
    TemplateBuilder,
)

from mfire.text.template import read_file
from mfire.settings import TEMPLATES_FILENAMES
from mfire.text.wind import WindSelector


# Logging
LOGGER = get_logger(name="wind_builder.mod", bind="wind_builder")

TEMPE_TPL_RETRIEVER = read_file(TEMPLATES_FILENAMES["fr"]["synthesis"]["wind"])


class WindBuilder(
    TemplateBuilder,
    SynonymeBuilder,
    PeriodBuilder,
    ZoneBuilder,
    BaseBuilder,
):
    """Builder spécifique pour gérer les textes de sythèse pour la température

    Args:
        Objet qui est capable de trouver et de et de fournir un modèle
        correspondant à self.reducer.

    Inheritance:
        BaseBuilder
        SynonymeBuilder
        ZoneBuilder
        PeriodBuilder
    """

    def process(self) -> str:
        pass

    def compute(self, reduction: dict) -> None:
        self.reset()
        self.reduction = reduction
        selector = WindSelector()
        key = self.find_template_key(selector)
        self.retrieve_template(key, TEMPE_TPL_RETRIEVER)
        self.process()
        self.handle_comment(reduction)
        self.build_period(reduction)
        self.build_zone()
        self.find_synonyme()
        self._text = self._text[0].upper() + self._text[1:]

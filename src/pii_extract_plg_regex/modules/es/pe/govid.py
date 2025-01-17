"""
Peruvian Goverment-issued CUI (Código Único de Identificación) for the DNI
(Documento Documento Nacional de Identidad)
"""

import re

from typing import Iterable

from stdnum.pe import cui

from pii_data.types import PiiEnum, PiiEntity
from pii_data.types.doc import DocumentChunk
from pii_extract.build.task import BasePiiTask

# Regex for DNI
_DNI_PATTERN_SIMPLE = r"\b \d{8} (?!-) \b"
_DNI_PATTERN_FULL = r"\b \d{8} - \d \b"


class PeruvianDniFull(BasePiiTask):
    """
    Match a Peru DNI number, and validate the checksum digit, if present, else
    use context.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Compile the regexes
        self.dni = re.compile(_DNI_PATTERN_FULL, flags=re.X)


    def find(self, chunk: DocumentChunk) -> Iterable[PiiEntity]:
        """
        Find & validate instances of either DNI or NIE
        """
        # DNI
        for item in self.dni.finditer(chunk.data):
            item_value = item.group()
            if cui.is_valid(item_value):
                yield PiiEntity(self.pii_info, item_value, chunk.id,
                                item.start())


# ---------------------------------------------------------------------

# Task descriptor
PII_TASKS = [
    {
        "class": "PiiTask",
        "task": PeruvianDniFull,
        "name": "Peruvian DNI",
        "pii": {
            "type": PiiEnum.GOV_ID,
            "subtype": "Peruvian DNI",
            "method": "soft-regex,checksum"
        }
    },
    {
        "class": "regex",
        "task": _DNI_PATTERN_SIMPLE,
        "name": "Peruvian DNI, using context",
        "pii": {
            "type": PiiEnum.GOV_ID,
            "subtype": "Peruvian DNI",
            "context": {
                "value": ["DNI", "documento nacional de identidad"],
                "width": [45, 0],
                "type": "word",
            },
            "method": "weak-regex,context"
        }
    }
]

import importlib
import inspect
import os
import pkgutil
from typing import List

from ingestion.parsers import base as parsers_pkg
from ingestion.parsers.base import BankOfferParser


def discover_parsers() -> list[BankOfferParser]:
    parsers: List[BankOfferParser] = []
    package = "ingestion.parsers"
    parser_path = os.path.dirname(parsers_pkg.__file__)
    for _, module_name, _ in pkgutil.iter_modules([parser_path]):
        if module_name != "base":
            module = importlib.import_module(f"{package}.{module_name}")
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BankOfferParser) and obj is not BankOfferParser:
                    parsers.append(obj())
    return parsers


test = discover_parsers()
a = 0

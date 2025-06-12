# src/cardwise/infrastructure/parsers/parser_registry.py

import importlib
import inspect
import os
import pkgutil
from typing import List

import cardwise.infrastructure.parsers as parsers_pkg
from cardwise.infrastructure.parsers.base_offer_parser import BankOfferParser


def discover_parsers() -> list[BankOfferParser]:
    parsers: List[BankOfferParser] = []
    package = "cardwise.infrastructure.parsers"
    parser_path = os.path.dirname(parsers_pkg.__file__)
    for _, module_name, _ in pkgutil.iter_modules([parser_path]):
        if module_name.endswith("_offer_parser") and module_name != "base_offer_parser":
            module = importlib.import_module(f"{package}.{module_name}")
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BankOfferParser) and obj is not BankOfferParser:
                    parsers.append(obj())
    return parsers

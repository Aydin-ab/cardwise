# Write a function that return a Json offer formatter if true, else a CLI offer formatter.
from cardwise.domain.formatters.base_offer_formatter import OfferFormatter
from cardwise.domain.formatters.cli_offer_formatter import CLIOfferFormatter
from cardwise.domain.formatters.json_offer_formatter import JSONOfferFormatter


def get_offer_formatter(json_output: bool) -> OfferFormatter:
    """
    Returns the appropriate OfferFormatter based on the json_output flag.

    :param json_output: If True, returns a JSON formatter; otherwise, returns a CLI formatter.
    :return: An instance of OfferFormatter (either JSONOfferFormatter or CLIOfferFormatter).
    :raises CardwiseError: If an unsupported formatter type is requested.
    """
    if json_output:
        return JSONOfferFormatter()
    else:
        return CLIOfferFormatter()

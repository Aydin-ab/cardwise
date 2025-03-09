class BankParserError(Exception):
    """Base class for all bank parser exceptions."""

    pass


class MissingHTMLFileError(BankParserError):
    """Raised when an HTML file is missing."""

    def __init__(self, bank_name, file_path):
        super().__init__(
            f"❌ Error: The HTML file '{file_path}' for {bank_name} does not exist. "
            "Please provide a valid file."
        )


class InvalidOfferDataError(BankParserError):
    """Raised when required offer data is missing from a parsed HTML file."""

    def __init__(self, bank_name, issue_detail):
        super().__init__(f"❌ Error: {issue_detail} in {bank_name} offers.")

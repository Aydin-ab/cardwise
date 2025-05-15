class BankParserError(Exception):
    """Base class for all bank parser exceptions."""

    pass


class MissingHTMLFileError(BankParserError):
    """Raised when an HTML file is missing."""

    def __init__(self, bank_name: str, file_path: str) -> None:
        error_message: str = (
            f"❌ Error: The HTML file '{file_path}' for {bank_name} does not exist. Please provide a valid file."
        )
        super().__init__(error_message)


class InvalidOfferDataError(BankParserError):
    """Raised when required offer data is missing from a parsed HTML file."""

    def __init__(self, bank_name: str, issue_detail: str) -> None:
        error_message: str = f"❌ Error: {issue_detail} in {bank_name} offers."
        super().__init__(error_message)

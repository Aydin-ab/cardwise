class CardwiseError(Exception):
    """Base exception for all Cardwise errors."""

    pass


class OfferParsingError(CardwiseError):
    """Raised when parsing of an offer fails."""

    def __init__(self, bank: str, message: str):
        super().__init__(f"[{bank}] Offer parsing failed: {message}")


class OfferShopNameParsingError(OfferParsingError):
    """Raised when the shop name for an offer can't be extracted."""

    def __init__(self, bank: str, detail: str):
        super().__init__(bank, f"Offer's shop name not found. {detail}")


class OfferDescriptionParsingError(OfferParsingError):
    """Raised when the offer description can't be extracted."""

    def __init__(self, bank: str, detail: str):
        super().__init__(bank, f"Offer's description not found. {detail}")


class OfferSourceNotFound(CardwiseError):
    """Raised when an expected HTML file is missing."""

    def __init__(self, bank: str, path: str):
        super().__init__(f"[{bank}] HTML file not found: {path}")

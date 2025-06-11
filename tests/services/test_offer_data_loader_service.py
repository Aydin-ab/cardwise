from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from cardwise.app.data_loader import OfferDataLoader
from cardwise.domain.models.bank import Bank
from cardwise.domain.models.offer import Offer, OfferTypeEnum
from cardwise.domain.models.shop import Shop


class FakeParser:
    def __init__(self, bank_id: str, offers: list[Offer]):
        self.bank = Bank(name=bank_id)
        self._offers = offers

    def parse(self, path: Path) -> list[Offer]:
        return self._offers


@pytest.fixture()
def offer(shop_name: str = "Costco") -> Offer:
    return Offer(
        shop=Shop(name=shop_name),
        bank=Bank(name="Amex"),
        offer_type=OfferTypeEnum.CASHBACK,
        description="10% back",
        expiry_date=datetime(2025, 12, 31),
    )


@pytest.fixture
def fake_repository():
    repo = MagicMock()
    repo.get_all.return_value = []
    return repo


@pytest.fixture
def offer_loader(tmp_path: Path, offer: Offer, fake_repository: MagicMock):
    parser = FakeParser("amex", [offer])
    file_path = tmp_path / f"{parser.bank.id}_offers.html"
    file_path.write_text("<html></html>")  # Simulate an HTML file
    loader = OfferDataLoader(
        parsers=[parser],  # type: ignore
        html_dir=tmp_path,
        repository=fake_repository,
    )
    return loader


def test_get_or_restore_offers_loads_from_parser_if_repo_empty(
    offer_loader: OfferDataLoader, fake_repository: MagicMock
):
    offers = offer_loader.get_or_restore_offers()

    assert len(offers) == 1
    fake_repository.save_all.assert_called_once_with(offers)


def test_get_or_restore_offers_returns_cached_repo_data(fake_repository: MagicMock, tmp_path: Path, offer: Offer):
    fake_repository.get_all.return_value = [offer]

    parser = FakeParser("amex", [])
    loader = OfferDataLoader(
        parsers=[parser],  # type: ignore
        html_dir=tmp_path,
        repository=fake_repository,
    )

    offers_ = loader.get_or_restore_offers()

    assert offers_ == [offer]
    fake_repository.save_all.assert_not_called()


def test_refresh_offers_from_html_parses_and_replaces_data(offer_loader: OfferDataLoader, fake_repository: MagicMock):
    offers = offer_loader.refresh_offers_from_html()

    assert len(offers) == 1
    fake_repository.refresh.assert_called_once()
    fake_repository.save_all.assert_called_once_with(offers)

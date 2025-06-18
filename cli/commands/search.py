# cli/commands/search.py
from typing import List

import requests
import typer

from cardwise.domain.models.offer import Offer
from cli.core.config import settings
from cli.utils import print_offers

app = typer.Typer()


def register(app: typer.Typer):
    @app.command()
    def search(shop: List[str]):  # type: ignore
        """
        Search offers for one or more shop names.
        Example: `cardwise search adidas "shake shack"`
        """
        print(f"🔍 Searching for: {shop}")
        search_api = f"{settings.backend_api_url}/offers/search"
        response = requests.get(search_api, params=[("shops", s) for s in shop], timeout=10)
        if response.status_code != 200:
            typer.echo(f"❌ Error: {response.status_code} — {response.text}")
            raise typer.Exit(code=1)

        offers_json = response.json()
        offers = [Offer(**offer_dict) for offer_dict in offers_json]
        print_offers(offers)

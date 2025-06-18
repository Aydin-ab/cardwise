# cli/commands/ingest.py
import typer

from ingestion.main import main as ingestion_main

app = typer.Typer()


def register(app: typer.Typer):
    @app.command()
    def ingest():  # type: ignore
        """Ingest all HTML offers and populate the database."""
        ingestion_main()

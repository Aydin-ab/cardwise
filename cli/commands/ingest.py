# cli/commands/ingest.py
import typer

from ingestion.main import main as ingestion_main

ingest_command = typer.Typer()


@ingest_command.command()
def run():
    """Ingest all HTML offers and populate the database."""
    ingestion_main()

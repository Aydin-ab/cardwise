# cli/commands/ingest.py
import typer

import ingestion.main

app = typer.Typer()


def register(app: typer.Typer):
    @app.command()
    def ingest(  # type: ignore
        upload: bool = typer.Option(False, "--upload", help="Upload local HTML files to GCS before ingestion"),
    ):
        """Ingest all HTML offers and populate the database.
        If --upload is specified, it will upload local HTML files to the GCS bucket before ingestion.
        The HTML files should be located in the 'ingestion/data/' folder."""
        ingestion.main.main(upload=upload)

    @app.command(name="upload")
    def upload_command():  # type: ignore
        """Upload local HTML files to the GCS bucket.
        The HTML files should be located in the 'ingestion/data/' folder."""

        typer.echo("☁️ Uploading HTML files to GCS...")
        ingestion.main.main_upload_htmls()

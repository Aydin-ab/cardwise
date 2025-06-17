# cli/main.py
import typer

from cli.commands.ingest import ingest_command
from cli.commands.search import search_command

app = typer.Typer()
app.add_typer(ingest_command, name="ingest")
app.add_typer(search_command, name="search")

if __name__ == "__main__":
    app()

import typer

from cli.commands import ingest, search

app = typer.Typer()
ingest.register(app)
search.register(app)

if __name__ == "__main__":
    app()

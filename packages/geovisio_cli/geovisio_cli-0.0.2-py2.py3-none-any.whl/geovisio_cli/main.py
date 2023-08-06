import typer
from pathlib import Path
from geovisio_cli import sequence, exception, model
from rich import print
from rich.panel import Panel
from typing import Optional


app = typer.Typer(help="GeoVisio command-line client")


@app.command()
def upload(
    path: Path = typer.Option(..., help="Local path to your sequence folder"),
    api_url: str = typer.Option(..., help="GeoVisio endpoint URL"),
    user: str = typer.Option(
        default=None,
        help="""GeoVisio user name if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the username will be asked during run.
""",
        envvar="GEOVISIO_USER",
    ),
    password: str = typer.Option(
        default=None,
        help="""GeoVisio password if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the password will be asked during run.
Note: is is advised to wait for prompt without using this variable.
""",
        envvar="GEOVISIO_PASSWORD",
    ),
    wait: bool = typer.Option(default=False, help="wait for all pictures to be ready"),
):
    """Processes and sends a given sequence on your GeoVisio API"""

    geovisio = model.Geovisio(url=api_url, user=user, password=password)
    try:
        sequence.upload(path, geovisio, wait)
    except exception.CliException as e:
        print(
            Panel(
                f"{e}",
                title="[red]Error while importing collection",
                border_style="red",
            )
        )
        return 1


@app.command()
def test_process(
    path: Path = typer.Option(..., help="Local path to your sequence folder"),
):
    """(For testing) Generates a JSON file with metadata used for upload"""

    import json
    from dataclasses import asdict

    try:
        collection = sequence.process(path)
        print(json.dumps(asdict(collection), indent=2))
    except exception.CliException as e:
        print(
            Panel(
                f"{e}",
                title="[red]Error while importing collection",
                border_style="red",
            )
        )
        return 1


@app.command()
def collection_status(
    id: Optional[str] = typer.Option(default=None, help="Id of the collection"),
    api_url: Optional[str] = typer.Option(default=None, help="GeoVisio endpoint URL"),
    location: Optional[str] = typer.Option(
        default=None, help="Full url of the collection"
    ),
    wait: bool = typer.Option(default=False, help="wait for all pictures to be ready"),
):
    """
    Print the status of a collection.\n
    Either a --location should be provided, with the full location url of the collection
    or only the --id combined with the --api-url
    """

    try:
        location = location
        if location is None:
            if api_url is None or id is None:
                raise exception.CliException(
                    "The way to identify the collection should be either with --location or with --id combined with --api-url"
                )
            location = f"{api_url}/api/collections/{id}"
        sequence.display_sequence_status(location)
        if wait:
            sequence.wait_for_sequence(location)
    except exception.CliException as e:
        print(
            Panel(
                f"{e}",
                title="[red]Error while getting collection status",
                border_style="red",
            )
        )
        return 1

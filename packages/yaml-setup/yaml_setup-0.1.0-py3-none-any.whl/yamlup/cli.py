import typer
import rich
import json
import sys
import re

from pathlib import Path
from rich.table import Table

from .schema import SetupFile, cerr, cout


app = typer.Typer(
    name="yamlup",
    help=f"A small CLI that's packaged with the yaml-setup lib",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

@app.command(
    "check",
    help=f"Checks the file given as argument",
    no_args_is_help=True,
)
def from_file(
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    schema: Path = typer.Option(None, "--schema", "-s", help="Use your own schema."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode.")
    ):
    if schema:
        cerr("❌ Not yet Implemented through CLI. Please use the python utils.")
    setup = SetupFile(filepath)
    cout.print(setup)

@app.command(
    "find",
    help=f"Finds a nested subitem within the file",
    no_args_is_help=True,
)
def find(
    key: str = typer.Argument(
        ...,
        help="The key to search within the setup file"
        ),
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    schema: Path = typer.Option(None, "--schema", "-s", help="Use your own schema."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Print statements during search")
    ):
    if schema:
        cerr("❌ Not yet Implemented through CLI. Please use the python utils.")
    setup = SetupFile(filepath)
    cout.print(setup.find(key.strip().lower(), debug=debug))

@app.command(
    "findall",
    help=f"Finds all nested subitems within the file",
    no_args_is_help=True,
)
def findall(
    key: str = typer.Argument(
        ...,
        help="The key to search within the setup file"
        ),
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    schema: Path = typer.Option(None, "--schema", "-s", help="Use your own schema."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Print statements during search"),
    array: bool = typer.Option(False, "-a", "--array", help="Reformat into flat array of records"),
    ):
    if schema:
        cerr("❌ Not yet Implemented through CLI. Please use the python utils.")
    setup = SetupFile(filepath)
    if array:
        result = setup.asArray(key.strip().lower())
    else:
        result = setup.all(key.strip().lower())

    cout.print(result)


@app.command("render")
def render(
    filepath: Path = typer.Argument(
        ...,
        help="The path to the file to upload.", 
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
        ),
    outfile: Path = typer.Option(
        None,
        '-o',
        '--outfile',
        help="Output file to write markdown to"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode.")
    ):
    setup = SetupFile(filepath)
    mdtext = setup.render()
    if outfile is not None:
        outfile = outfile or filepath.with_suffix('.md')
        outfile = Path(outfile)
        outfile.parent.mkdir(parents=True, exist_ok=True)
        outfile.with_suffix('.md').write_text(mdtext)

    else:
        cout.print(mdtext)

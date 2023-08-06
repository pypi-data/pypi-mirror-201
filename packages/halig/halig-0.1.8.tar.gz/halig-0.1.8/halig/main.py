#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from halig import literals
from halig.commands.edit import EditCommand
from halig.commands.notebooks import NotebooksCommand
from halig.commands.show import ShowCommand
from halig.settings import load_from_file
from halig.utils import capture
from halig.__version__ import __version__
from rich import print

app = Typer(pretty_exceptions_enable=False, pretty_exceptions_show_locals=False)

config_option = Option(None, "--config", "-c", help=literals.OPTION_CONFIG_HELP)


@app.command(help=literals.COMMANDS_NOTEBOOKS_HELP)
@capture
def notebooks(
        level: int = Option(  # noqa: B008
            -1,
            "--level",
            "-l",
            help=literals.OPTION_LEVEL_HELP,
        ),
        config: Optional[Path] = config_option,  # noqa: UP007
):
    if level < 0:
        level = float("inf")  # type: ignore[assignment]
    settings = load_from_file(config)
    command = NotebooksCommand(settings=settings, max_depth=level)
    command.run()


@app.command(help=literals.COMMANDS_EDIT_HELP)
@capture
def edit(
        note: Path = Argument(  # noqa: B008
            ...,
            help=literals.ARGUMENT_EDIT_NOTE_HELP,
        ),
        config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = EditCommand(settings=settings, note_path=note)
    command.run()


@app.command(help=literals.COMMANDS_SHOW_HELP)
@capture
def show(
        note: Path = Argument(  # noqa: B008
            ...,
            help=literals.ARGUMENT_SHOW_NOTE_HELP,
        ),
        config: Optional[Path] = config_option,  # noqa: UP007
):
    settings = load_from_file(config)
    command = ShowCommand(settings=settings, note_path=note)
    command.run()


@app.command(help=literals.COMMANDS_VERSION)
@capture
def version():
    print(__version__)


if __name__ == "__main__":
    app()

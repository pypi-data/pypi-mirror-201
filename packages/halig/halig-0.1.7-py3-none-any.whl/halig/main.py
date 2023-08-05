#!/usr/bin/env python3
from pathlib import Path
from typing import Optional

from halig.commands.edit import EditCommand
from halig.commands.notebooks import NotebooksCommand
from halig.commands.show import ShowCommand
from halig.settings import load_from_file

from typer import Typer, Option, Argument

app = Typer(pretty_exceptions_enable=False)

config_option = Option(
    None,
    "--config",
    "-c",
    help="Configuration file. Must be YAML and schema compatible",
)


@app.command(help="List all notebooks and notes, tree-style")
def notebooks(
        level: int = Option(
            -1,
            "--level",
            "-l",
            help="Tree max recursion level; negative numbers indicate a value of infinity",
        ),
        config: Optional[Path] = config_option,
):
    if level < 0:
        level = float("inf")  # type: ignore[assignment]
    settings = load_from_file(config)
    command = NotebooksCommand(settings=settings, max_depth=level)
    command.run()


@app.command(help="Edit or add a note into a notebook")
def edit(note: Path = Argument(
    ...,
    help="""A valid, settings-relative path.
Be aware that valid can also mean implicit notes, that is, pointing to a
current-day note just by its notebook name. For example, if today is
2023-04-04 and you have a notebook containing a 2023-04-04.age note,
simply pointing to the notebook's name, e.g. `halig edit notebook` will
edit the 2023-04-04.age note. Also keep in mind that the note may or may
not exist and it'll be created accordingly; the only requirement is that
the notebook folder structure is correct and exists""",
), config: Optional[Path] = config_option):
    settings = load_from_file(config)
    command = EditCommand(settings=settings, note_path=note)
    command.run()


@app.command(help="Show a note's contents")
def show(
        note: Path = Argument(
            ...,
            help="""A valid, settings-relative path.
Be aware that valid can also mean implicit notes, that is, pointing to a
current-day note just by its notebook name. For example, if today is
2023-04-04 and you have a notebook containing a 2023-04-04.age note,
simply pointing to the notebook's name, e.g. `halig show notebook` will
print the 2023-04-04.age note""",
        ),
        config: Optional[Path] = config_option,
):
    settings = load_from_file(config)
    command = ShowCommand(settings=settings, note_path=note)
    command.run()


if __name__ == "__main__":
    app()

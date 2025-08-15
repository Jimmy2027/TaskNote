"""Console script for tasknote."""

import os
from pathlib import Path
import sys
import click

from tasknote.tasknote_handler import TaskNoteHandler, TaskNoteError


@click.command()
@click.argument("task_id", type=int)
@click.option("--edit", "-e", is_flag=True)
@click.option("--config", "-c", default="~/.config/tasknote.toml")
def main(task_id, edit, config):
    """Console script for tasknote."""
    try:
        tasknote_hanlder = TaskNoteHandler.from_config(config)
        tasknote_hanlder.handle_note(task_id, edit)
    except TaskNoteError as e:
        click.secho(f"ERROR: {e}", fg="red")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

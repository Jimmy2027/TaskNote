"""Console script for tasknote."""

import os
from pathlib import Path
import sys
import click

from tasknote.tasknote_handler import TaskNoteHandler, TaskNoteError


@click.command()
@click.argument("task_id", type=str, required=False, default=None)
@click.option("--edit", "-e", is_flag=True)
@click.option("--config", "-c", default="~/.config/tasknote.toml")
@click.option("--all", "-a", "all_", is_flag=True)
def main(task_id, edit, config, all_):
    """Console script for tasknote."""
    try:
        tasknote_handler = TaskNoteHandler.from_config(config)
        if task_id is not None:
            tasknote_handler.handle_note(task_id, edit)
        else:
            tasknote_handler.list_notes(all_)
    except TaskNoteError as e:
        click.secho(f"ERROR: {e}", fg="red")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

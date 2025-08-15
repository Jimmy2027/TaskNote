"""Console script for tasknote."""

import os
from pathlib import Path
import sys
import click

from tasknote.tasknote_handler import TaskNoteHandler, TaskNoteError


@click.command()
@click.argument("task_id", type=str, required=False, default=None)
@click.option("--edit", "-e", "behavior", flag_value="edit",
              help="edit existing note")
@click.option("--view", "-v", "behavior", flag_value="view",
              help="view existing note")
@click.option("--config", "-c", default="~/.config/tasknote.toml", show_default=True,
              help="path to configuration file")
@click.option("--all", "-a", "all_", is_flag=True,
              help="also list tasks that are completed")
def main(task_id, behavior, config, all_):
    """Console script for tasknote."""
    try:
        tasknote_handler = TaskNoteHandler.from_config(config)
        if task_id is not None:
            tasknote_handler.handle_note(task_id, behavior)
        else:
            tasknote_handler.list_notes(all_)
    except TaskNoteError as e:
        click.secho(f"ERROR: {e}", fg="red")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

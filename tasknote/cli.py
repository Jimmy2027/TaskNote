"""Console script for tasknote."""

import os
from pathlib import Path
import sys
import click

from tasknote.tasknote_handler import TaskNoteHandler


@click.command()
@click.argument("task_id", type=int)
def main(task_id):
    """Console script for tasknote."""
    tasknote_hanlder = TaskNoteHandler.from_config(
        Path(os.environ["HOME"]) / ".config/tasknote.toml"
    )
    tasknote_hanlder.write_note(task_id)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

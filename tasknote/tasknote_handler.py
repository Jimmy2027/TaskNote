#!/usr/bin/env python

"""Manage Taskwarrior notes"""

import subprocess
import os
from pathlib import Path
import tomllib

EDITOR = Path(os.environ["EDITOR"])


class TaskNoteHandler:

    def __init__(self, notes_dir: Path):
        self.notes_dir = notes_dir

    @classmethod
    def from_config(cls, config_file: Path):
        toml_config = config_file.expanduser().read_text()
        toml_dict = tomllib.loads(toml_config)
        if "notes_dir" in toml_dict:
            toml_dict["notes_dir"] = Path(toml_dict["notes_dir"]).expanduser()
        return cls(**toml_dict)

    def write_note(self, task_id: int):
        """Open `$EDITOR` to take notes about task with ID `task_id`."""

        notes_file = self.create_note(task_id=task_id)

        os.chdir(self.notes_dir.parent)
        subprocess.run([EDITOR, notes_file], check=True)

    def create_note(self, task_id: int) -> Path:
        """
        Create a tasknote and modify the task description, signalising that it contains a tasknote.
        """
        # check if task_id is a digit
        if str(task_id).isdigit():
            task_uuid = subprocess.run(
                ["task", "_get", str(task_id) + ".uuid"],
                stdout=subprocess.PIPE,
                check=True,
                text=True,
            ).stdout.strip()
        else:
            task_uuid = task_id

        notes_dir = self.notes_dir
        notes_dir.mkdir(parents=True, exist_ok=True)
        notes_file = notes_dir / f"{task_uuid}.md"

        task_description = subprocess.run(
            ["task", "_get", str(task_id) + ".description"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        ).stdout.strip()

        if not notes_file.exists():
            with notes_file.open("w") as f:
                f.write(f"description: {task_description}\n\n")

        # modify the task description adding a 🗒️ to the beginning
        if not task_description.startswith("🗒️ "):
            subprocess.run(
                ["task", str(task_id), "mod", f"🗒️ {task_description}"],
                check=True,
            )

        return notes_file

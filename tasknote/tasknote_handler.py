#!/usr/bin/env python

"""Manage Taskwarrior notes"""

import subprocess
import os
from pathlib import Path
import shutil
import click
try:
    import tomllib
except ImportError:
    import tomli as tomllib

class TaskNoteError(Exception):
    pass

def resolve_directory(p: str, var="") -> Path:
    if var:
        var = var+": "
    pth = Path(p).expanduser()
    if pth.exists() and not pth.is_dir():
        raise TaskNoteError(f"{var}path is not a directory: {pth}")
    return pth

def resolve_executable(p: str, var="") -> Path:
    if var:
        var = var+": "
    pth = Path(p).expanduser()
    if pth.is_file():
        if not os.access(pth, os.X_OK):
            raise TaskNoteError(f"{var}file is not executable: {pth}")
    else:
        rp = shutil.which(p)
        if not rp:
            raise TaskNoteError(f"{var}executable not found: {p}")
        pth = Path(rp)
        if not os.access(pth, os.X_OK):
            raise TaskNoteError(f"{var}file is not executable: {pth}")
    return pth



class TaskNoteHandler:

    def __init__(self, notes_dir: str = "~/.local/share/tasknotes", 
                 task_command: str = "task",
                 note_mark: str = "[N]",
                 editor: str = "vim",
                 ):
        self.notes_dir = resolve_directory(notes_dir, "note_dir")
        self.task_command = resolve_executable(task_command, "task_command")
        self.editor = resolve_executable(editor, "editor")
        self.note_mark = note_mark

    @classmethod
    def from_config(cls, config_file: str):
        try:
            toml_config = Path(config_file).expanduser().read_text()
        except FileNotFoundError:
            click.secho(f"Warning: config file not found: {config_file}. Using defaults.", fg="yellow", err=True)
            toml_dict = {}
        else:
            toml_dict = tomllib.loads(toml_config)
        return cls(**toml_dict)

    def write_note(self, task_id: int):
        """Open `self.editor` to take notes about task with ID `task_id`."""

        notes_file = self.create_note(task_id=task_id)

        os.chdir(self.notes_dir.parent)
        subprocess.run([self.editor, notes_file], check=True)

    def create_note(self, task_id: int) -> Path:
        """
        Create a tasknote and modify the task description, signalising that it contains a tasknote.
        """
        # check if task_id is a digit
        if str(task_id).isdigit():
            task_uuid = subprocess.run(
                [self.task_command, "_get", f"{task_id}.uuid"],
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
            [self.task_command, "_get", str(task_id) + ".description"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        ).stdout.strip()

        if not notes_file.exists():
            with notes_file.open("w") as f:
                f.write(f"description: {task_description}\n\n")

        # modify the task description adding self.note_mark to the beginning
        if not task_description.startswith(self.note_mark):
            subprocess.run(
                [self.task_command, str(task_id), "mod", f"{self.note_mark} {task_description}"],
                check=True,
            )

        return notes_file

#!/usr/bin/env python

"""Manage Taskwarrior notes"""

import subprocess
import os
from pathlib import Path
import shutil
import click
import uuid
from rich.console import Console
from rich.markdown import Markdown
try:
    import tomllib
except ImportError:
    import tomli as tomllib

class TaskNoteError(Exception):
    pass

def check_uuid(u):
    try:
        uuid.UUID(u)
    except ValueError:
        return False
    return True

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
    DEFAULT_BEHAVIORS = ["edit", "view"]
    def __init__(self, notes_dir: str = "~/.local/share/tasknotes", 
                 task_command: str = "task",
                 note_mark: str = "[N]",
                 editor: list[str] = ["vim","+"],
                 default_behavior: str = "edit",
                 ):

        if default_behavior not in  self.DEFAULT_BEHAVIORS:
            raise TaskNoteError(f"Unknown default behavior: {default_behavior}. Should be one of {self.DEFAULT_BEHAVIORS}")

        self.notes_dir = resolve_directory(notes_dir, "note_dir")
        self.task_command = resolve_executable(task_command, "task_command")
        self.editor = editor
        self.editor[0] = resolve_executable(editor[0], "editor")
        self.note_mark = note_mark
        self.default_behavior = default_behavior

    @classmethod
    def from_config(cls, config_file: str):
        try:
            toml_config = Path(config_file).expanduser().read_text()
        except FileNotFoundError:
            click.secho(f"Warning: config file not found: {config_file}. Using defaults.", fg="yellow", err=True)
            toml_dict = {}
        else:
            try:
                toml_dict = tomllib.loads(toml_config)
            except tomllib.TOMLDecodeError as e:
                raise TaskNoteError(f"Configuration file: {e}")
            if isinstance(toml_dict.get("editor"),str):
                toml_dict["editor"] = [toml_dict["editor"]]
        return cls(**toml_dict)

    def handle_note(self, task_id: str, behavior: str):
        """Open `self.editor` to take notes about task with ID `task_id`."""

        note_file = self.get_note_file_path(task_id)
        if note_file.exists() and (behavior == "view" or (not behavior and self.default_behavior == "view")):
            self.print_note(note_file)
        else:
            self.create_note(task_id, note_file)


    def get_note_file_path(self, task_id: str) -> Path:
        """
        Create the note file path from task_id
        """
        try:
            task_uuid = subprocess.run(
                [self.task_command, "_get", f"{task_id}.uuid"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
                text=True,
            ).stdout.strip()
        except subprocess.CalledProcessError as e:
            raise TaskNoteError(f"Invalid task id [{task_id}]")
        if not task_uuid:
            raise TaskNoteError(f"Non-existant task id [{task_id}]")
        notes_dir = self.notes_dir
        notes_dir.mkdir(parents=True, exist_ok=True)
        note_file = notes_dir / f"{task_uuid}.md"
        return note_file


    def print_note(self, note_file):
        markdown_text = note_file.open("r").read()
        markdown_text += "\n---" # add an horizontal line at the end of the text
        console = Console()
        console.print(Markdown(markdown_text))


    def create_note(self, task_id: str, note_file):
        """
        Create a tasknote and modify the task description, signalising that it contains a tasknote.
        """

        task_description = subprocess.run(
            [self.task_command, "_get", str(task_id) + ".description"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        ).stdout.strip()

        if not note_file.exists():
            with note_file.open("w") as f:
                f.write(f"# description: {task_description}\n\n")

        # modify the task description adding self.note_mark to the beginning
        if not task_description.startswith(self.note_mark):
            subprocess.run(
                [self.task_command, str(task_id), "mod", f"{self.note_mark} {task_description}"],
                check=True,
            )

        os.chdir(self.notes_dir.parent)
        subprocess.run(self.editor+[note_file], check=True)

    def list_notes(self, all_=False):
        if not self.notes_dir.exists(): # no note taken yet
            return
        if not self.notes_dir.is_dir():
            raise TaskNoteError(f"[{self.notes_dir} is not a directory")

        task_list = [f.stem for f in self.notes_dir.iterdir() if check_uuid(f.stem)]
        if task_list:
            subprocess.run(
                [self.task_command, "all" if all_ else "list", *task_list],
                check=False) # task returns non-null exit status if no tasks

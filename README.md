# Markdown Task Notes for Taskwarrior

This is a simple python package that allows to add markdown notes to Taskwarrior tasks.

## Installation

### PiP

```bash
$ git clone https://github.com/Jimmy2027/TaskNote.git
$ cd TaskNote
$ pip install .
```

### Portage

The package is made available in [a portage overlay](https://github.com/Jimmy2027/overlay).

```bash
root@host # emerge tasknote
```

## Setup

Write a tasknote.toml file to `~/.config/tasknote.toml`, configuring the path to the tasknotes.

Example:

```toml
# ~/.config/tasknote.toml
notes_dir = "~/.local/share/tasknotes"
```

## Usage

```bash
$ tasknote {task_id}

```

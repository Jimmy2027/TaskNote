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

```shell
root@host $ emerge tasknote
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
$ task add "this is a test"
Created task 1.
$ tasknote 1
# Creates the tasknote and opens the default editor
# Also adds a note emoji to the task description
Modifying task 1 '🗒 this is a test'.

```

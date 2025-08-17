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
$ tasknote --help
Usage: tasknote [OPTIONS] [TASK_ID]

  Console script for tasknote.

Options:
  -e, --edit
  -c, --config TEXT
  -a, --all
  --help             Show this message and exit.
```

### Example usage

Creating 2 tasks to work on.

```bash
$ task add this is my first task
Created task 1.
$ task add this is my second task
Created task 2.
$ task

ID Age  Description            Urg 
 1 2s   this is my first task     0
 2 1s   this is my second task    0

2 tasks
```

Calling `tasknote` on task 1. Since no note exists, it is created. A mark is added to the task's description.

```bash
$ tasknote 1
## editor is run here to edit note for task 1
Modifying task 1 '[N] this is my first task'.
Modified 1 task.
$ task

ID Age   Description               Urg 
 1 16s   [N] this is my first task    0
 2 15s   this is my second task       0

2 tasks
```

If `tasknote` is called again on the same task, since the note exist, it is diplayed, rendered as markdown.

```bash
$ tasknote 1
```
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 description: this is my first task                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


                             First section                              

Hello, this is an example.                                              

 • point 1                                                              
 • point 2      
```

To edit it again, use the ```--edit``` or ```-e``` flag.

```bash
$ tasknote 1 -e
```

Giving no arguments, `tasknote` will display the list of pending tasks with a note.

```bash
$ tasknote

ID Age   Description                   Urg 
 1 41s   [N] this is my first task        0

1 task
$ task 1 done
Completed task 1 '[N] this is my first task'.
Completed 1 task.
$ tasknote
No matches.
```

To get the completed tasks too, use the ```--all``` or ```-a``` flag.

```bash
$ tasknote -a
True

ID St UUID     Age   Done Description              
 - C  ee03aec6 50s   7s   [N] this is my first task
```

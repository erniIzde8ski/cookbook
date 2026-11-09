"""Loads dodo file (a python module) and convert them to 'tasks'"""

from collections.abc import Callable
from collections.abc import Generator
from types import ModuleType
from typing import Any

from .task import Task

initial_workdir = ...
TASK_STRING = ...

def flat_generator(
    gen, gen_doc=...
) -> Generator[tuple[Any, Any | str] | tuple[Any, str], Any]:
    """return only values from generators
    if any generator yields another generator it is recursively called
    """

def get_module(dodo_file, cwd=..., seek_parent=...) -> ModuleType:
    """
    Find python module defining tasks, it is called "dodo" file.

    @param dodo_file(str): path to file containing the tasks
    @param cwd(str): path to be used cwd, if None use path from dodo_file
    @param seek_parent(bool): search for dodo_file in parent paths if not found
    @return (module) dodo module
    """

def create_after(executed=..., target_regex=..., creates=...) -> Callable[..., Any]:
    """Annotate a task-creator function with delayed loader info"""

def task_params(param_def=...) -> Callable[..., Any]:
    """Annotate a task-creator function with definition of parameters
    to get arguments from cmd line
    """

def load_tasks(
    namespace, command_names=..., allow_delayed=..., args=..., config=..., task_opts=...
) -> list[Any]:
    """Find task-creators and create tasks

    @param namespace: (dict) containing the task creators, it might
                        contain other stuff
    @param command_names: (list - str) blacklist for task names
    @param allow_delayed: (bool) if True ignore doit_crate_after['executed']
    @param args: (list - str) command line arguments (task names and option arguments)
    @param config: (dict) configuration taken from TOML and INI files

    `load_all == False` is used by the runner to delay the creation of
    tasks until a dependent task is executed. This is only used by the `run`
    command, other commands should always load all tasks since it wont execute
    any task.

    @return task_list (list) of Tasks in the order they were defined on the file
    """

def load_doit_config(dodo_module) -> dict[Any, Any]:
    """
    @param dodo_module (dict) dict with module members
    """

def generate_tasks(
    func_name, gen_result, gen_doc=...
) -> tuple[Task] | list[Task] | list[Any] | tuple[()]:
    """Create tasks from a task generator result.

    @param func_name: (string) name of taskgen function
    @param gen_result: value returned by a task generator function
                       it can be a dict or generator (generating dicts)
    @param gen_doc: (string/None) docstring from the task generator function
    @param param_def: (dict) additional task parameter definitions
                      passed down from generator
    @return: (list - Task)
    """

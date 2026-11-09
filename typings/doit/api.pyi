"""APIs to execute doit in non standard way.

- run(): shortcut to get tasks from current module/dict (instead of dodo.py).
- run_tasks(): to be used by custom CLIs, run tasks without CLI parsing.

"""

from typing import Any

def run(task_creators):
    """run doit using task_creators

    @param task_creators: module or dict containing task creators
    """

def run_tasks(loader, tasks, extra_config=...) -> Any:
    """run DoitMain instance with speficied tasks and parameters

    :params tasks: list of task names (str)
    """

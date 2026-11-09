"""Control tasks execution order"""

from collections.abc import Callable
from collections.abc import Generator
from typing import Any

class RegexGroup:
    """Helper to keep track of all delayed-tasks which regexp target
    matches the target specified from command line.
    """

    def __init__(self, target, tasks) -> None: ...

class TaskControl:
    """Manages tasks inter-relationship

    There are 3 phases
      1) the constructor gets a list of tasks and do initialization
      2) 'process' the command line options for tasks are processed
      3) 'task_dispatcher' dispatch tasks to runner

    Process dependencies and targets to find out the order tasks
    should be executed. Also apply filter to exclude tasks from
    execution. And parse task cmd line options.

    @ivar tasks: (dict) Key: task name ([taskgen.]name)
                               Value: L{Task} instance
    @ivar targets: (dict) Key: fileName
                          Value: task_name
    """

    def __init__(self, task_list, auto_delayed_regex=...) -> None: ...
    @staticmethod
    def set_implicit_deps(targets, task_list) -> None:
        """set/add task_dep based on file_dep on a target from another task
        @param targets: (dict) fileName -> task_name
        @param task_list: (list - Task) task with newly added file_dep
        """

    @staticmethod
    def add_implicit_task_dep(targets, task, deps_list) -> None:
        """add implicit task_dep for `task` for newly added `file_dep`

        @param targets: (dict) fileName -> task_name
        @param task: (Task) task with newly added file_dep
        @param dep_list: (list - str): list of file_dep for task
        """

    def process(self, task_selection) -> None:
        """
        @param task_selection: list of strings with task names/params
        @return (list - string) each element is the name of a task
        """

    def task_dispatcher(self) -> TaskDispatcher:
        """return a TaskDispatcher generator"""

class ExecNode:
    """Each task will have an instance of this.
    This used to keep track of waiting events and the generator for dep nodes

    @ivar run_status (str): contains the result of Dependency.get_status().status
            modified by runner, value can be:
           - None: not processed yet
           - run: task is selected to be executed (it might be running or
                   waiting for setup)
           - ignore: task wont be executed (user forced deselect)
           - up-to-date: task wont be executed (no need)
           - done: task finished its execution
    """

    def __init__(self, task, parent) -> None: ...
    def reset_task(self, task, generator) -> None:
        """reset task & generator after task is created by its own `loader`"""

    def parent_status(self, parent_node) -> None: ...
    def step(self) -> None:
        """get node's next step"""

def no_none(decorated) -> Callable[..., Generator[Any, Any]]:
    """decorator for a generator to discard/filter-out None values"""

class TaskDispatcher:
    """Dispatch another task to be selected/executed, mostly handle with MP

    Note that a dispatched task might not be ready to be executed.
    """

    def __init__(self, tasks, targets, selected_tasks) -> None: ...

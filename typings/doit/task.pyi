from typing import Any
from typing import Literal
from typing import LiteralString

from .action import BaseAction
from .action import CmdAction
from .action import PythonAction
from .dependency import UptodateCalculator
from .exceptions import BaseFail
from .exceptions import TaskError
from .exceptions import TaskFailed

"Tasks are the main abstractions managed by doit"

def first_line(doc) -> Literal[""]:
    """extract first non-blank line from text, to extract docstring title"""

class DelayedLoader:
    """contains info for delayed creation of tasks from a task-creator

    :ivar creator: reference to task-creator function
    :ivar task_dep: (str) name of task that should be executed before the
                    the loader call the creator function
    :ivar basename: (str) basename used when creating tasks
                   This is used when doit creates new tasks to handle
                   tasks and targets specified on command line
    :ivar target_regex: (str) regex for all targets that this loader tasks
                        will create
    :ivar created: (bool) whether this creator was already executed or not
    """

    def __init__(self, creator, executed=..., target_regex=..., creates=...) -> None: ...

DelayedLoaded = ...

class Stream:
    """Control task output stream verbosity

    :ivar verbosity: 0,1,2 see Task.execute

    Priority is given by:
    1) command line -> force_global=True
    2) task value
    3) other config (INI, DOIT_CONFIG)
    """

    def __init__(self, verbosity, force_global=...) -> None: ...
    def effective_verbosity(self, task_verbosity) -> int:
        """return effective verbosity used on task"""

class IOConfig:
    def __init__(self, io_data) -> None: ...

class Task:
    """Task

    @ivar name string
    @ivar actions: list - L{BaseAction}
    @ivar clean_actions: list - L{BaseAction}
    @ivar loader (DelayedLoader)
    @ivar teardown (list - L{BaseAction})
    @ivar targets: (list -string)
    @ivar task_dep: (list - string)
    @ivar wild_dep: (list - string) task dependency using wildcard *
    @ivar file_dep: (set - string)
    @ivar calc_dep: (set - string) reference to a task
    @ivar dep_changed (list - string): list of file-dependencies that changed
          (are not up_to_date). this must be set before
    @ivar uptodate: (list - bool/None) use bool/computed value instead of
                                       checking dependencies
    @ivar value_savers (list - callables) that return dicts to be added to
                           task values. Always executed on main process.
                           To be used by `uptodate` implementations.
    @ivar setup_tasks (list - string): references to task-names
    @ivar subtask_of: (string) indicate this task is a subtask of task name
    @ivar has_subtask: (bool) indicate this task has subtasks
    @ivar result: (str) last action "result". used to check task-result-dep
    @ivar values: (dict) values saved by task that might be used by other tasks
    @ivar getargs: (dict) values from other tasks
    @ivar doc: (string) task documentation
    @ivar meta: (dict) extra info from user/plugin not directly used by doit

    @ivar options: (dict) calculated params values (from getargs and taskopt)
    @ivar taskopt: (cmdparse.CmdParse)
    @ivar pos_arg: (str) name of parameter in action to receive positional
                     parameters from command line
    @ivar pos_arg_val: (list - str) list of positional parameters values
    @ivar custom_title: function reference that takes a task object as
                        parameter and returns a string.
    """

    DEFAULT_VERBOSITY = ...
    string_types = ...
    valid_attr = ...

    def __init__(
        self,
        name,
        actions,
        file_dep=...,
        targets=...,
        task_dep=...,
        uptodate=...,
        calc_dep=...,
        setup=...,
        clean=...,
        teardown=...,
        subtask_of=...,
        has_subtask=...,
        doc=...,
        params=...,
        pos_arg=...,
        verbosity=...,
        io=...,
        title=...,
        getargs=...,
        watch=...,
        meta=...,
        loader=...,
    ) -> None:
        """sanity checks and initialization

        @param params: (list of dict for parameters) see cmdparse.CmdOption
        """
    _expand_map = ...

    def update_deps(self, deps) -> None:
        """expand all kinds of dep input"""

    def init_options(self, args=...) -> None:
        """Put default values on options.

        This function will only initialize task options once. If provided the args
        parameter will be parsed for command line arguments intended for this task.

        Return value: unparsed command line task arguments or None.
        """

    @staticmethod
    def check_attr(task, attr, value, valid) -> None:
        """check input task attribute is correct type/value

        @param task (string): task name
        @param attr (string): attribute name
        @param value: actual input from user
        @param valid (list): of valid types/value accepted
        @raises InvalidTask if invalid input
        """

    @property
    def actions(self) -> list[BaseAction | CmdAction | PythonAction]:
        """lazy creation of action instances"""

    def save_extra_values(self) -> None:
        """run value_savers updating self.values"""

    def overwrite_verbosity(self, stream) -> None: ...
    def execute(self, stream) -> TaskError | TaskFailed | BaseFail | None:
        """Executes the task.
        @return failure: see CmdAction.execute
        """

    def execute_teardown(self, stream) -> TaskError | TaskFailed | BaseFail | None:
        """Executes task's teardown
        @return failure: see CmdAction.execute
        """

    def clean(self, outstream, dryrun) -> None:
        """Execute task's clean
        @ivar outstream: 'write' output into this stream
        @ivar dryrun (bool): if True clean tasks are not executed
                             (just print out what would be executed)
        """

    def title(self):
        """String representation on output.

        @return: (str) Task name and actions
        """

    def __getstate__(self) -> dict[str, Any]:
        """remove attributes that never used on process that only execute tasks"""

    def pickle_safe_dict(self) -> dict[str, Any]:
        """remove attributes that might contain unpickleble content
        mostly probably closures
        """

    def update_from_pickle(self, pickle_obj) -> None:
        """update self with data from pickled Task"""

    def __eq__(self, other) -> bool: ...
    def __lt__(self, other) -> bool:
        """used on default sorting of tasks (alphabetically by name)"""

def dict_to_task(task_dict) -> Task:
    """Create a task instance from dictionary.

    The dictionary has the same format as returned by task-generators
    from dodo files.

    @param task_dict (dict): task representation as a dict.
    @raise InvalidTask: If unexpected fields were passed in task_dict
    """

def clean_targets(task, dryrun) -> None:
    """remove all targets from a task"""

class result_dep(UptodateCalculator):
    """check if result of the given task was modified"""

    def __init__(self, dep_task_name, setup_dep=...) -> None:
        """
        :param setup_dep: controls if dependent task is task_dep or setup
        """

    def configure_task(self, task) -> None:
        """to be called by doit when create the task"""

    def __call__(self, task, values) -> Literal[False]:
        """return True if result is the same as last run"""

    def __repr__(self) -> LiteralString: ...

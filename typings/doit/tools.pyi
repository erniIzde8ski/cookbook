from typing import Literal
from typing import LiteralString

from doit.task import result_dep as result_dep

from .action import CmdAction
from .action import PythonAction
from .exceptions import TaskError
from .exceptions import TaskFailed

"extra goodies to be used in dodo files"

def create_folder(dir_path) -> None:
    """create a folder in the given path if it doesnt exist yet."""

def title_with_actions(task) -> str:
    """return task name task actions"""

def run_once(task, values):
    """execute task just once
    used when user manually manages a dependency
    """

class config_changed:
    """check if passed config was modified
    @var config (str) or (dict)
    @var encoder (json.JSONEncoder) Encoder used to convert non-default values.
    """

    def __init__(self, config, encoder=...) -> None: ...
    def configure_task(self, task) -> None: ...
    def __call__(self, task, values) -> Literal[False]:
        """return True if config values are UNCHANGED"""

    def __repr__(self) -> LiteralString: ...

class timeout:
    """add timeout to task

    @param timeout_limit: (datetime.timedelta, int) in seconds

    if the time elapsed since last time task was executed is bigger than
    the "timeout" time the task is NOT up-to-date
    """

    def __init__(self, timeout_limit) -> None: ...
    def __call__(self, task, values) -> Literal[False]: ...

class check_timestamp_unchanged:
    """check if timestamp of a given file/dir is unchanged since last run.

    The C{cmp_op} parameter can be used to customize when timestamps are
    considered unchanged, e.g. you could pass L{operator.ge} to also consider
    e.g. files reverted to an older copy as unchanged; or pass a custom
    function to completely customize what unchanged means.

    If the specified file does not exist, an exception will be raised.  Note
    that if the file C{fn} is a target of another task you should probably add
    C{task_dep} on that task to ensure the file is created before checking it.
    """

    def __init__(self, file_name, time=..., cmp_op=...) -> None:
        """initialize the callable

        @param fn: (str) path to file/directory to check
        @param time: (str) which timestamp field to check, can be one of
                     (atime, access, ctime, status, mtime, modify)
        @param cmp_op: (callable) takes two parameters (prev_time, current_time)
                   should return True if the timestamp is considered unchanged

        @raises ValueError: if invalid C{time} value is passed
        """

    def __call__(self, task, values) -> Literal[False]:
        """register action that saves the timestamp and check current timestamp

        @raises OSError: if cannot stat C{self._file_name} file
                         (e.g. doesn't exist)
        """

class LongRunning(CmdAction):
    """Action to handle a Long running shell process,
    usually a server or service.
    Properties:

        * the output is never captured
        * it is always successful (return code is not used)
        * "swallow" KeyboardInterrupt
    """

    def execute(self, out=..., err=...) -> None: ...

InteractiveAction = LongRunning

class Interactive(CmdAction):
    """Action to handle Interactive shell process:

    * the output is never captured
    """

    def execute(self, out=..., err=...) -> TaskFailed | None: ...

class PythonInteractiveAction(PythonAction):
    """Action to handle Interactive python:

    * the output is never captured
    * it is successful unless a exception is raised
    """

    def execute(self, out=..., err=...) -> TaskError | None: ...

def set_trace() -> None:
    """start debugger, make sure stdout shows pdb output.
    output is not restored.
    """

def load_ipython_extension(ip=...) -> None:
    """
    Defines a ``%doit`` magic function[1] that discovers and execute tasks
    from IPython's interactive variables (global namespace).

    It will fail if not invoked from within an interactive IPython shell.

    .. Tip::
        To permanently add this magic-function to your IPython, create a new
        script inside your startup-profile
        (``~/.ipython/profile_default/startup/doit_magic.ipy``) with the
        following content:

            %load_ext doit
            %reload_ext doit
            %doit list

    [1] http://ipython.org/ipython-doc/dev/interactive/tutorial.html#magic-functions
    """

register_doit_as_IPython_magic = ...

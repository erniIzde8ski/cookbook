"""Implements actions used by doit tasks"""

from typing import Any
from typing import Literal

from .exceptions import TaskError
from .exceptions import TaskFailed

def normalize_callable(ref) -> list[Any] | list[Any | tuple[()] | dict[Any, Any]]:
    """return a list with (callable, *args, **kwargs)
    ref can be a simple callable or a tuple
    """

class BaseAction:
    """Base class for all actions"""

class CmdAction(BaseAction):
    """
    Command line action. Spawns a new process.

    @ivar action(str,list,callable): subprocess command string or string list,
         see subprocess.Popen first argument.
         It may also be a callable that generates the command string.
         Strings may contain python mappings with the keys: dependencies,
         changed and targets. ie. "zip %(targets)s %(changed)s"
    @ivar task(Task): reference to task that contains this action
    @ivar save_out: (str) name used to save output in `values`
    @ivar shell: use shell to execute command
                 see subprocess.Popen `shell` attribute
    @ivar encoding (str): encoding of the process output
    @ivar decode_error (str): value for decode() `errors` param
                              while decoding process output
    @ivar pkwargs: Popen arguments except 'stdout' and 'stderr'
    """

    STRING_FORMAT = ...

    def __init__(
        self,
        action,
        task=...,
        save_out=...,
        shell=...,
        encoding=...,
        decode_error=...,
        buffering=...,
        **pkwargs,
    ) -> None:
        """
        :ivar buffering: (int) stdout/stderr buffering.
               Not to be confused with subprocess buffering
               -   0 -> line buffering
               -   positive int -> number of bytes
        """

    @property
    def action(self) -> str | list[Any]: ...
    def execute(self, out=..., err=...) -> TaskError | TaskFailed | None:
        """
        Execute command action

        both stdout and stderr from the command are captured and saved
        on self.out/err. Real time output is controlled by parameters
        @param out: None - no real time output
                    a file like object (has write method)
        @param err: idem
        @return failure:
            - None: if successful
            - TaskError: If subprocess return code is greater than 125
            - TaskFailed: If subprocess return code isn't zero (and
        not greater than 125)
        """

    def expand_action(self) -> str | list[Any]:
        """Expand action using task meta informations if action is a string.
        Convert `Path` elements to `str` if action is a list.
        @returns: string -> expanded string if action is a string
                  list - string -> expanded list of command elements
        """

class Writer:
    """Write to N streams.

    This is used on python-actions to allow the stream to be output to terminal
    and captured at the same time.
    """

    def __init__(self, *writers) -> None:
        """@param writers - file stream like objects"""

    def add_writer(self, stream, *, is_original=...) -> None:
        """adds a stream to the list of writers
        @param is: (bool) if specified overwrites real isatty from stream
        """

    def write(self, text) -> None:
        """write 'text' to all streams"""

    def flush(self) -> None:
        """flush all streams"""

    def isatty(self) -> Literal[False]: ...
    def fileno(self): ...

class PythonAction(BaseAction):
    """Python action. Execute a python callable.

    @ivar py_callable: (callable) Python callable
    @ivar args: (sequence)  Extra arguments to be passed to py_callable
    @ivar kwargs: (dict) Extra keyword arguments to be passed to py_callable
    @ivar task(Task): reference to task that contains this action
    @ivar pm_pdb: if True drop into PDB on exception when executing task
    """

    pm_pdb = ...

    def __init__(self, py_callable, args=..., kwargs=..., task=...) -> None: ...
    def execute(self, out=..., err=...) -> TaskError | TaskFailed | None:
        """Execute command action

        both stdout and stderr from the command are captured and saved
        on self.out/err. Real time output is controlled by parameters
        @param out: None - no real time output
                    a file like object (has write method)
        @param err: idem

        @return failure: see CmdAction.execute
        """

def create_action(action, task_ref, param_name) -> BaseAction | CmdAction | PythonAction:
    """
    Create action using proper constructor based on the parameter type

    @param action: Action to be created
    @type action: L{BaseAction} subclass object, str, tuple or callable
    @param task_ref: Task object this action belongs to
    @param param_name: str, name of task param. i.e actions, teardown, clean
    @raise InvalidTask: If action parameter type isn't valid
    """

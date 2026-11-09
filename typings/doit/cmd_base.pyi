from collections.abc import Generator
from typing import Any
from typing import LiteralString

from doit.dependency import DbmDB
from doit.dependency import JSONCodec
from doit.dependency import JsonDB
from doit.dependency import MD5Checker
from doit.dependency import SqliteDB
from doit.dependency import TimestampChecker

from .cmdparse import CmdOption
from .cmdparse import CmdParse

def version_tuple(ver_in) -> list[Any]:
    """convert a version string or tuple into a 3-element tuple with ints
    Any part that is not a number (dev0, a2, b4) will be converted to -1
    """

class Command:
    """third-party should subclass this for commands that do no use tasks

    :cvar name: (str) name of sub-cmd to be use from cmdline
    :cvar doc_purpose: (str) single line cmd description
    :cvar doc_usage: (str) describe accepted parameters
    :cvar doc_description: (str) long description/help for cmd
    :cvar cmd_options:
          (list of dict) see cmdparse.CmdOption for dict format
    """

    name = ...
    doc_purpose = ...
    doc_usage = ...
    doc_description = ...
    cmd_options = ...
    execute_tasks = ...

    def __init__(self, config=..., bin_name=..., opt_vals=..., **kwargs) -> None:
        """configure command

        :param bin_name: str - name of command line program
        :param config: dict

        Set extra configuration values, this vals can come from:
         * directly passed when using the API - through DoitMain.run()
         * from an INI configuration file
        """

    @classmethod
    def get_name(cls) -> str:
        """get command name as used from command line"""

    @property
    def cmdparser(self) -> CmdParse:
        """get CmdParser instance for this command

        initialize option values:
          - Default are taken from harded option definition
          - Defaults are overwritten from user's cfg (INI) file
        """

    def get_options(self) -> list[CmdOption]:
        """@reutrn list of CmdOption"""

    def execute(self, opt_values, pos_args):
        """execute command
        :param opt_values: (dict) with cmd_options values
        :param pos_args: (list) of cmd-line positional arguments
        """

    def parse_execute(self, in_args):
        """helper. just parse parameters and execute command

        @args: see method parse
        @returns: result of self.execute
        """

    def help(self) -> LiteralString:
        """return help text"""

opt_depfile = ...
opt_backend = ...
opt_codec = ...
opt_check_file_uptodate = ...
opt_dodo = ...
opt_cwd = ...
opt_seek_file = ...

class TaskLoader:
    def __init__(self) -> None: ...

class TaskLoader2:
    """Interface of task loaders with new-style API.

    :cvar cmd_options:
          (list of dict) see cmdparse.CmdOption for dict format

    This API separates the loading of the configuration and the loading
    of the actual tasks, which enables additional elements to be available
    during task creation.
    """

    API = ...
    cmd_options = ...

    def __init__(self) -> None: ...
    def setup(self, opt_values) -> None:
        """Delayed initialization.

        To be implemented if the data is needed by derived classes.

        :param opt_values: (dict) with values for cmd_options
        """

    def load_doit_config(self):
        """Load doit configuration.

        The method must not be called before invocation of ``setup``.

        :return: (dict) Dictionary of doit configuration values.
        """

    def load_tasks(self, cmd, pos_args):
        """Load tasks.

        The method must not be called before invocation of ``load_doit_config``.

        :param cmd: (doit.cmd_base.Command) current command being executed
        :param pos_args: (list str) positional arguments from command line
        :return: (List[Task])
        """

class NamespaceTaskLoader(TaskLoader2):
    """Implementation of a loader of tasks from an abstract namespace.

    A namespace is simply a dictionary to objects like functions and
    objects. See the derived classes for some concrete namespace types.
    """

    def __init__(self) -> None: ...
    def load_doit_config(self) -> dict[Any, Any]: ...
    def load_tasks(self, cmd, pos_args) -> list[Any]: ...

class ModuleTaskLoader(NamespaceTaskLoader):
    """load tasks from a module/dictionary containing task generators
    Usage: `ModuleTaskLoader(my_module)` or `ModuleTaskLoader(globals())`
    """

    def __init__(self, mod_dict) -> None: ...

class DodoTaskLoader(NamespaceTaskLoader):
    """default task-loader create tasks from a dodo.py file"""

    cmd_options = ...

    def setup(self, opt_values) -> None: ...

def get_loader(config, task_loader=..., cmds=...) -> DodoTaskLoader | Any:
    """get task loader and configure it

    :param config: (dict) the whole config from INI
    :param task_loader: a TaskLoader class
    :param cmds: dict of available commands
    """

type DbBackend = DbmDB | JsonDB | SqliteDB

class DoitCmdBase(Command):
    """
    subclass must define:
    cmd_options => list of option dictionary (see CmdOption)
    _execute => method, argument names must be option names
    """

    base_options = ...

    def __init__(self, task_loader, cmds=..., **kwargs) -> None: ...
    def get_options(self) -> list[CmdOption]:
        """from base class - merge base_options, loader_options and cmd_options"""

    @staticmethod
    def check_minversion(minversion) -> None:
        """check if this version of doit satisfy minimum required version
        Minimum version specified by configuration on dodo.
        """

    def get_checker_cls(self, check_file_uptodate) -> type[MD5Checker | TimestampChecker]:
        """return checker class to be used by dep_manager"""

    def get_codec_cls(self, codec) -> type[JSONCodec]:
        """return a class used to encode or decode python-action results"""

    def get_backends(self) -> dict[str, DbBackend]:
        """return PluginDict of DB backends, including core and plugins"""

    def execute(self, params, args):
        """load dodo.py, set attributes and call self._execute

        :param params: instance of cmdparse.DefaultUpdate
        :param args: list of string arguments (containing task names)
        """

def check_tasks_exist(tasks, name_list, skip_wildcard=...) -> None:
    """check task exist"""

def tasks_and_deps_iter(tasks, sel_tasks, yield_duplicates=...) -> Generator[Any, Any]:
    """iterator of select_tasks and its dependencies

    @param tasks (dict - Task)
    @param sel_tasks(list - str)
    """

def subtasks_iter(tasks, task) -> Generator[Any, Any]:
    """find all subtasks for a given task
    @param tasks (dict - Task)
    @param task (Task)
    """

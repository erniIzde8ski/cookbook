"""doit CLI (command line interface)"""

from collections import defaultdict
from configparser import ConfigParser
from types import ModuleType
from typing import Any
from typing import Literal

from .plugin import PluginDict

_CMDLINE_VARS = ...

def reset_vars() -> None: ...
def get_var(name, default=...) -> None: ...
def set_var(name, value) -> None: ...

class DoitConfig:
    """Parse and store values taken from INI and TOML configuration files"""

    _TOML_LIBS = ...
    PLUGIN_TYPES = ...

    def __init__(self) -> None: ...
    def loads(self, config_filenames) -> None: ...
    @property
    def toml(self) -> ModuleType | None:
        """get available toml lib, if any"""

    def as_dict(self) -> defaultdict[Any, dict[Any, Any]]:
        """return values in legacy dict format"""

    @staticmethod
    def load_config_ini(filenames) -> ConfigParser:
        """read config from INI files

        :param files: str or list of str.
                      Like ConfigParser.read() param filenames
        """

    def load_config_toml(self, filename, prefix) -> dict[Any, Any]:
        """read config from a TOML file, adapt to ConfigParser structure

        :param filename: str

        returns an empty dictionary if tool.doit is not present in the parsed data
        """

class DoitMain:
    BIN_NAME = ...
    DOIT_CMDS = ...

    def __init__(self, task_loader=..., config_filenames=..., extra_config=...) -> None:
        """
        :param extra_config: dict of extra argument values (by argument name)
                             This is parameter is only used by explicit API call.
        """

    @staticmethod
    def print_version() -> None:
        """print doit version (includes path location)"""

    def get_cmds(self) -> PluginDict:
        """get all sub-commands
        :return dict: name - Command class
        """

    def process_args(self, cmd_args) -> list[Any]:
        """process cmd line set "global" variables/parameters
        return list of args without processed variables
        """

    def get_commands(self):
        """Notice for application subclassing DoitMain with old API"""

    def run(self, all_args) -> Any | Literal[0, 3]:
        """entry point for all commands

        :param all_args: list of string arguments from command line

        return codes:
          0: tasks executed successfully
          1: one or more tasks failed
          2: error while executing a task
          3: error before task execution starts,
             in this case the Reporter is not used.
             So be aware if you expect a different formatting (like JSON)
             from the Reporter.
        """

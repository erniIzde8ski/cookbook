"""Parse command line options and execute it.

Built on top of getopt. optparse can't handle sub-commands.
"""

from typing import Any
from typing import Literal
from typing import LiteralString

class DefaultUpdate(dict):
    """A dictionary that has an "update_defaults" method where
    only items with default values are updated.

    This is used when you have a dict that has multiple source of values
    (i.e. hardcoded, config file, command line). And values are updated
    beginning from the source with higher priority.

    A default value is added with the method set_default or add_defaults.
    """

    def __init__(self, *args, **kwargs) -> None: ...
    def set_default(self, key, value) -> None:
        """set default value for given key"""

    def add_defaults(self, source) -> None:
        """add default values from another dict
        @param source: (dict)"""

    def update_defaults(self, update_dict) -> None:
        """like dict.update but do not update items that have
        a non-default value"""

    def __setitem__(self, key, value) -> None:
        """overwrite to keep track of _non_default_keys"""

class CmdParseError(Exception):
    """Error parsing options"""

class CmdOption:
    """a command line option

    - name (string) : variable name
    - section (string): meta info used to group entries when generating help
    - default (value from its type): default value
    - type (type): type of the variable. must be able to be initialized
                   taking a single string parameter.
                   if type is bool. option is just a flag. and if present
                   its value is set to True.
    - short (string): argument short name
    - long (string): argument long name
    - inverse (string): argument long name to be the inverse of the default
                        value (only used by boolean options)
    - choices(list - 2-tuple str): sequence of 2-tuple of choice name,
                                   choice description.
    - help (string): option description
    """

    def __init__(self, opt_dict) -> None: ...
    def set_default(self, val) -> None:
        """set default value, value is already the expected type"""

    def validate_choice(self, given_value) -> None:
        """raise error is value is not a valid choice"""
    _boolean_states = ...

    def str2boolean(self, str_val) -> bool:
        """convert string to boolean"""

    def str2type(self, str_val) -> bool | list[str]:
        """convert string value to option type value"""

    def help_param(self) -> LiteralString:
        """return string of option's short and long name
        i.e.:   -f ARG, --file=ARG
        """

    def help_choices(self) -> LiteralString | Literal[""]:
        """return string with help for option choices"""

    def help_doc(self) -> list[Any]:
        """return list of string of option's help doc

        Note this is used only to display help on tasks.
        For commands a better and more complete version is used.
        see cmd_base:Command.help
        """

class CmdParse:
    """Process string with command options

    @ivar options: (list - CmdOption)
    """

    _type = ...

    def __init__(self, options) -> None: ...
    def __contains__(self, key) -> bool: ...
    def __getitem__(self, key): ...
    @property
    def options(self) -> list[Any]:
        """return list of options for backward compatibility"""

    def get_short(self) -> Literal[""]:
        """return string with short options for getopt"""

    def get_long(self) -> list[Any]:
        """return list with long options for getopt"""

    def get_option(
        self, opt_str
    ) -> tuple[Any, Literal[False]] | tuple[Any, Literal[True]] | tuple[None, None]:
        """return tuple
        - CmdOption from matching opt_str. or None
        - (bool) matched inverse
        """

    def overwrite_defaults(self, new_defaults) -> None:
        """overwrite self.options default values

        This values typically come from an INI file
        """

    def parse_only(self, in_args, params=...) -> tuple[Any | dict[Any, Any], Any]:
        """parse arguments into options(params) and positional arguments

        @param in_args (list - string): typically sys.argv[1:]
        @return params, args
             params(dict): params contain the actual values from the options.
                           where the key is the name of the option.
             pos_args (list - string): positional arguments
        """

    def parse(self, in_args) -> tuple[DefaultUpdate | dict[Any, Any], Any]:
        """parse arguments into options(params) and positional arguments

        Also get values from shell ENV.

        Returned params is a `DefaultUpdate` type and includes
        an item for every option.

        @param in_args (list - string): typically sys.argv[1:]
        @return params, args
             params(dict): params contain the actual values from the options.
                           where the key is the name of the option.
             pos_args (list - string): positional arguments
        """

class TaskParse(CmdParse):
    """Process string with command options (for tasks)"""

    _type = ...

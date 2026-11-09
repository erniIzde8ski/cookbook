from collections.abc import Callable
from importlib.metadata import EntryPoints
from typing import Any
from typing import LiteralString

def entry_points_impl() -> Callable[..., EntryPoints]: ...

class PluginEntry:
    """A Plugin entry point

    The entry-point is not loaded/imported on creation.
    Use the method `get()` to import the module and get the attribute.
    """

    class Sentinel: ...
    NOT_LOADED = ...

    def __init__(self, category, name, location) -> None:
        """
        :param category str: plugin category name
        :param name str: plugin name (as used by doit)
        :param location str: python object location as <module>:<attr>
        """

    def __repr__(self) -> LiteralString: ...
    def get(self) -> Any | Sentinel:
        """return obj, get from cache or load"""

    def load(self) -> Any:
        """load/import reference to obj from named module/obj"""

class PluginDict(dict):
    """Item values *might* be a PluginEntry or a direct reference to class/obj.

    Values should not be accessed directly, use `get_plugin()`
    to make sure the plugin is loaded.

    Typically, one dict is created for each kind of plugin.
    doit supports 4 categories:
     - COMMAND
     - LOADER
     - BACKEND
     - REPORTER
    """

    entry_point_prefix = ...

    def add_plugins(self, cfg_data, category) -> None:
        """read all items from a ConfigParser section containing plugins & entry-points.

        Plugins from entry-point have higher priority
        """

    def get_plugin(self, key) -> Any | PluginEntry.Sentinel:
        """load and return a single plugin"""

    def to_dict(self) -> dict[Any, Any | PluginEntry.Sentinel]:
        """return a standard dict with all plugins values loaded (no PluginEntry)"""

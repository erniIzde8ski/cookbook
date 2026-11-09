import os
from os import stat_result
from types import ModuleType
from typing import Any

"Manage (save/check) task dependency-on-files data."

class DatabaseException(Exception):
    """Exception class for whatever backend exception"""

def get_md5(input_data) -> str:
    """return md5 from string or unicode"""

def get_file_md5(path) -> str:
    """Calculate the md5 sum from file content.

    @param path: (string) file path
    @return: (string) md5
    """

class JSONCodec:
    """default implmentation for codec used to save individual task's data"""

    def __init__(self) -> None: ...
    def encode(self, data) -> str: ...
    def decode(self, data) -> Any: ...

class JsonDB:
    """Backend using a single text file with JSON content"""

    def __init__(self, name, codec, *, module_name=...) -> None:
        """Open/create a DB file"""

    def dump(self) -> None:
        """save DB content in file"""

    def set(self, task_id, dependency, value) -> None:
        """Store value in the DB."""

    def get(self, task_id, dependency) -> None:
        """Get value stored in the DB.

        @return: (string) or (None) if entry not found
        """

    def in_(self, task_id) -> bool:
        """@return bool if task_id is in DB"""

    def remove(self, task_id) -> None:
        """remove saved dependencies from DB for taskId"""

    def remove_all(self) -> None:
        """remove saved dependencies from DB for all tasks"""

def get_dbm_module(mod_name) -> ModuleType: ...

class DbmDB:
    """Backend using a DBM file with individual values encoded in JSON

    On initialization all items are read from DBM file and loaded on ``_dbm``.
    During execution whenever an item is read (``get`` method) the `json` value
    is cached on ``_db``.
    If an item is modified ``_db`` is update and the `id` is added
    to the `dirty` set. Only on ``dump`` all dirty items values are encoded
    in json into ``_dbm`` and the DBM file is saved.

    :ivar str name: file name/path
    :ivar module: DBM implementation name one of: 'dbm.gun', 'dbm.ndbm', 'dbm.dumb'.
    :ivar dbm _dbm: items with json encoded values
    :ivar dict _db: items with python-dict as value
    :ivar set dirty: id of modified tasks
    """

    DBM_CONTENT_ERROR_MSG = ...

    def __init__(self, name, codec, *, module_name=...) -> None:
        """Open/create a DB file"""

    def dump(self) -> None:
        """save/close DBM file"""

    def set(self, task_id, dependency, value) -> None:
        """Store value in the DB."""

    def get(self, task_id, dependency) -> None:
        """Get value stored in the DB.

        :return: string or None if entry not found
        """

    def in_(self, task_id) -> bool:
        """@return bool if task_id is in DB"""

    def remove(self, task_id) -> None:
        """remove saved dependencies from DB for taskId"""

    def remove_all(self) -> None:
        """remove saved dependencies from DB for all tasks"""

class SqliteDB:
    """sqlite3 json backend"""

    def __init__(self, name, codec, *, module_name=...) -> None: ...
    def get(self, task_id, dependency) -> Any | None:
        """Get value stored in the DB.

        @return: (string) or (None) if entry not found
        """

    def set(self, task_id, dependency, value) -> None:
        """Store value in the DB."""

    def in_(self, task_id) -> bool: ...
    def dump(self) -> None:
        """save/close sqlite3 DB file"""

    def remove(self, task_id) -> None:
        """remove saved dependencies from DB for taskId"""

    def remove_all(self) -> None:
        """remove saved dependencies from DB for all task"""

class FileChangedChecker:
    """Base checker for dependencies, must be inherited."""

    CheckerError = os.error

    def exists(self, file_path) -> bool: ...
    def info(self, file_path) -> stat_result: ...
    def check_modified(self, file_path, file_stat, state):
        """Check if file in file_path is modified from previous "state".

        @param file_path (string): file path
        @param file_stat: result of os.stat() of file_path
        @param state: state that was previously saved with ``get_state()``
        @returns (bool): True if dep is modified

        """

    def get_state(self, dep, current_state):
        """Compute the state of a task after it has been successfully executed.

        @param dep (str): path of the dependency file.
        @param current_state (tuple): the current state, saved from a previous
            execution of the task (None if the task was never run).
        @returns: the new state. Return None if the state is unchanged.

        The parameter `current_state` is passed to allow speed optimization,
        see MD5Checker.get_state().
        """

class MD5Checker(FileChangedChecker):
    """MD5 checker, uses the md5sum.

    This is the default checker used by doit.

    As an optimization the check uses (timestamp, file-size, md5).
    If the timestamp is the same it considers that the file has the same
    content. If file size is different its content certainly is modified.
    Finally the md5 is used for a different timestamp with the same size.
    """

    def check_modified(self, file_path, file_stat, state) -> bool:
        """Check if file in file_path is modified from previous "state"."""

    def get_state(self, dep, current_state) -> tuple[float, int, str] | None: ...

class TimestampChecker(FileChangedChecker):
    """Checker that use only the timestamp."""

    def check_modified(self, file_path, file_stat, state): ...
    def get_state(self, dep, current_state) -> float:
        """@returns float: mtime for file `dep`"""

CHECKERS = ...

class DependencyStatus:
    """Result object for Dependency.get_status.

    @ivar status: (str) one of "run", "up-to-date" or "error"
    """

    def __init__(self, get_log) -> None: ...
    def add_reason(self, reason, arg, status=...) -> bool:
        """sets state and append reason for not being up-to-date
        :return boolean: processing should be interrupted
        """

    def set_reason(self, reason, arg) -> bool:
        """sets state and reason for not being up-to-date
        :return boolean: processing should be interrupted
        """

    def get_error_message(self) -> None:
        """return str with error message"""

class Dependency:
    """Manage tasks dependencies.

    Each dependency is saved in "db". There are several "db" backends.
    It uses a Key-Value format where the key is task-name
    and value is a dictionary.
    Each task has a dictionary where keys are `dependency`'s (absolute file path),
    and the value is the dependency signature.
    Apart from dependencies other values are also saved on the task dictionary:

    * ``_values_:`` task's values
    * ``result:`` task result

    And also some internal doit attributes:

    * ``ignore:``
    * ``deps:``
    * ``checker:``

    Those can be accessed with generic DB ``get()``, see below...

    :ivar string name: filepath of the DB file
    :ivar bool _closed: DB was flushed to file
    """

    def __init__(
        self, db_class, backend_name, checker_cls=..., codec_cls=..., module_name=...
    ) -> None: ...
    def close(self) -> None:
        """Write DB in file"""

    def save_success(self, task, result_hash=...) -> None:
        """save info after a task is successfully executed

        :param str result_hash: explicitly set result_hash
        """

    def get_values(self, task_name) -> dict[Any, Any]:
        """get all saved values from a task

        :return dict:
        """

    def get_value(self, task_id, key_name):
        """get saved value from task

        :param str task_id:
        :param str key_name: key result dict of the value
        """

    def get_result(self, task_name):
        """get the result saved from a task

        :return (dict or md5sum):
        """

    def remove_success(self, task) -> None:
        """remove saved info from task"""

    def ignore(self, task) -> None:
        """mark task to be ignored"""

    def status_is_ignore(self, task):
        """check if task is marked to be ignored"""

    def get_status(self, task, tasks_dict, get_log=...):
        """Check if task is up to date. set task.dep_changed

        If the checker class changed since the previous run, the task is
        deleted, to be sure that its state is not re-used.

        @param task: (Task)
        @param tasks_dict: (dict: Task) passed to objects used on uptodate
        @param get_log: (bool) if True, adds all reasons to the return
                               object why this file will be rebuild.
        @return: (DependencyStatus) a status object with possible status
                                    values up-to-date, run or error

        task.dep_changed (list-strings): file-dependencies that are not
        up-to-date if task not up-to-date because of a target, returned value
        will contain all file-dependencies regardless they are up-to-date
        or not.
        """

class UptodateCalculator:
    """Base class for 'uptodate' that need access to all tasks"""

    def __init__(self) -> None: ...
    def setup(self, dep_manager, tasks_dict) -> None:
        """@param"""

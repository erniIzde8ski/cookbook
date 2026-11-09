"""Handle exceptions generated from 'user' code"""

class InvalidCommand(Exception):
    """Invalid command line argument."""

    def __init__(self, *args, **kwargs) -> None: ...

class InvalidDodoFile(Exception):
    """Invalid dodo file"""

class InvalidTask(Exception):
    """Invalid task instance. User error on specifying the task."""

class CatchedException:
    """DEPRECATED, use BaseFail instead. 2022-04-22 0.36.0 release.

    Wrong grammar and not all BaseFail contains an Exception

    :ivar report: used by (some) reporters to decide if Failure/Error should be in printed
    """

    def __init__(self, msg, exception=..., report=...) -> None: ...
    def get_msg(self) -> str:
        """return full exception description (includes traceback)"""

    def get_name(self) -> str:
        """get fail kind name"""

class BaseFail(CatchedException):
    """This used to save info Task failures/errors

    Might contain a caught Exception.
    """

class TaskFailed(BaseFail):
    """Task execution was not successful."""

class TaskError(BaseFail):
    """Error while trying to execute task."""

class UnmetDependency(TaskError):
    """Task was not executed because a dependent task failed or is ignored"""

class SetupError(TaskError):
    """Error while trying to execute setup object"""

class DependencyError(TaskError):
    """Error while trying to check if task is up-to-date or saving task status"""

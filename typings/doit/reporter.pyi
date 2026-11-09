from typing import Any

from .exceptions import BaseFail

"Reports doit execution status/results"

class ConsoleReporter:
    """Default reporter. print results on console/terminal (stdout/stderr)

    @ivar failure_verbosity: (int) include captured stdout/stderr on failure
                             report even if already shown.
    """

    desc = ...

    def __init__(self, outstream, options) -> None: ...
    def write(self, text) -> None: ...
    def initialize(self, tasks, selected_tasks) -> None:
        """called just after tasks have been loaded before execution starts"""

    def get_status(self, task) -> None:
        """called when task is selected (check if up-to-date)"""

    def execute_task(self, task) -> None:
        """called when execution starts"""

    def add_failure(self, task, fail: BaseFail) -> None:
        """called when execution finishes with a failure"""

    def add_success(self, task) -> None:
        """called when execution finishes successfully"""

    def skip_uptodate(self, task) -> None:
        """skipped up-to-date task"""

    def skip_ignore(self, task) -> None:
        """skipped ignored task"""

    def cleanup_error(self, exception) -> None:
        """error during cleanup"""

    def runtime_error(self, msg) -> None:
        """error from doit (not from a task execution)"""

    def teardown_task(self, task) -> None:
        """called when starts the execution of teardown action"""

    def complete_run(self) -> None:
        """called when finished running all tasks"""

class ExecutedOnlyReporter(ConsoleReporter):
    """No output for skipped (up-to-date) and group tasks

    Produces zero output unless a task is executed
    """

    desc = ...

    def skip_uptodate(self, task) -> None:
        """skipped up-to-date task"""

    def skip_ignore(self, task) -> None:
        """skipped ignored task"""

class ZeroReporter(ConsoleReporter):
    """Report only internal errors from doit"""

    desc = ...
    complete_run = ...

    def runtime_error(self, msg) -> None: ...

class ErrorOnlyReporter(ZeroReporter):
    desc = ...

    def add_failure(self, task, fail_info: BaseFail) -> None: ...

class TaskResult:
    """result object used by JsonReporter"""

    def __init__(self, task) -> None: ...
    def start(self) -> None:
        """called when task starts its execution"""

    def set_result(self, result, error=...) -> None:
        """called when task finishes its execution"""

    def to_dict(self) -> dict[str, Any | str | float | None]:
        """convert result data to dictionary"""

class JsonReporter:
    """output results in JSON format

    - out (str)
    - err (str)
    - tasks (list - dict):
         - name (str)
         - result (str)
         - out (str)
         - err (str)
         - error (str)
         - started (str)
         - elapsed (float)
    """

    desc = ...

    def __init__(self, outstream, options=...) -> None: ...
    def get_status(self, task) -> None:
        """called when task is selected (check if up-to-date)"""

    def execute_task(self, task) -> None:
        """called when execution starts"""

    def add_failure(self, task, exception) -> None:
        """called when execution finishes with a failure"""

    def add_success(self, task) -> None:
        """called when execution finishes successfully"""

    def skip_uptodate(self, task) -> None:
        """skipped up-to-date task"""

    def skip_ignore(self, task) -> None:
        """skipped ignored task"""

    def cleanup_error(self, exception) -> None:
        """error during cleanup"""

    def runtime_error(self, msg) -> None:
        """error from doit (not from a task execution)"""

    def teardown_task(self, task) -> None:
        """called when starts the execution of teardown action"""

    def complete_run(self) -> None:
        """called when finished running all tasks"""

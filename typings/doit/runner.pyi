from collections.abc import Callable
from threading import Thread
from typing import Any
from typing import Literal

"Task runner"
pickle_dumps = ...
SUCCESS = ...
FAILURE = ...
ERROR = ...

class Runner:
    """Task runner

    run_all()
      run_tasks():
        for each task:
            select_task()
            execute_task()
            process_task_result()
      finish()

    """

    def __init__(
        self, dep_manager, reporter, continue_=..., always_execute=..., stream=...
    ) -> None:
        """
        @param dep_manager: DependencyBase
        @param reporter: reporter object to be used
        @param continue_: (bool) execute all tasks even after a task failure
        @param always_execute: (bool) execute even if up-to-date or ignored
        @param stream: (task.Stream) global verbosity
        """

    def select_task(self, node, tasks_dict) -> bool:
        """Returns bool, task should be executed
         * side-effect: set task.options

        Tasks should be executed if they are not up-to-date.

        Tasks that contains setup-tasks must be selected twice,
        so it gives chance for dependency tasks to be executed after
        checking it is not up-to-date.
        """

    def execute_task(self, task):
        """execute task's actions"""

    def process_task_result(self, node, base_fail) -> None:
        """handles result"""

    def run_tasks(self, task_dispatcher) -> None:
        """This will actually run/execute the tasks.
        It will check file dependencies to decide if task should be executed
        and save info on successful runs.
        It also deals with output to stdout/stderr.

        @param task_dispatcher: L{TaskDispacher}
        """

    def teardown(self) -> None:
        """run teardown from all tasks"""

    def finish(self) -> int:
        """finish running tasks"""

    def run_all(self, task_dispatcher) -> int:
        """entry point to run tasks
        @ivar task_dispatcher (TaskDispatcher)
        """

class JobHold:
    """Indicates there is no task ready to be executed"""

    type = ...

class JobTask:
    """Contains a Task object"""

    type = ...

    def __init__(self, task) -> None: ...

class JobTaskPickle:
    """dict of Task object excluding attributes that might be unpicklable"""

    type = ...

    def __init__(self, task) -> None: ...
    @property
    def name(self): ...

class MReporter:
    """send reported messages to master process

    puts a dictionary {'name': <task-name>,
                       'reporter': <reporter-method-name>}
    on runner's 'result_q'
    """

    def __init__(self, runner, reporter_cls) -> None: ...
    def __getattr__(self, method_name) -> Callable[..., None]:
        """substitute any reporter method with a dispatching method"""

    def complete_run(self) -> None:
        """ignore this on MReporter"""

class MRunner(Runner):
    """MultiProcessing Runner"""

    Queue = ...
    Child = ...

    @staticmethod
    def available() -> bool:
        """check if multiprocessing module is available"""

    def __init__(
        self,
        dep_manager,
        reporter,
        continue_=...,
        always_execute=...,
        stream=...,
        num_process=...,
    ) -> None: ...
    def __getstate__(self) -> dict[str, Any]: ...
    def get_next_job(self, completed) -> JobHold | JobTask | JobTaskPickle | None:
        """get next task to be dispatched to sub-process

        On MP needs to check if the dependencies finished its execution
        @returns : - None -> no more tasks to be executed
                   - JobXXX
        """

    def run_tasks(self, task_dispatcher) -> None:
        """controls subprocesses task dispatching and result collection"""

    def execute_task_subprocess(self, job_q, result_q, reporter_class) -> None:
        """executed on child processes
        @param job_q: task queue,
            * None elements indicate process can terminate
            * JobHold indicate process should wait for next task
            * JobTask / JobTaskPickle task to be executed
        """

class MThreadRunner(MRunner):
    """Parallel runner using threads"""

    Queue = ...

    class DaemonThread(Thread):
        """daemon thread to make sure process is terminated if there is
        an uncatch exception and threads are not correctly joined.
        """

        def __init__(self, *args, **kwargs) -> None: ...

    Child = ...

    @staticmethod
    def available() -> Literal[True]: ...

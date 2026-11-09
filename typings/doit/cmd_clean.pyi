from typing import Any

from .cmd_base import DoitCmdBase

opt_clean_dryrun = ...
opt_clean_cleandep = ...
opt_clean_cleanall = ...
opt_clean_forget = ...

class Clean(DoitCmdBase):
    doc_purpose = ...
    doc_usage = ...
    doc_description = ...
    cmd_options = ...

    def clean_tasks(self, tasks, dryrun, cleanforget) -> None:
        """ensure task clean-action is executed only once"""

class CleanDepTree:
    """Create node structure where each node is a task and its children
    are tasks that has the node as a task_dep/setup_task.
    This creates an upside-down tree where leaf nodes should be
    the first ones to be "cleaned".
    """

    def __init__(self) -> None: ...
    def build_nodes_with_deps(self, tasks, task_name) -> None:
        """build node including task_dep's"""

    def build_nodes(self, tasks, clean_list) -> None:
        """build nodes with sub-tasks but no other task_dep"""

    def flat(self) -> list[Any]:
        """return list of tasks in the order they should be `clean`"""

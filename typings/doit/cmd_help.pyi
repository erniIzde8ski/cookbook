from typing import Literal

from .cmd_base import DoitCmdBase

HELP_TASK = ...

class Help(DoitCmdBase):
    doc_purpose = ...
    doc_usage = ...
    doc_description = ...

    def __init__(self, cmds=..., **kwargs) -> None:
        """
        :param cmds: PluginDict
        """

    def print_usage(self, cmds) -> None:
        """print doit "usage" (basic help) instructions

        :var cmds: dict name -> Command class
        """

    @staticmethod
    def print_task_help() -> None:
        """print help for 'task' usage"""

    def execute(self, params, args) -> Literal[0]:
        """execute cmd 'help'"""

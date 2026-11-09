from typing import LiteralString

from .cmd_base import DoitCmdBase

"command doit info - display info on task metadata"
opt_hide_status = ...

class Info(DoitCmdBase):
    """command doit info"""

    doc_purpose = ...
    doc_usage = ...
    doc_description = ...
    cmd_options = ...

    @staticmethod
    def get_reasons(reasons) -> LiteralString:
        """return string with description of reason task is not up-to-date"""

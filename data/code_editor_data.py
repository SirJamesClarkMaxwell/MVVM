import attr
from data import Data
from typing import Optional

@attr.s(auto_attribs=True)
class ScriptTab:
    filename: str
    content: str
    output:Optional[str]=""
    is_dirty: bool = False


@attr.s(auto_attribs=True)
class CodeEditorData(Data):
    current_tab_name: str = "Unknown Script"


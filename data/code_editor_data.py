from dataclasses import dataclass
from typing import Optional

@dataclass
class ScriptTab:
    filename: str
    content: str
    filepath:str
    output:Optional[str]=""
    is_dirty: bool = False


@dataclass
class CodeEditorData:
    current_tab_name: str = "Unknown Script"


import attr
from data import Data


@attr.s(auto_attribs=True)
class CodeEditorData(Data):
    selected_script: str = None
    editor_content: str = ""
    output_log: str = ""
    code: str = ""
    exec_result: str = ""
    script_list: list[str] = attr.Factory(list)
    code_space_factor:float = 0.75

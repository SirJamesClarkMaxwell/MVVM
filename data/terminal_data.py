from .data import Data
import attr

@attr.s(auto_attribs=True)
class TerminalData(Data):
    terminal_input: str = ""
    terminal_output: str = ""
    terminal_history: list[str] = attr.Factory(list)
    auto_scroll: bool = True

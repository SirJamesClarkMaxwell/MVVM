from dataclasses import dataclass, field

@dataclass
class TerminalData:
    terminal_input: str = ""
    terminal_output: str = ""
    terminal_history: list[str] = field(default_factory=list)
    auto_scroll: bool = True

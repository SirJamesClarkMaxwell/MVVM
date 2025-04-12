from dataclasses import dataclass, field
from .code_editor_data import CodeEditorData
from .calculator_data import CalculatorData
from .assets import Assets

@dataclass
class ApplicationData:
    calculator_data: CalculatorData = field(default_factory=CalculatorData)
    code_editor_data: CodeEditorData = field(default_factory=CodeEditorData)
    assets: Assets = field(default_factory=Assets)
    open_file_dialog_requested: bool = False



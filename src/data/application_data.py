from dataclasses import dataclass, field

from data.app_settings import AppSettings
from .code_editor_data import CodeEditorData
from .calculator_data import CalculatorData

@dataclass
class ApplicationData:
    calculator_data: CalculatorData = field(default_factory=CalculatorData)
    code_editor_data: CodeEditorData = field(default_factory=CodeEditorData)
    app_settings: AppSettings() = field(default_factory=AppSettings)
    open_file_dialog_requested: bool = False



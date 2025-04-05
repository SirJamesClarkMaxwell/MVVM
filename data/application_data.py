
import attr
from .calculator_data import CalculatorData
from .code_editor_data import *

@attr.s
class ApplicationData:
	calculator_data: CalculatorData
	code_editor_data:CodeEditorData
	open_file_dialog_requested = False

	
	

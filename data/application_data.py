
import attr
from .code_editor_data import *
from .calculator_data import CalculatorData
from .assets import Assets

@attr.s(auto_attribs=True)
class ApplicationData:
	calculator_data: CalculatorData = CalculatorData()
	code_editor_data:CodeEditorData = CodeEditorData()
	assets:Assets = Assets()
	open_file_dialog_requested = False
	
	

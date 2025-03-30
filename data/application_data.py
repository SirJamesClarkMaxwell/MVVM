
import attr
from .calculator_data import CalculatorData

@attr.s
class ApplicationData:
	calculator_data = attr.ib(type=CalculatorData,default=CalculatorData())
	
	

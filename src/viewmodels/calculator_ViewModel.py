from src.core.logger import AppLogger
from src.data.calculator_data import CalculatorData
from src.models.calculator_model import CalculatorModel


class CalculatorViewModel:
    def __init__(self, app,*args,**kwargs) -> None:
        self.model: CalculatorModel = CalculatorModel()
        self.data: CalculatorData = CalculatorData()
        self.app = app
        self.data.result = 0.0

    def compute(self):
        self.data.result = self.model.evaluate(
            self.data.a, self.data.b, self.data.operation)
        AppLogger.get().info(
            f"Computed: {self.data.a} {self.data.operation} {self.data.b} = {self.data.result}")

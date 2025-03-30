
from utils.logger import AppLogger

from viewmodels import ViewModel
from models.calculator_model import CalculatorModel
from data.calculator_data import CalculatorData

import attr




@attr.s(auto_attribs=True)
class CalculatorViewModel(ViewModel):
    model:  CalculatorModel
    data:  CalculatorData

    def compute(self):
        self.data.result = self.model.evaluate(self.data.a, self.data.b, self.data.operation)
        AppLogger.get().info(f"Computed: {self.data.a} {self.data.operation} {self.data.b} = {self.data.result}")

    def __getattr__(self, name):
        # fallback to data
        if hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(f"{name} not found")

    def __setattr__(self, name, value):
        if name in {"model", "data"}:
            super().__setattr__(name, value)
        elif hasattr(self.data, name):
            setattr(self.data, name, value)
        else:
            super().__setattr__(name, value)
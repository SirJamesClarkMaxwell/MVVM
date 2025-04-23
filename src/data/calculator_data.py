from dataclasses import dataclass
@dataclass
class CalculatorData:
    a:float = 10
    b:float = 10
    result:float = -1
    operation:str = "+"

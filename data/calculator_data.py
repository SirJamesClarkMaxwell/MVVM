import attr
from data import Data

@attr.s
class CalculatorData(Data):
    a = attr.ib(type=float,default=0)
    b = attr.ib(type=float,default=0)
    result = attr.ib(type=float,default=0)
    operation = attr.ib(type=str,default="+")

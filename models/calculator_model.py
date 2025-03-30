import pandas as pd

class CalculatorModel:
    def evaluate(self, a: float, b: float, op: str) -> float:
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '*': return a * b
        elif op == '/': return a / b if b != 0 else float('inf')
        elif op == '^': return a ** b
        else: raise ValueError(f"Unknown operation: {op}")
    def load_csv(self, path: str):
        self.df = pd.read_csv(path)
        return self.df

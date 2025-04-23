import os
from src.models.calculator_model import CalculatorModel

import pandas as pd
import pytest


@pytest.fixture
def calculator_model():
    return CalculatorModel()

def test_evaluate_addition(calculator_model):
    assert calculator_model.evaluate(2, 3, "+") == 5

def test_evaluate_subtraction(calculator_model):
    assert calculator_model.evaluate(5, 3, "-") == 2

def test_evaluate_multiplication(calculator_model):
    assert calculator_model.evaluate(4, 3, "*") == 12

def test_evaluate_division(calculator_model):
    assert calculator_model.evaluate(10, 2, "/") == 5

def test_evaluate_division_by_zero(calculator_model):
    assert calculator_model.evaluate(10, 0, "/") == float("inf")

def test_evaluate_exponentiation(calculator_model):
    assert calculator_model.evaluate(2, 3, "^") == 8

def test_evaluate_invalid_operation(calculator_model):
    with pytest.raises(ValueError):
        calculator_model.evaluate(2, 3, "%")


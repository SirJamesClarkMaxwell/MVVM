import pytest
from unittest.mock import MagicMock
from src.viewmodels.calculator_ViewModel import CalculatorViewModel
from src.data.calculator_data import CalculatorData

@pytest.fixture
def calculator_viewmodel():
    mock_app = MagicMock()
    viewmodel = CalculatorViewModel(mock_app)
    viewmodel.data = CalculatorData()
    viewmodel.data.a = 5
    viewmodel.data.b = 3
    viewmodel.data.operation = "+"
    return viewmodel

def test_compute_addition(calculator_viewmodel):
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == 8

def test_compute_subtraction(calculator_viewmodel):
    calculator_viewmodel.data.operation = "-"
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == 2

def test_compute_multiplication(calculator_viewmodel):
    calculator_viewmodel.data.operation = "*"
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == 15

def test_compute_division(calculator_viewmodel):
    calculator_viewmodel.data.operation = "/"
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == 5 / 3

def test_compute_division_by_zero(calculator_viewmodel):
    calculator_viewmodel.data.b = 0
    calculator_viewmodel.data.operation = "/"
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == float("inf")

def test_compute_exponentiation(calculator_viewmodel):
    calculator_viewmodel.data.operation = "^"
    calculator_viewmodel.compute()
    assert calculator_viewmodel.data.result == 5**3
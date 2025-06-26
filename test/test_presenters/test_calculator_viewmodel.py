import pytest
from unittest.mock import MagicMock
from presenters.calculator_presenter import CalculatorPresenter
from src.data.calculator_data import CalculatorData

@pytest.fixture
def calculator_presenter():
    mock_app = MagicMock()
    presenter = CalculatorPresenter(mock_app)
    presenter.data = CalculatorData()
    presenter.data.a = 5
    presenter.data.b = 3
    presenter.data.operation = "+"
    return presenter

def test_compute_addition(calculator_presenter):
    calculator_presenter.compute()
    assert calculator_presenter.data.result == 8

def test_compute_subtraction(calculator_presenter):
    calculator_presenter.data.operation = "-"
    calculator_presenter.compute()
    assert calculator_presenter.data.result == 2

def test_compute_multiplication(calculator_presenter):
    calculator_presenter.data.operation = "*"
    calculator_presenter.compute()
    assert calculator_presenter.data.result == 15

def test_compute_division(calculator_presenter):
    calculator_presenter.data.operation = "/"
    calculator_presenter.compute()
    assert calculator_presenter.data.result == 5 / 3

def test_compute_division_by_zero(calculator_presenter):
    calculator_presenter.data.b = 0
    calculator_presenter.data.operation = "/"
    calculator_presenter.compute()
    assert calculator_presenter.data.result == float("inf")

def test_compute_exponentiation(calculator_presenter):
    calculator_presenter.data.operation = "^"
    calculator_presenter.compute()
    assert calculator_presenter.data.result == 5**3

import pytest

from calculator_olu_ile.calculator import Calculator
from calculator_olu_ile.customerror import NoneNumericValueError


def test_addition():
    """test addition method when correct input is provided"""
    cal = Calculator()
    cal.add(2)
    cal.add(2)
    assert cal.accum == 4, "Should be 4"


def test_addition_exception_path():
    """test addition method when incorrect input(non-numeric) is provided"""
    cal = Calculator()
    with pytest.raises(Exception) as e:
        cal.add('wrong message')
    assert e.type == NoneNumericValueError, "Should be NoneNumericValueError"


def test_subtraction():
    """test subtract method when correct input is provided"""
    cal = Calculator()
    cal.subtract(2)
    cal.subtract(2)
    assert cal.accum == -4, "Should be -4"


def test_subtraction_exception_path():
    """test subtract method when incorrect input(non-numeric) is provided"""
    cal = Calculator()
    with pytest.raises(Exception) as e:
        cal.subtract('wrong message')
    assert e.type == NoneNumericValueError, "Should be NoneNumericValueError"


def test_multiplication():
    """test multiplication method when correct input is provided"""
    cal = Calculator()
    cal.accum = 2
    cal.multiply(2)
    assert cal.accum == 4, "Should be 4"


def test_multiply_exception_path():
    """test multiplication method when incorrect input(non-numeric) is provided"""
    cal = Calculator()
    with pytest.raises(Exception) as e:
        cal.multiply('wrong message')
    assert e.type == NoneNumericValueError, "Should be NoneNumericValueError"


def test_division():
    """test division method when correct input is provided"""
    cal = Calculator()
    cal.accum = 2
    cal.divide(2)
    assert cal.accum == 1, "Should be 1"


def test_division_exception_path():
    """test division method when incorrect input(non-numeric) is provided"""
    cal = Calculator()
    with pytest.raises(Exception) as e:
        cal.divide('wrong message')
    assert e.type == NoneNumericValueError, "Should be NoneNumericValueError"


def test_root():
    """test root method when correct input is provided"""
    cal = Calculator()
    cal.accum = 9
    cal.root(2)
    assert cal.accum == 3.0, "Should be 3.0"


def test_root_exception_path():
    """test root method when incorrect input(non-numeric) is provided"""
    cal = Calculator()
    with pytest.raises(Exception) as e:
        cal.root('wrong message')
    assert e.type == NoneNumericValueError, "Should be NoneNumericValueError"

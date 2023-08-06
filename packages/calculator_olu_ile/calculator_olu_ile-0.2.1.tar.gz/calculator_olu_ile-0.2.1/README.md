# Calculator

> Arithmetic calculator with operations add, subtract, divide, multipy and root.


## Installation
```sh
pip install calculator_olu_ile
```

## Usage
```python

For example: Addition with package on IDLE 
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.add(2)
    >>> print(cal.accum)
    2
    >>> cal.add(2)
    >>> print(cal.accum)
    4

For example: Subtraction with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.subtract(2)
    >>> print(cal.accum)
    -2
    >>> cal.subtract(2)
    >>> print(cal.accum)
    -4

For example: Multiplication with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.multiply(2)
    >>> print(cal.accum)
    0
    >>> cal.accum = 2
    >>> cal.multiply(2)
    >>> print(cal.accum)
    4

For example: Divide with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.divide(2)
    >>> print(cal.accum)
    0.0
    >>> cal.accum = 2
    >>> cal.divide(2)
    >>> print(cal.accum)
    1.0

For example: Root with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> cal.accum = 9
    >>> cal.root(2)
    >>> print(cal.accum)
    3.0

For example: Is_input_valid with package on IDLE
    >>> from calculator_olu_ile.calculator import Calculator
    >>> cal = Calculator()
    >>> print(cal.is_input_valid("text"))
    False
    >>> print(cal.is_input_valid(6))
    True
```
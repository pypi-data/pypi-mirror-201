""" Calculator Module """

from typing import Union

from calculator_olu_ile.customerror import NoneNumericValueError


class Calculator:
    def __init__(self, accum=0):
        """default state of the accumulator is 0"""
        self.__accum = accum

    def add(self, num: Union[int, float]) -> None:
        """add num to accumulator,
        if num has an invalid value eg string then raise an exception.

        For example:
            >>> cal = Calculator()
            >>> cal.add(2)
            >>> print(cal.accum)
            2
            >>> cal.add(2)
            >>> print(cal.accum)
            4
        """
        if self.is_input_valid(num):
            self.__accum += num
        else:
            raise NoneNumericValueError(num)

    def subtract(self, num: Union[int, float]) -> None:
        """subtract num from accumulator,
        if num has an invalid value eg string then raise an exception.

        For example:
            >>> cal = Calculator()
            >>> cal.subtract(2)
            >>> print(cal.accum)
            -2
            >>> cal.subtract(2)
            >>> print(cal.accum)
            -4
        """
        if self.is_input_valid(num):
            self.__accum -= num
        else:
            raise NoneNumericValueError(num)

    def multiply(self, num: Union[int, float]) -> None:
        """multipy accumulator by num,
        if num has an invalid value eg string then raise an exception.

        For example:
            >>> cal = Calculator()
            >>> cal.multiply(2)
            >>> print(cal.accum)
            0
            >>> cal.accum = 2
            >>> cal.multiply(2)
            >>> print(cal.accum)
            4
        """
        if self.is_input_valid(num):
            self.__accum *= num
        else:
            raise NoneNumericValueError(num)

    def divide(self, num: Union[int, float]) -> None:
        """divide accumulator by num,
        if num has an invalid value eg string then raise an exception.

        For example:
            >>> cal = Calculator()
            >>> cal.divide(2)
            >>> print(cal.accum)
            0.0
            >>> cal.accum = 2
            >>> cal.divide(2)
            >>> print(cal.accum)
            1.0
        """
        if self.is_input_valid(num):
            self.__accum /= num
        else:
            raise NoneNumericValueError(num)

    def root(self, pwr: Union[int]) -> None:
        """find root of number.
           if num has an invalid value .eg string then raise an exception.

        For example:
            >>> cal = Calculator()
            >>> cal.accum = 9
            >>> cal.root(2)
            >>> print(cal.accum)
            3.0
        """
        if self.is_input_valid(pwr):
            self.__accum = self.__accum ** (1 / pwr)
        else:
            raise NoneNumericValueError(pwr)

    @property
    def accum(self) -> Union[int, float]:
        """
        getter: gets current state/value of accumulator

        For example:
            >>> cal = Calculator()
            >>> print(cal.accum)
            0

        setter: sets the state of the accumulator
                if num has an invalid value .eg string then raise an exception

        For example:
            >>> cal = Calculator()
            >>> cal.accum = 5
            >>> print(cal.accum)
            5
        """
        return self.__accum

    @accum.setter
    def accum(self, state=0) -> None:
        if self.is_input_valid(state):
            self.__accum = state
        else:
            raise NoneNumericValueError(state)

    @staticmethod
    def is_input_valid(num: Union[int, float]) -> bool:
        """check that library user has put in a numeric value (float or int)

        For example:
            >>> cal = Calculator()
            >>> print(cal.is_input_valid("text"))
            False
            >>> print(cal.is_input_valid(6))
            True
        """
        return isinstance(num, (int, float))

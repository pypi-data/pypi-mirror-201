from hypothesis import given, assume, strategies as st
from mypackage.src.pycalculator_TomasJ.calculator import Calculator


@given(st.floats(min_value=-10, max_value=10),
       st.floats(min_value=-10, max_value=10))
def test_calculator_add(a, b):
    calc = Calculator(a)
    calc.add(b)
    assert calc.memory == a + b


@given(st.floats(min_value=-10, max_value=10),
       st.floats(min_value=-10, max_value=10))
def test_calculator_subtract(a, b):
    calc = Calculator(a)
    calc.subtract(b)
    assert calc.memory == a - b


@given(st.floats(min_value=-10, max_value=10),
       st.floats(min_value=-10, max_value=10))
def test_calculator_multiply_by(a, b):
    calc = Calculator(a)
    calc.multiply_by(b)
    assert calc.memory == a * b


@given(st.floats(min_value=-10, max_value=10),
       st.floats(min_value=-10, max_value=10).filter(lambda x: x != 0))
def test_calculator_divide_by(a, b):
    calc = Calculator(a)
    calc.divide_by(b)
    assert calc.memory == a / b


@given(st.floats(min_value=-4, max_value=4).filter(lambda x: x != 0),
       st.floats(min_value=-4, max_value=4).filter(lambda x: x != 0))
def test_calculator_root_extraction(a, b):
    assume(-0.01 < abs(a) > 0.1)
    assume(-0.01 < abs(b) > 0.01)
    calc = Calculator(a)
    calc.root_extraction(b)
    if b % 2 == 0 and a < 0:
        pass
    else:
        assert calc.memory == a ** (1 / b)


def test_calculator_reset():
    calc = Calculator(6)
    calc.reset()
    assert calc.memory == 0

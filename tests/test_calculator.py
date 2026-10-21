import pytest

from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


@pytest.mark.parametrize(
    "a, b, expected",
    [(2, 3, 5), (-2, -3, -5), (-2, 3, 1), (0, 0, 0), (0.1, 0.2, 0.3), (10**20, 1, 10**20 + 1)],
)
def test_add(calc, a, b, expected):
    assert calc.add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a, b, expected", [(5, 3, 2), (3, 5, -2), (-5, -5, 0), (0, 7, -7), (0.3, 0.1, 0.2)])
def test_subtract(calc, a, b, expected):
    assert calc.subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a, b, expected", [(4, 5, 20), (-4, 5, -20), (-4, -5, 20), (7, 0, 0), (2.5, 4, 10)])
def test_multiply(calc, a, b, expected):
    assert calc.multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a, b, expected", [(10, 2, 5), (7, 2, 3.5), (-9, 3, -3), (0, 5, 0), (1, 3, 0.3333333333)])
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("zero", [0, 0.0, -0.0])
def test_divide_by_zero_raises(calc, zero):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль невозможно"):
        calc.divide(10, zero)


@pytest.mark.parametrize(
    "n, expected",
    [(-7, False), (0, False), (1, False), (2, True), (3, True), (4, False), (9, False),
     (17, True), (25, False), (97, True), (100, False), (7919, True)],
)
def test_is_prime_number(calc, n, expected):
    assert calc.is_prime_number(n) is expected


@pytest.mark.parametrize("value", [7.5, "7", None])
def test_is_prime_number_rejects_non_integers(calc, value):
    with pytest.raises(TypeError):
        calc.is_prime_number(value)

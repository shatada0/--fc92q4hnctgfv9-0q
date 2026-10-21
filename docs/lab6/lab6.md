# ЛР6. Модульные тесты (unit tests)

Объект тестирования: класс `Calculator` (`calculator.py`) с методами `add`, `subtract`, `multiply`, `divide`, `is_prime_number`. Тот же класс использует веб-калькулятор из ЛР1.

```python
class Calculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def is_prime_number(self, n):
        if n < 2:
            return False
        return all(n % d for d in range(2, math.isqrt(n) + 1))
```

## Тесты

Файл `tests/test_calculator.py`, фреймворк pytest. Каждый тест вызывает метод изолированно, без браузера, сети и файлов. Экземпляр калькулятора создаёт фикстура `calc`.

Все тесты параметризованы (`@pytest.mark.parametrize`): одна функция проверяет несколько наборов данных, каждый набор — отдельный тест в отчёте pytest.

| Тест | Наборы данных | Что проверяет |
|------|---------------|---------------|
| `test_add` | 6 | целые, отрицательные, нули, дроби (0.1 + 0.2 через `pytest.approx`), очень большие числа |
| `test_subtract` | 5 | положительный и отрицательный результат, ноль, дроби |
| `test_multiply` | 5 | комбинации знаков, умножение на 0, дробь |
| `test_divide` | 5 | целый и дробный результат, отрицательные, 0 в делимом, бесконечная дробь |
| `test_divide_by_zero_raises` | 3 (0, 0.0, -0.0) | возникает `ZeroDivisionError` с текстом «Деление на ноль невозможно» (`pytest.raises`) |
| `test_is_prime_number` | 12 | отрицательные, 0, 1 (не простые), 2 и 3 (наименьшие простые), квадраты простых 9 и 25, 97, 7919 |
| `test_is_prime_number_rejects_non_integers` | 3 (7.5, "7", None) | для нецелых значений возникает `TypeError` |

Дробные результаты сравниваются через `pytest.approx`: точное сравнение `0.1 + 0.2 == 0.3` в Python ложно из-за двоичного представления вещественных чисел.

Проверка исключения при делении на ноль:

```python
@pytest.mark.parametrize("zero", [0, 0.0, -0.0])
def test_divide_by_zero_raises(calc, zero):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль невозможно"):
        calc.divide(10, zero)
```

## Запуск и результат

```
.venv\Scripts\python -m pytest tests/test_calculator.py -v
```

Результат 21.10.2026: **39 passed** за 0,02 с (полный вывод в `pytest_output.txt`).

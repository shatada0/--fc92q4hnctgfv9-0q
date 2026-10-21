# ЛР9. Интеграция автотестов в CI/CD (GitHub Actions)

Объект: автотесты из предыдущих ЛР (по условию ЛР9 своё приложение не пишется):

| Набор | Файл | Тестов |
|-------|------|--------|
| Unit-тесты калькулятора (ЛР6) | `tests/test_calculator.py` | 39 |
| API-тесты JSONPlaceholder (ЛР5) | `tests/test_api.py` | 4 |
| UI-тест входа, Selenium (ЛР3) | `tests/test_login.py` | 2 |
| UI-тесты формы, Page Object (ЛР4) | `tests/test_contact.py` | 7 |
| **Всего** | | **52** |

Мобильный тест (ЛР7) и нагрузочный скрипт (ЛР8) в CI не входят: им нужны эмулятор и долгоживущий сервер. Мобильный тест лежит вне папки `tests/`, а `pytest.ini` (`testpaths = tests`) собирает тесты только оттуда.

## 1. Репозиторий

Публичный репозиторий GitHub: **https://github.com/shatada0/--fc92q4hnctgfv9-0q**. В него загружен весь проект: стенд, тесты, документация.

## 2. Workflow

Файл `.github/workflows/run-tests.yml`:

```yaml
name: run-tests

on:
  push:
  pull_request:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - name: Получить код
        uses: actions/checkout@v5
      - name: Установить Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.13"
          cache: pip
      - name: Установить зависимости
        run: pip install -r requirements.txt
      - name: Запустить тесты (unit, API, UI в headless Firefox)
        run: pytest -v
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

| Требование задания | Как выполнено |
|--------------------|---------------|
| Установка ОС | `runs-on: ubuntu-latest` — виртуальная машина Ubuntu от GitHub; Firefox на ней предустановлен |
| Установка Python | `actions/setup-python@v6`, версия 3.13 (как локально); `cache: pip` кэширует пакеты между запусками |
| Зависимости | `pip install -r requirements.txt` |
| Запуск тестов pytest | `pytest -v` |

Запуск: при каждом `push` и pull request, а также вручную на вкладке Actions (`workflow_dispatch`).

## 3. Как UI-тесты работают в CI

- GitHub Actions выставляет переменную `CI=true`; фикстура `driver` в `tests/conftest.py` в этом случае запускает Firefox без окна (`-headless`). На сервере нет экрана.
- Стенд отдельно не запускается: фикстура `base_url` поднимает Flask-приложение в фоновом потоке на свободном порту.
- `GH_TOKEN`: webdriver-manager узнаёт актуальную версию geckodriver через GitHub API. Без токена лимит 60 запросов в час на IP, а у раннеров GitHub общие IP. Встроенный токен `secrets.GITHUB_TOKEN` снимает это ограничение.
- Версия geckodriver запрашивается один раз на прогон (фикстура `geckodriver_path` с `scope="session"`). Изначально запрос шёл на каждый тест, и при локальных прогонах лимит 60 запросов в час был исчерпан; это и стало поводом вынести запрос в общую фикстуру.

## 4. Результат

<вставить скриншот вкладки Actions с зелёной галочкой и лог шага «Запустить тесты»>

Локальная проверка того же набора перед загрузкой: `pytest -v` — 52 passed.

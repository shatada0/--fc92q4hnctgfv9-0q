# Лабораторные работы по тестированию ПО

Учебный стенд и автотесты к лабораторным работам 1–9.

| Что | Где |
|-----|-----|
| Веб-стенд (Flask): калькулятор, список задач с заложенными багами, вход, форма обратной связи, API | `app.py`, `calculator.py`, `templates/` |
| Автотесты: unit (ЛР6), UI Selenium (ЛР3, ЛР4), API (ЛР5) | `tests/` |
| Page Object (ЛР4) | `tests/pages/` |
| Коллекция Postman (ЛР5) | `postman/` |
| Android-приложение «Заметки» и Appium-тест (ЛР7) | `mobile/` |
| Нагрузочный скрипт k6 (ЛР8) | `load/get.js` |
| CI (ЛР9) | `.github/workflows/run-tests.yml` |
| Документация и результаты по каждой ЛР | `docs/labN/` |

## Запуск

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python app.py          # стенд на http://127.0.0.1:5000
.venv\Scripts\python -m pytest -v    # тесты из tests/ (UI-тесты сами поднимают стенд)
```

UI-тесты используют Firefox. Если Firefox установлен не в стандартную папку, укажите путь к `firefox.exe` в переменной окружения `FIREFOX_BIN`. Переменная `CI` включает режим без окна (headless).

Учётная запись стенда: `student` / `Passw0rd!`.

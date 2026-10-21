import pytest

from pages.contact_page import ContactPage

VALID = {
    "name": "Иван Петров",
    "email": "ivan@example.com",
    "phone": "+79991234567",
    "topic": "Предложение",
    "message": "Здравствуйте! Хочу записаться на курс.",
    "consent": True,
}
FIELDS = ["name", "email", "phone", "message", "consent"]


def test_submit_valid_form(driver, base_url):
    page = ContactPage(driver, base_url).open().fill(**VALID).submit()

    assert page.success_text() == "Спасибо! Сообщение отправлено."
    assert all(page.error_text(field) == "" for field in FIELDS)


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("name", "", "Введите имя"),
        ("email", "", "Введите email"),
        ("message", "", "Введите сообщение"),
        ("consent", False, "Нужно согласие на обработку данных"),
        ("email", "ivan@example", "Некорректный email"),
        ("phone", "123", "Некорректный телефон"),
    ],
    ids=["empty_name", "empty_email", "empty_message", "no_consent", "bad_email", "bad_phone"],
)
def test_invalid_field_shows_error(driver, base_url, field, value, error):
    page = ContactPage(driver, base_url).open().fill(**{**VALID, field: value}).submit()

    assert page.error_text(field) == error
    assert not page.has_success()

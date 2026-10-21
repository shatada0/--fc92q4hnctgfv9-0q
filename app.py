import os
import re

from flask import Flask, redirect, render_template, request, session, url_for

from calculator import Calculator

app = Flask(__name__)
app.secret_key = os.urandom(16)

OPS = {"add": "+", "subtract": "−", "multiply": "×", "divide": "÷"}
NUMBER = re.compile(r"-?[0-9]+(\.[0-9]+)?")
LIMIT = 1_000_000_000
USERS = {"student": "Passw0rd!"}  # учебный стенд: одна учётка в открытом виде
EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
PHONE = re.compile(r"\+?[0-9]{10,15}")
TOPICS = ["Вопрос", "Предложение", "Жалоба"]


def calculate(a, b, op):
    """Общая логика /calc и /api/calc. Ошибки ввода — исключения с текстом для пользователя."""
    if op not in OPS:
        raise ValueError("Неизвестная операция")
    a, b = (v.strip().replace(",", ".") for v in (a, b))
    if not (NUMBER.fullmatch(a) and NUMBER.fullmatch(b)):
        raise ValueError("Введите два числа")
    x, y = float(a), float(b)
    if abs(x) > LIMIT or abs(y) > LIMIT:
        raise ValueError("Допустимы числа от -1000000000 до 1000000000")
    result = round(getattr(Calculator(), op)(x, y), 10)
    return int(result) if result.is_integer() else result


@app.get("/")
def index():
    return redirect(url_for("calc"))


@app.route("/calc", methods=["GET", "POST"])
def calc():
    f = request.form
    result = error = None
    if request.method == "POST":
        try:
            result = calculate(f.get("a", ""), f.get("b", ""), f.get("op", ""))
        except (ValueError, ZeroDivisionError) as e:
            error = str(e)
    return render_template("calc.html", ops=OPS, form=f, result=result, error=error)


@app.get("/api/calc")
def api_calc():
    q = request.args
    try:
        return {"result": calculate(q.get("a", ""), q.get("b", ""), q.get("op", ""))}
    except (ValueError, ZeroDivisionError) as e:
        return {"error": str(e)}, 400


@app.get("/todo")
def todo():
    return render_template("todo.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username", "")
        if user in USERS and USERS[user] == request.form.get("password"):
            session["user"] = user
            return redirect(url_for("home"))
        error = "Неверный логин или пароль"
    return render_template("login.html", error=error)


@app.get("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    f, errors = request.form, {}
    if request.method == "POST":
        email = f.get("email", "").strip()
        phone = f.get("phone", "").strip()
        if not f.get("name", "").strip():
            errors["name"] = "Введите имя"
        if not email:
            errors["email"] = "Введите email"
        elif not EMAIL.fullmatch(email):
            errors["email"] = "Некорректный email"
        if phone and not PHONE.fullmatch(phone):
            errors["phone"] = "Некорректный телефон"
        if not f.get("message", "").strip():
            errors["message"] = "Введите сообщение"
        if "consent" not in f:
            errors["consent"] = "Нужно согласие на обработку данных"
    sent = request.method == "POST" and not errors
    return render_template("contact.html", form={} if sent else f, errors=errors, sent=sent, topics=TOPICS)


if __name__ == "__main__":
    app.run(debug=True)

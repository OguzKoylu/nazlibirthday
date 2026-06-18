import json
import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-on-render")

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "users.json"


def load_users():
    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")

    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = {}

    if not isinstance(data, dict):
        return {}

    return data


def save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    if session.get("username"):
        return redirect(url_for("celebration"))
    return redirect(url_for("login"))


@app.route("/iyi-ki-dogdun-nazli")
def nazli_special():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()

        if users.get(username) == password:
            session["username"] = username
            return redirect(url_for("celebration"))

        error = "Kullanıcı adı veya şifre hatalı."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()

        if not username:
            error = "Kullanıcı adı boş olamaz."
        elif not password:
            error = "Şifre boş olamaz."
        elif username in users:
            error = "Bu kullanıcı adı zaten var."
        else:
            users[username] = password
            save_users(users)
            return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/celebration")
def celebration():
    if not session.get("username"):
        return redirect(url_for("login"))

    return render_template("celebration.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

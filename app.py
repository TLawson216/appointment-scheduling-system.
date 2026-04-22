from flask import Flask, render_template
from database.db import init_db


app = Flask(__name__ )
init_db()

@app.route("/")
def login():
    return render_template("login.html")

from flask import request, redirect
import sqlite3

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]

        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)",
            (name, date, time)
        )

        conn.commit()
        conn.close()

        return redirect("/schedule")

    return render_template("book.html")

@app.route("/schedule")
def schedule():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, date, time FROM appointments")
    appointments = cursor.fetchall()

    conn.close()

    return render_template("schedule.html", appointments=appointments)

if __name__ == "__main__":
    app.run(debug=True)



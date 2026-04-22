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

        #Check for existing appointments
        cursor.execute(
            "SELECT * FROM appointments WHERE date=? AND time=?",
            (date, time)
        )

        existing = cursor.fetchone()

        if existing:
            conn.close()
            return "Time slot unavailable. Please choose another time."
        # If no conflict, insert appointments
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

    cursor.execute("SELECT id, name, date, time FROM appointments")
    appointments = cursor.fetchall()

    conn.close()

    return render_template("schedule.html", appointments=appointments)
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM appointments WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/schedule")




if __name__ == "__main__":
    app.run(debug=True)



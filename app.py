from flask import Flask, render_template, request, redirect, session
from database.db import init_db


app = Flask(__name__ )
app.secret_key = "supersecretkey"
init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
       username = request.form["username"] 
       password = request.form["password"] 
        
       print("INPUT:", username, password)

       conn = sqlite3.connect('database/database.db')
       cursor = conn.cursor()

       cursor.execute("SELECT * FROM users")
       all_users = cursor.fetchall()
       print("ALL USERS:", all_users)

       cursor.execute(
           "SELECT * FROM users WHERE username=? and password=?",
           (username, password)
       ) 

       user = cursor.fetchone()
       print("MATCH:", user)

       conn.close()

       if user:
          session["user"] = username
          return redirect("/book")
       else:
           return render_template("login.html", error="Invalid login")
       
                
    return render_template("login.html")

from flask import request, redirect
import sqlite3

@app.route("/book", methods=["GET", "POST"])
def book():
    if "user" not in session:
        return redirect("/")
   
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
            return render_template("book.html", error="Time slot already booked!")
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
    if "user" not in session:
        return redirect("/")
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print("REGISTER INPUT:", username, password)

        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        print("EXISTING USER:", existing_user)

        if existing_user:
            conn.close()
            print("USER ALREADY EXISTS")
            return render_template("register.html", error="User already exists")

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        print("INSERTED USER")  # 👈 IMPORTANT

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)



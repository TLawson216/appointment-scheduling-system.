from flask import Flask, render_template, request, redirect, session
import sqlite3
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
          session["role"] =user[3]
          return redirect("/dashboard")
       else:
           return render_template("login.html", error="Invalid login")
       
                
    return render_template("login.html")

from flask import request, redirect


@app.route("/book/<int:business_id>", methods=["GET", "POST"])
def book(business_id):
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        time = request.form["time"]
        description = request.form["description"]

        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        # Check for existing appointments (FOR THIS BUSINESS ONLY)
        cursor.execute(
            "SELECT * FROM appointments WHERE date=? AND time=? AND business_id=?",
            (date, time, business_id)
        )

        existing = cursor.fetchone()

        if existing:
            conn.close()
            return render_template(
                "book.html",
                error="Time slot already booked!",
                business_id=business_id
            )

        # Insert appointment
        cursor.execute(
            "INSERT INTO appointments (name, date, time, description, business_id) VALUES (?, ?, ?, ?, ?)",
            (name, date, time, description, business_id)
        )

        conn.commit()
        conn.close()

        return redirect("/schedule")

    return render_template("book.html", business_id=business_id)

@app.route("/schedule")
def schedule():
    if "user" not in session:
        return redirect("/")
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, date, time, description, status, cancel_reason FROM appointments")
    appointments = cursor.fetchall()

    conn.close()
    print(appointments)

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
        role = request.form["role"]

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
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password,role)
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

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    if session["role"] == "business":
        return redirect("/business")
    else:
        return redirect("/user")
    
@app.route("/user")
def user_view():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM users WHERE role='business'")
    businesses = cursor.fetchall()

    conn.close()

    return render_template("user.html", businesses=businesses)

@app.route("/business")
def business_view():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    # get business id
    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    business = cursor.fetchone()

    cursor.execute(
    "SELECT id, name, date, time, description, status, cancel_reason FROM appointments WHERE business_id=?",
    (business[0],)
)

    appointments = cursor.fetchall()

    conn.close()

    return render_template("business.html", appointments=appointments)

@app.route("/cancel/<int:id>", methods=["POST"])
def cancel(id):
    if "user" not in session:
        return redirect("/")

    reason = request.form["reason"]

    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE appointments SET status='Cancelled', cancel_reason=? WHERE id=?",
        (reason, id)
    )

    conn.commit()
    conn.close()

    return redirect("/business")

if __name__ == "__main__":
    app.run(debug=True)



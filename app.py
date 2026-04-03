from flask import Flask, render_template

app = Flask(__name__ )

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/schedule")
def schedule():
    return render_template("schedule.html")

if __name__ == "__main__":
    app.run(debug=True)
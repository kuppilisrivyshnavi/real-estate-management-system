from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db()
    properties = conn.execute("SELECT * FROM properties").fetchall()
    conn.close()
    return render_template("index.html", properties=properties)


@app.route("/dashboard")
def dashboard():
    conn = get_db()
    properties = conn.execute("SELECT * FROM properties").fetchall()
    conn.close()
    return render_template("dashboard.html", properties=properties)


@app.route("/add", methods=["GET","POST"])
def add_property():

    if request.method == "POST":

        title = request.form["title"]
        location = request.form["location"]
        price = request.form["price"]

        conn = get_db()

        conn.execute(
        "INSERT INTO properties(title,location,price) VALUES (?,?,?)",
        (title,location,price)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_property.html")


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()
    conn.execute("DELETE FROM properties WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            return redirect("/dashboard")

        else:
            flash("Invalid Login")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

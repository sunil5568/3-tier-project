from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "data/tasks.db"

# Create database
def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks
    )

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "INSERT INTO tasks(task) VALUES(?)",
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
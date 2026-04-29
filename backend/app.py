from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Create DB connection
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(row) for row in tasks])

# Add task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO tasks (task) VALUES (?)", (data["task"],))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added"})

# Delete task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
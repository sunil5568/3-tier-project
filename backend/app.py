from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import time

app = Flask(__name__)
CORS(app)

# 🔷 Database connection
def get_db():
    return psycopg2.connect(
        host="db",            # docker service name
        database="taskdb",
        user="admin",
        password="admin"
    )

# 🔷 Wait for DB (important for Docker startup)
def wait_for_db():
    while True:
        try:
            conn = get_db()
            conn.close()
            print("✅ Connected to PostgreSQL")
            break
        except Exception as e:
            print("⏳ Waiting for DB...")
            time.sleep(2)

# 🔷 Initialize DB
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table initialized")

# 🔷 Run init
wait_for_db()
init_db()

# 🔷 GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT id, task FROM tasks")
        tasks = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([{"id": t[0], "task": t[1]} for t in tasks])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔷 ADD task
@app.route("/tasks", methods=["POST"])
def add_task():
    try:
        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO tasks (task) VALUES (%s)",
            (data["task"],)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Task added"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔷 DELETE task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM tasks WHERE id = %s",
            (id,)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Task deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔷 Health check (important for Kubernetes later)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# 🔷 Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
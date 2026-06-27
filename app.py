from flask import Flask, render_template
import sqlite3
from flask import request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

def create_table():

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route("/add", methods=["POST"])
def add_task():

    data = request.json

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks(task) VALUES(?)",
        (data["task"],)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Added"})

@app.route("/tasks")
def get_tasks():

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "task": row[1]
        })

    return jsonify(tasks)

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_task(id):

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Deleted"})

@app.route("/update/<int:id>", methods=["PUT"])
def update_task(id):

    data = request.json

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE tasks SET task=? WHERE id=?",
        (data["task"], id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Updated"})

if __name__ == "__main__":
    app.run(debug=True)
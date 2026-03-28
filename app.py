from flask import Flask, render_template, request, redirect
from datetime import datetime   # add this at top if not added

import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
@app.route("/")
def home():
    search = request.args.get("search")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if search:
        cur.execute("SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?", 
                    ('%' + search + '%', '%' + search + '%'))
    else:
        cur.execute("SELECT * FROM notes")

    notes = cur.fetchall()
    conn.close()

    return render_template("index.html", notes=notes)
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/add_note", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)",
        (title, content, created_at)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM notes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")
@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = cur.fetchone()

    conn.close()

    return render_template("edit.html", note=note)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    title = request.form["title"]
    content = request.form["content"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (title, content, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")
if __name__ == "__main__":
    init_db()   # This creates DB + table
    app.run(debug=True)
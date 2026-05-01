from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB", "contacts"),
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ.get("POSTGRES_PASSWORD", "password"),
        host="db"
    )

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        return "Error: All fields are required.", 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Form submitted successfully!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
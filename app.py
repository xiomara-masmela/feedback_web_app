from flask import Flask
import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "dbname=feedback_app")

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT 1', []) # Query to check that the DB connected
    conn.close()
    return 'Hello, world Yang!'

if __name__ == "__main__":
    app.run(debug=True)
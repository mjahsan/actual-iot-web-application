import os
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "landfill_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")

def get_live_data():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute("SELECT sensor_id, methane_level, truck_weight, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 10;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    except Exception as e:
        return [("Error", f"Could not connect to DB: {e}", 0, "N/A")]

@app.route('/')
def index():
    records = get_live_data()
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
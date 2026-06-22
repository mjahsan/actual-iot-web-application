import os
import time
import random
import psycopg2

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "landfill_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def init_db():
    while True:
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id SERIAL PRIMARY KEY,
                    sensor_id VARCHAR(50),
                    methane_level FLOAT,
                    truck_weight INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully.")
            break
        except Exception as e:
            print(f"Waiting for database connection... Error: {e}")
            time.sleep(5)

def simulate_data():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    
    sensors = ["SENSOR-NORTH-01", "SENSOR-SOUTH-02", "WEIGHBRIDGE-MAIN"]
    
    while True:
        sensor = random.choice(sensors)
        methane = round(random.uniform(1.2, 4.8), 2) if "SENSOR" in sensor else 0.0
        weight = random.randint(12000, 45000) if "WEIGHBRIDGE" in sensor else 0
        
        cur.execute(
            "INSERT INTO sensor_data (sensor_id, methane_level, truck_weight) VALUES (%s, %s, %s)",
            (sensor, methane, weight)
        )
        conn.commit()
        print(f"Ingested data from {sensor}: Methane={methane}%, Weight={weight}kg")
        time.sleep(10)

if __name__ == "__main__":
    init_db()
    simulate_data()
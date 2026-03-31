import sqlite3
import csv
import os

DB_NAME = "accidents.db"
DATA_DIR = "data"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON") 
    return conn


def load_csv(conn, file_name, table_name):
    cursor = conn.cursor()
    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader) 

        placeholders = ",".join(["?"] * len(headers))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        cursor.executemany(query, reader)

    conn.commit()
    print(f"Loaded {file_name} into {table_name}")


def main():
    conn = connect_db()

    try:
        print("Loading data...")

        load_csv(conn, "location.csv", "Location")
        load_csv(conn, "weather.csv", "Weather_Condition")
        load_csv(conn, "vehicle.csv", "Vehicle")
        load_csv(conn, "accident.csv", "Accident")
        load_csv(conn, "accident_vehicle.csv", "Accident_Vehicle")
        load_csv(conn, "report.csv", "Accident_Report")

        print("All data loaded successfully!")

    except Exception as e:
        print("Error occurred:", e)
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
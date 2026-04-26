import oracledb
import csv

# --- SETUP ---
LIB_DIR = r"C:\Users\Brandon\Downloads\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"
DB_USER = "BBACHOCO7534_SCHEMA_VR52O"
DB_PASS = "1F2PZ0L5R#3KSCLEMPBKH6N6tPBAM3"
DB_DSN  = "db.freesql.com:1521/23ai_34ui2"

oracledb.init_oracle_client(lib_dir=LIB_DIR)


def load_csv(cursor, file_path, table_name, sql):
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [row for row in reader]

    print(f"Loading {file_path} → {table_name} ({len(data)} rows)")
    cursor.executemany(sql, data)


def main():
    try:
        # Connect once
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
        cursor = conn.cursor()

        print("Starting data load...")

        # Location
        load_csv(cursor, "data/location.csv", "Location",
                 "INSERT INTO Location (location_id, latitude, longitude) VALUES (:1, :2, :3)")

        # Weather
        load_csv(cursor, "data/weather.csv", "Weather_Condition",
                 "INSERT INTO Weather_Condition (weather_id, condition_type) VALUES (:1, :2)")

        # Vehicle
        load_csv(cursor, "data/vehicle.csv", "Vehicle",
                 "INSERT INTO Vehicle (vehicle_id, vehicle_type) VALUES (:1, :2)")

        # Accident (FIXED DATE/TIME FORMAT)
        load_csv(cursor, "data/accident.csv", "Accident",
                 """
                 INSERT INTO Accident (
                     accident_id, accident_date, accident_time,
                     severity_level, location_id, weather_id
                 )
                 VALUES (
                     :1,
                     TO_DATE(:2, 'YYYY-MM-DD'),
                     TO_DATE(:3, 'HH24:MI:SS'),
                     :4, :5, :6
                 )
                 """)

        # Accident_Vehicle
        load_csv(cursor, "data/accident_vehicle.csv", "Accident_Vehicle",
                 "INSERT INTO Accident_Vehicle (accident_id, vehicle_id) VALUES (:1, :2)")

        # Accident_Report (timestamp handled automatically)
        load_csv(
            cursor,
            "data/report.csv",
            "Accident_Report",
            """INSERT INTO Accident_Report (accident_id, report_timestamp)
               VALUES (:1, TO_TIMESTAMP(:2, 'YYYY-MM-DD HH24:MI:SS.FF6'))"""
        )

        # Commit everything once
        conn.commit()
        print("All data loaded successfully!")

    except Exception as e:
        print("Error:", e)
        if 'conn' in locals():
            conn.rollback()

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


if __name__ == "__main__":
    main()

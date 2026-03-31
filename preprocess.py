import csv
import random
from datetime import datetime, timedelta

NUM_RECORDS = 120

# ---------- Location ----------
with open("data/location.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["location_id", "latitude", "longitude"])
    for i in range(1, NUM_RECORDS+1):
        writer.writerow([i, random.uniform(-90, 90), random.uniform(-180, 180)])

# ---------- Weather ----------
weather_types = ["Clear", "Rain", "Fog", "Snow", "Cloudy"]

with open("data/weather.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["weather_id", "condition_type"])
    for i in range(1, len(weather_types)+1):
        writer.writerow([i, weather_types[i-1]])

# ---------- Vehicle ----------
vehicle_types = ["Car", "Truck", "Motorcycle", "SUV", "Bus"]

with open("data/vehicle.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["vehicle_id", "vehicle_type"])
    for i in range(1, NUM_RECORDS+1):
        writer.writerow([i, random.choice(vehicle_types)])

# ---------- Accident ----------
start_date = datetime(2020, 1, 1)

with open("data/accident.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["accident_id", "accident_date", "accident_time", "severity_level", "location_id", "weather_id"])
    
    for i in range(1, NUM_RECORDS+1):
        date = start_date + timedelta(days=random.randint(0, 1000))
        time = timedelta(seconds=random.randint(0, 86400))
        writer.writerow([
            i,
            date.date(),
            str(time),
            random.randint(1, 5),
            random.randint(1, NUM_RECORDS),   # FK to Location
            random.randint(1, len(weather_types))  # FK to Weather
        ])

# ---------- Accident_Vehicle ----------
with open("data/accident_vehicle.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["accident_id", "vehicle_id"])

    for i in range(1, NUM_RECORDS+1):
        vehicles = random.sample(range(1, NUM_RECORDS+1), random.randint(1, 3))
        for v in vehicles:
            writer.writerow([i, v])

# ---------- Accident Report ----------
with open("data/report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["accident_id", "report_timestamp"])

    for i in range(1, NUM_RECORDS+1):
        writer.writerow([i, datetime.now()])
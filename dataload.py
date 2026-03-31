import csv

def csv_to_sql(csv_file, table_name, output_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)

        for row in reader:
            values = []
            for val in row:
                if val == '':
                    values.append('NULL')
                elif val.replace('.', '', 1).isdigit():
                    values.append(val)
                else:
                    values.append(f"'{val}'")

            line = f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n"
            output_file.write(line)

with open("dataload.sql", "w") as out:
    csv_to_sql("data/location.csv", "Location", out)
    csv_to_sql("data/weather.csv", "Weather_Condition", out)
    csv_to_sql("data/vehicle.csv", "Vehicle", out)
    csv_to_sql("data/accident.csv", "Accident", out)
    csv_to_sql("data/accident_vehicle.csv", "Accident_Vehicle", out)
    csv_to_sql("data/report.csv", "Accident_Report", out)
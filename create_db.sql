-- Drop tables (optional, for reruns)
DROP TABLE IF EXISTS Accident_Vehicle;
DROP TABLE IF EXISTS Accident_Report;
DROP TABLE IF EXISTS Accident;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Weather_Condition;

-- Location
CREATE TABLE Location (
    location_id INT PRIMARY KEY,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);

-- Weather
CREATE TABLE Weather_Condition (
    weather_id INT PRIMARY KEY,
    condition_type VARCHAR(50)
);

-- Accident
CREATE TABLE Accident (
    accident_id INT PRIMARY KEY,
    accident_date DATE,
    accident_time TIMESTAMP,
    severity_level INT,
    location_id INT,
    weather_id INT,
    FOREIGN KEY (location_id) REFERENCES Location(location_id),
    FOREIGN KEY (weather_id) REFERENCES Weather_Condition(weather_id)
);

-- Vehicle
CREATE TABLE Vehicle (
    vehicle_id INT PRIMARY KEY,
    vehicle_type VARCHAR(50)
);

-- Accident Vehicle
CREATE TABLE Accident_Vehicle (
    accident_id INT,
    vehicle_id INT,
    PRIMARY KEY (accident_id, vehicle_id),
    FOREIGN KEY (accident_id) REFERENCES Accident(accident_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
);

-- Accident Report
CREATE TABLE Accident_Report (
    accident_id INT PRIMARY KEY,
    report_timestamp TIMESTAMP,
    FOREIGN KEY (accident_id) REFERENCES Accident(accident_id)
);
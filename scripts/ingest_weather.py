import json
import os
import sys
from datetime import datetime, timezone

import requests
import psycopg2
from psycopg2.extras import execute_values

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

CITIES = [
    ("Perth", -31.9523, 115.8613),       # Perth, Australia
    ("Houston", 29.7604, -95.3698),      # Houston, Texas
    ("Melbourne", -37.8136, 144.9631),   # Melbourne, Australia
]

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "analytics"),
        user=os.getenv("PGUSER", "warehouse"),
        password=os.getenv("PGPASSWORD", "warehouse123"),
    )

def fetch_weather(city, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto",
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch weather for {city}: {e}")

    if "current" not in data:
        raise RuntimeError(f"Missing 'current' data for {city}")

    return data

def main():
    if len(CITIES) != 3:
        sys.exit(1)
    batch_ingested_at = datetime.now(timezone.utc)

    rows = []
    for city, lat, lon in CITIES:
        data = fetch_weather(city, lat, lon)
        rows.append((city, batch_ingested_at, json.dumps(data)))
        print(f"Fetched weather for {city}")
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO raw.weather_raw (city, batch_ingested_at, data_json)
                    VALUES %s
                """
                execute_values(cur, sql, rows, template="(%s, %s, %s::jsonb)")
    finally:
        conn.close()
    print("Inserted weather data into database.")

if __name__ == "__main__":
    main()



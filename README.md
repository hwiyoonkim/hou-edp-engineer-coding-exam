# Data Pipeline Take-Home Assessment

## Overview

Build a small data pipeline that ingests weather data and transforms it into analytics-ready views.

**Time estimate:** 60–120 minutes

---

## The Task

You'll build a pipeline that:

1. Fetches current weather for **3 cities** from a public API
2. Inserts **3 rows** (one per city) into a raw table as JSON
3. Creates SQL views to parse and expose the data

The key concept: each script run is a **batch**. All 3 rows from a single run share the same `batch_ingested_at` timestamp.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- `psql` command-line tool (optional, for verification)

### Start the Database

```bash
docker compose up -d
```

This starts PostgreSQL with the schema already created. Verify it's running:

```bash
docker compose ps
```

### Python Environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install requests psycopg2-binary
```

---

## What You'll Build

### 1. Python Ingestion Script

**Create:** `scripts/ingest_weather.py`

**Requirements:**

- Fetch current weather for exactly 3 hardcoded cities using the Open-Meteo API
- Insert 3 rows into `raw.weather_raw`
- All 3 rows must share the same `batch_ingested_at` timestamp
- Store the full API response in `data_json`
- If any city fetch fails, fail the entire run (no partial batch)

**API Example:**

```
GET https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current=temperature_2m,wind_speed_10m&timezone=auto
```

**Sample Response:**

```json
{
  "latitude": 40.710335,
  "longitude": -73.99307,
  "timezone": "America/New_York",
  "current": {
    "time": "2024-01-15T14:00",
    "temperature_2m": 5.2,
    "wind_speed_10m": 12.3
  }
}
```

**Database Connection:**

Use environment variables if set, otherwise default to:

| Parameter | Default Value   |
|-----------|-----------------|
| Host      | localhost       |
| Port      | 5432            |
| Database  | analytics       |
| User      | warehouse       |
| Password  | warehouse123    |

**Run with:**

```bash
python scripts/ingest_weather.py
```

---

### 2. SQL Transforms

**Create:** `sql/01_staging.sql`

Create a view `staging.weather_typed` that parses the JSON into typed columns:

| Column            | Type        | Description                    |
|-------------------|-------------|--------------------------------|
| city              | text        | City name                      |
| batch_ingested_at | timestamptz | When this batch was ingested   |
| ingested_at       | timestamptz | Row insert timestamp           |
| temperature       | numeric     | Temperature in Celsius         |
| wind_speed        | numeric     | Wind speed in km/h             |

---

**Create:** `sql/02_current.sql`

Create a view `analytics.weather_current` that returns **only the latest batch** (all 3 rows from the most recent run).

---

### 3. Short Writeup

**Create:** `SOLUTION.md`

Answer these questions briefly:

1. If this pipeline ran every hour unattended, what could cause **silent data quality issues**?
2. What **single metric** would you alert on first?
3. What's **one improvement** you'd make next?

---

## Verification

After completing the deliverables:

```bash
# Run your ingestion
python scripts/ingest_weather.py

# Apply your SQL transforms
psql "postgres://warehouse:warehouse123@localhost:5432/analytics" -f sql/01_staging.sql
psql "postgres://warehouse:warehouse123@localhost:5432/analytics" -f sql/02_current.sql

# Check results
psql "postgres://warehouse:warehouse123@localhost:5432/analytics" \
  -c "SELECT city, batch_ingested_at, temperature, wind_speed FROM analytics.weather_current ORDER BY city;"
```

**Expected:** 3 rows, all with the same `batch_ingested_at` value.

---

## Deliverables Checklist

```
weather-pipeline-assessment/
├── scripts/
│   └── ingest_weather.py      # Your Python script
├── sql/
│   ├── 01_staging.sql         # staging.weather_typed view
│   └── 02_current.sql         # analytics.weather_current view
└── SOLUTION.md                # Your writeup
```

---

## Evaluation Criteria

| Area                | What We're Looking For                                      |
|---------------------|-------------------------------------------------------------|
| **Correctness**     | Pipeline works end-to-end; current view returns full batch  |
| **Error Handling**  | API failures handled; no partial batches inserted           |
| **SQL Quality**     | Clean transforms; proper JSON parsing with type handling    |
| **Operational Mind**| Thoughtful answers about monitoring and failure modes       |

---

## Cleanup

When you're done:

```bash
docker compose down -v
```

---

## Questions?

If anything is unclear, document your assumptions in `SOLUTION.md` and proceed with your best judgment.
Any questions can be directed to tate.walker@versent.com.au

Good luck!

-- Schema setup
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Raw landing table for weather data
CREATE TABLE IF NOT EXISTS raw.weather_raw (
    id                BIGSERIAL PRIMARY KEY,
    city              TEXT NOT NULL,
    batch_ingested_at TIMESTAMPTZ NOT NULL,
    ingested_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_json         JSONB NOT NULL
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_weather_raw_batch
    ON raw.weather_raw (batch_ingested_at DESC);

CREATE INDEX IF NOT EXISTS idx_weather_raw_city_batch
    ON raw.weather_raw (city, batch_ingested_at DESC);

CREATE OR REPLACE VIEW analytics.weather_current AS
SELECT
    city,
    batch_ingested_at,
    ingested_at,
    temperature,
    wind_speed
FROM staging.weather_typed
WHERE batch_ingested_at = (
    SELECT MAX(batch_ingested_at)
    FROM raw.weather_raw
);

CREATE OR REPLACE VIEW staging.weather_typed AS
SELECT
    city,
    batch_ingested_at,
    ingested_at,
    (data_json -> 'current' ->> 'temperature_2m')::numeric AS temperature,
    (data_json -> 'current' ->> 'wind_speed_10m')::numeric AS wind_speed
FROM raw.weather_raw;
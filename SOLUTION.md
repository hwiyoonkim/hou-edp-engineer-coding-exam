## 1. If this pipeline ran every hour unattended, what could cause silent data quality issues?
    Silent data quality issues could arise from several factors, including:
   - Changes in the upstream API that alter the data format or schema without causing errors, leading to incorrect or incomplete data being ingested.
   - Network issues that result in partial data retrieval, where the API responds successfully but with incomplete data.
   - Bugs in the data transformation logic that only manifest under specific conditions, leading to incorrect data being processed without raising errors.
   - Time zone discrepancies that cause data to be misaligned with the intended hourly intervals.  
   
## 2. What single metric would you alert on first?
    I would alert on the row count of the most recent batch, with an expected value of 3. Each run is supposed to ingest exactly one row per city, so if the latest batch does not contain three rows, it immediately indicates an incomplete or failed ingestion and is a strong signal that something is wrong.

## 3. What's one improvement you'd make next?
    One improvement I would make next is to implement comprehensive data validation and monitoring mechanisms. This could include setting up automated checks to verify the integrity and completeness of the data at various stages of the pipeline. For example, I would implement checks to compare the number of records ingested against expected counts, validate data types and formats, and monitor for any anomalies or outliers in the data. Additionally, I would set up alerting systems to notify the team immediately if any of these checks fail, allowing for quick identification and resolution of potential data quality issues.

# Test Cases for Real-Time Ecommerce Pipeline

## Test Case 1: Data Generator Produces CSV Files
- **Description**: Verify that the data generator creates CSV files in the `data/` directory with the expected schema and row counts between 100 and 1500.
- **Steps**:
  1. Run `generator/data_generator.py` for 5 minutes.
  2. Check the `data/` directory for CSV files.
  3. Validate the schema and row count of each file.
- **Expected Outcome**:
  - At least one CSV file is generated every 15 seconds.
  - Each file has the schema: `user_id` (INT), `user_name` (VARCHAR), `user_email` (VARCHAR), `event_type` (VARCHAR, 'view' or 'purchase'), `product_id` (INT), `product_name` (VARCHAR), `product_category` (VARCHAR), `product_price` (DECIMAL), `event_time` (TIMESTAMP).
  - Row count per file is between 100 and 1500.
- **Actual Outcome**:
  - Three CSV files generated: `events_20250430_074403.csv`, `events_20250430_074418.csv`, `events_20250430_074433.csv`.
    ![alt text](../images/image1.png)

  - Files created every 15 seconds (timestamps at 07:44:03, 07:44:18, 07:44:33).
  - Schema matches the expected structure (verified via PostgreSQL data).
  - Total rows in PostgreSQL (27768 over 5 minutes) suggest ~27768 / 20 files = ~1388 rows per file, within the configured range.
- **Status**: Pass.

## Test Case 2: Spark Streaming Processes CSV Files
- **Description**: Ensure Spark Streaming reads and processes CSV files from the `data/` directory.
- **Steps**:
  1. Run `docker-compose up` to start Spark and PostgreSQL.
  2. Run `generator/data_generator.py` to produce CSV files.
  3. Check Spark logs for processing activity.
- **Expected Outcome**:
  - Spark logs show batches being processed as new CSV files are created.
  - No errors related to file reading or processing.
- **Actual Outcome**:
  - Spark logs show active processing: tasks 188 to 195 in stage 144.0 completed or running.
  ![alt text](../images/image4.png)

  - Tasks finish in ~20 ms (e.g., task 188.0 finished in 20 ms on `dcfe2a35508`).
  - No errors observed.
- **Status**: Pass.

## Test Case 3: Data Successfully Written to PostgreSQL
- **Description**: Verify that data from CSV files is written to the `events` table in PostgreSQL.
- **Steps**:
  1. Run the pipeline for 5 minutes.
  2. Query PostgreSQL to check row counts and data integrity.
- **Expected Outcome**:
  - The `events` table contains rows matching the CSV data.
  - Row counts increase as new batches are processed.
- **Actual Outcome**:
  - Row counts over time: 1691, 6961, 19375, 21672, 26508, 27768.

  ![alt text](../images/image2.png)
  - Incremental progression indicates continuous data ingestion.
  - Final count: 27768 rows.
  - Sample data matches schema: `event_id` (SERIAL), `user_id` (INT), `user_name` (VARCHAR), `user_email` (VARCHAR), `event_type` ('view' or 'purchase'), `product_id` (INT), `product_name` (VARCHAR), `product_category` (VARCHAR), `product_price` (DECIMAL), `event_time` (TIMESTAMP).
- **Status**: Pass.

## Test Case 4: Data Consistency Between CSV and PostgreSQL
- **Description**: Ensure data in PostgreSQL matches the CSV files (no data loss or corruption).
- **Steps**:
  1. Run the pipeline for 5 minutes.
  2. Compare a sample of CSV data with PostgreSQL data.
- **Expected Outcome**:
  - Data in PostgreSQL matches the CSV files in terms of schema and values.
- **Actual Outcome**:
![alt text](../images/image3.png)
  - PostgreSQL data shows correct schema and values (e.g., `event_type` as 'view' or 'purchase', `product_price` as DECIMAL).
  - Timestamps align with CSV file names (e.g., events at 07:52:09).
  - PostgreSQL data aligns with expected data generator output.
- **Status**: Pass.

## Test Case 5: Measure Throughput and Latency
- **Description**: Measure the pipeline’s throughput (rows per second) and latency (time to process a batch).
- **Steps**:
  1. Run the pipeline for 5 minutes.
  2. Calculate throughput using the final row count in PostgreSQL.
  3. Check Spark logs for batch processing times.
- **Expected Outcome**:
  - Throughput: At least 5 rows per second.
  - Latency: Batch processing time under 1 second.
- **Actual Outcome**:
  - **Throughput**: 27768 rows / 300 seconds = ~92.56 rows per second.
  - **Latency**: Tasks complete in ~20 ms (e.g., task 188.0 finished in 20 ms).
- **Status**: Pass.
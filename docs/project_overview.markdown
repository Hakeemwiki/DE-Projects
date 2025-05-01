# Project Overview: Real-Time Ecommerce Pipeline

![alt text](images/system_architecture.png)

## Purpose
The Real-Time Ecommerce Pipeline project simulates an ecommerce platform’s event tracking system, processing user events (e.g., 'view' or 'purchase') in real-time and storing them in a PostgreSQL database for analysis. It leverages Apache Spark Streaming for scalable, fault-tolerant processing.

## Components
1. **Data Generator (`generator/data_generator.py`)**:
   - Generates synthetic ecommerce events as CSV files.
   - Configurable via `.env` (e.g., `MIN_EVENTS`, `MAX_EVENTS`, `SLEEP_INTERVAL`).
   - Writes files to the `data/` directory every 15 seconds.
2. **Spark Streaming (`spark/spark_streaming_to_postgres.py`)**:
   - Reads CSV files from `data/` as a streaming data source.
   - Cleans data by removing duplicates based on `user_id` and `event_time`.
   - Writes processed data to PostgreSQL using the `foreachBatch` method.
3. **PostgreSQL Database**:
   - Stores event data in the `events` table.
   - Schema: `event_id` (SERIAL PRIMARY KEY), `user_id` (INT), `user_name` (VARCHAR), `user_email` (VARCHAR), `event_type` (VARCHAR, 'view' or 'purchase'), `product_id` (INT), `product_name` (VARCHAR), `product_category` (VARCHAR), `product_price` (DECIMAL), `event_time` (TIMESTAMP).
   - Includes indexes on `event_time` and `user_id` for query optimization.
4. **Docker Compose (`docker-compose.yml`)**:
   - Orchestrates `postgres` and `spark` services.
   - Uses `spark/dockerfile` to build the Spark service.
   - Ensures network connectivity and resource limits.

## Architecture
The system architecture is depicted in `System_architecture.png`:
- **Data Generator**: Produces CSV files to `data/`.
- **CSV Files**: Input data source for Spark Streaming.
- **Spark Streaming**: Reads CSV files, processes them, and writes to PostgreSQL.
- **PostgreSQL**: Stores processed events for persistence and querying.

## Workflow
1. The data generator creates a CSV file every 15 seconds, containing 100–1500 rows of ecommerce events.
2. Spark Streaming monitors `data/`, reading new CSV files.
3. Spark processes each batch, removing duplicates, and writes to the `events` table in PostgreSQL.
4. The pipeline runs continuously with checkpointing for fault tolerance.

## Key Features
- **Real-Time Processing**: Low latency (~20 ms per batch).
- **Scalability**: Spark Streaming scales with data volume.
- **Fault Tolerance**: Checkpointing ensures recovery from failures.
- **Data Integrity**: Removes duplicates and enforces `event_type` constraints.

## Performance
- **Throughput**: 92.56 rows per second (27768 rows over 5 minutes).
- **Latency**: ~20 ms per batch.
- Detailed metrics in `docs/performance_metrics.md`.

## Setup and Usage
Refer to `docs/User_guide.md` for setup instructions, including running `db/postgres_setup.sql` to initialize the database. The project uses Docker Compose for containerized deployment.
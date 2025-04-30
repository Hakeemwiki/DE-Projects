# User Guide for Real-Time Ecommerce Pipeline

## Overview
This guide provides instructions for setting up and running the Real-Time Ecommerce Pipeline, which processes synthetic ecommerce events in real-time using Apache Spark Streaming and stores them in a PostgreSQL database. The project is containerized using Docker Compose, manageable via **Docker Desktop**, and the PostgreSQL database can be initialized using `db/postgres_setup.sql` and accessed via **pgAdmin 4** or command-line tools. **VS Code** is used for file management and terminal operations.

## Prerequisites
- **Docker Desktop** installed and running on your system.
- **pgAdmin 4** installed (desktop or web version) for graphical PostgreSQL management.
- **VS Code** installed for editing and running scripts.
- Python 3.8+ for running the data generator locally.
- Basic familiarity with Docker Desktop, pgAdmin 4, and VS Code.

## Project Structure
- `generator/data_generator.py`: Generates synthetic ecommerce event data as CSV files.
- `spark/spark_streaming_to_postgres.py`: Spark Streaming script to process CSV files and write to PostgreSQL.
- `db/postgres_setup.sql`: SQL script to create the `events` table and indexes in PostgreSQL.
- `spark/dockerfile`: Dockerfile for the Spark service.
- `spark/postgresql-42.7.5.jar`: PostgreSQL JDBC driver for Spark.
- `docker-compose.yml`: Defines services for Spark and PostgreSQL.
- `.env`: Stores environment variables (e.g., database credentials, data generator settings).
- `data/`: Directory for storing generated CSV files (mounted as a volume).
- `checkpoints/`: Directory for Spark checkpointing (mounted as a volume).
- `docs/`: Contains documentation (e.g., `User_guide.md`, `project_overview.md`).

## Setup Instructions

### 1. Clone the Repository
Clone the project repository and open it in VS Code:
```bash
git clone <repository-url>
cd <repository-directory>
code .
```
In **VS Code**, the project folder will open, displaying directories like `generator/`, `spark/`, and `db/`.

### 2. Configure Environment Variables
In **VS Code**, create or edit `.env` in the project root with:
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword
POSTGRES_DB=ecommerce
MIN_EVENTS=100
MAX_EVENTS=1500
SLEEP_INTERVAL=15
```
- `POSTGRES_*`: PostgreSQL credentials and database name.
- `MIN_EVENTS` and `MAX_EVENTS`: Range of rows per CSV file.
- `SLEEP_INTERVAL`: Time (in seconds) between CSV file generations.
Save the file in VS Code.

### 3. Set Up Directories
Create directories for data and checkpoints:
```bash
mkdir data checkpoints
```
In **VS Code**, these should appear in the Explorer pane as `data/` and `checkpoints/`, or create them via right-click > **New Folder**.

### 4. Verify PostgreSQL JDBC Driver
The `spark/postgresql-42.7.5.jar` file should already be in the `spark/` directory (visible in VS Code’s Explorer). If not, download it:
```bash
curl -o spark/postgresql-42.7.5.jar https://jdbc.postgresql.org/download/postgresql-42.7.5.jar
```
Or download manually from `https://jdbc.postgresql.org/download.html` and move it to `spark/` in VS Code.

### 5. Build and Start Docker Services with Docker Desktop
1. Open **Docker Desktop** and ensure it’s running.
2. In **VS Code**, open the integrated terminal (Ctrl+`) and run:
   ```bash
   docker-compose up -d
   ```
   This builds the Spark service using `spark/dockerfile` and starts the `postgres` and `spark` services.
3. In **Docker Desktop**:
   - Go to the **Containers** tab.
   - Verify that two containers (e.g., `<project-directory>_postgres_1` and `<project-directory>_spark_1`) are running.
   - Click a container to view logs or access its CLI by clicking the **CLI** button.

### 6. Initialize the PostgreSQL Database with db/postgres_setup.sql
The `db/postgres_setup.sql` script creates the `events` table with the correct schema and indexes. Run it using pgAdmin 4, VS Code’s terminal, or Docker Desktop’s CLI.

#### Option 1: Using pgAdmin 4
1. Launch **pgAdmin 4**.
2. Add a new server:
   - Right-click **Servers** > **Create** > **Server**.
   - Name: `ecommerce_db`.
   - In the **Connection** tab:
     - **Host**: `localhost` (or `postgres` if pgAdmin is on the same Docker network).
     - **Port**: `5433`.
     - **Maintenance database**: `ecommerce`.
     - **Username**: `admin`.
     - **Password**: `securepassword` (from `.env`).
   - Save the connection.

   - After connecting to port 5433 and everything in the docker file is up and running your events table should be created.
   - Verify the `events` table exists under `Tables` with indexes (`idx_event_time`, `idx_user_id`).

#### Option 2: Using VS Code Terminal
1. In **VS Code**, open the integrated terminal (Ctrl+`).
2. Copy `db/postgres_setup.sql` to the PostgreSQL container:
   ```bash
   docker cp db/postgres_setup.sql <postgres-container-id>:/postgres_setup.sql
   ```
3. Access the PostgreSQL container:
   ```bash
   docker exec -it <postgres-container-id> bash
   ```
4. Run the script:
   ```bash
   psql -U admin -d ecommerce -f /postgres_setup.sql
   ```
5. Exit the container:
   ```bash
   exit
   ```

#### Option 3: Using Docker Desktop CLI
1. In **Docker Desktop**, click the `postgres` container > **CLI** button.
2. Copy `db/postgres_setup.sql` to the container (from VS Code terminal):
   ```bash
   docker cp db/postgres_setup.sql <postgres-container-id>:/postgres_setup.sql
   ```
3. In the Docker Desktop CLI, run:
   ```bash
   psql -U admin -d ecommerce -f /postgres_setup.sql
   ```

### 7. Verify Database Schema
In **pgAdmin 4**, expand `ecommerce_db` > `Tables` > `events` to confirm the schema:
- Columns: `event_id` (SERIAL PRIMARY KEY), `user_id` (INT), `user_name` (VARCHAR), `user_email` (VARCHAR), `event_type` (VARCHAR), `product_id` (INT), `product_name` (VARCHAR), `product_category` (VARCHAR), `product_price` (DECIMAL), `event_time` (TIMESTAMP).
- Constraint: `valid_event_type` (ensures `event_type` is 'view' or 'purchase').
- Indexes: `idx_event_time`, `idx_user_id`.

## Running the Pipeline

### 1. Start the Data Generator
In **VS Code**, open the integrated terminal and run:
```bash
python3 generator/data_generator.py
```
- The script generates one CSV file every 15 seconds (per `SLEEP_INTERVAL`).
- Files appear in the `data/` directory with names like `events_YYYYMMDD_HHMMSS.csv`.
- In VS Code’s Explorer, monitor `data/` to confirm file creation.

### 2. Run the Spark Streaming Job
Submit the Spark Streaming job to process CSV files and write to PostgreSQL:
1. In **Docker Desktop**, click the `spark` container > **CLI** button.
2. Run:
   ```bash
   spark-submit --jars /spark/postgresql-42.7.5.jar /spark/spark_streaming_to_postgres.py
   ```
Or, in **VS Code**’s terminal:
```bash
docker exec -it <spark-container-id> spark-submit \
  --jars /spark/postgresql-42.7.5.jar \
  /spark/spark_streaming_to_postgres.py
```
- The job monitors the `data/` directory, processes new CSV files, and writes to the `events` table.
- In **Docker Desktop**, view the `spark` container’s logs to monitor processing.

### 3. Verify Data in PostgreSQL with pgAdmin 4
1. In **pgAdmin 4**, connect to `ecommerce_db`.
2. Open the **Query Tool** and run:
   ```sql
   SELECT COUNT(*) FROM events;
   ```
3. View sample data:
   - Right-click `events` table > **View/Edit Data** > **First 100 Rows**.
   - Or run:
     ```sql
     SELECT * FROM events LIMIT 5;
     ```
4. Confirm `event_type` values are 'view' or 'purchase' and `product_price` is in DECIMAL format.

### 4. (Optional) Verify Data via VS Code Terminal
In **VS Code**’s terminal:
```bash
docker exec -it <postgres-container-id> psql -U admin -d ecommerce -c "SELECT COUNT(*) FROM events;"
```
Sample data query:
```sql
SELECT * FROM events LIMIT 5;
```

## Stopping the Pipeline
1. Stop the data generator by pressing `Ctrl+C` in the VS Code terminal running `generator/data_generator.py`.
2. Stop the Spark job by pressing `Ctrl+C` in the Spark container’s CLI or VS Code terminal.
3. Shut down Docker services:
   - In **Docker Desktop**, select both containers, click **Stop**, then **Remove**.
   - Or, in **VS Code**’s terminal:
     ```bash
     docker-compose down
     ```

## Troubleshooting
- **Spark cannot find `data/` directory**:
  - Ensure `data/` exists in the project root (check in VS Code’s Explorer).
  - In **Docker Desktop**, inspect the `spark` container’s **Volumes** tab to verify the `data/` mount.
- **PostgreSQL connection refused**:
  - Confirm the `postgres` container is running in **Docker Desktop**’s **Containers** tab.
  - Verify `POSTGRES_HOST=postgres` in `spark/spark_streaming_to_postgres.py`.
- **Missing JDBC driver**:
  - Ensure `spark/postgresql-42.7.5.jar` is in the `spark/` directory and mounted to the Spark container.
- **pgAdmin 4 cannot connect to PostgreSQL**:
  - Verify host (`localhost` or `postgres`), port (`5433`), and credentials match `.env`.
- **Schema mismatch**:
  - Confirm `db/postgres_setup.sql` was executed (check `events` table schema in pgAdmin 4).
  - Ensure `generator/data_generator.py` outputs data matching the schema (e.g., `INT` for `user_id`, `event_type` as 'view' or 'purchase').

## Performance Monitoring
- **Throughput**: Calculate rows per second in **pgAdmin 4** (e.g., 27768 rows / 300 seconds = 92.56 rows/second).
- **Latency**: Check Spark logs in **Docker Desktop** (typically ~20 ms).
- Refer to `docs/performance_metrics.md` for detailed metrics.

## Notes
- The pipeline uses checkpointing (`checkpoints/`) for fault tolerance. Do not delete `checkpoints/` while running.
- Adjust `MAX_EVENTS` and `SLEEP_INTERVAL` in `.env` (edit in VS Code) to simulate different data loads.
- **Docker Desktop**’s **Images** tab can help manage disk space by removing unused images.
- Ensure `generator/data_generator.py` and `spark/spark_streaming_to_postgres.py` match the `events` table schema in `db/postgres_setup.sql`.

For further details, refer to `docs/project_overview.md` and `docs/test_cases.md`.
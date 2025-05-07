# Heartbeat Monitoring Project

![alt text](<Data Flow Diagram.png>)

## Overview
This project implements a real-time heartbeat monitoring system using Apache Kafka for message streaming, a PostgreSQL database for data storage, and visualization tools (Kafka-UI and Grafana). The system generates synthetic heartbeat data for 1,000 unique customers(Trial purposes), sends it to a Kafka topic, processes it with a consumer, stores it in PostgreSQL, and visualizes it for monitoring purposes.

### Architecture
- **Producer**: Generates heartbeat data (customer ID, timestamp, heart rate) and sends it to the `heartbeats` Kafka topic.
- **Kafka**: Manages the message queue with a single broker and auto-created topics.
- **Consumer**: Subscribes to the `heartbeats` topic, processes messages, and stores them in a PostgreSQL database.
- **PostgreSQL**: Stores heartbeat records in the `heartbeats` table.
- **Kafka-UI**: Provides a web interface to monitor Kafka topics and messages.
- **Grafana**: Visualizes heartbeat data from PostgreSQL in real-time dashboards.

## Prerequisites
- Docker and Docker Compose installed on your system.
- Environment variables defined in a `.env` file (e.g., `POSTGRESQL_USERNAME`, `POSTGRESQL_PASSWORD`, `POSTGRESQL_DATABASE`).

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd heart_beat_monitoring
```

### 2. Configure Environment Variables
Create a `.env` file in the project root with the following content (replace with your values):
```
POSTGRESQL_USERNAME=admin
POSTGRESQL_PASSWORD=your_password
POSTGRESQL_DATABASE=heartbeat_db
```

### 3. Build and Start the Services
Run the following command to build and start all services using Docker Compose:
```bash
docker-compose up -d --build
```

- This starts ZooKeeper, Kafka, PostgreSQL, Kafka-UI, the producer, the consumer, and Grafana.
- The `-d` flag runs services in detached mode.

### 4. Verify Services
- **Kafka-UI**: Open `http://localhost:8080` to monitor the `heartbeats` topic.
- **Grafana**: Open `http://localhost:3000`, log in with `admin`/`admin` (change password on first login), and set up the PostgreSQL data source (see Visualization section).
- **PostgreSQL**: Connect using `psql -h localhost -p 5434 -U admin -d heartbeat_db` to verify data.

### 5. Check Logs
Monitor service status and troubleshoot issues:
```bash
docker-compose logs -f producer consumer
docker-compose logs -f kafka
```

## Usage

### Data Generation
- The `data_generator.py` script generates synthetic heartbeat data for 1,000 unique customers with heart rates between 50 and 120 bpm (90% in 60-100 range, 10% outliers).
- The `kafka_producer.py` sends this data to the `heartbeats` topic every 1 second.

### Data Consumption
- The `kafka_consumer.py` subscribes to the `heartbeats` topic, processes messages, and inserts them into the PostgreSQL `heartbeats` table.

### Database Schema
The `heartbeats` table is created using `schema.sql`:
- Columns: `id` (SERIAL PRIMARY KEY), `customer_id` (VARCHAR), `timestamp` (TIMESTAMPTZ), `heart_rate` (INTEGER).
- Constraints: `heart_rate` must be between 1 and 300.
- Indexes: `idx_timestamp` and `idx_customer_id` for efficient queries.

### Visualization
- **Kafka-UI**: View message counts and details at `http://localhost:8080`.
- **Grafana**:
  1. Add a PostgreSQL data source:
     - Host: `postgresql:5432`
     - Database: `heartbeat_db`
     - User: `${POSTGRESQL_USERNAME}`
     - Password: `${POSTGRESQL_PASSWORD}`
     - SSL Mode: `disable`
  2. Create a dashboard with a panel:
     - Query: `SELECT "timestamp" AS "time", "heart_rate" AS "value" FROM heartbeats WHERE $__timeFilter("timestamp") ORDER BY "timestamp" ASC`
     - Visualization: Time Series
     - Title: “Heartbeat Rate Over Time”
  3. Save and monitor live data.

## Project Files
- `config.yml`: Configuration for Kafka and PostgreSQL connections.
- `data_generator.py`: Generates synthetic heartbeat data.
- `kafka_producer.py`: Sends data to Kafka.
- `kafka_consumer.py`: Processes Kafka messages and stores them in PostgreSQL.
- `docker-compose.yml`: Defines all services and their dependencies.
- `requirements.txt`: Lists Python dependencies.
- `Dockerfile.consumer`: Builds the consumer container.
- `Dockerfile.producer`: Builds the producer container.
- `schema.sql`: Defines the PostgreSQL table structure.

## Screenshots
- Kafka-UI showing `heartbeats` topic with >250 messages: 
![alt text](images/Kafka_UI.png)


- Grafana dashboard displaying heartbeat rate over time: 
![alt text](<dashboard/Grafana Dashboard.png>)


- PostgreSQL query results (e.g., `SELECT * FROM heartbeats LIMIT 10`):
![alt text](images/Sql_table.png)


- Logs showing successful `Sent` and `Stored` messages:
![alt text](images/Producer_consumer.png)



## Troubleshooting
- **Producer fails with `NoBrokersAvailable`**: Increase the `sleep` delay in `docker-compose.yml` (e.g., `sleep 30`) and check Kafka logs.
- **Consumer not storing data**: Verify PostgreSQL connection in `config.yml` (use `postgresql:5432`) and check logs for errors.
- **No data in Grafana**: Ensure the producer is running and the PostgreSQL data source is correctly configured.

## Acknowledgments
- Uses open-source tools: Kafka, PostgreSQL, Grafana, and Python libraries.
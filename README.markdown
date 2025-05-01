# Real-Time E-Commerce Data Pipeline

## Overview
This project implements a real-time data pipeline for processing e-commerce events using **Apache Spark Structured Streaming**, **PostgreSQL**, and **Docker**. It ingests synthetic event data (e.g., product views and purchases) from CSV files, processes them with PySpark, and stores the results in a PostgreSQL database. The pipeline is designed for scalability, fault tolerance, and ease of deployment, making it ideal for real-time analytics in an e-commerce context.

For a detailed project overview, see [Project Overview](docs/project_overview.markdown).

## Features
- **Data Generation**: Generates synthetic e-commerce events using a Python script.
- **Real-Time Processing**: Uses Spark Structured Streaming to process CSV files as they are generated.
- **Persistent Storage**: Stores processed events in a PostgreSQL database with a predefined schema.
- **Containerized Deployment**: Runs Spark and PostgreSQL in Docker containers for consistency.
- **Comprehensive Documentation**: Includes performance metrics, test cases, and a user guide in the `docs/` directory.

## Repository Structure
```
DE-PROJECTS/
├── data/                     # Directory for generated CSV files
├── db/
│   └── postgres_setup.sql    # SQL script to initialize the PostgreSQL events table
├── docs/
│   ├── performance_metrics.markdown  # Performance metrics and benchmarks
│   ├── project_overview.markdown     # Detailed project overview
│   ├── test_cases.markdown           # Test cases for validation
│   └── User_guide.markdown           # User guide for setup and usage
├── generator/
│   └── data_generator.py     # Script to generate synthetic event data
├── spark/
│   ├── dockerfile            # Dockerfile for building the Spark container
│   ├── postgresql-42.7.5.jar # PostgreSQL JDBC driver for Spark
│   └── spark_streaming_to_postgres.py # PySpark script for streaming data to PostgreSQL
├── .env                      # Environment variables (not tracked in Git)
├── .gitignore                # Git ignore file
├── docker-compose.yml        # Docker Compose configuration for Spark and PostgreSQL
└── README.md                 # Project documentation
```

## Prerequisites
- **Docker** and **Docker Desktop**: For running containers.
- **pgAdmin 4**: For optional database management (GUI).
- **Python 3.8+**: For running the data generator locally.
- **Git**: For cloning the repository.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd DE-PROJECTS
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with the following:
     ```
     POSTGRES_USER=your_username
     POSTGRES_PASSWORD=your_password
     POSTGRES_DB=ecommerce_db
     POSTGRES_PORT=5433
     EVENT_TYPES=view,purchase
     MIN_EVENTS=100
     MAX_EVENTS=1000
     SLEEP_INTERVAL=15
     ```
   - Ensure `.env` is listed in `.gitignore` to avoid committing sensitive data.

3. **Prepare the Data Directory**:
   - Create the `data/` directory if it doesn't exist:
     ```bash
     mkdir -p data
     ```

4. **Verify the PostgreSQL JDBC Driver**:
   - Ensure `postgresql-42.7.5.jar` is in the `spark/` directory. If missing, download it from [Maven Repository](https://mvnrepository.com/artifact/org.postgresql/postgresql/42.7.5).

## Usage
For detailed usage instructions, refer to the [User Guide](docs/User_guide.markdown). A brief overview is provided below:

1. **Start the Services**:
   - Launch PostgreSQL and Spark containers using Docker Compose:
     ```bash
     docker-compose up -d
     ```
   - Verify the services are running:
     ```bash
     docker ps
     ```

2. **Generate Synthetic Data**:
   - Run the data generator script:
     ```bash
     python3 generator/data_generator.py
     ```
   - This generates CSV files in the `data/` directory every 15 seconds (configurable via `.env`).

3. **Monitor Spark Processing**:
   - Spark processes the CSV files and writes to PostgreSQL.
   - Check Spark logs:
     ```bash
     docker logs spark
     ```
   - Access the Spark web UI at `http://localhost:8080` (if enabled).

4. **Query the Database**:
   - Use pgAdmin 4 to connect to PostgreSQL (host: `localhost`, port: `5432`, database: `ecommerce_db`, credentials from `.env`).
   - Or use `psql`:
     ```bash
     docker exec -it postgres psql -U your_username -d ecommerce_db
     ```

5. **Stop the Services**:
   - Shut down the containers:
     ```bash
     docker-compose down
     ```

## Documentation
- **Project Overview**: Learn more about the project's goals and architecture in [Project Overview](docs/project_overview.markdown).
- **Performance Metrics**: Review benchmarks and performance data in [Performance Metrics](docs/performance_metrics.markdown).
- **Test Cases**: Explore validation and testing details in [Test Cases](docs/test_cases.markdown).
- **User Guide**: Find detailed setup and usage instructions in [User Guide](docs/User_guide.markdown).

## Key Components
- **`docker-compose.yml`**: Defines PostgreSQL and Spark services with network and volume configurations.
- **`db/postgres_setup.sql`**: Initializes the `events` table in PostgreSQL with constraints and indexes.
- **`generator/data_generator.py`**: Generates synthetic e-commerce events using the `Faker` library.
- **`spark/spark_streaming_to_postgres.py`**: PySpark script for streaming data processing and storage.
- **`spark/dockerfile`**: Builds the Spark container with necessary dependencies.

## Troubleshooting
- **Spark Cannot Find Data**:
  - Ensure CSV files are being generated in `data/` and the volume mapping (`./data:/data:rw`) is correct.
- **PostgreSQL Connection Issues**:
  - Verify `.env` settings and ensure the `postgres` service is running before Spark.
- **Missing JDBC Driver**:
  - Confirm `postgresql-42.7.5.jar` is in `spark/` and correctly copied in the Dockerfile.
- **Syntax Errors**:
  - Check for comments after backslashes (`\`) in Python files or the Dockerfile, which can cause issues.

## Development Notes
- **Performance**: See [Performance Metrics](docs/performance_metrics.markdown) for optimization details.
- **Testing**: Refer to [Test Cases](docs/test_cases.markdown) for validation steps.
- **Fault Tolerance**: Spark uses checkpointing (`/data/checkpoints`) for recovery.
- **Scalability**: Configurable via `maxFilesPerTrigger` in `spark_streaming_to_postgres.py`.



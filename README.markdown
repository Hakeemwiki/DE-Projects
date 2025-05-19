# Flight Price Analysis Project

## Overview

The **Flight Price Analysis** project is a data pipeline designed to extract, process, and analyze flight price data to provide actionable insights through key performance indicators (KPIs). The pipeline uses Apache Airflow to orchestrate the workflow, MySQL for raw data storage, PostgreSQL for processed data and Airflow metadata, and Grafana for visualization. The goal is to help stakeholders (e.g., airlines, travel agencies) understand pricing trends, such as average fares by airline, seasonal fare variations, and popular routes.

### Project Components

- **MySQL**: Stores raw flight price data in a `staging` database.
- **PostgreSQL**: Stores processed KPIs (e.g., `kpi_fare_by_airline`) and Airflow metadata in the `airflow` database.
- **Apache Airflow**: Manages the ETL pipeline, scheduling tasks to extract data from MySQL, transform it into KPIs, and load it into PostgreSQL.
- **Grafana**: Visualizes KPIs in an interactive dashboard for stakeholders.

### Project Workflow

1. **Data Extraction**: Raw flight data is extracted from the MySQL `staging` database.
2. **Data Transformation**: Airflow processes the data to compute KPIs (e.g., average fare by airline, seasonal trends).
3. **Data Loading**: Processed KPIs are loaded into PostgreSQL tables (e.g., `kpi_fare_by_airline`).
4. **Visualization**: Grafana connects to PostgreSQL to display KPIs in a dashboard.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- MySQL Workbench (optional, for inspecting MySQL data).
- A web browser (e.g., Chrome) to access Airflow and Grafana UIs.

## Setup Instructions

### 1. Clone the Repository
Clone the project repository to your local machine:
```bash
git clone <repository-url>
cd Flight_price_analysis
```

### 2. Configure Environment Variables
Create a `.env` file in the project directory with the following content:
```
# MySQL Credentials
MYSQL_PASSWORD=root
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=staging

# PostgreSQL Credentials
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DATABASE=airflow

# Airflow Settings
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow

# Grafana Credentials
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

### 3. Start Docker Containers
Run the following command to start all services (MySQL, PostgreSQL, Airflow, Grafana):
```bash
docker-compose up -d
```
- Wait for all services to be healthy (check `docker ps`).

### 4. Access Airflow UI
- Open `http://localhost:8080` in your browser.
- Log in with username `admin` and password `admin`.
- Verify the `flight_price_pipeline` DAG is visible.

**Attach Image**: Screenshot of Airflow UI showing the `flight_price_pipeline` DAG in the Grid view. 
 
![alt text](images/AirflowUI1.png)

### 5. Inspect MySQL Data
- Use MySQL Workbench to connect to the MySQL database:
  - **Host**: `localhost`
  - **Port**: `3308`
  - **Username**: `root`
  - **Password**: `root`
  - **Database**: `staging`
- Run a query to verify raw flight data:
  ```sql
  SELECT * FROM flight_prices LIMIT 10;
  ```

**Attach Image**: Screenshot of MySQL Workbench showing the `flight_prices` table with sample data.
 
![alt text](images/Workbench.png)

### 6. Inspect PostgreSQL Data
- Connect to the PostgreSQL database using a tool like `psql`:
  ```bash
  docker exec -it flight_price_analysis_postgres_1 psql -U airflow -d airflow
  ```
- Verify KPI tables:
  ```sql
  SELECT * FROM kpi_fare_by_airline LIMIT 10;
  ```

**Attach Image**: Screenshot of `psql` output or a GUI tool showing the `kpi_fare_by_airline` table.

![alt text](images/Postgres.png)

### 7. Set Up Grafana Dashboard
- Open `http://localhost:3000` and log in with `admin`/`admin`.
- Add a PostgreSQL data source:
  - **Name**: `FlightPriceAnalytics`
  - **Host**: `postgres:5432`
  - **Database**: `airflow`
  - **User**: `airflow`
  - **Password**: `airflow`
  - **SSL Mode**: `disable`
- Create a dashboard:
  - Add a panel for “Average Fare by Airline”:
    ```sql
    SELECT Airline, Average_Fare AS "Average Fare (BDT)"
    FROM kpi_fare_by_airline
    ORDER BY Average_Fare DESC
    ```
    - Visualization: Bar Chart
    - Unit: Currency > Bangladeshi Taka (৳)

**Attach Image**: Screenshot of Grafana dashboard showing the “Average Fare by Airline” panel.

![alt text](images/Dashboard.png)

## Project Structure

- `dags/`: Contains Airflow DAG definitions (e.g., `flight_price_pipeline.py`).
- `scripts/`: Contains helper scripts for data processing.
- `data/`: Stores raw and processed data (if any).
- `logs/`: Airflow logs.
- `init-db.sh`: Initializes the PostgreSQL database.
- `docker-compose.yml`: Defines Docker services.
- `.env`: Environment variables.

## Usage

1. Trigger the `flight_price_pipeline` DAG in Airflow to process flight data.
2. Monitor the DAG run in the Airflow UI.
3. Check PostgreSQL for updated KPI tables.
4. View the results in the Grafana dashboard.

## Troubleshooting

- **Airflow UI not loading**: Check logs (`docker logs flight_price_analysis_airflow-webserver_1`) and ensure PostgreSQL is healthy.
- **Grafana data source error**: Verify PostgreSQL credentials and network connectivity.
- **DAG failures**: Check task logs in Airflow UI for errors.


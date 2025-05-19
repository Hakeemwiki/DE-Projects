# User Testing Guide for Flight Price Analysis Project

## Introduction

This guide is for users testing the **Flight Price Analysis** project. The system extracts flight price data, processes it into KPIs (e.g., average fares by airline), and visualizes the results in a Grafana dashboard. Your role as a tester is to verify the functionality of the pipeline, ensure the dashboard displays accurate data, and provide feedback on usability.

### Objectives

- Verify that the Airflow pipeline runs successfully.
- Confirm that KPIs are correctly calculated and stored.
- Ensure the Grafana dashboard displays meaningful visualizations.
- Identify any usability issues or bugs.

## Prerequisites

- Access to a running instance of the project (see `README.md` for setup).
- A web browser (e.g., Chrome).
- Basic knowledge of SQL (optional, for data verification).

## Test Scenarios

### 1. Test Airflow Pipeline Execution
**Objective**: Ensure the `flight_price_pipeline` DAG runs successfully and processes data.

1. **Access Airflow UI**:
   - Open `http://localhost:8080` in your browser.
   - Log in with `admin`/`admin`.
   - Navigate to the **DAGs** page and find `flight_price_pipeline`.

2. **Trigger the DAG**:
   - Click the play button to trigger a manual run.
   - Monitor the run in the **Grid** view.

3. **Verify Success**:
   - Ensure all tasks (e.g., `extract_from_mysql`, `transform_data`, `load_to_postgres`) complete with a green status.
   - Check the logs of the `load_to_postgres` task for any errors.

**Expected Result**: All tasks complete successfully, and the DAG run is marked as “success.”  
**Feedback**: Did the DAG run as expected? Were there any errors or delays?  
**Attach Image**: Screenshot of the Airflow Grid view showing a successful DAG run.  

![alt text](../images/AirflowGraph.png)

---

### 2. Verify MySQL Data
**Objective**: Confirm that raw flight data is available in MySQL.

1. **Connect to MySQL**:
   - Use MySQL Workbench or a similar tool.
   - Connect to:
     - Host: `localhost`
     - Port: `3308`
     - Username: `root`
     - Password: `root`
     - Database: `staging`

2. **Query Data**:
   - Run:
     ```sql
     SELECT * FROM flight_prices LIMIT 10;
     ```
   - Note the number of rows and sample data (e.g., airline, price, date).

**Expected Result**: The `flight_prices` table contains raw flight data with columns like `airline`, `price`, and `date`.  
**Feedback**: Was the data accessible? Did the table structure match expectations?  
**Attach Image**: Screenshot of MySQL query results.

![alt text](../images/Workbench.png)
---

### 3. Verify PostgreSQL Data
**Objective**: Confirm that processed KPIs are correctly stored in PostgreSQL.

1. **Connect to PostgreSQL**:
   - Run:
     ```bash
     docker exec -it flight_price_analysis_postgres_1 psql -U airflow -d airflow
     ```

2. **Query KPI Data**:
   - Run:
     ```sql
     SELECT * FROM kpi_fare_by_airline LIMIT 10;
     ```
   - Check columns like `Airline` and `Average_Fare`.

**Expected Result**: The `kpi_fare_by_airline` table contains computed KPIs with reasonable values (e.g., average fares in a realistic range).  
**Feedback**: Were the KPI values accurate? Did the table contain the expected data?  
**Attach Image**: Screenshot of PostgreSQL query results. 

![alt text](../images/Postgres.png)

---

### 4. Test Grafana Dashboard
**Objective**: Ensure the Grafana dashboard displays KPIs correctly.

1. **Access Grafana**:
   - Open `http://localhost:3000` and log in with `admin`/`admin`.

2. **Open Dashboard**:
   - Navigate to the “Flight Price Analytics” dashboard.
   - View the “Average Fare by Airline” panel.

3. **Verify Visualization**:
   - Check that the bar chart shows airlines on the x-axis and average fares on the y-axis.
   - Hover over bars to see exact values.
   - Verify the unit is Bangladeshi Taka (৳).

**Expected Result**: The dashboard displays a bar chart with correct airline names and average fares, matching the PostgreSQL data.  
**Feedback**: Was the visualization clear and accurate? Were there any display issues?  
**Attach Image**: Screenshot of the Grafana dashboard.  

![alt text](../images/Dashboard.png)

---

### 5. Usability and Feedback
**Objective**: Provide feedback on the overall user experience.

1. **Ease of Use**:
   - Was the Airflow UI intuitive for triggering and monitoring DAGs?
   - Was the Grafana dashboard easy to navigate?

2. **Performance**:
   - Did the DAG run complete in a reasonable time?
   - Did the dashboard load quickly?

3. **Suggestions**:
   - Are there additional KPIs or visualizations you’d like to see?
   - Any other improvements?

**Feedback**: Write your thoughts on usability, performance, and suggestions for improvement.

## Reporting Issues

If you encounter any issues (e.g., DAG failures, missing data, dashboard errors):
1. Note the error message and context (e.g., which step failed).
2. Take a screenshot of the error.
3. Share the logs:
   - Airflow: `docker logs flight_price_analysis_airflow-webserver_1`
   - PostgreSQL: `docker logs flight_price_analysis_postgres_1`
   - Grafana: `docker logs grafana`

## Conclusion

Thank you for testing the Flight Price Analysis project! Your feedback will help improve the system for future users.
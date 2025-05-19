# flight_price_pipeline.py
# This script defines an Apache Airflow DAG to orchestrate a data pipeline for processing flight price data from Bangladesh.
# The pipeline includes ingestion, validation, transformation, and loading stages, with tasks executed sequentially.

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add the scripts directory to the Python path to allow importing custom modules
sys.path.append('/opt/airflow')

# Import custom Python functions from the scripts directory for each pipeline stage
from scripts.ingestion import ingest_csv_to_mysql
from scripts.validation import validate_data
from scripts.transformation import transform_and_compute_kpis
from scripts.loading import load_to_postgres

# Define default arguments for the DAG to configure its behavior
default_args = {
    'owner': 'airflow',  # Specifies the owner of the DAG for Airflow UI
    'depends_on_past': False,  # Tasks do not depend on previous runs
    'email_on_failure': False,  # Disable email notifications on failure
    'email_on_retry': False,  # Disable email notifications on retry
    'retries': 2,  # Number of retries for failed tasks
    'retry_delay': timedelta(minutes=1),  # Delay between retries
    'start_date': datetime(2025, 5, 17)  # Earliest date the DAG can run
}

# Initialize the DAG with its configuration
with DAG(
    'flight_price_pipeline',  # Unique identifier for the DAG
    default_args=default_args,  # Apply the default arguments defined above
    description='Flight Price Analysis Pipeline for Bangladesh',  # Description shown in Airflow UI
    schedule_interval=None,  # Manual trigger (no automatic scheduling)
    start_date=datetime(year=2025, month=5, day=17),  # DAG start date
    catchup=False,  # Prevent backfilling for past dates
) as dag:
    
    # Task 1: Ingest CSV data into MySQL staging database
    ingest_task = PythonOperator(
        task_id='ingest_csv_to_mysql',  # Unique ID for the task
        python_callable=ingest_csv_to_mysql,  # Function to execute
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',  # Airflow connection ID for MySQL
            'csv_path': '/opt/airflow/data/input/Flight_Price_Dataset_of_Bangladesh.csv',  # Path to input CSV
            'table_name': 'flight_prices_raw'  # Target MySQL table
        }, 
        doc_md="Ingests 50,000-row CSV into MySQL with column validation"  # Task documentation
    )

    # Task 2: Validate the ingested data in MySQL
    validate_task = PythonOperator(
        task_id='validate_data',  # Unique ID for the task
        python_callable=validate_data,  # Function to execute
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',  # Airflow connection ID for MySQL
            'table_name': 'flight_prices_raw'  # Table to validate
        },
        doc_md="Validates data for nulls, types, and inconsistencies"  # Task documentation
    )

    # Task 3: Transform data and compute KPIs
    transform_task = PythonOperator(
        task_id='transform_and_compute_kpis',  # Unique ID for the task
        python_callable=transform_and_compute_kpis,  # Function to execute
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',  # Airflow connection ID for MySQL
            'table_name': 'flight_prices_raw'  # Table to transform
        }, 
        provide_context=True,  # Pass Airflow context (e.g., for XCom)
        doc_md="Calculates Total Fare and computes KPIs using Seasonality"  # Task documentation
    )

    # Task 4: Load transformed data and KPIs to PostgreSQL
    load_task = PythonOperator(
        task_id='load_to_postgres',  # Unique ID for the task
        python_callable=load_to_postgres,  # Function to execute
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',  # Airflow connection ID for MySQL
            'postgres_conn_id': 'postgres_analytics',  # Airflow connection ID for PostgreSQL
            'mysql_table': 'flight_prices_raw_transformed',  # Source MySQL table
        },
        provide_context=True,  # Pass Airflow context (e.g., for XCom)
        doc_md="Loads transformed data and KPIs to PostgreSQL"  # Task documentation
    )

    # Define task dependencies to enforce execution order
    ingest_task >> validate_task >> transform_task >> load_task
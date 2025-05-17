
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.ingestion import ingest_csv_to_mysql
from scripts.validation import validate_data
from scripts.transformation import transform_and_compute_kpis   
from scripts.loading import load_to_postgres

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# Define the DAG
with DAG(
    'flight_price_pipeline',
    default_args=default_args,
    description='Flight Price Analysis Pipeline for Bangladesh',
    schedule_interval=None,  # Set to None for manual trigger
    start_date=datetime(year=2025, month=5, day=17),
    catchup=False, # Do not backfill 
) as dag:
    
    # Task 1: Ingest CSV to MySQL
    ingest_task = PythonOperator(
        task_id='ingest_csv_to_mysql',
        python_callable = ingest_csv_to_mysql,
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',
            'csv_path': '/opt/airflow/data/input/Flight_Price_Dataset_of_Bangladesh.csv',
            'table_name': 'flight_prices_raw'
        }, 
        doc_md = "Ingests 50000-rows CSV into MySQL with column validation"
    )

    # Task 2: Validate Data
    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',
            'table_name': 'flight_prices_raw'
        },
        doc_md = "Validates data for nulls, types and inconsistencies"
    )
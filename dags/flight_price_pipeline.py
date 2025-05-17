
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
    
) as dag
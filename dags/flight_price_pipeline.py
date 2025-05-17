
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

    # Task 3: Transform and Compute KPIs
    transform_task = PythonOperator(
        task_id='transform_and_compute_kpis',
        python_callable=transform_and_compute_kpis,
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',
            'table_name': 'flight_prices_raw'
        }, 
        provide_context=True, # Pass context to the function
        doc_md = "Calculates Total Fare and computes KPIs using Seasonality."
    )

    # Task 4: Load to PostgreSQL
    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres,
        op_kwargs={
            'mysql_conn_id': 'mysql_staging',
            'postgres_conn_id': 'postgres_analytics',
            'mysql_table': 'flight_prices_raw_transformed',
            'kpis': '{{ task_instance.xcom_pull(task_ids="transform_and_compute_kpis") }}' # Pull KPIs from the previous task
        },
        doc_md = "Loads transformed data and KPIs to PostgreSQL"
    )

    # Set task dependencies
    ingest_task >> validate_task >> transform_task >> load_task

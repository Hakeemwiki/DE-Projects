
import pandas as pd
from sqlalchemy import create_engine
import logging
import os
from dotenv import load_dotenv

# Load dotenv variable
load_dotenv()

# Configure logging with time format and handlers
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/opt/airflow/logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def load_to_postgres(mysql_conn_id, csv_path, table_name):
    """
    Load transformed data and KPIs to PostgreSQL.

    Args:
        mysql_conn_id (str): Airflow connection ID for MySQL (future use)
        postgres_conn_id (str): Airflow connection ID for PostgreSQL (future use)
        mysql_table (str): MySQL table with transformed data
        kpis (dict): Dictionary of KPI DataFrames

    Raises:
        Exception: For database connection or insertion errors
    """
    logger = logging.getLogger("loading")
    logger.info(f"Starting data loading from MYSQL table {table_name} to PostgreSQL")

    # Construct database connection strings
    mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    
    postgres_conn_string = (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}")
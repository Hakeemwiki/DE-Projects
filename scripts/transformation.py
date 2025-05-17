
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

def transform_and_compute_kpis(mysql_conn_id, table_name):
    """
    Transform data and compute KPIs from MySQL staging table.

    Args:
        mysql_conn_id (str): Airflow connection ID for MySQL (future use)
        table_name (str): MySQL table name to process

    Returns:
        dict: Dictionary of KPI DataFrames

    Raises:
        Exception: For database connection or processing errors
    """
    
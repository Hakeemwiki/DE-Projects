import pandas as pd
from sqlalchemy import create_engine
import logging
import os
from dotenv import load_dotenv

#load dotenv variable
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

def validate_data(mysql_conn_id, table_name):
    """
    Validate data in the MySQL staging table.

    Args:
        mysql_conn_id (str): Airflow connection ID for MySQL (future use)
        table_name (str): MySQL table name to validate

    Returns:
        bool: True if validation passes, raises exception otherwise

    Raises:
        ValueError: If validation checks fail
        Exception: For database connection or query errors
    """
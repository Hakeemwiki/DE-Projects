
#Importing Libraries

import pandas as pd
from sqlalchemy import create_engine
import logging
import os
from dotenv import load_dotenv

#Load dotenv variable
load_dotenv()

# Configure logging with time format and handlers
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", 
                    handlers=[logging.FileHandler("/opt/airflow/logs/pipeline.log"),
                    logging.StreamHandler()])

def ingest_csv_to_mysql(mysql_conn_id, csv_path, table_name):
    """
    Load CSV data into a MySQL staging table.

    Args:
        mysql_conn_id (str): Airflow connection ID for MySQL (future use)
        csv_path (str): Path to the input CSV file
        table_name (str): MySQL table name for staging data

    Raises:
        FileNotFoundError: If CSV file is missing
        ValueError: If required columns are missing
        Exception: For database connection or insertion errors
        """

    logger = logging.getLogger("ingestion")
    logger.info(f"Starting ingestion process{csv_path} to mysql table {table_name}")

    # Read csv file
    try:
        df = pd.read_csv(csv_path)
        logger.info(f"Read {len(df)} rows from csv")
    except FileNotFoundError as e:
        logger.error(f'CSV file not found: {csv_path}')
        raise
    except Exception as e:
        logger.error(f'Failed to read CSV file')
        raise

    # Validate reqiured Columns
    required_columns = ['Airline', 'Source', 'Destination', 'Base Fare', 'Tax & Surcharge', 'Total Fare']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logger.error(f'Missing required columns: {missing_columns}')
        raise ValueError(f'Missing required columns: {missing_columns}')

    # Construct mysql connection string from .env file
    mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")


    







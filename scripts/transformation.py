
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
    logger = logging.getLogger("transformation")
    logger.info(f"Starting transformation and KPI computation for table {table_name}")

    # Construct mysql connection string from .env file
    mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    
    # Read data from MySQL table
    try:
        engine = create_engine(mysql_conn_string)
        df = pd.read_sql_table(f"Select * from {table_name}", con=engine)
        logger.info(f"Read {len(df)} rows from {table_name} table")
    except Exception as e:
        logger.error(f'Failed to read data from MySQL {e}')
        raise

    # Transformation: Calculate Total Fare if missing
    if df['Total Fare (BDT)'].isnull().any():
        df['Total Fare (BDT)'] = df['base_fare'] + df['tax_and_surcharge']
        logger.info("Calculated missing Total Fare (BDT) values")

    # Clean negative fares
    negative_fares = df['Total Fare (BDT)'] < 0
    if negative_fares.any():
        df.loc[negative_fares, 'Total Fare (BDT)'] = 0
        logger.warning(f'Set {negative_fares.sum()} negative Total Fare values to 0')
    
    # KPI 1: Average Total Fare by Airline
    average_total_fare = df.groupby('Airline')['Total Fare (BDT)'].mean().reset_index()
    average_total_fare.columns = ['Airline', 'Average Fare']
    logger.info("Computed average total fare by airline")

    # KPI 2: Seasonal fare variations

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

def load_to_postgres(mysql_conn_id, postgres_conn_id, mysql_table, kpis):
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
    
    #connect to databases
    try:
        mysql_engine = create_engine(mysql_conn_string)
        postgres_engine = create_engine(postgres_conn_string)
    except Exception as e:
        logger.error(f'Failed to connect to databases: {e}')
        raise

    # Load transformed data from MySQL to PostgreSQL
    try:
        df = pd.read_sql_table(f"Select * from {mysql_table}", con=mysql_engine)
        df.to_sql(mysql_table, con=postgres_engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(df)} rows from MySQL {mysql_table} to PostgreSQL")
    except Exception as e:
        logger.error(f'Failed to load data from MySQL to PostgreSQL: {e}')
        raise

    # Load KPIs to PostgreSQL
    kpi_tables = {
        'avg_fare_by_airline': 'kpi_fare_by_airline',
        'peak_vs_off_peak': 'kpi_peak_vs_off_peak',
        'seasonal_fares': 'kpi_seasonal_fares',
        'booking_count': 'kpi_booking_count',
        'popular_routes': 'kpi_popular_routes'
    }

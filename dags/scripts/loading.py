
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
    logger.info(f"Starting data loading from MYSQL table {mysql_table} to PostgreSQL")

    # Construct database connection strings
    # mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    #     f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    mysql_conn_string = (f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
                    f"@mysql:3306/{os.getenv('MYSQL_DATABASE')}")
    
    # postgres_conn_string = (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    #     f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}")
    postgres_conn_string = (f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                       f"@postgres:5432/{os.getenv('POSTGRES_DATABASE')}")
    
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

    for kpi_name, table_name in kpi_tables.items():
        kpi_df = kpis.get(kpi_name)
        if kpi_df is not None:
            try:
                kpi_df.to_sql(table_name, con=postgres_engine, if_exists='replace', index=False)
                logger.info(f"Loaded {len(kpi_df)} rows from {kpi_name} to PostgreSQL {table_name}")
            except Exception as e:
                logger.error(f'Failed to load KPI {kpi_name} to PostgreSQL: {e}')
                raise
        else:
            logger.warning(f'KPI {kpi_name} is None, skipping loading to PostgreSQL')

    logger.info("Data loading to PostgreSQL completed successfully")

if __name__ == "__main__":
    # Mock KpI data for testing
    # Mock KPIs for testing
    kpis = {
        'avg_fare_by_airline': pd.DataFrame({'Airline': ['Emirates'], 'Average_Fare': [50000.0]}),
        'peak_vs_non_peak_fares': pd.DataFrame({'Peak_Season': ['Peak (Eid/Hajj/Winter)'], 'Average_Fare': [60000.0]}),
        'seasonal_fares': pd.DataFrame({'Seasonality': ['Eid'], 'Average_Fare': [60000.0]}),
        'booking_count': pd.DataFrame({'Airline': ['Emirates'], 'Booking_Count': [1000]}),
        'popular_routes': pd.DataFrame({'Source': ['DAC'], 'Destination': ['LHR'], 'Booking_Count': [500]})
    }

    load_to_postgres(
        mysql_conn_id='mysql_staging',
        postgres_conn_id='postgres_analytics',
        mysql_table='flight_prices_raw_transformed',
        kpis=kpis
    )
# ingestion.py
# This script loads CSV data into a MySQL staging table.
# It validates required columns and handles errors during file reading and database insertion.

import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file for database credentials
load_dotenv()

# Configure logging to capture ingestion events with timestamps
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    handlers=[
        logging.StreamHandler()  # Output logs to console
    ]
)

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
    # Initialize logger for this module
    logger = logging.getLogger("ingestion")
    logger.info(f"Starting ingestion process from {csv_path} to MySQL table {table_name}")

    # Read CSV file into a Pandas DataFrame
    try:
        logger.info(f"Attempting to read CSV from {csv_path}")
        df = pd.read_csv(csv_path)  # Load CSV data
        logger.info(f"Successfully read {len(df)} rows from CSV")
        logger.info(f"DataFrame columns: {list(df.columns)}")
    except FileNotFoundError as e:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise

    # Define required columns for validation
    required_columns = [
        'Airline', 'Source', 'Destination', 'Base Fare (BDT)', 'Tax & Surcharge (BDT)',
        'Total Fare (BDT)', 'Departure Date & Time', 'Class', 'Seasonality', 'Stopovers'
    ]

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Construct MySQL connection string using environment variables
    logger.info("Building MySQL connection string")
    mysql_conn_string = (f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
                        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")

    # Create a connection to the MySQL database and load data
    try:
        engine = create_engine(mysql_conn_string)  # Create SQLAlchemy engine
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))  # Simple query to verify connection
            logger.info("MySQL connection successful")
        
        # Save DataFrame to MySQL table
        logger.info(f"Saving {len(df)} rows to MySQL table '{table_name}'")
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logger.info(f"Successfully loaded {len(df)} rows into {table_name}")
        return "success"
    except Exception as e:
        logger.error(f"Failed to load data to MySQL: {e}")
        raise

if __name__ == "__main__":
    # Test the function with sample parameters
    ingest_csv_to_mysql(
        mysql_conn_id="mysql_staging",
        csv_path="data/input/Flight_Price_Dataset_of_Bangladesh.csv",
        table_name="flight_prices_raw"
    )
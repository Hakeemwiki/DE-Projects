import pandas as pd
from sqlalchemy import create_engine, text
import logging
import os
from dotenv import load_dotenv


#Load dotenv variable
load_dotenv()

# Configure logging with time format and handlers
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", 
                    handlers=[ #logging.FileHandler("/opt/airflow/logs/pipeline.log"),
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
    logger.info(f"Starting ingestion process from {csv_path} to mysql table {table_name}")

    # Read csv file
    try:
        logger.info(f"Attempting to read CSV from {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Successfully read {len(df)} rows from csv")
        logger.info(f"DataFrame columns: {list(df.columns)}")
    except FileNotFoundError as e:
        logger.error(f'CSV file not found: {csv_path}')
        raise
    except Exception as e:
        logger.error(f'Failed to read CSV file: {e}')
        raise

    # Validate reqiured Columns
    # required_columns = [
    #         "Airline", "Source", "Source Name", "Destination", "Destination Name",
    #         "Departure Date & Time", "Arrival Date & Time", "Duration (hrs)", "Stopovers",
    #         "Aircraft Type", "Class", "Booking Source", "Base Fare (BDT)",
    #         "Tax & Surcharge (BDT)", "Total Fare (BDT)", "Seasonality", "Days Before Departure"
    #     ]
    required_columns = [
        'Airline', 'Source', 'Destination', 'Base Fare (BDT)', 'Tax & Surcharge (BDT)',
        'Total Fare (BDT)', 'Departure Date & Time', 'Class', 'Seasonality', 'Stopovers'
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logger.error(f'Missing required columns: {missing_columns}')
        raise ValueError(f'Missing required columns: {missing_columns}')

    # Construct mysql connection string from .env file
    logger.info("Building MySQL connection string")
    mysql_conn_string = (f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    
    logger.info(f"Connecting to MySQL database at {os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}")
    
    # Create a connection to the MySQL database and load data
    try:
        engine = create_engine(mysql_conn_string)
        # Test connection first
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("MySQL connection successful")
        
        # Now save the data
        logger.info(f"Saving {len(df)} rows to MySQL table '{table_name}'")
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logger.info(f"Successfully loaded {len(df)} rows into {table_name}")
        return "success"
    except Exception as e:
        logger.error(f'Failed to load data to MySQL: {e}')
        raise


if __name__ == "__main__":
    ingest_csv_to_mysql(
        mysql_conn_id="mysql_staging",
        # csv_path="/opt/airflow/data/input/Flight_Price_Dataset_of_Bangladesh.csv",
        csv_path="data/input/Flight_Price_Dataset_of_Bangladesh.csv",
        table_name="flight_prices_raw"
    )
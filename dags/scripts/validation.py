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
    logger = logging.getLogger("validation")
    logger.info(f"Start validation for table {table_name}")

    # Construct mysql connection string from .env file
    # mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    #     f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    mysql_conn_string = (f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
                    f"@mysql:3306/{os.getenv('MYSQL_DATABASE')}")
    
    # Read data from MySQL table
    try:
        engine = create_engine(mysql_conn_string)
        df = pd.read_sql(f"Select * from {table_name}", con=engine)
        logger.info(f"Read {len(df)} rows from {table_name} table")
    except Exception as e:
        logger.error(f'Failed to read data from MySQL {e}')
        raise

    # Define validation checks
    required_columns = [
        'Airline', 'Source', 'Destination', 'Base Fare (BDT)', 'Tax & Surcharge (BDT)',
        'Total Fare (BDT)', 'Departure Date & Time', 'Class', 'Seasonality', 'Stopovers'
    ]
    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f'Missing required columns: {missing_columns}')
        raise ValueError(f'Missing required columns: {missing_columns}')
    
    # Check for null values
    null_counts = df[required_columns].isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            logger.warning(f"Found {count} null values in column {col}")

    
    # Validate data types
    expected_types = {
        'Airline': str,
        'Source': str,
        'Destination': str,
        'Base Fare (BDT)': float,
        'Tax & Surcharge (BDT)': float,
        'Total Fare (BDT)': float,
        'Departure Date & Time': str,  # Will convert to datetime later
        'Class': str,
        'Seasonality': str,
        'Stopovers': str
    }

    for col, expected_type in expected_types.items():
        actual_type = df[col].dtype
        if not pd.api.types.is_numeric_dtype(actual_type) and expected_type in (float, int):
            logger.error(f'Invalid data type for column {col}: expected {expected_type}, got {actual_type}')
            raise ValueError(f'Invalid data type for column {col}')
        if not pd.api.types.is_string_dtype(actual_type) and expected_type == str:
            logger.error(f'Invalid data type for column {col}: expected {expected_type}, got {actual_type}')
            raise ValueError(f'Invalid data type for column {col}')
        
    # Check for inconsistencies
    negative_fares = df[df['Base Fare (BDT)'] < 0]
    if not negative_fares.empty:
        logger.warning(f"Found {len(negative_fares)} rows with negative Base Fare")
    
    invalid_cities = df[~df['Source'].str.match(r'^[A-Z]{3}$') | ~df['Destination'].str.match(r'^[A-Z]{3}$')]
    if not invalid_cities.empty:
        logger.warning(f"Found {len(invalid_cities)} rows with invalid city names")

    # Invalid seasonality values
    valid_seasons = ['Regular', 'Eid', 'Hajj', 'Winter'] #According to the data
    invalid_season = df[~df['Seasonality'].isin(valid_seasons)]
    if not invalid_season.empty:
        logger.warning(f"Found {len(invalid_season)} rows with invalid seasonality values")

    
    # Check for duplicate rows
    duplicates = df[df.duplicated()]
    if not duplicates.empty:
        logger.warning(f"Found {len(duplicates)} duplicate rows")

    # Flag invalid records
    invalid_records = df[
        df['Base Fare (BDT)'].lt(0) |
        ~df['Source'].str.match(r'^[A-Z]{3}$') |
        ~df['Destination'].str.match(r'^[A-Z]{3}$') |
        ~df['Seasonality'].isin(valid_seasons)]

    if not invalid_records.empty:
        try:
            invalid_records.to_sql(f"{table_name}_invalid_records", con=engine, if_exists='replace', index=False)
            logger.info(f"Flagged {len(invalid_records)} invalid records in {table_name}_invalid_records")
        except Exception as e:
            logger.error(f'Failed to save invalid records to MySQL: {e}')
            raise

    logger.info(f"Validation completed successfully for table {table_name}")
    return True

if __name__ == "__main__":
    validate_data(
        mysql_conn_id="mysql_staging",
        table_name="flight_prices_raw"
    )
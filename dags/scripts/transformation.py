
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
    # mysql_conn_string = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    #     f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
    mysql_conn_string = (f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
                    f"@mysql:3306/{os.getenv('MYSQL_DATABASE')}")
    
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
    # Peak season is the time that people travel the most
    df['Is_Peak_Season'] = df['Seasonality'].apply(lambda x: 1 if x == 'Peak' else 0)
    peak_vs_off_peak = df.groupby('Is_Peak_Season')['Total Fare (BDT)'].mean().reset_index()
    peak_vs_off_peak.columns = ['Is_Peak_Season', 'Average Fare']
    peak_vs_off_peak['Is_Peak_Season'] = peak_vs_off_peak['Is_Peak_Season'].map({0: 'Off-Peak (Regular)', 1: 'Peak (Winter/Eid/Hajj)'})
    logger.info("Computed average fare for peak vs off-peak seasons")

    # Retain per season averages for analysis
    seasonal_fare = df.groupby('Seasonality')['Total Fare (BDT)'].mean().reset_index()
    seasonal_fare.columns = ['Seasonality', 'Average Fare']
    logger.info("Computed seasonal fare variation (peak vs. non-peak and per-season)")

    # KPI 3: Booking Count by Airline
    booking_count = df.groupby('Airline')['Airline'].size().reset_index(name='Booking_Count')
    logger.info("Computed booking count by airline")

    # KPI 4: Most popular routes
    routes = df.groupby(['Source', 'Destination']).size().reset_index(name='Booking_Count')
    popular_routes = routes.sort_values(by='Booking_Count', ascending=False).head(10)
    logger.info("Computed most popular routes")

    # Save transformed data and KPIs to MySQL
    try:
        df.to_sql(f'{table_name}_transformed', con=engine, if_exists='replace', index=False)
        logger.info(f"Saved transformed data to {table_name}_transformed")
    except Exception as e:
        logger.error(f'Failed to save transformed data to MySQL {e}')
        raise

    # Return KPIs
    kpis = {
        'average_total_fare': average_total_fare,
        'peak_vs_off_peak': peak_vs_off_peak,
        'seasonal_fare': seasonal_fare,
        'booking_count': booking_count,
        'popular_routes': popular_routes
    }
    logger.info("Transformation and KPI computation completed successfully")
    return kpis

if __name__ == "__main__":
    kpis = transform_and_compute_kpis(
        mysql_conn_id="mysql_staging",
        table_name="flight_price_dataset"
    )

    for kpi_name, kpi_df in kpis.items():
        print(f"{kpi_name}:\n{kpi_df}\n")


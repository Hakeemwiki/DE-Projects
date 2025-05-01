
"""
Spark streaming script to process real-time e-commerce event data from CSV files
and write it to a PostgreSQL database.
"""

# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType, DoubleType, TimestampType
import os
import logging
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# Configure logging for monitoring and debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a Spark session for processing streaming data
spark = (SparkSession.builder
         .appName('RealTimeEcommercePipeline') # Name of the Spark application
         .config('spark.driver.memory', '1g') # Allocate 1GB memory for the driver
         .config('spark.sql.streaming.checkpointLocation', '/data/checkpoints')  # Directory for checkpointing to ensure fault tolerance
         .getOrCreate())

# Define the schema for incoming CSV data to ensure correct data types
schema = (StructType()
          .add('user_id', IntegerType())
          .add('user_name', StringType())
          .add('user_email', StringType())
          .add('event_type', StringType())
          .add('product_id', IntegerType())
          .add('product_name', StringType())
          .add('product_category', StringType())
          .add('product_price', DoubleType())
          .add('event_time', TimestampType())
          )

# Read CSV files as a streaming DataFrame from the /data directory
input_df = (spark.readStream
            .schema(schema) # Apply the defined schema
            .option("header", "true") # CSV files have a header row
            .option('maxFilesPerTrigger', 1) # Process one file at a time to control load
            .csv("/data"))

# Remove duplicate events based on user_id and event_time to ensure data quality
cleaned_df = input_df.dropDuplicates(['user_id', 'event_time'])


def write_to_postgres(batch_df, batch_id):
    """
    Write a batch of streaming data to PostgreSQL.
    
    Args:
        batch_df: DataFrame containing the batch data.
        batch_id: ID of the batch.
    """
    try:
        # Write the batch to PostgreSQL using JDBC
        batch_df.write \
            .format('jdbc') \
            .option("url", f"jdbc:postgresql://postgres:5432/{os.getenv('POSTGRES_DB')}") \
            .option('dbtable', 'events') \
            .option('user', os.getenv('POSTGRES_USER')) \
            .option('password', os.getenv('POSTGRES_PASSWORD')) \
            .option('driver', "org.postgresql.Driver")\
            .option('batchsize', 1500)\
            .mode("append") \
            .save()
        logger.info(f"Batch {batch_id} written to PostgreSQL successfully")
    except Exception as e:
        logger.error(f"Error writing batch {batch_id} to PostgreSQL: {e}")
        raise

# Set up the stream to use the foreachbatch method
query = cleaned_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode('append') \
    .start()


# Keep the streaming query running until termination or error
try:
    query.awaitTermination() # Wait for the streaming job to complete
except Exception as e:
    logger.error(f"Streaming query failed: {e}")
finally:
    query.stop() # Stop the streaming query
    spark.stop() # Stop the Spark session
    logger.info("Spark streaming job terminated")

            
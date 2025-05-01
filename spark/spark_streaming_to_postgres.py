
# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType, DoubleType, TimestampType
import os
import logging
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# Configure logging for monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a spark session
spark = (SparkSession.builder
         .appName('RealTimeEcommercePipeline')
         .config('spark.driver.memory', '1g')
         .config('spark.sql.streaming.checkpointLocation', '/data/checkpoints')  # Checkpointing for fault tolerance
         .getOrCreate())

# Define the structure of the incoming data
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

# Read incoming CSV files as a data stream
input_df = (spark.readStream
            .schema(schema)
            .option("header", "true")
            .option('maxFilesPerTrigger', 1) #Process one file at a time for stability
            .csv("/data"))

# Basic data cleaning: Remove duplicates based on user_id and event_time
cleaned_df = input_df.dropDuplicates(['user_id', 'event_time'])


def write_to_postgres(batch_df, batch_id):
    """
    Write a batch of streaming data to PostgreSQL.
    
    Args:
        batch_df: DataFrame containing the batch data.
        batch_id: ID of the batch.
    """
    try:
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


# Wait for streaming to finish
try:
    query.awaitTermination()
except Exception as e:
    logger.error(f"Streaming query failed: {e}")
finally:
    query.stop()
    spark.stop()
    logger.info("Spark streaming job terminated")

            
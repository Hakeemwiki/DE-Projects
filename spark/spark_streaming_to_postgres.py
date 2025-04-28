
# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType, DoubleType, TimestampType


# Create a spark session
spark = (SparkSession.builder()
         .appName('RealTimeEcommercePipeline')
         .config('spark.driver.memory', '1g')
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
input_df = (spark.readStream()
            .schema(schema)
            .option("header", "true")
            .csv("data"))

def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format('jdbc') \
        .option("url", "jdbc:postgresql://postgres:5433/events_db") \
        .option('dbtable', 'events') \
        .option('user', "my_user") \
        .option('password', 'mypass') \
        .option('driver', "org.postgresql.driver")\
        .mode("append") \
        .save()

# Set up the stream to use the foreachbatch method
query = input_df.writeStream \
    .foreachbatch(write_to_postgres) \
    .outputmMode('append') \
    .start()

# Wait for streaming to finish
query.awaitTermination()

            

# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import StructType, IntegerType, StringType, DoubleType, TimestampType


# Create a spark session
spark = (SparkSession.builder()
         .appName('RealTimeEcommercePipeline')
         .getOrCreate())


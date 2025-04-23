import os
import json
import logging
import requests
from requests.adapters import HTTPAdapter # Used to configure custom HTTP adapters for handling retries in API requests.
from urllib3.util.retry import Retry # Provides retry logic for HTTP requests to handle transient failures (e.g., server errors).
from pyspark.sql import SparkSession, Row, DataFrame
# SparkSession: Entry point for PySpark functionality.
# Row: Represents a row of data in a DataFrame, used to structure API data.
# DataFrame: PySpark’s distributed data structure, like a table in a database.

from pyspark.sql.functions import col, array_join, expr, size, when, to_date, mean, sum as spark_sum, count as spark_count, lit, explode, split
# col: References a DataFrame column for operations (e.g., filtering, sorting).
# array_join: Joins array elements into a string (e.g., genres into "Action|Adventure").
# expr: Allows SQL-like expressions for complex transformations.
# size: Counts elements in an array column (e.g., number of cast members).
# when: Conditional logic for column transformations (e.g., replace 0 with NULL).
# to_date: Converts string dates to date type.
# mean, spark_sum, spark_count: Aggregation functions for analysis (e.g., average revenue).
# lit: Creates a column with a constant value (used in franchise_vs_standalone).
# explode, split: Handle pipe-separated strings (used in analyze_directors).

from pyspark.sql.types import *
from typing import * # Type hints for better code clarity and IDE support.
from dotenv import load_dotenv

# ------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configures logging to show INFO-level messages and above (INFO, WARNING, ERROR).

load_dotenv()

TMDB_API_KEY = os.getenv('api_key')

if not TMDB_API_KEY:
    raise ValueError("API_KEY environment variable not set")

TMDB_URL = "https://api.themoviedb.org/3/movie/{id}?api_key={api}&append_to_response=credits" 
# append_to_response=credits: Includes cast and crew data in the response.

JSON_ARRAY_FIELDS = ['genres', 'production_companies', 'production_countries', 'spoken_languages']
# Lists fields from the TMDB API response that should be arrays (lists).
# Used to ensure these fields are processed as lists, even if malformed.

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MovieDataAnalysis") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# config: Allocates 4GB of memory to the driver (controls Spark execution).

# ------------------------------------------------------------------------
# SCHEMA DEFINITION
# ------------------------------------------------------------------------

def build_schema() -> StructType:
    """
    Define the schema for the movie DataFrame based on TMDB API response structure.
    
    Returns:
        StructType: Spark schema for movie data
    """
    basic_field = [
        StructField('id', IntegerType(), False),  # Movie ID (non-nullable integer)
        StructField('title', StringType(), True),  # Movie title (string, nullable)
        StructField('tagline', StringType(), True),  # Movie tagline (string, nullable)
        StructField('release_date', StringType(), True),  # Release date (string, e.g., "2019-04-24")
        StructField('original_language', StringType(), True),  # Language code (e.g., "en")
        StructField('budget', LongType(), True),  # Budget in USD (long for large values)
        StructField('revenue', LongType(), True),  # Revenue in USD (long for large values)
        StructField('vote_count', IntegerType(), True),  # Number of votes (integer)
        StructField('vote_average', DoubleType(), True),  # Average rating (float, e.g., 7.8)
        StructField('popularity', DoubleType(), True),  # Popularity score (float)
        StructField('runtime', IntegerType(), True),  # Runtime in minutes (integer, e.g., 181)
        StructField('overview', StringType(), True),  # Movie summary (string)
        StructField('poster_path', StringType(), True)  # Path to poster image (string)

    ]

    collection_field = StructField('belongs_to_collection', MapType(StringType(), StringType()), True)
    # MapType for collection metadata (e.g., {"id": 123, "name": "Avengers Collection"}).
    
    def array_struct(name: str, fields: List[StructField]) -> StructField:
        return StructField(name, ArrayType(StructType(fields)), True)
    # Creates a StructField for an array of structs (e.g., list of genres).
    # ArrayType: Represents a list.
    # StructType: Defines the structure of each element in the list.

    array_fields = [
        array_struct('genres', [
            StructField('id', IntegerType(), True),
            StructField('name', StringType(), True)
        ]),
        array_struct('production_companies', [
            StructField('id', IntegerType(), True),
            StructField('name', StringType(), True)
        ]),
        array_struct('production_countries', [
            StructField('iso_3166_1', StringType(), True),  # Country code (e.g., "US")
            StructField('name', StringType(), True)  # Country name
        ]),
        array_struct('spoken_languages', [
            StructField('iso_639_1', StringType(), True),  # Language code (e.g., "en")
            StructField('name', StringType(), True)  # Language name
        ])
    ]

    credits_field = StructField(
        'credits', 
        StructType([
            StructField('cast', ArrayType(StructType([
                StructField('name', StringType(), True),
                StructField('character', StringType(), True)
            ])), True),
            StructField('crew', ArrayType(StructType([
                StructField('name', StringType(), True),
                StructField('job', StringType(), True)
            ])), True)
        ]),
        True
    )

    return StructType(basic_field + [collection_field] + array_fields + [credits_field])
    # Returns a StructType combining all fields for the DataFrame.


# ------------------------------------------------------------------------
# DATA FETCHING
# ------------------------------------------------------------------------

def get_session_with_retries(total_retries: int = 3, backoff: float = 0.3) -> requests.Session:
    """
    Create a requests session with retry configuration for handling transient API errors.
    
    Args:
        total_retries (int): Number of retry attempts
        backoff (float): Backoff factor for retry delays
    
    Returns:
        requests.Session: Configured session object
    """
    session = requests.Session()
    # Creates a new HTTP session for making API requests.

    retry = Retry(
        total = total_retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    # Configures retries for specific HTTP errors (e.g., 429: Too Many Requests).
    # total_retries: Try up to 3 times.
    # backoff_factor: Delay between retries (0.3s, 0.6s, 1.2s).
    # status_forcelist: Retry on these HTTP status codes.

    session.mount('htttps://', HTTPAdapter(max_retries=retry))     # Attaches the retry logic to HTTPS requests.

    return session





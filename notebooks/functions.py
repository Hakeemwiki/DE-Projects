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

def fetch_movie_data(movie_ids: List[int], schema: StructType) -> DataFrame:
    """
    Fetch movie data from TMDB API for a list of movie IDs.
    
    Args:
        movie_ids (List[int]): List of TMDB movie IDs
        schema (StructType): Spark schema for the DataFrame
    Returns:
        DataFrame: Spark DataFrame containing raw movie data
    """

    session = get_session_with_retries()
    # Creates a session with the retry logic for API calls above

    raw_records = []
    # List to store Row objects for each movie’s data.

    for movie_id in movie_ids:
        # Loops through each movie ID to fetch its data.
        try:
            response = session.get(
                TMDB_URL.format(id = movie_id, api = TMDB_API_KEY),
                timeout= 0.5
            )
            # Makes an HTTP GET request to the TMDB API.
            # Formats the URL with the movie ID and API key.
            # timeout=5: Fails if the request takes longer than 5 seconds.
            
            response.raise_for_status()
            # Raises an exception if the HTTP status code indicates an error

            payload = response.json()
            # Parses the API response (JSON) into a Python dictionary.

            if payload.get('success') is False:
                logging.warning(f"Skipping movie ID {movie_id}: API returned failure")
                continue
            # Checks if the API response indicates failure (e.g., invalid ID).
            # Logs a warning and skips to the next movie ID.

            # Clean and structure the record
            record = {
                'id': payload.get('id'),
                'title': payload.get('title'),
                'tagline': payload.get('tagline'),
                'release_date': payload.get('release_date'),
                'original_language': payload.get('original_language'),
                'budget': payload.get('budget'),
                'revenue': payload.get('revenue'),
                'vote_count': payload.get('vote_count'),
                'vote_average': payload.get('vote_average'),
                'popularity': payload.get('popularity'),
                'runtime': payload.get('runtime'),
                'overview': payload.get('overview'),
                'poster_path': payload.get('poster_path'),
                'belongs_to_collection': payload.get('belongs_to_collection')
            } 
            # Creates a dictionary with key-value pairs for each field.
            # get() safely retrieves values, returning None if the key is missing.

            # Log raw payload for debugging type issues
            logging.debug(f"Raw payload for movie ID{movie_id}: {json.dumps(record, indent=2)}")
            # Logs the raw record at DEBUG level for troubleshooting (not shown unless logging level is DEBUG).

            # Process array fields
            for field in JSON_ARRAY_FIELDS:
                arr = payload.get(field)
                if not isinstance(arr, List):
                    try:
                        arr = json.loads(arr) if arr else []
                    except Exception:
                        arr = []
                record[field] = arr
            # Ensures array fields (genres, etc.) are lists.
            # If not a list, tries to parse as JSON; if that fails, sets to empty list.
            

            #  Process credits  
            credits = payload.get('credits', {})
            record['credits'] = {
                'cast': [{'name': p['name'], 'character': p.get('character', '')}
                         for p in credits.get('cast', [])],
                 'crew': [{'name': p['name'], 'job': p.get('job', '')}
                        for p in credits.get('crew', [])]                    
            }

            # Structures credits into a dictionary with cast and crew lists.
            # Each cast/crew entry is a dictionary with name and character/job.
            # get() ensures safe access to nested fields, defaulting to empty lists.
            
            raw_records.append(Row(**record))
            # Converts the record dictionary to a Row object and adds it to raw_records.
            # **record unpacks the dictionary into keyword arguments for Row.
            
        except Exception as e:
            logging.warning(f"Failed to fetch movie ID {movie_id}: {e}")
            # Catches any errors (e.g., network issues, invalid JSON) and logs a warning.
            # Continues to the next movie ID without stopping the program.
    
    if not raw_records:
        return spark.createDataFrame([], schema)
    # If no records were fetched (e.g., all IDs failed), returns an empty DataFrame with the schema.
    
    return spark.createDataFrame(raw_records, schema)
    # Creates a Spark DataFrame from the list of Row objects, applying the provided schema.

def clean_movie_data(df: DataFrame) -> DataFrame:
    """
    Clean and transform the raw movie DataFrame, processing JSON-like columns and adding derived metrics.
    
    Args:
        df (DataFrame): Raw movie DataFrame
    
    Returns:
        DataFrame: Cleaned and transformed DataFrame
    """
    # Process collection name
    cleaned_df = df.withColumn(
        'collection_name',
        col('belongs_to_collection').getItem('name')
    )
    # Extracts the 'name' field from the belongs_to_collection map (e.g., "Avengers Collection").
    # withColumn: Adds or replaces a column in the DataFrame.
    # col: References the belongs_to_collection column.
    # getItem: Accesses a key in a MapType column.
    
    # Process array fields to pipe-separated strings
    array_transforms = {
        'genre_names': 'genres',
        'production_companies_str': 'production_companies',
        'production_countries_str': 'production_countries',
        'spoken_languages_str': 'spoken_languages'
    }
    # Dictionary mapping output column names to input array columns.
    
    for output_col, input_col in array_transforms.items():
        cleaned_df = cleaned_df.withColumn(
            output_col,
            array_join(expr(f'transform({input_col}, x -> x.name)'), '|')
        )
    # Loops through array fields to convert them to strings.
    # expr: Uses SQL-like syntax to transform each array element.
    # transform: Applies a function to each element (x -> x.name extracts the 'name' field).
    # array_join: Joins the resulting names with '|' (e.g., "Action|Adventure").
    
    # Process credits
    cleaned_df = cleaned_df \
        .withColumn(
            'cast_names',
            array_join(expr('transform(credits.cast, x -> x.name)'), '|')
        ) \
        .withColumn(
            'cast_size',
            size(col('credits.cast'))
        ) \
        .withColumn(
            'director',
            array_join(
                expr("transform(filter(credits.crew, x -> x.job = 'Director'), x -> x.name)"),
                '|'
            )
        ) \
        .withColumn(
            'crew_size',
            size(col('credits.crew'))
        )
    # Processes the credits struct:
    # - cast_names: Joins cast names with '|' (e.g., "Robert Downey Jr.|Chris Evans").
    # - cast_size: Counts the number of cast members.
    # - director: Joins names of crew members with job="Director".
    # - crew_size: Counts the number of crew members.
    # filter: Selects crew members where job is "Director".
    # \: Line continuation for readability.
    
    # Convert data types and handle zeros
    cleaned_df = cleaned_df \
        .withColumn('budget', when(col('budget') == 0, None).otherwise(col('budget'))) \
        .withColumn('revenue', when(col('revenue') == 0, None).otherwise(col('revenue'))) \
        .withColumn('runtime', when(col('runtime') == 0, None).otherwise(col('runtime'))) \
        .withColumn('release_date', to_date(col('release_date')))
    # Cleans data:
    # - Replaces 0 with NULL for budget, revenue, runtime (0 often means missing data).
    # - Converts release_date string to a date type (e.g., "2019-04-24" to date).
    # when: If condition is true, sets value; otherwise, keeps original.
    
    # Calculate financial metrics
    cleaned_df = cleaned_df \
        .withColumn('budget_millions', col('budget') / 1e6) \
        .withColumn('revenue_millions', col('revenue') / 1e6) \
        .withColumn('profit', col('revenue_millions') - col('budget_millions')) \
        .withColumn('roi', col('revenue_millions') / col('budget_millions'))
    # Adds derived columns:
    # - budget_millions: Budget in millions (divides by 1,000,000).
    # - revenue_millions: Revenue in millions.
    # - profit: Revenue minus budget (in millions).
    # - roi: Return on investment (revenue/budget).
    
    # Standardize specific fields
    cleaned_df = cleaned_df \
        .withColumn(
            'genre_names',
            when(
                col('genre_names').isin(
                    'Adventure|Science Fiction|Action',
                    'Adventure|Action|Science Fiction'
                ),
                'Action|Adventure|Science Fiction'
            ).otherwise(col('genre_names'))
        ) \
        .withColumn(
            'production_countries_str',
            when(
                col('production_countries_str') == 'United Kingdom|United States of America',
                'United States of America|United Kingdom'
            ).otherwise(col('production_countries_str'))
        )
    # Standardizes data for consistency:
    # - genre_names: Unifies similar genre combinations into one format.
    # - production_countries_str: Reorders UK|US to US|UK.
    # isin: Checks if a value is in a list.
    # otherwise: Keeps original value if condition is false.
    
    # Select final columns
    desired_columns = [
        'id', 'title', 'tagline', 'release_date', 'genre_names', 'collection_name',
        'original_language', 'budget_millions', 'revenue_millions', 'production_companies_str',
        'production_countries_str', 'vote_count', 'vote_average', 'popularity', 'runtime',
        'overview', 'spoken_languages_str', 'poster_path', 'cast_names', 'cast_size',
        'director', 'crew_size', 'profit', 'roi'
    ]
    # Lists the columns to keep in the final DataFrame.
    
    return cleaned_df.select([c for c in desired_columns if c in cleaned_df.columns])
    # Selects only the desired columns, filtering out any that don’t exist.
    # Returns the cleaned DataFrame.


# ------------------------------------------------------------------------
# ANALYSIS FUNCTIONS
# ------------------------------------------------------------------------

def kpi_ranking(df: DataFrame, metric: str, n: int = 10, top: bool = True, 
                filter_col: Optional[str] = None, filter_val: Optional[float] = None) -> DataFrame:
    """
    Rank movies by a specified metric with optional filtering.
    
    Args:
        df (DataFrame): Input DataFrame
        metric (str): Column name to rank by
        n (int): Number of results to return
        top (bool): True for top ranks, False for bottom
        filter_col (str, optional): Column to filter on
        filter_val (float, optional): Minimum value for filter
    
    Returns:
        DataFrame: Ranked results
    """
    data = df
    # Assigns the input DataFrame to a variable for processing.
    
    if filter_col and filter_val is not None:
        data = data.filter(col(filter_col) >= filter_val)
    # Applies a filter if both filter_col and filter_val are provided.
    # filter: Keeps rows where the condition is true (e.g., revenue_millions >= 100).
    
    order = col(metric).desc() if top else col(metric).asc()
    # Sets the sort order: descending for top ranks, ascending for bottom.
    # desc: Sorts in descending order (highest first).
    # asc: Sorts in ascending order (lowest first).
    
    return data.orderBy(order).limit(n)
    # Sorts the DataFrame by the metric and returns the top/bottom n rows.
    # orderBy: Sorts the DataFrame.
    # limit: Restricts the output to n rows.

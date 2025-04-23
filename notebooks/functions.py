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
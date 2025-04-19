
import os
import ast
import json
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# ------------------------------------------------------------------------
# API KEY
# ------------------------------------------------------------------------

def get_api_key():
    """
    Get TMDB API key from the environment.
    Raises an error if not set.
    """
    key = os.getenv('api_key')
    if not key:
        raise EnvironmentError("Please set the API_KEY environment variable.")
    return key


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

# ------------------------------------------------------------------------
# DATA FETCHING
# ------------------------------------------------------------------------

movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397,
420818, 24428, 168259, 99861, 284054, 12445,
181808, 330457, 351286, 109445, 321612, 260513]

def fetch_movie_data(ids):
    """
    Fetch movie details (with credits) for a list of TMDB IDs.
    Retries on common HTTP errors.
    """
    api = get_api_key()
    url = (
        "https://api.themoviedb.org/3/movie/{id}?api_key={api}&append_to_response=credits"
    )
    
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.3,
                  status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retry))

    results = []
    for mid in ids:
        try:
            r = session.get(url.format(id=mid, api=api), timeout=5)
            r.raise_for_status()
            results.append(r.json())
        except Exception as e:
            logging.warning(f"Could not fetch {mid}: {e}")

    return pd.DataFrame(results)

# ------------------------------------------------------------------------
# SAVE & LOAD
# ------------------------------------------------------------------------

def save_df(df, path):
    """Save DataFrame to CSV (no index)."""
    df.to_csv(path, index=False)
    logging.info(f"Saved to {path}")

def load_df(path):
    """Load DataFrame from CSV."""
    return pd.read_csv(path)


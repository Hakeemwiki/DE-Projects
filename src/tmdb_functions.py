
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

# ------------------------------------------------------------------------
# CLEANING
# ------------------------------------------------------------------------

def clean_df(df):
    """
    Cleans a TMDB DataFrame by processing complex columns, converting data types,
    computing financial metrics, and organizing the output.
    Handles list columns, dictionary columns, origin_country, credits, and other transformations.
    """
    # Create a copy of the input DataFrame to avoid modifying the original
    df = df.copy()

    # Drop irrelevant columns that are not needed for analysis, ignore if missing
    df.drop(columns=['adult', 'imdb_id', 'original_title', 'video', 'homepage'], errors='ignore', inplace=True)

    # Process list-like columns: genres, production_countries, production_companies, spoken_languages
    for col in ['genres', 'production_countries', 'production_companies', 'spoken_languages']:
        if col in df:
            def process_list(x):
                # Check if value is a string (possibly stringified list from API)
                if isinstance(x, str):
                    try:
                        x = ast.literal_eval(x)  # Convert string to list
                    except:
                        try:
                            x = json.loads(x)  # Fallback to JSON parsing
                        except:
                            x = []  # Use empty list if parsing fails
                # If value is a list, extract 'name' from each dict and join with '|'
                if isinstance(x, list):
                    names = [item['name'] for item in x if isinstance(item, dict) and 'name' in item]
                    return '|'.join(names)
                return x  # Return unchanged if not a list
            # Apply the list processing to the column
            df[col] = df[col].apply(process_list)

    # Process belongs_to_collection (dictionary-like column)
    if 'belongs_to_collection' in df:
        def process_dict(x):
            # Check if value is a string (possibly stringified dict)
            if isinstance(x, str):
                try:
                    x = ast.literal_eval(x)  # Convert string to dict
                except:
                    try:
                        x = json.loads(x)  # Fallback to JSON parsing
                    except:
                        x = {}  # Use empty dict if parsing fails
            # If value is a dict, extract 'name'
            if isinstance(x, dict):
                return x.get('name')
            return pd.NA  # Return NA for missing or invalid data
        # Apply the dict processing to the column
        df['belongs_to_collection'] = df['belongs_to_collection'].apply(process_dict)

    # Process origin_country (extract first element from list)
    if 'origin_country' in df:
        def process_origin(x):
            # Check if value is a string (possibly stringified list)
            if isinstance(x, str):
                try:
                    x = ast.literal_eval(x)  # Convert string to list
                except:
                    try:
                        x = json.loads(x)  # Fallback to JSON parsing
                    except:
                        x = []  # Use empty list if parsing fails
            # If value is a list and non-empty, take first element
            if isinstance(x, list) and x:
                return x[0]
            return x  # Return unchanged if not a list or empty
        # Apply the origin_country processing to the column
        df['origin_country'] = df['origin_country'].apply(process_origin)

    # Process credits column (extract cast, cast_size, director, crew_size)
    if 'credits' in df:
        def process_credits(credits):
            # Check if value is a string (possibly stringified dict)
            if isinstance(credits, str):
                try:
                    credits = ast.literal_eval(credits)  # Convert string to dict
                except:
                    try:
                        credits = json.loads(credits)  # Fallback to JSON parsing
                    except:
                        credits = {}  # Use empty dict if parsing fails
            # Ensure value is a dict
            if not isinstance(credits, dict):
                credits = {}
            # Extract cast information
            cast = credits.get('cast', [])
            cast_names = '|'.join([person['name'] for person in cast if isinstance(person, dict) and 'name' in person])
            cast_size = len(cast)
            # Extract crew information
            crew = credits.get('crew', [])
            directors = [person['name'] for person in crew if isinstance(person, dict) and person.get('job') == 'Director']
            director_names = '|'.join(directors)
            crew_size = len(crew)
            # Return extracted data as a Series
            return pd.Series([cast_names, cast_size, director_names, crew_size], index=['cast', 'cast_size', 'director', 'crew_size'])
        # Apply credits processing and create new columns
        df[['cast', 'cast_size', 'director', 'crew_size']] = df['credits'].apply(process_credits)
        # Drop original credits column
        df.drop(columns=['credits'], inplace=True)

    # Convert specified columns to numeric types, invalid values become NaN
    for col in ['budget', 'revenue', 'id', 'popularity']:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert release_date to datetime, invalid dates become NaT
    if 'release_date' in df:
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Replace zeros with NaN in budget, revenue, and runtime (zeros likely indicate missing data)
    for col in ['budget', 'revenue', 'runtime']:
        if col in df:
            df[col] = df[col].replace(0, pd.NA)

    # Create budget_millions by scaling budget to millions
    df['budget_millions'] = df['budget'] / 1e6
    # Create revenue_millions by scaling revenue to millions
    df['revenue_millions'] = df['revenue'] / 1e6
    # Calculate profit as revenue minus budget in millions
    df['profit'] = df['revenue_millions'] - df['budget_millions']
    # Calculate ROI as revenue divided by budget in millions
    df['roi'] = df['revenue_millions'] / df['budget_millions']

    # Noticed that the genres and production countries Columns had some values 
# that can be one but due to positioning its seen a different value eg. US|UK and UK|US. 

    df['genres'] = df['genres'].replace('Adventure|Science Fiction|Action', 'Action|Adventure|Science Fiction')
    df['genres'] = df['genres'].replace('Adventure|Action|Science Fiction', 'Action|Adventure|Science Fiction')

    df['production_countries'] = df['production_countries'].replace('United Kingdom|United States of America', 'United States of America|United Kingdom')   

    # Define desired order of columns for consistent output
    cols = ['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
            'original_language', 'budget_millions', 'revenue_millions',
            'production_companies', 'production_countries', 'vote_count', 'vote_average',
            'popularity', 'runtime', 'overview', 'spoken_languages', 'poster_path',
            'cast', 'cast_size', 'director', 'crew_size']
    # Reorder columns, only including those present in the DataFrame
    df = df.reindex(columns=[c for c in cols if c in df])

    # These 2 extra columns are for the KPI functions
    #Calculating profit
    df['profit'] = df['revenue_millions'] - df['budget_millions'] 

    #Calculating Return On Investment
    df['roi'] = df['revenue_millions']/df['budget_millions']
    
    # Reset index to be sequential and drop old index
    return df.reset_index(drop=True)

# Example usage:
# data = pd.DataFrame(...)  # Your TMDB data here
# cleaned_data = clean_df(data)


# ------------------------------------------------------------------------
# KPI RANKING FUNCTION
# ------------------------------------------------------------------------

def kpi_ranking(df, metric, n=10, top=True, filter_col=None, filter_val=None):
    """
    Rank movies by any metric with optional filtering.
      - df: DataFrame of movie data
      - metric: column name to sort by
      - n: number of movies to return
      - top: True => highest, False => lowest
      - filter_col, filter_val: if provided, only include rows where df[filter_col]>=filter_val
    """

    data = df.copy()
    
    
    if filter_col and filter_val is not None:
        data = data[data[filter_col] >= filter_val]
    return data.nlargest(n, metric) if top else data.nsmallest(n, metric)


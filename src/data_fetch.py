import requests
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()  #load variable from .env

API_KEY = os.getenv('api_key')
url = "https://api.themoviedb.org/3/movie/{}?api_key={}" #Placeholders for the movie id and api key


movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397,
420818, 24428, 168259, 99861, 284054, 12445,
181808, 330457, 351286, 109445, 321612, 260513]

movie_data = []

for movie_id in movie_ids:
    response = requests.get(url.format(movie_id, API_KEY))
    if response.status_code == 200:
        movie_data.append(response.json())
    else:
        print(f"Failed to fetch data for ID: {movie_id}: {response.status_code}, {response.json()}")

data = pd.DataFrame(movie_data)
data.to_csv("data/raw/raw_movie_data.csv", index=False) 

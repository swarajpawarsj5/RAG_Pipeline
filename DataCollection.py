from dotenv import load_dotenv
import requests
import time
import os
import json
from pathlib import Path

# load the .env file environment variables
load_dotenv()

# check if the TMDB key is available
API_KEY = os.environ['TMDB_API_KEY']
if API_KEY is None:
    raise Exception("TMDB api key is missing")

# define the constants
BASE_URL = "https://api.themoviedb.org/3"
DATA_DIR = "./tmdb/"
SLEEP_TIME = 0.25
PAGE_COUNT = 1

# define a client class which will download the movie data from TMDB
class TMDBClient:
    def __init__(self, api_key):
        # use this api key to send the request to TMDB REST APIs
        self._api_key = api_key

    def get(self, endpoint, **params):
        # define the set of parameters which are required to send to the API
        params["api_key"] = self._api_key

        # build the final url
        url = BASE_URL + endpoint

        # send the request to the server
        response = requests.get(url, params=params)

        # wait till response is available
        response.raise_for_status()

        # wait for few seconds
        time.sleep(SLEEP_TIME)

        # return the response in json format
        return response.json()

    def get_popular_movies(self, page):
        return self.get("/movie/popular", page=page)

    def get_movie_details(self, movie_id):
        return self.get(f'/movie/{movie_id}')

    def get_movie_recommendation(self, movie_id):
        return self.get(f'/movie/{movie_id}/recommendations')

    def get_movie_keywords(self, movie_id):
            return self.get(f'/movie/{movie_id}/keywords')

    def get_movie_credits(self, movie_id):
            return self.get(f'/movie/{movie_id}/credits')

# create the client instance
client = TMDBClient(api_key=API_KEY)

for page in range(1, PAGE_COUNT + 1):

    print(f"-- downloading movies on page {page}")

    # download the popular movies
    movies = client.get_popular_movies(page=page)
    
    # process each movie
    for movie in movies['results']:
        # get the movie id 
        movie_id = movie['id']

        # check if the movie details are already dumped
        file_name = f"./tmdb/{movie_id}.json"
        path = Path(file_name)
        if path.exists():
            print(f"movie {movie_id} already exists")
            
            # since the movie is already saved, there is no need to download the data again
            continue

        # get the movie details
        movie_details = client.get_movie_details(movie_id)

        # get the movie credits
        movie_credits = client.get_movie_credits(movie_id)
        
        # get the movie recommendations
        movie_recommendations = client.get_movie_recommendation(movie_id)

        # get the movie keywords
        movie_keywords = client.get_movie_keywords(movie_id)

        # create a movie document
        document = {
             "id": movie_id,
             "details": movie_details,
             "cast": movie_credits.get('cast',[]),
             "crew": movie_credits.get('crew', []),
             "keywords": movie_keywords.get('keywords', []),
             "recommendations": movie_recommendations.get("results", [])
        }

        # save the movie details in a file document
        with open(file_name, "w") as file:
            json.dump(document, file, indent=4)

        print(f"saved movie {movie_id}")

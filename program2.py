from dotenv import load_dotenv
import requests
import time
import os

# load the .env file enviornment variables
load_dotenv()

# Check if TMDB api key is available or not
API_KEY = os.environ['TMDB_API_KEY']
if API_KEY is None:
    raise Exception("TMDB api key is missing")

# define the constants
BASE_URL = "https://api.themoviedb.org/3"
DATA_DIR = "./tmdb/"
SLEEP_TIME = 5 # seconds
PAGE_COUNT = 2

# define a Client class which will download the movie data from TMDB
class TMDBClient:
    def __init__(self, api_key):
        # use this api key to send the request to TMDB ReST APIs
        self._api_key = api_key
        
    def get(self, endpoint, **params):
        # define the set of parameters which are required to send to api
        params["api_key"] = self._api_key
        
        
        # build the final url
        url = BASE_URL + endpoint
        
        # send the request to server
        response = requests.get(url,params=params)
        
        # wait till response is available
        response.raise_for_status()
        
        # wait for few seconds
        time.sleep(SLEEP_TIME)
        
        # return the response in json format
        return response.json()
    
    
    def get_popular_movies(self, page):
        return self.get("/movie/popular",page=page)
    
    def  get_movie_details(self, movie_id):
        return self.get(f"/movie/{movie_id}")
    
    def  get_movie_recommendation(self, movie_id):
        return self.get(f"/movie/{movie_id}/recommendations")
    
    def  get_movie_keywords(self, movie_id):
        return self.get(f"/movie/{movie_id}/keywords")
        
    def  get_movie_credits(self, movie_id):
        return self.get(f"/movie/{movie_id}/credits")
    
# create the client instance
client = TMDBClient(api_key=API_KEY)

for page in range(1,PAGE_COUNT + 1):
    
    print(f" -- downloading movies on page {page}")
    
    # download the popular movies
    movies = client.get_popular_movies(page = page)
    # print(movies)
    
    # process for each movie
    for movie in movies['results']:
        print(movie)
        print("-" * 80)
        
        # get the movie id
        movie_id = movie['id']
        
        # get the movie details
        movie_details = client.get_movie_details(movie_id)
        print(movie_details)
        print('-' * 80)
        
        # get the movie credits
        movie_credits = client.get_movie_credits(movie_id)
        print(movie_credits)
        print('-' * 80)
        
        
        # get the movie recommendations
        movie_recommendations = client.get_movie_recommendation(movie_id)
        print(movie_recommendations)
        print('-' * 80) 
        
        # get the movie keywords
        movie_keywords = client.get_movie_keywords(movie_id)
        print(movie_keywords)
        print('-' * 80) 
        
        break
        
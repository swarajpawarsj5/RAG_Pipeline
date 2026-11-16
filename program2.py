from dotenv import load_dotenv
import requests

# load the .env file enviornment variables
load_dotenv()

# define the constants
BASE_URL = "https://api.themoviedb.org/3"
DATA_DIR = "./tmdb/"

# define a Client class which will download the movie data from TMDB
class TMDBClient:
    def __init__(self, api_key):
        # use this api key to send the request to TMDB ReST APIs
        self._api_key = api_key
        
    def get(self, endpoint):
        # define the set of parameters which are required to send to api
        params = {
            "api_key": self._api_key
        }
        
        # build the final url
        url = BASE_URL + endpoint
        
        # send the request to server
        response = requests.get(url,params=params)
        
        # wit till response is available
        response.raise_for_status()
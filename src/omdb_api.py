import json
import requests


# Parse the API key
with open('data/keys.json') as keys_json_file:
    api_key = json.load(keys_json_file)['omdb_key']

# OMDb url
url = f'http://www.omdbapi.com/?apikey={api_key}&t=%s'


def get_movie_json(movie_title):
    r = requests.get(url % movie_title)

    if r.status_code == 200:
        data = r.json()

        if data['Response']:
            return data

        else:
            raise Exception(f'{movie_title}: Not found')

    else:
        raise Exception(f'{movie_title}: Status code != 200')

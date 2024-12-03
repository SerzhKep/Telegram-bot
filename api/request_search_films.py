from http.client import responses

import requests
import os


def search_movie_api(name: str, genre: str, limit: int):
    url = 'https://api.kinopoisk.dev/v1.3/movie'
    headers = {'X-API-KEY' : os.getenv('KINOPOISK_API_KEY')}
    params ={
        'query': name,
        'genres': genre,
        'page': 1,
        'limit': limit
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['docs']
    else:
        return []
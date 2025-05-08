import requests
import json
import time


# Emby server API URL and authentication information
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'WIZ-LT'  # Optional, if the API requires user authentication

# 以下代码用于调试
def debug_function(message):
    print(f"DEBUG: {message}")


#列出库中所有的电影流派
def emby_get_all_movie_genres():

    # Set API request headers
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    # Get the API endpoint for all movies
    items_endpoint = f'{emby_url}/Items'

    # Set query parameters
    params = {
        'Recursive': 'true',
        'IncludeItemTypes': 'Movie',
        'Fields': 'Genres',  # Request to include the Genres field
        'Limit': '1000000'  # Adjust the limit according to your needs
    }

    # Send request to get the list of movies
    response = requests.get(items_endpoint, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        movies = response.json()['Items']
        # Use a set to remove duplicate genres
        all_genres = set()
        
        for movie in movies:

            # Dynamically parse all fields in the JSON data
            # debug_function("\nParsed fields:")
            # for key, value in movie.items():
            #     debug_function(f"{key}: {value}")

            movie_name = movie['Name']
            genres = movie.get('Genres', [])
            if genres:
                # Add genres to the set
                all_genres.update(genres)
                # debug_function(f"Movie: {movie_name}")
                # debug_function(f"Genres: {', '.join(genres)}")
                # debug_function('-' * 30)
            else:
                debug_function(f"Movie '{movie_name}' has no specified genres.")
        
        # debug_function all unique genres
        print("All unique genres:")
        print(', '.join(sorted(all_genres)))
    else:
        print(f"Request failed, status code: {response.status_code}")
        print(response.text)


emby_get_all_movie_genres()
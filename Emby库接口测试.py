import requests
import json
import time


# Emby server API URL and authentication information
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'cefa80922459464484efd3ac11a714b8' #  是从wireshark抓包工具中获取的
    
def emby_get_all_movie_genres():

    # Set API request headers
    headers = {
        'X-Emby-Token': api_key
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
            '''
            print("\nParsed fields:")
            for key, value in movie.items():
                print(f"{key}: {value}")
            '''

            movie_name = movie['Name']
            genres = movie.get('Genres', [])
            if genres:
                # Add genres to the set
                all_genres.update(genres)
                '''
                print(f"Movie: {movie_name}")
                print(f"Genres: {', '.join(genres)}")
                print('-' * 30)
                '''
            else:
                print(f"Movie '{movie_name}' has no specified genres.")
        
        # Print all unique genres
        print("All unique genres:")
        print(', '.join(sorted(all_genres)))
    else:
        print(f"Request failed, status code: {response.status_code}")
        print(response.text)

#GET /Search/Hints
#搜索媒体库
def emby_Search_all_movie():

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
        'Limit': '1'  # Adjust the limit according to your needs
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
            print("\nParsed fields:")
            for key, value in movie.items():
                print(f"{key}: {value}")

            movie_name = movie['Name']
            genres = movie.get('Genres', [])
            if genres:
                # Add genres to the set
                all_genres.update(genres)
                print(f"Movie: {movie_name}")
                print(f"Genres: {', '.join(genres)}")
                print('-' * 30)
            else:
                print(f"Movie '{movie_name}' has no specified genres.")
        
        # Print all unique genres
        print("All unique genres:")
        print(', '.join(sorted(all_genres)))
    else:
        print(f"Request failed, status code: {response.status_code}")
        print(response.text)



def emby_get_item_info(movie_id):

    # Set API request headers
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    # Get the API endpoint for the movie
    detail_item_endpoint = f'{emby_url}/users/{user_id}/items/{movie_id}'


    detail_item_response = requests.get(detail_item_endpoint, headers=headers)

    if detail_item_response.status_code == 200:
        print("Successfully retrieved complete movie information")
        movie_data = detail_item_response.json()
        # Dynamically parse all fields in the JSON data
        print("\nParsed fields:")
        for key, value in movie_data.items():
            print(f"{key}: {value}")
    else:
        print(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        print(f"Response content: {detail_item_response.text}")


def emby_get_item_MetadataEditorInfo():

    # Set API request headers
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    movie_id = '429692'
    # Get the API endpoint for the movie
    detail_item_endpoint = f'{emby_url}/Items/{movie_id}/MetadataEditor'

    # Set query parameters
    params = {
        'api_key': api_key,
        'Content-Type': 'application/json'
    }

    detail_item_response = requests.get(detail_item_endpoint, headers=headers, params=params)

    if detail_item_response.status_code == 200:
        print("Successfully retrieved complete movie information")
        movie_data = detail_item_response.json()
        # Dynamically parse all fields in the JSON data
        print("\nParsed fields:")
        for key, value in movie_data.items():
            print(f"{key}: {value}")
    else:
        print(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        print(f"Response content: {detail_item_response.text}")









emby_get_all_movie_genres()#PASSc
emby_get_item_info('429692')#PASS
emby_get_item_MetadataEditorInfo()#PASS


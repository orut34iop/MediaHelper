import requests
import json
import os
from datetime import datetime

# 定义日志文件路径
log_file_path = os.path.join(os.getcwd(), 'genres.log')

# 定义日志记录函数
def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')

# Emby server API URL and authentication information
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'cefa80922459464484efd3ac11a714b8'


def emby_get_item_info(movie_id):
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }
    detail_item_endpoint = f'{emby_url}/users/{user_id}/items/{movie_id}'
    detail_item_response = requests.get(detail_item_endpoint, headers=headers)

    if detail_item_response.status_code == 200:
        return detail_item_response.json()
    else:
        log_message(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        log_message(f"Response content: {detail_item_response.text}")
        return None

def emby_tv_translate_genres_and_update_whole_item():
    update_count = 0

    genres_map = {
    'Action': '动作',
    'Adventure': '冒险',
    'Animation': '动画',
    'Biography': '传记',
    'Comedy': '喜剧',
    'Crime': '犯罪',
    'Documentary': '纪录',
    'Drama': '剧情',
    'Family': '家庭',
    'Fantasy': '奇幻',
    'Food': '美食',
    'Game Show': '游戏节目',
    'History': '历史',
    'Holiday': '节日',
    'Horror': '恐怖',
    'Mini-Series': '迷你剧',
    'Music': '音乐',
    'Musical': '音乐剧',
    'Mystery': '悬疑',
    'Reality': '真人秀',
    'Reality TV': '真人秀电视',
    'Romance': '浪漫',
    'Sci-Fi & Fantasy': '科幻与奇幻',
    'Science Fiction': '科幻',
    'Short': '短片',
    'Soap': '肥皂剧',
    'Sport': '运动',
    'Suspense': '悬念',
    'Talk Show': '脱口秀',
    'Thriller': '惊悚',
    'Travel': '旅行',
    'War': '战争',
    'Western': '西部'
    }

    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }
    items_endpoint = f'{emby_url}/Items'
    params = {
        'Recursive': 'true',
        'IncludeItemTypes': 'Series',
        'Fields': 'Genres',
        'Limit': '1000000'
    }

    response = requests.get(items_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        tvs = response.json().get('Items', [])
        
        for each_tv in tvs:
            tv_id = each_tv['Id']
            original_genres = each_tv.get('Genres', [])
            translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

            if original_genres == translated_genres:
                continue

            tv = emby_get_item_info(tv_id)
            if not tv:
                log_message(f"剧集ID '{tv_id}' 的信息读取失败.(Total updates: {update_count})")
                continue

            original_genres = tv.get('Genres', [])
            translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

            if original_genres != translated_genres:
                genreitems = [{'Name': genres_map.get(genreitem['Name'], genreitem['Name']), 'Id': genreitem['Id']} for genreitem in tv.get('GenreItems', [])]
                tv['Genres'] = translated_genres
                tv['GenreItems'] = genreitems

                update_endpoint = f'{emby_url}/emby/Items/{tv_id}?/api_key={api_key}'
                update_response = requests.post(update_endpoint, headers=headers, data=json.dumps(tv))

                if update_response.status_code in [200, 204]:
                    update_count += 1
                    log_message(f"剧集: {tv['Name']} 流派信息已更新。(Total updates: {update_count})")
                else:
                    log_message(f"更新失败，状态码: {update_response.status_code}(Total updates: {update_count})")
                    log_message(update_response.text)
            else:
                log_message(f"剧集 '{tv['Name']}' 的流派信息没有改变.")
    else:
        log_message(f"请求失败，状态码: {response.status_code}")
        log_message(response.text)

def emby_get_item_info(movie_id):
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }
    detail_item_endpoint = f'{emby_url}/users/{user_id}/items/{movie_id}'
    detail_item_response = requests.get(detail_item_endpoint, headers=headers)

    if detail_item_response.status_code == 200:
        return detail_item_response.json()
    else:
        log_message(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        log_message(f"Response content: {detail_item_response.text}")
        return None

def emby_movie_translate_genres_and_update_whole_item():
    update_count = 0
    genres_map = {
        'Action': '动作', 'Adult': '成人', 'Adventure': '冒险', 'Animation': '动画', 'Anime': '动漫',
        'Biography': '传记', 'Children': '儿童', 'Comedy': '喜剧', 'Crime': '犯罪', 'Documentary': '纪录',
        'Drama': '剧情', 'Eastern': '东方', 'Erotic': '情色', 'Family': '家庭', 'Fantasy': '奇幻',
        'Film Noir': '黑色电影', 'History': '历史', 'Holiday': '节日', 'Horror': '恐怖', 'Indie': '独立电影',
        'Martial Arts': '武术', 'Music': '音乐', 'Musical': '音乐剧', 'Mystery': '悬疑', 'News': '新闻',
        'Reality TV': '真人秀', 'Romance': '爱情', 'Science Fiction': '科幻', 'Short': '短片', 'Sport': '运动',
        'Suspense': '悬念', 'TV Movie': '电视电影', 'Thriller': '惊悚', 'War': '战争', 'Western': '西部',
        'superhero': '超级英雄'
    }

    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }
    items_endpoint = f'{emby_url}/Items'
    params = {
        'Recursive': 'true',
        'IncludeItemTypes': 'Movie',
        'Fields': 'Genres',
        'Limit': '1000000'
    }

    response = requests.get(items_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        movies = response.json().get('Items', [])
        
        for each_movie in movies:
            movie_id = each_movie['Id']
            original_genres = each_movie.get('Genres', [])
            translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

            if original_genres == translated_genres:
                continue

            movie = emby_get_item_info(movie_id)
            if not movie:
                log_message(f"电影ID '{movie_id}' 的信息读取失败.(Total updates: {update_count})")
                continue

            original_genres = movie.get('Genres', [])
            translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

            if original_genres != translated_genres:
                genreitems = [{'Name': genres_map.get(genreitem['Name'], genreitem['Name']), 'Id': genreitem['Id']} for genreitem in movie.get('GenreItems', [])]
                movie['Genres'] = translated_genres
                movie['GenreItems'] = genreitems

                update_endpoint = f'{emby_url}/emby/Items/{movie_id}?/api_key={api_key}'
                update_response = requests.post(update_endpoint, headers=headers, data=json.dumps(movie))

                if update_response.status_code in [200, 204]:
                    update_count += 1
                    log_message(f"电影: {movie['Name']} 流派信息已更新。(Total updates: {update_count})")
                else:
                    log_message(f"更新失败，状态码: {update_response.status_code}(Total updates: {update_count})")
                    log_message(update_response.text)
            else:
                log_message(f"电影 '{movie['Name']}' 的流派信息没有改变.")
    else:
        log_message(f"请求失败，状态码: {response.status_code}")
        log_message(response.text)


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
            # log_message("\nParsed fields:")
            # for key, value in movie.items():
            #     log_message(f"{key}: {value}")

            movie_name = movie['Name']
            genres = movie.get('Genres', [])
            if genres:
                # Add genres to the set
                all_genres.update(genres)
                # log_message(f"Movie: {movie_name}")
                # log_message(f"Genres: {', '.join(genres)}")
                # log_message('-' * 30)
            else:
                log_message(f"Movie '{movie_name}' has no specified genres.")
        
        # debug_function all unique genres
        log_message("All unique genres:")
        log_message(', '.join(sorted(all_genres)))
    else:
        log_message(f"Request failed, status code: {response.status_code}")
        log_message(response.text)

#列出库中所有的电视剧集流派
def emby_get_all_tv_genres():

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
        'IncludeItemTypes': 'Series',
        'Fields': 'Genres',  # Request to include the Genres field
        'Limit': '1000000'  # Adjust the limit according to your needs 后续解析"TotalRecordCount":1812字段
    }

    # Send request to get the list of movies
    response = requests.get(items_endpoint, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        tvs = response.json()['Items']
        # Use a set to remove duplicate genres
        all_genres = set()
        
        for tv in tvs:

            # Dynamically parse all fields in the JSON data
            log_message("\nParsed fields:")
            for key, value in tv.items():
                log_message(f"{key}: {value}")

            tv_name = tv['Name']
            genres = tv.get('Genres', [])
            if genres:
                # Add genres to the set
                all_genres.update(genres)
                log_message(f"tv: {tv_name}")
                log_message(f"tv: {', '.join(genres)}")
                log_message('-' * 30)
            else:
                log_message(f"tv '{tv_name}' has no specified genres.")
        
        # log_message all unique genres
        log_message("All unique genres:")
        log_message(', '.join(sorted(all_genres)))
    else:
        log_message(f"Request failed, status code: {response.status_code}")
        log_message(response.text)

# emby_get_all_movie_genres() # PASS TESTING
# emby_get_all_tv_genres() # PASS TESTING
# emby_movie_translate_genres_and_update_whole_item() # PASS TESTING
emby_tv_translate_genres_and_update_whole_item()

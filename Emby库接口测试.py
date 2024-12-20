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
        #print("Successfully retrieved complete movie information")
        movie_data = detail_item_response.json()
        # Dynamically parse all fields in the JSON data
        #print("\nParsed fields:")
        #for key, value in movie_data.items():
        #    print(f"{key}: {value}")
        return movie_data
    else:
        print(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        print(f"Response content: {detail_item_response.text}")
        return None


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





def emby_translate_genres():

    genreitems = []

    # 设置API请求头
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    # 流派映射表
    genres_map = {
        'Action': '动作',
        'Adventure': '冒险',
        'Animation': '动画',
        'Biography': '传记',
        'Comedy': '喜剧',
        'Crime': '犯罪',
        'Documentary': '纪录片',
        'Drama': '戏剧',
        'Erotic': '情色',
        'Family': '家庭',
        'Fantasy': '奇幻',
        'History': '历史',
        'Horror': '恐怖',
        'Music': '音乐',
        'Musical': '音乐剧',
        'Mystery': '悬疑',
        'Reality TV': '真人秀',
        'Romance': '浪漫',
        'Science Fiction': '科幻',
        'Sport': '运动',
        'TV Movie': '电视电影',
        'Thriller': '惊悚',
        'War': '战争',
        'Western': '西部片'
    }

    # 获取所有电影的API端点
    items_endpoint = f'{emby_url}/Items'

    # 设置查询参数
    params = {
        'Recursive': 'true',
        'IncludeItemTypes': 'Movie',
        'Fields': 'Genres',  # 请求包含Genres字段
        'Limit': '1'  # 根据你的需求调整限制数量
    }

    # 发送请求获取电影列表
    response = requests.get(items_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        movies = response.json()['Items']
        
        for movie in movies:

            print("\nParsed fields:")
            for key, value in movie.items():
                print(f"{key}: {value}")

            movie_id = movie['Id']
            movie_name = movie['Name']
            genres = movie.get('Genres', [])

            # 打印原有和翻译后的流派
            print(f"电影: {movie_name}")
            print(f"原流派: {', '.join(genres)}")
            #print(f"原流派项目表: {', '.join(movie.get('GenreItems', []))}")
            



            
            #print(f"原流派项目表: {', '.join(genreitems)}")

            if genres:
                # 使用映射表翻译流派
                translated_genres = [genres_map.get(genre, genre) for genre in genres]
                print(f"翻译后流派: {', '.join(translated_genres)}")

                # 解析并保存GenreItems字段
                for genreitem in movie.get('GenreItems', []):
                    translated_genreitem = genres_map.get(genreitem['Name'], genreitem['Name'])
                    genreitems.append({'Name': translated_genreitem, 'Id': genreitem['Id']})
                
                # 更新电影的流派信息
                update_endpoint = f'{emby_url}/emby/Items/{movie_id}?/api_key={api_key}' #URL接口应该正确了，但是参数可能有问题
                update_data = {
                    "Genres": translated_genres,
                    'GenreItems': genreitems
                }
                update_response = requests.post(update_endpoint, headers=headers, data=json.dumps(update_data))

                if update_response.status_code == 200:
                    print("流派信息已更新。")
                else:
                    print(f"更新失败，状态码: {update_response.status_code}")
                    print(update_response.text)
                
                print('-' * 30)
            else:
                print(f"电影 '{movie_name}' 没有指定流派.")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)




def emby_translate_genres_and_update_whole_item():

    genreitems = []

    # 设置API请求头
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    # 流派映射表
    genres_map = {
        'Action': '动作',
        'Adult': '成人',
        'Adventure': '冒险',
        'Animation': '动画',
        'Anime': '动漫',
        'Biography': '传记',
        'Children': '儿童',
        'Comedy': '喜剧',
        'Crime': '犯罪',
        'Documentary': '纪录',
        'Drama': '剧情',
        'Eastern': '东方',
        'Erotic': '情色',
        'Family': '家庭',
        'Fantasy': '奇幻',
        'Film Noir': '黑色电影',
        'History': '历史',
        'Holiday': '节日',
        'Horror': '恐怖',
        'Indie': '独立电影',
        'Martial Arts': '武术',
        'Music': '音乐',
        'Musical': '音乐剧',
        'Mystery': '悬疑',
        'News': '新闻',
        'Reality TV': '真人秀',
        'Romance': '爱情',
        'Science Fiction': '科幻',
        'Short': '短片',
        'Sport': '运动',
        'Suspense': '悬念',
        'TV Movie': '电视电影',
        'Thriller': '惊悚',
        'War': '战争',
        'Western': '西部',
        'superhero': '超级英雄'
    }

    # 获取所有电影的API端点
    items_endpoint = f'{emby_url}/Items'

    # 设置查询参数
    params = {
        'Recursive': 'true',
        'IncludeItemTypes': 'Movie',
        'Fields': 'Genres',  # 请求包含Genres字段
        'Limit': '1000000'  # 根据你的需求调整限制数量
    }

    # 发送请求获取电影列表
    response = requests.get(items_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        movies = response.json()['Items']
        
        for each_movie in movies:

#            print("\nParsed fields:")
#            for key, value in each_movie.items():
#                print(f"{key}: {value}")

            movie_id = each_movie['Id']

            movie = emby_get_item_info(movie_id)

            movie_name = movie['Name']
            genres = movie.get('Genres', [])

            # 打印原有和翻译后的流派
            print(f"电影: {movie_name}")
#            print(f"原流派: {', '.join(genres)}")
            #print(f"原流派项目表: {', '.join(movie.get('GenreItems', []))}")       
            #print(f"原流派项目表: {', '.join(genreitems)}")

            if genres:
                # 使用映射表翻译流派
                translated_genres = [genres_map.get(genre, genre) for genre in genres]
#                print(f"翻译后流派: {', '.join(translated_genres)}")

                # 解析并保存GenreItems字段
                for genreitem in movie.get('GenreItems', []):
                    translated_genreitem = genres_map.get(genreitem['Name'], genreitem['Name'])
                    genreitems.append({'Name': translated_genreitem, 'Id': genreitem['Id']})
                
                # 更新电影的流派信息
                movie['Genres'] = translated_genres
                movie['GenreItems'] = genreitems
                
                update_endpoint = f'{emby_url}/emby/Items/{movie_id}?/api_key={api_key}' 
            
                update_response = requests.post(update_endpoint, headers=headers, data=json.dumps(movie))

                if update_response.status_code in [200, 204]:
                    print("流派信息已更新。")
                else:
                    print(f"更新失败，状态码: {update_response.status_code}")
                    print(update_response.text)
                
                print('-' * 30)
            else:
                print(f"电影 '{movie_name}' 没有指定流派.")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)



#emby_get_all_movie_genres()#PASSc
#emby_get_item_info('429692')#PASS
#emby_get_item_MetadataEditorInfo()#PASS
#emby_translate_genres()
emby_translate_genres_and_update_whole_item()
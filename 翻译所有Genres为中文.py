import requests
import json
import time


# Emby server API URL and authentication information
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'cefa80922459464484efd3ac11a714b8' #  是从wireshark抓包工具中获取的



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
        # print("Successfully retrieved complete movie information")
        movie_data = detail_item_response.json()
        # Dynamically parse all fields in the JSON data
        # print("\nParsed fields:")
        # for key, value in movie_data.items():
        #    print(f"{key}: {value}")
        return movie_data
    else:
        print(f"Failed to retrieve complete movie information, status code: {detail_item_response.status_code}")
        print(f"Response content: {detail_item_response.text}")
        return None

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

            # print("\nParsed fields:")
            # for key, value in each_movie.items():
            #     print(f"{key}: {value}")

            movie_id = each_movie['Id']
            movie_name = each_movie['Name']
            original_genres = each_movie.get('Genres', [])
            # 使用映射表翻译流派
            translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

            # 只有当Genres值和原来不同时，才发起更新item信息
            if original_genres == translated_genres:
                #print(f"电影 '{movie_name}' 的流派信息不需要翻译.")
                continue

            # 更新item前需要先获取完整的item信息
            movie = emby_get_item_info(movie_id)

            if not movie:
                print(f"电影ID '{movie_id}' 的信息读取失败.")
                continue
    
            movie_name = movie['Name']
            original_genres = movie.get('Genres', [])
            
            if original_genres:
                # 使用映射表翻译流派
                translated_genres = [genres_map.get(genre, genre) for genre in original_genres]

                # 只有当Genres值和原来不同时，才发起更新item信息
                if original_genres != translated_genres:
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
                        # 打印原有和翻译后的流派
                        print(f"电影: {movie_name} 流派信息已更新。")
                    else:
                        print(f"更新失败，状态码: {update_response.status_code}")
                        print(update_response.text)
                    
                    print('-' * 30)
                #else:
                #    print(f"电影 '{movie_name}' 的流派信息没有改变.")
                    
            else:
                print(f"电影 '{movie_name}' 没有指定流派.")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)


emby_translate_genres_and_update_whole_item()
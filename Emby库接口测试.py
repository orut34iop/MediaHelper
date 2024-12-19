import requests
import json
import time


# Emby服务器的API URL和认证信息
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'WIZ-LT'  # 可选，如果API需要用户身份验证

def emby_get_all_movie_genres():

    # 设置API请求头
    headers = {
        'X-Emby-Token': api_key
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

    # 检查请求是否成功
    if response.status_code == 200:
        movies = response.json()['Items']
        # 使用集合来去重流派信息
        all_genres = set()
        
        for movie in movies:
            movie_name = movie['Name']
            genres = movie.get('Genres', [])
            if genres:
                # 将流派添加到集合中
                all_genres.update(genres)
                print(f"电影: {movie_name}")
                print(f"流派: {', '.join(genres)}")
                print('-' * 30)
            else:
                print(f"电影 '{movie_name}' 没有指定流派.")
        
        # 打印所有不重复的流派
        print("所有不重复的流派:")
        print(', '.join(sorted(all_genres)))
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)




def emby_get_item_info():

    # 设置API请求头
    headers = {
        'X-Emby-Token': api_key
    }

    movie_id = '429692'
    # 获取所有电影的API端点
    #detail_item_endpoint = f'{emby_url}/Users/{user_id}/Items/{movie_id}'
    detail_item_endpoint = f'{emby_url}/emby/Users/{user_id}/Items/{movie_id}'

    # 设置查询参数
    params = {
        'api_key': api_key
    }

    #detail_item_response = requests.get(detail_item_endpoint, headers=headers, params=params)
    detail_item_response = requests.get(detail_item_endpoint, headers=headers)

    if detail_item_response.status_code == 200:
        print("已获取完整电影信息")
        movie_data = detail_item_response.json()
        # 动态解析json数据中的所有字段
        print("\n解析到的所有字段:")
        for key, value in movie_data.items():
            print(f"{key}: {value}")
    else:
        print(f"获取完整电影信息失败，状态码: {detail_item_response.status_code}")
        print(f"响应内容: {detail_item_response.text}")


def emby_get_item_MetadataEditorInfo():

    # 设置API请求头
    headers = {
        'X-Emby-Token': api_key,
        'Content-Type': 'application/json'
    }

    movie_id = '429692'
    # 获取所有电影的API端点
    detail_item_endpoint = f'{emby_url}/Items/{movie_id}/MetadataEditor'

    # 设置查询参数
    params = {
        'api_key': api_key
    }

    detail_item_response = requests.get(detail_item_endpoint, headers=headers, params=params)

    if detail_item_response.status_code == 200:
        print("已获取完整电影信息")
        movie_data = detail_item_response.json()
        # 动态解析json数据中的所有字段
        print("\n解析到的所有字段:")
        for key, value in movie_data.items():
            print(f"{key}: {value}")
    else:
        print(f"获取完整电影信息失败，状态码: {detail_item_response.status_code}")
        print(f"响应内容: {detail_item_response.text}")

#emby_get_all_movie_genres()#PASS
emby_get_item_info()#FAIL
#emby_get_item_MetadataEditorInfo()#PASS

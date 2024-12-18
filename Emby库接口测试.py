import requests
import json

# 配置Emby服务器信息
# EMBY_SERVER_URL = "http://192.168.2.42:8096"
# API_KEY = "850d6a3a78bc4ec6b584077b34b2a956"


import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"总耗时: {total_time:.2f} 秒")
        return result

    return wrapper




# Emby服务器的API URL和认证信息
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"
user_id = 'your_user_id_here'  # 可选，如果API需要用户身份验证

# 设置API请求头
headers = {
    'X-Emby-Token': api_key,
    'Content-Type': 'application/json'
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

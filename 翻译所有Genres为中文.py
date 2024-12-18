import requests
import json


# Emby服务器的API URL和认证信息
emby_url = "http://192.168.2.42:8096"
api_key = "850d6a3a78bc4ec6b584077b34b2a956"

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
    'Limit': '1'  # 限制数量改为1
}

# 发送请求获取电影列表
response = requests.get(items_endpoint, headers=headers, params=params)

if response.status_code == 200:
    movies = response.json()['Items']
    
    for movie in movies:
        # 动态解析json数据中的所有字段
        movie_data = {}
        print("\n解析到的所有字段:")
        for key, value in movie.items():
            movie_data[key] = value
            print(f"{key}: {value}")
        
        movie_id = movie_data.get('Id')
        if not movie_id:
            print(f"电影ID为空，跳过此电影: {movie_data.get('Name')}")
            continue
        
        movie_name = movie_data.get('Name')
        genres = movie_data.get('Genres', [])
        
        if genres:
            # 使用映射表翻译流派
            translated_genres = [genres_map.get(genre, genre) for genre in genres]
            
            # 打印原有和翻译后的流派
            print(f"电影: {movie_name}")
            print(f"原流派: {', '.join(genres)}")
            print(f"翻译后流派: {', '.join(translated_genres)}")
            
            # 更新电影的流派信息
            if not translated_genres:
                print("翻译后流派为空，跳过更新。")
                continue
            
            update_endpoint = f'{emby_url}/Items/{movie_id}'
            
            # 更新movie_data中的Genres
            movie_data['Genres'] = translated_genres
            
            update_response = requests.post(update_endpoint, headers=headers, data=json.dumps(movie_data))
            
            if update_response.status_code == 200:
                print("电影信息已更新。")
            else:
                print(f"更新失败，状态码: {update_response.status_code}")
                print(f"响应内容: {update_response.text}")
            
            print('-' * 30)
        else:
            print(f"电影 '{movie_name}' 没有指定流派.")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)

#功能说明： 输入指定的tmdb值，查询emby电影库中是否已存在
#注意: tmdb对应nfo中根元素movie里的tmdbid字段


import requests




# 配置Emby服务器信息
EMBY_SERVER_URL = "http://127.0.0.1:8096"
API_KEY = "850d6a3a78bc4ec6b584077b34b2a956"
query_emdb_value = "1173"  # 替换为您要查询的 TMDB 值




# 获取所有电影的信息
def get_all_movies():
    url = f"{EMBY_SERVER_URL}/emby/Items"
    params = {
        "api_key": API_KEY,
        "IncludeItemTypes": "Movie",
        "Recursive": True,
        "Fields": "ProviderIds,Path",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()["Items"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # 输出HTTP错误
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")  # 输出其他错误
    except ValueError:
        print("Error parsing JSON response")
        print("Response content:", response.content)  # 输出响应内容以便调试
    return []


# 查询TMDb ID
def query_movies_by_tmdbid(movies,tmdb_value):

    for movie in movies:
        tmdb_id = movie.get("ProviderIds", {}).get("Tmdb", "")
        if tmdb_value == tmdb_id:
            print(f"电影 '{movie['Name']}' 存在于 Emby 库中，TMDB 值: {tmdb_value}")
            return;
    
    print(f"没有找到与 TMDB 值 {tmdb_value} 相同的电影。")
    return




# 主函数
def main():
    all_movies = get_all_movies()
    if not all_movies:
        print("没有电影")
        return
    
    query_movies_by_tmdbid(all_movies,query_emdb_value)


if __name__ == "__main__":
    main()

#功能说明： 输入指定的tmdb值，查询emby电影库中是否已存在
#注意: tmdb对应nfo中根元素movie里的tmdbid字段


import requests




# 配置Emby服务器信息
EMBY_SERVER_URL = "http://192.168.2.42:8096"
API_KEY = "850d6a3a78bc4ec6b584077b34b2a956"




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

# 获取所有电影的信息
def get_all_tvs():
    url = f"{EMBY_SERVER_URL}/emby/Items"
    params = {
        "api_key": API_KEY,
        "IncludeItemTypes": "Series",
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
def query_miss_tmdbid():

    movies = get_all_movies()

    for movie in movies:
        tmdb_id = movie.get("ProviderIds", {}).get("Tmdb", "")
        if not tmdb_id:
            print(f"电影 '{movie['Name']}' 缺少 TMDB 值")
    
    tvs = get_all_tvs()

    for tv in tvs:
        tmdb_id = tv.get("ProviderIds", {}).get("Tmdb", "")
        if not tmdb_id:
            print(f"剧集 '{tv['Name']}' 缺少 TMDB 值")

    return




# 主函数
def main():
    
    query_miss_tmdbid()


if __name__ == "__main__":
    main()

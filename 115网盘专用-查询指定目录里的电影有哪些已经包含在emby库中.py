#功能说明： 输入指定的tmdb值，查询emby电影库中是否已存在
#注意: tmdb对应nfo中根元素movie里的tmdbid字段


import requests
import os
import xml.etree.ElementTree as ET



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
            return True;
    
    print(f"没有找到与 TMDB 值 {tmdb_value} 相同的电影。")
    return False




def extract_tmdbid_from_nfo(nfo_path):
    try:
        # 解析 .nfo 文件
        tree = ET.parse(nfo_path)
        root = tree.getroot()
        
        # 查找名为 movie 的根元素下的一级子元素 tmdbid
        #tmdbid_element = root.find('movie/tmdbid')
        tmdbid_element = root.find('tmdbid')
        
        if tmdbid_element is not None:
            query_tmdbid = tmdbid_element.text.strip()

            print(f"在 '{nfo_path}' 中找到 tmdbid: {query_tmdbid}")

            return query_tmdbid
        else:
            print(f"在 '{nfo_path}' 中未找到 tmdbid 元素。")
    except ET.ParseError as e:
        print(f"解析错误：无法解析文件 '{nfo_path}'，错误信息: {e}")
    except Exception as e:
        print(f"发生错误：在处理文件 '{nfo_path}' 时出错，错误信息: {e}")

    return None

def process_nfo_files_in_directory(directory):
    
    all_movies = get_all_movies()
    if not all_movies:
        print("Emby库里没有电影")
        return
    

    # 归地遍历指定路径下的所有子目录和文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.nfo'):
                nfo_path = os.path.join(root, file)
                query_emdb_value = extract_tmdbid_from_nfo(nfo_path)
                if query_emdb_value is not None:
                    if not query_movies_by_tmdbid(all_movies,query_emdb_value):
                        print(f"新增电影 : '{nfo_path}' ")
                    else:
                        if remove_duplicate_nfo_file == "yes":
                            os.remove(nfo_path)
                            print(f"删除重复电影nfo : '{nfo_path}' ")

if __name__ == "__main__":
    # 用户输入路径
    source_directory = input("请输入包含 .nfo 文件的路径：")
    remove_duplicate_nfo_file = input("是否删除重复的nfo文件, 请输入 yes 或 no :")
    process_nfo_files_in_directory(source_directory)
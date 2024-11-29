import os
import re

def search_nfo_files_in_text():
    # 获取用户输入的目录和文本文件路径
    #directory = input("请输入要扫描的目录路径：").strip()
    directory="C:\\emby-as-115\\PreLibs\\外语电影"
    text_file ="C:\\emby-as-115\\PreLibs\\外语电影\\script\\目录树.txt"
    #text_file = input("请输入文本文件的路径：").strip()
    # 询问是否需要删除无效的nfo文件
    delete_confirmation = input("是否删除没有对应视频的nfo文件？(y/n): ").strip().lower()


    # 读取文本文件内容
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            text_content = file.read()
    except FileNotFoundError:
        print(f"错误：无法找到文件 {text_file}")
        return
    except IOError:
        print(f"错误：无法读取文件 {text_file}")
        return

 
    # 遍历目录中的所有文件
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.nfo'):
                nfo_file_path = os.path.join(root, file)
                # 获取文件名，不包括扩展名
                file_name = os.path.splitext(file)[0]
                
                # 在文本中搜索匹配文件名+".mkv"或".ts"的字符串
                
                pattern = re.compile(rf'{re.escape(file_name)}\.(mkv|ts|mp4|avi|rmvb|m2ts)',re.IGNORECASE | re.UNICODE)
                match = pattern.search(text_content)
                if match:
                    #print(f"找到匹配：{match.group()}")
                    i = 1
                else:
                    #print(f"没有找到匹配的视频：{nfo_file_path}")
                    if delete_confirmation == 'y':
                        try:
                            # 删除文件
                            os.remove(nfo_file_path)
                            print(f"已删除文件：{nfo_file_path}")
                        except PermissionError:
                            print(f"错误：无法删除文件 {nfo_file_path}，权限不足。")
                        except Exception as e:
                            print(f"错误：删除文件 {nfo_file_path} 时发生错误：{e}")



if __name__ == "__main__":
    search_nfo_files_in_text()

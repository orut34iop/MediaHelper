import os
import xml.etree.ElementTree as ET

#功能说明： 扫描指定目录下所有已经tmm刮削完成的电影文件夹，根据文件夹里的nfo里的title，year字段重新命名文件夹的名称
#示例：
#指定目录下：有movie1-xxxx","movie2-uuuu" 电影文件夹
#脚本处理后，文件夹重新命名为"movie1（year)","movie2（year)"


def process_folders(path):
    # 遍历给定路径下的一级子文件夹
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)

        # 只处理一级子文件夹
        if os.path.isdir(folder_path):
            # 获取文件夹下的所有文件
            files = os.listdir(folder_path)
            
            # 筛选出 .nfo 文件
            nfo_files = [f for f in files if f.endswith('.nfo')]
            
            # 确保只有一个 .nfo 文件
            if len(nfo_files) == 1:
                nfo_file = nfo_files[0]
                nfo_name, _ = os.path.splitext(nfo_file)
                
                # 查找与 .nfo 文件同名的视频文件
                video_files = [f for f in files if f.startswith(nfo_name) and f.endswith(('.mp4', '.mkv', '.avi', '.mov', '.rm', '.flv', '.mpg', '.m2ts', '.wmv', '.rmvb', '.ts', '.iso'))]

                if video_files:
                    nfo_file_path = os.path.join(folder_path, nfo_file)
                    try:
                        # 解析 .nfo 文件
                        tree = ET.parse(nfo_file_path)
                        root = tree.getroot()

                        # 提取 title 和 year 元素的文本
                        title_element = root.find('title')
                        year_element = root.find('year')
                        if title_element is not None and year_element is not None:
                            title = title_element.text.strip()
                            year = year_element.text.strip()

                            # 新文件夹名: "B (Y)"
                            new_folder_name = f"{title} ({year})"
                            new_folder_path = os.path.join(path, new_folder_name)

                            # 如果新名称与现有名称不同，重命名文件夹
                            if not os.path.exists(new_folder_path) and new_folder_name != folder_name:                            
                                os.rename(folder_path, new_folder_path)
                                print(f"Renamed folder '{folder_name}' to '{new_folder_name}'")
                            else:
                                print(f"Renamed folder fail")                      
                        else:
                            print(f"No 'title' or 'year' element found in {nfo_file_path}")
                    except ET.ParseError:
                        print(f"Failed to parse XML in file: {nfo_file_path}")
                    except Exception as e:
                        print(f"Error occurred: {e}")
                else:
                    # 如果没有与 nfo 文件同名的视频文件
                    print(f"No matching nfo file found in {folder_path}")
            else:
                # 如果不符合条件的文件夹，输出其绝对路径
                print(f"Folder does not meet criteria: {os.path.abspath(folder_path)}")

# 调用函数，传入路径A


# 用户输入路径
source_directory = input("请输入需要标准化名称的文件夹路径：")
process_folders(source_directory)
import os
import xml.etree.ElementTree as ET
import shutil

#功能说明： 扫描指定目录下所有的nfo文件，为每部电影创建单独的目录
#示例：
#指定目录下：有movie1.iso,movie1.nfo.movie1-post.jpg,movie1xxxx.xx，movie2.mkv,movie2.nfo.movie2-post.jpg,movie2xxxx.xx
#脚本处理后，创建两个文件夹"movie1（year)","movie2（year)",相关文件移动到对应的文件夹中



# 使用示例：替换为您要处理的文件夹路径
movie_folder_path = "D:\\115\\Movies\\Movies-Iso\\Part2-512s"
# movie_folder_path = "C:\\tmp-movie"


def process_movie_folder(folder_path):
    # 遍历指定路径下的所有.nfo文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.nfo'):
            nfo_file_path = os.path.join(folder_path, filename)

            try:
                # 解析.nfo文件
                tree = ET.parse(nfo_file_path)
                root = tree.getroot()

                # 提取"title"和"year"子元素的文本值
                title_elem = root.find('title')
                year_elem = root.find('year')

                if title_elem is not None and year_elem is not None:
                    B = title_elem.text
                    Y = year_elem.text
                    
                    # 重命名当前一级子文件夹
                    new_folder_name = f"{B} ({Y})"
                    # current_folder_name = os.path.basename(folder_path)
                    new_folder_path = os.path.join(folder_path, new_folder_name)

                    # 重命名文件夹
                    # if current_folder_name != new_folder_name:
                    #     os.rename(folder_path, new_folder_path)

                    # 创建新文件夹
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                    # else:
                    #     print(f"文件夹 {nfo_file_path} 已存在，请再次确认.")
                    #     continue

                    # 移动包含filename字符串的文件到新创建的文件夹中
                    for item in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item)
                        if filename[:-4] in item and os.path.isfile(item_path):  # 这里filename[:-4]去掉了.nfo后缀
                            item_path = os.path.join(folder_path, item)
                            move_folder_path = os.path.join(new_folder_path, item)
                            shutil.move(item_path, move_folder_path)

                else:
                    print(f"警告: 在文件 {nfo_file_path} 中找不到标题或年份元素.")

            except ET.ParseError:
                print(f"错误: 解析文件 {nfo_file_path} 时出错.")
            except Exception as e:
                print(f"处理文件 {nfo_file_path} 时出现错误: {e}")




# process_movie_folder("D:\\115\\Movies\\tmp")
process_movie_folder("C:\\tmp-movie")
import os
import shutil


#115网盘专用，115的同名文件夹处理策略中，拷贝/移动文件夹时，如果目标路径下已经有同名文件夹，则会重命名拷贝/移动的文件夹为 dirname(1),dirname(2)...
#扫描指定目录下文件夹，把同名的重复文件夹合并，如： dirname, dirname(1),dirname(2)
#注意事项：注意只合并文件夹目录下的文件，子文件夹不合并


def move_files_and_create_directory(source_directory, search_string):
    # 遍历指定路径下的所有一级子目录
    for entry in os.listdir(source_directory):
        full_path = os.path.join(source_directory, entry)

        # 检查是否为目录，并且目录名称中包含搜索字符串
        if os.path.isdir(full_path) and search_string in entry:
            # 创建新文件夹名称，去掉字符串B
            new_folder_name = entry.replace(search_string, '').strip()
            new_folder_path = os.path.join(source_directory, new_folder_name)

            # 创建新文件夹
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path, exist_ok=True)
                print(f"Created directory '{new_folder_path}.")
            else:
                print(f"existed directory '{new_folder_path}.")
            

            # 移动该目录下的所有文件到新创建的文件夹中
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                # 确保只移动文件而不是子目录
                # 对于windows软链接文件，os.path.isfile返回false，所以加iso判断
                if os.path.isfile(item_path) or item.endswith('.iso'):
                    move_file_path = os.path.join(new_folder_path, item)

                    # 检查目标路径中是否已存在同名文件
                    if os.path.exists(move_file_path):
                        print(f"文件 '{move_file_path}' 已存在，跳过移动。")
                    else:
                        shutil.move(item_path, move_file_path)
                        print(f"Moved '{item_path}' to '{move_file_path}'")

                    
            print(f"Created directory '{new_folder_path}' and moved files from '{full_path}'.")


            # 检查源目录是否为空，如果为空则删除
            if not os.listdir(full_path):
                os.rmdir(full_path)
                print(f"已删除空目录 '{full_path}'。")
            else:
                print(f"目录 '{full_path}' 仍有文件，未删除。")

if __name__ == "__main__":
    # 用户输入路径和字符串
    # source_directory = "D:\\115\\Movies\\Movies-Iso\\iso"
    # search_string = 

    # move_files_and_create_directory("D:\\115\\Movies\\emby-libs", "(2)")
    # move_files_and_create_directory("D:\\115\\Movies\\emby-libs", "(1)")
    move_files_and_create_directory("D:\\115\\Movies\\video", "(1)")
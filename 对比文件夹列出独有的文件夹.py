import os
import shutil

def remove_unique_subfolders(source_path, target_path):
    # 获取source_path和target_path下的一级子文件夹列表
    source_folders = set(f for f in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, f)))
    target_folders = set(f for f in os.listdir(target_path) if os.path.isdir(os.path.join(target_path, f)))

    # 找出target_path中独有的子文件夹
    unique_to_target = target_folders - source_folders

    # 删除target_path中独有的子文件夹
    for folder in unique_to_target:
        folder_path = os.path.join(target_path, folder)
        print(f"Deleting unique folder: {folder_path}")

if __name__ == "__main__":
 


    # 调用函数进行处理
    remove_unique_subfolders(r"C:\Users\wiz\Downloads\tvs", r"D:\115\预处理\预处理-剧集\lastest-tv\欧美剧130.31T 已刮削")
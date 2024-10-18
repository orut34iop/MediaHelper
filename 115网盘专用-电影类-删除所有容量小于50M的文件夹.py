#功能说明： 输入指定路径，查询该路径下的所有一级子文件夹，删除容量小于50M的目录

import os
import shutil

def delete_small_dirs(path):
    # 遍历指定路径下的所有一级子文件夹
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # 检查是否为目录
        if os.path.isdir(item_path):
            # 获取目录大小
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(item_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path)

            # 如果目录大小小于50MB，则删除该目录
            if total_size < 50 * 1024 * 1024:
                print(f"Deleting directory: {item_path} (Size: {total_size / (1024 * 1024):.2f} MB)")
                shutil.rmtree(item_path)

if __name__ == "__main__":
    # 指定需要遍历的路径
    # 用户输入路径
    target_path = input("请输入扫描路径：")
    delete_small_dirs(target_path) 
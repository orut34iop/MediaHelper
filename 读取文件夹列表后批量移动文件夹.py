import os
import shutil
import argparse

def clean_path(path):
    """清理路径字符串中的不可见字符"""
    return ''.join(c for c in path if c.isprintable())

def move_folders_from_file(text_file_path, target_folder):
    # 清理路径字符串
    text_file_path = clean_path(text_file_path)
    target_folder = clean_path(target_folder)

    # Ensure the target folder exists; create it if it doesn't.
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Read the text file line by line.
    with open(text_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        # Strip any leading/trailing whitespace characters (including '\n').
        folder_path = line.strip()
        
        # Skip empty lines or lines that don't look like valid paths.
        if not folder_path or not os.path.isdir(folder_path):
            print(f"Skipping invalid or non-existent path: {folder_path}")
            continue
        
        # Move the folder to the target directory.
        try:
            # Construct a new path in the target folder using the original folder's name.
            target_path = os.path.join(target_folder, os.path.basename(folder_path))
            shutil.move(folder_path, target_path)
            print(f"Moved: {folder_path} -> {target_path}")
        except Exception as e:
            print(f"Failed to move {folder_path}: {e}")

if __name__ == "__main__":
    input_file_path = input("请输入列表文件的完整路径: ")
    target_dir = input("请输入要移动目标目录路径: ")

    move_folders_from_file(input_file_path, target_dir)

    input("按回车键退出程序...")
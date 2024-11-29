import os
import shutil

def delete_symlinks_in_directory():
    # 获取用户输入的目录路径
    directory = input("请输入要删除符号链接文件的目录路径：").strip()

    # 遍历目录中的所有文件
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 检查是否为符号链接
            if os.path.islink(file_path):
                try:
                    # 删除符号链接
                    os.unlink(file_path)
                    print(f"已删除符号链接：{file_path}")
                except PermissionError:
                    print(f"错误：无法删除符号链接 {file_path}，权限不足。")
                except Exception as e:
                    print(f"错误：删除符号链接 {file_path} 时发生错误：{e}")

if __name__ == "__main__":
    # 设置控制台输出编码为UTF-8
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    delete_symlinks_in_directory()

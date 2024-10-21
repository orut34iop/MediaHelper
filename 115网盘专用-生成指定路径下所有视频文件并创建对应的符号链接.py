#下面是一个Python脚本，它允许用户输入指定文件的路径和目标文件夹路径，
#然后在目标文件夹中创建同名的符号链接，并检查链接是否成功创建。
#最后等待用户按回车键退出程序
import os
import sys
import ctypes

def is_admin():
    """检查当前用户是否为管理员"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"检查管理员权限时出错: {e}")
        return False

def run_as_admin():
    """请求管理员权限运行脚本"""
    if not is_admin():
        print("请求管理员权限...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit()

def create_symlink(source_file, target_folder):
    try:
        file_name = os.path.basename(source_file)
        symlink_path = os.path.join(target_folder, file_name)
        os.symlink(source_file, symlink_path)
        return symlink_path
    except FileExistsError:
        print(f"符号链接 '{symlink_path}' 已存在，跳过创建。")
    except OSError as e:
        print(f"创建符号链接失败：{e}")

def process_files(source_folder, target_folder, valid_extensions):
    files_and_links = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            # 获取完整文件路径
            source_file_path = os.path.join(root, file)
            if (any(file.lower().endswith(ext) for ext in valid_extensions) 
                    and not os.path.islink(source_file_path)):
                symlink_path = create_symlink(source_file_path, target_folder)
                if symlink_path:
                    files_and_links.append((source_file_path, symlink_path))
    return files_and_links

if __name__ == "__main__":
    run_as_admin()  # 请求管理员权限
    source_folder = input("请输入源文件夹路径：")
    target_folder = input("请输入目标文件夹路径：")

    valid_extensions = [
        '.mp4', '.mkv', '.avi', '.mov', '.rm', '.flv', '.mpg',
        '.m2ts', '.wmv', '.rmvb', '.ts', '.iso'
    ]

    results = process_files(source_folder, target_folder, valid_extensions)

    if results:
        print("\n符合要求的文件及对应创建的符号链接：")
        for source, link in results:
            print(f"源文件: {source} -> 符号链接: {link}")
    else:
        print("未找到符合要求的文件。")

    input("\n按回车键退出程序...")
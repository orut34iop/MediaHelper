#下面是一个Python脚本，它允许用户输入指定文件的路径和目标文件夹路径，
#然后在目标文件夹中创建同名的符号链接，并检查链接是否成功创建。
#最后等待用户按回车键退出程序

import os
import ctypes
import sys

def request_admin_privileges():
    """请求管理员权限"""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # 以管理员权限重新启动脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

def create_symbolic_link(file_path, target_folder):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"文件 '{file_path}' 不存在，无法创建符号链接。")
        return False

    # 获取文件名
    file_name = os.path.basename(file_path)
    
    # 定义符号链接的完整路径
    link_name = os.path.join(target_folder, file_name)  # 在目标文件夹中同名创建链接

    # 创建符号链接
    result = ctypes.windll.kernel32.CreateSymbolicLinkW(link_name, file_path, 0)

    if result:
        print(f"符号链接已创建: {link_name} -> {file_path}")
        return link_name
    else:
        print("符号链接创建失败。")
        return None

def check_symbolic_link(link_name):
    if os.path.islink(link_name):
        print(f"符号链接 '{link_name}' 存在。")
        target = os.readlink(link_name)  # 读取链接指向的目标
        print(f"符号链接指向: {target}")
    else:
        print(f"符号链接 '{link_name}' 不存在。")

# 主程序
if __name__ == "__main__":
    # 请求管理员权限
    #if not request_admin_privileges():
    #    sys.exit()

    # 用户输入文件路径和目标文件夹路径
    file_path = input("请输入文件的完整路径: ")
    target_folder = input("请输入目标文件夹的路径: ")

    # 检查目标文件夹是否存在
    if not os.path.isdir(target_folder):
        print(f"目标文件夹 '{target_folder}' 不存在，请检查路径。")
    else:
        # 创建符号链接
        link_name = create_symbolic_link(file_path, target_folder)

        # 如果链接创建成功，检查符号链接
        if link_name:
            check_symbolic_link(link_name)

    # 等待用户输入回车键再退出
    input("按回车键退出程序...")
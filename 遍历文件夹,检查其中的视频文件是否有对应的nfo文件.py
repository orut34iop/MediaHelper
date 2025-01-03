import os
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg', '.iso', '.ts', '.rmvb', '.rm'}


def check_nfo_files(folder_path):
    # 遍历指定文件夹及其子文件夹
    for root, _, files in os.walk(folder_path):
        video_files = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS]
        
        for video_file in video_files:
            base_name, _ = os.path.splitext(video_file)
            nfo_file = base_name + '.nfo'
            
            if not os.path.exists(os.path.join(root, nfo_file)):
                logging.info(f"No .nfo file found for: {os.path.join(root, video_file)}")

if __name__ == "__main__":

    folder_to_check = input("请输入检查文件夹的完整路径: ")

    # 检查提供的路径是否存在且是一个文件夹
    if not os.path.isdir(folder_to_check):
        logging.error(f"The provided path is not a valid directory: {folder_to_check}")
    else:
        check_nfo_files(folder_to_check)

    input("按回车键退出程序...")
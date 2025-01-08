import os
import logging
from pathlib import Path

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg', '.iso', '.ts', '.rmvb', '.rm'}

def find_related_videos(nfo_file_path):
    """
    对于给定的 .nfo 文件，查找相同文件夹下的同名视频文件。
    
    :param nfo_file_path: .nfo 文件的路径
    :return: 包含同名视频文件路径的列表
    """
    # 获取 .nfo 文件所在的目录和不带后缀的文件名
    nfo_dir = os.path.dirname(nfo_file_path)
    base_name = os.path.splitext(os.path.basename(nfo_file_path))[0]
    
    # 查找同名但不同后缀的视频文件
    for ext in VIDEO_EXTENSIONS:
        video_path = os.path.join(nfo_dir, base_name + ext)
        if os.path.isfile(video_path) or os.path.islink(video_path):
            return video_path
        
    return None

def check_nfo_files(folder_path):
    """
    遍历给定文件夹中的所有 .nfo 文件，并检查对应的同名视频文件。
    
    :param folder_path: 要检查的文件夹路径
    :return: 汇总查询结果的字典
    """
    # 初始化结果汇总
    results = {
        'total_nfo': 0,
        'no_video_nfo': [],
        'found_video_nfo': []
    }    

    # 使用 glob 递归查找所有的 .nfo 文件
    for nfo_path in Path(folder_path).rglob('*.nfo'):
        nfo_str_path = str(nfo_path)
        if os.path.basename(nfo_str_path) == 'tvshow.nfo':
            continue
        results['total_nfo'] += 1
        
        video_path = find_related_videos(nfo_str_path)

        if video_path:
            results['found_video_nfo'].append(nfo_str_path)
        else:
            results['no_video_nfo'].append(nfo_str_path)

    return results

def check_video_files(folder_path):
    # 初始化结果汇总
    results = {
        'total_videos': 0,
        'no_nfo_videos': [],
        'found_nfo_videos': []
    }
    
    # 遍历指定文件夹及其子文件夹
    for root, _, files in os.walk(folder_path):
        video_files = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS]
        
        for video_file in video_files:
            results['total_videos'] += 1
            base_name, _ = os.path.splitext(video_file)
            nfo_file = base_name + '.nfo'
            
            video_full_path = os.path.join(root, video_file)
            nfo_full_path = os.path.join(root, nfo_file)
            
            if not os.path.exists(nfo_full_path):
                results['no_nfo_videos'].append(video_full_path)
                #logging.info(f"No .nfo file found for: {video_full_path}")
            else:
                results['found_nfo_videos'].append(video_full_path)
                #logging.info(f"Found .nfo file for: {video_full_path}")
    
    return results


if __name__ == "__main__":
    folder_to_check = input("请输入检查文件夹的完整路径: ")

    # 检查提供的路径是否存在且是一个文件夹
    if not os.path.isdir(folder_to_check):
        logging.error(f"The provided path is not a valid directory: {folder_to_check}")
    else:
        video_check_result = check_video_files(folder_to_check)
        nfo_check_result = check_nfo_files(folder_to_check)

        logging.info(f"-------------汇总信息------------------------")
        logging.info(f"总共检查了 {video_check_result['total_videos']} 个视频文件。")
        logging.info(f"其中有 {len(video_check_result['no_nfo_videos'])} 个视频文件没有找到对应的.nfo文件：")
        for video in video_check_result['no_nfo_videos']:
            logging.info(f"没有找到 .nfo 文件的视频文件: {video}")
        logging.info(f"总共检查了 {nfo_check_result['total_nfo']} 个nfo文件。")
        logging.info(f"其中有 {len(nfo_check_result['no_video_nfo'])} 个nfo文件没有找到对应的视频文件：")
        for nfo in nfo_check_result['no_video_nfo']:
            logging.info(f"没有找到视频文件的 .nfo 文件: {nfo}")
        logging.info(f"-------------检查结束------------------------")

    logging.info("done!")
    input("按回车键退出程序...")
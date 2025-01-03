import os
import time
import logging


# 定义颜色代码
RED = '\033[91m'
RESET = '\033[0m'

class ColorFormatter(logging.Formatter):
    def format(self, record):
        # 如果日志级别是ERROR或CRITICAL，则添加红色
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            record.msg = RED + str(record.msg) + RESET
        return super().format(record)

# 配置基本的日志记录设置
logging.basicConfig(
    level=logging.DEBUG,  # 设置最低的日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 输出到控制台
    ]
)






# 定义视频文件扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg', '.iso', '.ts', '.rmvb', '.rm'}


def check_nfo_files(folder_path):
    errors = []
    video_count = 0
    # 遍历指定文件夹及其子文件夹
    for root, _, files in os.walk(folder_path):
        video_files = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS]
        video_count += len(video_files)
        
        for video_file in video_files:
            base_name, _ = os.path.splitext(video_file)
            nfo_file = base_name + '.nfo'
            
            if not os.path.exists(os.path.join(root, nfo_file)):
                error_msg = f"没有匹配的nfo : {os.path.join(root, video_file)}"
                logging.error(error_msg)
                errors.append(error_msg)
            else:
                logging.info(f"存在匹配的nfo : {os.path.join(root, video_file)}")
    
    if video_count == 0:
        error_msg = f"目录中没有找到视频文件: {folder_path}"
        logging.error(error_msg)
        errors.append(error_msg)
    
    return errors

def read_folder_list(file_path):
    """读取文本文件中的文件夹路径列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取所有行并去除空行和空白字符
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"读取文件失败: {str(e)}")
        return []

if __name__ == "__main__":

    # 获取默认的根记录器，并设置自定义格式化程序
    logger = logging.getLogger()
    handler = logger.handlers[0]  # 假设我们只使用一个处理器
    formatter = ColorFormatter(handler.formatter._fmt)
    handler.setFormatter(formatter)

    # 测试不同的日志级别
    logger.error("这是一个错误信息，应该以红色显示。")
    logger.info("这是一条普通信息，不应该改变颜色。")
    file_path = input("请输入包含文件夹路径列表的文本文件路径: ")
    
    if not os.path.isfile(file_path):
        logging.error(f"找不到文件: {file_path}")
    else:
        all_errors = []
        folder_list = read_folder_list(file_path)
        total_folders = len(folder_list)
        current_folder = 0
        
        for folder in folder_list:
            current_folder += 1
            if not os.path.isdir(folder):
                error_msg = f"进度: {current_folder}/{total_folders}, 无效的文件夹路径: {folder}"
                logging.error(error_msg)
                all_errors.append(error_msg)
                continue
                
            logging.info(f"进度: {current_folder}/{total_folders},  正在检查文件夹: {folder} ")
            time.sleep(2)  # 防止115 服务器检测
            folder_errors = check_nfo_files(folder)
            all_errors.extend(folder_errors)
        
        # 在程序结束前显示错误汇总
        if all_errors:
            logging.error("\n错误汇总:")
            for i, error in enumerate(all_errors, 1):
                logging.error(f"{i}. {error}")
            logging.error(f"\n共发现 {len(all_errors)} 个错误")

    input("按回车键退出程序...")
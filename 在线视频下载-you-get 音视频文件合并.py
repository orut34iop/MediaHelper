'''
问题： you-get 下载在线视频时会分别下载音频和视频文件， 需要合并文件操作

解决方案:
要合并由 you-get 下载的视频和音频文件，可以使用 FFmpeg 这个强大的音视频处理工具。以下是具体的步骤和方法：

1. 确保 FFmpeg 已安装并配置环境变量
首先，你需要确保你的系统中已经安装了 FFmpeg，并且将其路径添加到系统的环境变量中。
。

2. 使用 FFmpeg 合并视频和音频
如果 you-get 下载的视频和音频文件是分开的，你可以使用以下 FFmpeg 命令来合并它们：

bash
ffmpeg -i 视频文件.mp4 -i 音频文件.mp4 -vcodec copy -acodec copy 输出文件.mp4
这里的 视频文件.mp4 和 音频文件.mp4 是你下载的视频和音频文件的名称，输出文件.mp4 是你希望生成的合并后的文件名。-vcodec copy 和 -acodec copy 选项表示复制视频和音频流，不进行重新编码
。

使用 Python 脚本批量合并
批量合并多个视频和音频文件，可以使用 Python 脚本来自动化这个过程。以下是一个 Python 脚本示例，它会遍历指定目录，查找视
频文件和对应的音频文件，然后使用 FFmpeg 合并它们

使用这个脚本之前，请确保你已经安装了 FFmpeg 并且将其路径添加到了系统的环境变量中。然后，将上述代码保存为一个 Python 脚
本文件，例如 merge_video_audio.py，并在命令行中运行脚本，提供要处理的根路径作为参数：

bash
python merge_video_audio.py /path/to/your/directory
这样，脚本就会自动查找并合并指定目录下的所有视频和音频文件。

多线程处理版本

使用ThreadPoolExecutor来并行处理文件合并
将文件合并逻辑封装到单独的函数中
添加错误处理和日志记录
优化线程数量配置

代码已成功优化为多线程处理版本。主要改进：

使用ThreadPoolExecutor实现并行处理
自动根据CPU核心数优化线程数量(最多8线程)
添加了完整的错误处理和日志记录
提供了处理进度和统计信息
保持了原有功能的完整性
新版本将显著提高处理大量文件时的效率，同时提供更好的用户体验和错误处理能力。用户可以直接运行优化后的脚本，它会自动利用多线程来加速处理过程。
'''	
import os
import sys
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def merge_single_pair(root, base_name, video_file, audio_file):
    """合并单个视频音频对"""
    try:
        output_file = os.path.join(root, f"{base_name}.mp4")
        command = f'ffmpeg -i "{os.path.join(root, video_file)}" -i "{os.path.join(root, audio_file)}" -c:v copy -c:a aac -strict experimental -threads 8 "{output_file}"'
        
        logging.info(f"开始合并文件: {output_file}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # 删除源文件
            os.remove(os.path.join(root, video_file))
            os.remove(os.path.join(root, audio_file))
            logging.info(f"成功合并并删除源文件: {video_file} 和 {audio_file}")
            return True, output_file
        else:
            logging.error(f"合并失败: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        logging.error(f"处理文件时发生错误: {str(e)}")
        return False, str(e)

def merge_video_audio(directory):
    """使用多线程处理所有视频音频对"""
    # 获取CPU核心数，设置合适的线程数
    max_workers = min(os.cpu_count() or 4, 8)  # 最多8个线程
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        for root, _, files in os.walk(directory):
            video_audio_pairs = {}
            
            # 查找匹配的视频音频对
            for file in files:
                if file.endswith('.mp4'):
                    name_part = file[:-4]
                    if name_part.endswith('[00]'):
                        base_name = name_part[:-5]
                        video_audio_pairs[base_name] = video_audio_pairs.get(base_name, {})
                        video_audio_pairs[base_name]['video'] = file
                    elif name_part.endswith('[01]'):
                        base_name = name_part[:-5]
                        video_audio_pairs[base_name] = video_audio_pairs.get(base_name, {})
                        video_audio_pairs[base_name]['audio'] = file
            
            # 提交合并任务
            for base_name, files_dict in video_audio_pairs.items():
                if 'video' in files_dict and 'audio' in files_dict:
                    future = executor.submit(
                        merge_single_pair,
                        root,
                        base_name,
                        files_dict['video'],
                        files_dict['audio']
                    )
                    futures.append(future)
        
        # 等待所有任务完成并收集结果
        successful_merges = 0
        failed_merges = 0
        
        for future in as_completed(futures):
            success, result = future.result()
            if success:
                successful_merges += 1
            else:
                failed_merges += 1
        
        # 打印最终统计信息
        logging.info(f"\n合并完成统计:")
        logging.info(f"成功: {successful_merges} 个文件")
        logging.info(f"失败: {failed_merges} 个文件")

if __name__ == "__main__":
    try:
        # 获取用户输入的目录路径
        root_directory = input("请输入要合并的音视频文件的目录路径：").strip()
        
        if not os.path.isdir(root_directory):
            logging.error(f"提供的路径 '{root_directory}' 不是一个有效的目录。")
            sys.exit(1)
        
        merge_video_audio(root_directory)
        
    except KeyboardInterrupt:
        logging.info("\n用户中断操作")
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")
    finally:
        # 等待用户输入回车键再退出
        input("\n按回车键退出程序...")

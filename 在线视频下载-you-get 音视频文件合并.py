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
批量合并多个视频和音频文件，可以使用 Python 脚本来自动化这个过程。以下是一个 Python 脚本示例，它会遍历指定目录，查找视频文件和对应的音频文件，然后使用 FFmpeg 合并它们

使用这个脚本之前，请确保你已经安装了 FFmpeg 并且将其路径添加到了系统的环境变量中。然后，将上述代码保存为一个 Python 脚本文件，例如 merge_video_audio.py，并在命令行中运行脚本，提供要处理的根路径作为参数：

bash
python merge_video_audio.py /path/to/your/directory
这样，脚本就会自动查找并合并指定目录下的所有视频和音频文件。
'''
import os
import sys
import subprocess

def merge_video_audio(directory):
    for root, dirs, files in os.walk(directory):
        video_audio_pairs = {}
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
        for base_name, files in video_audio_pairs.items():
            if 'video' in files and 'audio' in files:
                video_file = files['video']
                audio_file = files['audio']
                output_file = os.path.join(root, f"{base_name}.mp4")
                command = f"ffmpeg -i \"{os.path.join(root, video_file)}\" -i \"{os.path.join(root, audio_file)}\" -c:v copy -c:a aac -strict experimental -threads 8 \"{output_file}\""
                print(f"合并文件: {output_file}")
                subprocess.call(command, shell=True)
                os.remove(os.path.join(root, video_file))
                os.remove(os.path.join(root, audio_file))
                print(f"删除文件: {video_file} 和 {audio_file}")

if __name__ == "__main__":

    # 获取用户输入的目录路径
    root_directory = input("请输入要合并的音视频文件的目录路径：").strip()
    '''
    if len(sys.argv) < 2:
        print("请提供要处理的根路径 !")
        sys.exit(1)
    root_directory = sys.argv[1]
    '''
    if not os.path.isdir(root_directory):
        print(f"提供的路径 '{root_directory}' 不是一个有效的目录。")
        sys.exit(1)
    merge_video_audio(root_directory)
    # 等待用户输入回车键再退出
    input("按回车键退出程序...")
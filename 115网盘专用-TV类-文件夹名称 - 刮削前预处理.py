import os
import shutil
import re

def process_directories(source_dir, target_base_dir):
    # 正则表达式匹配任意位置的 S 后跟数字的部分，提取前面的字符串
    pattern = re.compile(r'(.*?)(S\d{1,2})', re.IGNORECASE)
    
    # 遍历源目录下的所有子目录
    for item in os.listdir(source_dir):
        full_path = os.path.join(source_dir, item)
        
        # 确保是目录
        if os.path.isdir(full_path):
            # 使用正则表达式匹配
            match = pattern.search(item)
            if match:
                prefix = match.group(1)
                
                # 如果前缀为空，跳过该目录
                if not prefix:
                    print(f"警告：目录名 {item} 的前缀为空，跳过。")
                    continue
                
                # 构建目标目录路径
                new_dir_name = prefix
                target_dir = os.path.join(target_base_dir, new_dir_name)
                
                # 创建目标目录（如果不存在）
                os.makedirs(target_dir, exist_ok=True)
                
                # 移动目录到目标位置
                try:
                    shutil.move(full_path, target_dir)
                    print(f"成功移动目录：{item} -> {target_dir}")
                except Exception as e:
                    print(f"移动目录 {item} 时出错：{e}")
            else:
                print(f"目录名 {item} 未匹配到 S+数字 模式，跳过。")
        else:
            print(f"{item} 是文件，跳过。")

if __name__ == "__main__":
    # 获取用户输入的源目录和目标目录
    source_directory = input("请输入源目录路径：")
    target_directory = source_directory
    
    # 确保源目录存在
    if not os.path.exists(source_directory):
        print(f"源目录 {source_directory} 不存在，请检查路径。")
    else:
        # 执行目录处理
        process_directories(source_directory, target_directory)
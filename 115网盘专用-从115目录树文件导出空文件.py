#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从115网盘导出的目录树文件创建空文件结构
用途：保持目录结构，但文件内容为空，用于测试或结构验证
"""

import os
import re
import shutil
import sys
from typing import List, Tuple

# 设置标准输出编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

def replace_special_chars(path: str) -> str:
    """
    替换路径中的特殊字符
    Args:
        path: 原始路径
    Returns:
        处理后的路径
    """
    if '*' in path:
        new_path = path.replace('*', 's')
        print(f'Replace special chars: {path} -> {new_path}')
        return new_path
    return path

def read_file_with_encodings(file_path: str) -> List[str]:
    """
    尝试使用不同的编码读取文件
    Args:
        file_path: 文件路径
    Returns:
        文件内容行列表
    Raises:
        UnicodeDecodeError: 当所有编码都无法正确读取文件时
    """
    encodings = ['utf-8', 'gbk', 'ansi', 'mbcs', 'gb2312']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError(f"无法使用以下编码读取文件: {encodings}")

def parse_lines_to_tuples(file_path: str) -> List[Tuple[int, str]]:
    """
    解析文件内容为层级和名称的元组列表
    Args:
        file_path: 要解析的文件路径
    Returns:
        包含(层级,名称)元组的列表
    """
    tuples_list = []
    try:
        lines = read_file_with_encodings(file_path)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
        return []
    
    for line in lines:
        line = line.strip()
        level = line.count('|')
        if line.startswith('|——'):
            name = line[3:].strip()  # 修复拼写错误
        elif line.startswith('| |-'):
            name = line[4:].strip()
        elif line.startswith('| | |-'):
            name = line[6:].strip()
        elif line.startswith('| | | |-'):
            name = line[8:].strip()
        elif line.startswith('| | | | |-'):
            name = line[10:].strip()
        elif line.startswith('| | | | | |-'):
            name = line[12:].strip()
        elif line.startswith('| | | | | | |-'):
            name = line[14:].strip()
        elif line.startswith('| | | | | | | |-'):
            name = line[16:].strip()
        elif line.startswith('| | | | | | | | |-'):
            name = line[18:].strip()
        elif line.startswith('| | | | | | | | | |-'):
            name = line[20:].strip()
        else:
            continue
        tuples_list.append((level, name))
    
    return tuples_list

def create_empty_files_from_list(file_path: str, tmp_dir: str) -> None:
    """
    根据目录树文件创建空文件结构
    Args:
        file_path: 目录树文件路径
        tmp_dir: 输出目录路径
    """
    # 清空目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    
    file_items = parse_lines_to_tuples(file_path)
    current_dir = tmp_dir
    pre_level = 1 # init
    pre_item_type = '' # init
    inogre_level = 0 # init
    for item in file_items:
        level, name = item

        if 'Bagman.2024.WEB-DL.1080p.X264' in name:
            pass
        
        empty_file_path = '' # RESET

        try:
            # 如果前面有异常错误的文件夹,跳过出错的目录下所有的子目录和文件
            if inogre_level > 0 and level > inogre_level: 
                print(f'ingogre : {name}')
                continue
            else:
                inogre_level = 0

            if level == 1:
                current_dir = os.path.join(tmp_dir, name)
                current_dir = replace_special_chars(current_dir)
                pre_level = level
                pre_item_type = 'dir'
                os.makedirs(current_dir, exist_ok=True)
            else:
                if not re.match(r'.*\.[a-zA-Z0-9]{2,4}$', name):  #名称尾部不是'.xxx',表示2或者3或者4个数字或大小写字母,判定为目录
                    '''
                    ########对于 pre_item_type == 'dir' 的情况
                    子一级  level == pre_level + 1
                    | | | |-folder1
                    | | | | |-folder2

                    同级    level == pre_level
                    | | | |-folder1
                    | | | |-folder2

                    上多级  level < pre_level
                    | | | |-folder1
                    | | |-folder2

                    ########对于 pre_item_type == 'file' 的情况
                    子一级  level == pre_level + 1
                    | | | |-file
                    | | | | |-folder
                    这种情况不可能出现, 错误退出

                    同级    level == pre_level
                    | | | |-file
                    | | | |-folder

                    上多级  level < pre_level
                    | | | |-file
                    | | |-folder
                    '''

                    if pre_item_type == 'dir':  # 上一个是文件,回到上级目录
                        if level == pre_level + 1:  # 子目录
                            current_dir = os.path.join(current_dir, name)
                        elif level == pre_level:  # 同级目录
                            current_dir = os.path.dirname(current_dir)
                            current_dir = os.path.join(current_dir, name) 
                        elif level < pre_level:  # 上级目录
                            for _ in range(pre_level - level):
                                current_dir = os.path.dirname(current_dir)
                            current_dir = os.path.join(os.path.dirname(current_dir), name)
                        else:  # 致命错误
                            print(f'level error! pls check: {name}')
                            return
                    elif pre_item_type == 'file':  # 上一个操作的文件
                        if level == pre_level + 1:  # 子目录
                            print(f'level error! pls check: {name}')
                            return
                        elif level == pre_level:  # 同级
                            current_dir = os.path.join(current_dir, name) 
                        elif level < pre_level:  # 上级目录
                            for _ in range(pre_level - level):
                                current_dir = os.path.dirname(current_dir)
                            current_dir = os.path.join(current_dir, name)
                        else:  # 致命错误
                            print(f'level error! pls check: {name}')
                            return
                    elif pre_item_type == '': # 初始状态
                        pass
                    else:  # 致命错误
                        print(f'level error! pls check: {name}')
                        return


                    try:
                        current_dir = replace_special_chars(current_dir)
                        os.makedirs(current_dir, exist_ok=True)
                        pre_level = level
                        pre_item_type = 'dir'
                        print(f'{pre_level} -- {level} dir  :  {current_dir}')
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                        inogre_level = level
                        return
                    
                else:  # 文件
                    '''
                    ########对于 pre_item_type == 'dir' 的情况
                    子一级  level == pre_level + 1
                    | | | |-folder1
                    | | | | |-file

                    同级    level == pre_level
                    | | | |-folder1
                    | | | |-file

                    上多级  level < pre_level
                    | | | |-folder1
                    | | |-file

                    ########对于 pre_item_type == 'file' 的情况
                    子一级  level == pre_level + 1
                    | | | |-file1
                    | | | | |-file2
                    这种情况不可能出现, 错误退出

                    同级    level == pre_level
                    | | | |-file1
                    | | | |-file2

                    上多级  level < pre_level
                    | | | |-file1
                    | | |-file2
                    '''       
                    if pre_item_type == 'dir':  # 上一个是目录             
                        if level == pre_level + 1:  # 目录中的文件
                            empty_file_path = os.path.join(current_dir, name)
                        elif level == pre_level:  # 同级目录的文件
                            current_dir = os.path.dirname(current_dir)
                            empty_file_path = os.path.join(current_dir, name)
                        elif level < pre_level:  # 上级目录(可能多级)的文件 !!!!!!!!!!!需要测试检查 !!!!!!!!!!!
                            for _ in range(pre_level - level):
                                current_dir = os.path.dirname(current_dir)
                            empty_file_path = os.path.join(current_dir, name)           
                        else:  # 致命错误
                            print(f'level error! pls check: {name}')
                            return
                    elif pre_item_type == 'file':  # 上一个操作的文件      
                        if level == pre_level + 1:  # 不可能出现的情况
                            print(f'level error! pls check: {name}')
                            return
                        elif level == pre_level:  # 同级目录的文件
                            empty_file_path = os.path.join(current_dir, name)
                        elif level < pre_level:  # 上级目录(可能多级)的文件!!!!!!!!!!!需要测试检查 !!!!!!!!!!!
                            for _ in range(pre_level - level):
                                current_dir = os.path.dirname(current_dir)
                            empty_file_path = os.path.join(current_dir, name)                         
                        else:  # 致命错误
                            print(f'level error! pls check: {name}')
                            return
                    elif pre_item_type == '':
                        pass
                    else:  # 致命错误
                        print(f'level error! pls check: {name}')
                        return
                    

                    try:
                        empty_file_path = replace_special_chars(empty_file_path)
                        open(empty_file_path, 'a').close()
                        pre_level = level
                        pre_item_type = 'file'
                        print(f'{pre_level} -- {level} file :  {empty_file_path}')
                        continue
                    except Exception as e:
                        print(f"Error creating file: {e}")
                        inogre_level = level
                        return                   

            # 检查 current_dir 是否以 tmp_dir 开头
            if 'tmdbid-1118343' in current_dir:
                pass
                # print(f'Error: current_dir {current_dir} is not within {tmp_dir}')


        except Exception as e:
            print(f"Error processing {name}: {e}")
            current_dir = os.path.dirname(current_dir)  # 回到上一级目录
            print(f'Error , set current_dir: {current_dir}')
            inogre_level = level

if __name__ == "__main__":

    input_file_path = input("请输入文件的完整路径: ")
    tmp_dir = input("请输入要保存空文件的目录路径: ")
    create_empty_files_from_list(input_file_path, tmp_dir)
    '''
    # 使用示例路径进行测试
    create_empty_files_from_list(
        r'C:\Users\wiz\Downloads\预处理-影片20241231203309_目录树.txt', 
        r'C:\tmp_115'
    )
    '''    
    input("按回车键退出程序...")

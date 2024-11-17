import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import pyperclip  # 用来操作剪贴板

import re

# 创建主窗口
root = TkinterDnD.Tk()

# 设置窗口大小
root.geometry('800x400')
root.title('文件夹拖拽示例')

# 创建一个Frame用于包含所有控件，使其可以自适应大小
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# 第一行输入框（可以拖拽文件夹）
entry = tk.Entry(frame, width=200)
entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

# 第二行输出框（显示文件夹路径）
output_text = tk.Text(frame, width=200, height=10)
output_text.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# 导出按钮
def export_to_clipboard():
    # 获取文本框中的内容
    content = output_text.get(1.0, tk.END).strip()
    
    if content:  # 如果内容不为空
        pyperclip.copy(content)  # 将内容拷贝到剪贴板
        print("内容已复制到剪贴板")
    else:
        print("输出框为空，无法导出")

export_button = tk.Button(frame, text="导出", command=export_to_clipboard)
export_button.grid(row=2, column=0, padx=10, pady=10)

def scan_string(input_string):
    result = []
    i = 0
    while i < len(input_string):
        # 如果字符是'{'
        if input_string[i] == '{':
            # 找到匹配的'}'
            i += 1
            start = i
            while i < len(input_string) and input_string[i] != '}':
                i += 1
            # 保存 '{}' 之间的内容
            result.append(input_string[start:i])
            #跳过 '}' 
            i += 1
        # 如果字符不是'{'
        else:
            start = i
            while (i < len(input_string) and input_string[i] != ' ' ):
                i += 1
            # 保存空格或'{''之前的内容
            result.append(input_string[start:i])
        
        # 跳过空格
        if i < len(input_string) and input_string[i] == ' ':
            i += 1
    
    return result


# 拖拽到输入框的回调函数
def on_drop(event):


    """
    event.data 字符串格式如下:
    规律： 如果文件路径中有空格，就用{}包起来，否则直接用空格区分
    '{C:/Users/wiz/Documents/华为电脑管家13.0.6.360 雷蛇已验证AI字幕} C:/Users/wiz/Documents/HonorSuite {C:/Users/wiz/Documents/Virtual Machines} C:/Users/wiz/Documents/华为电脑管家'
    'C:/Users/wiz/Documents/华为电脑管家 C:/Users/wiz/Documents/HonorSuite {C:/Users/wiz/Documents/Virtual Machines}'
    """
    """
    data_start = re.sub(r'^\{', '', event.data, count=1)
    # 使用 re.sub() 替换 '} ' 和 ' {' 成换行符
    data_mid= re.sub(r'\}\s|\s\{', '\n', data_start)
    data_end = re.sub(r'\}', '', data_mid, count=1)
    # 获取拖拽的文件夹路径
    folder_paths = data_end.split('\n')  # 拖拽的路径数据，可能会是多个文件夹路径
    """

    folder_paths = scan_string(event.data)

    # 获取文件夹的名称
    folder_names = [os.path.basename(folder) for folder in folder_paths]
    
    # 获取当前输入框中的内容
    current_text = entry.get()
    
    # 如果当前输入框有内容，添加分号和空格
    if current_text:
        current_text += "; "
    
    # 更新输入框中的内容，将新的文件夹名称追加到原有内容后面
    entry.delete(0, tk.END)
    entry.insert(tk.END, current_text + '; '.join(folder_names))  # 显示文件夹名称，用分号分隔
    
    # 获取当前输出框中的内容
    current_output_text = output_text.get(1.0, tk.END)
    
    # 如果输出框已有内容，添加换行
    if current_output_text.strip():
        current_output_text += "\n"
    
    # 更新输出框，追加文件夹的绝对路径
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, current_output_text + '\n'.join(folder_paths) + '\n')  # 将文件夹路径按行插入输出框

# 绑定拖拽事件到输入框
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', on_drop)

# 运行主循环
root.mainloop()
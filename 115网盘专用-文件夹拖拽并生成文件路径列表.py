"""
GPT4 代码生成提示

需求说明：

我们需要开发一个Windows桌面应用，要求如下：

应用窗口设置：

窗口大小：600x300。
输入框（第一行）：

用户可以将一个或多个文件夹从文件管理器拖拽到此输入框中。
每次拖拽文件夹时：
仅显示文件夹的名称（去除路径），且各个文件夹名称用分号（;）分隔。
如果已经有文件夹名称，新的文件夹名称应以追加的方式添加到现有内容末尾。
输出框（第二行）：

每次拖拽文件夹时，自动更新并显示拖拽的文件夹的完整路径（每个路径占一行）。
如果已有内容，新的文件夹路径应追加到现有内容后面。
导出按钮：

点击按钮时，第二行的文本框内容（即文件夹路径列表）应复制到系统剪贴板。
功能细节：

拖拽操作：

用户可以通过拖拽文件夹（一个或多个）到输入框，实现文件夹路径的更新。
路径格式：

输入框只显示文件夹名称，并用分号分隔。
输出框显示文件夹的完整路径，每个路径占一行。
追加模式：

每次拖拽时，输入框和输出框中的内容都应以追加模式更新。
剪贴板功能：

点击“导出”按钮时，输出框中的路径列表将被复制到剪贴板。
目标：

通过该应用，用户能够方便地查看和操作拖拽进来的文件夹路径，并能够轻松地将路径信息复制到剪贴板。

这种描述简洁明了，明确了每个功能点，同时对开发人员的理解和实现方式更为友好。
"""

import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import pyperclip  # 用来操作剪贴板

import re

# 创建主窗口
root = TkinterDnD.Tk()

# 设置窗口大小
root.geometry('216x300')
root.title('文件夹拖拽示例')

# 第一行输入框（可以拖拽文件夹）
entry = tk.Entry(root, width=200)
entry.grid(row=0, column=0, padx=10, pady=10)

# 第二行输出框（显示文件夹路径）
output_text = tk.Text(root, width=200, height=10)
output_text.grid(row=1, column=0, padx=10, pady=10)

# 导出按钮
def export_to_clipboard():
    # 获取文本框中的内容
    content = output_text.get(1.0, tk.END).strip()
    
    if content:  # 如果内容不为空
        pyperclip.copy(content)  # 将内容拷贝到剪贴板
        print("内容已复制到剪贴板")
    else:
        print("输出框为空，无法导出")

export_button = tk.Button(root, text="导出", command=export_to_clipboard)
export_button.grid(row=2, column=0, pady=10)

# 拖拽到输入框的回调函数
def on_drop(event):

    new_data1 = re.sub(r'^\{', '', event.data, count=1)
    # 使用 re.sub() 替换 '} ' 和 ' {' 成换行符
    new_data2 = re.sub(r'\}\s|\s\{', '\n', new_data1)
    # 获取拖拽的文件夹路径
    folder_paths = new_data2.split('\n')  # 拖拽的路径数据，可能会是多个文件夹路径
    
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

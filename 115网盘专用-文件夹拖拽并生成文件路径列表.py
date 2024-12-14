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


115网盘文件夹路径生成器

功能说明：
将文件夹拖拽到输入框，自动生成文件夹路径列表。

改进说明：
1. 界面优化：
   - 添加了清晰的使用说明标签
   - 优化了按钮布局和文字说明
   - 添加了清空功能按钮
   - 改进了界面布局结构

2. 用户体验提升：
   - 使用消息框替代控制台输出
   - 提供更友好的操作反馈
   - 改进了剪贴板操作的提示
   - 添加了重复路径检测，自动忽略重复项

3. 错误处理：
   - 添加了异常捕获机制
   - 提供清晰的错误提示
   - 改进了空内容处理

4. 代码改进：
   - 优化了代码结构和组织
   - 添加了中文注释说明
   - 保持了代码的简洁性
"""

import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import pyperclip
from tkinter import messagebox

# 创建主窗口
root = TkinterDnD.Tk()
root.geometry('800x400')
root.title('115网盘文件夹路径生成器')

# 创建主框架
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# 添加使用说明标签
help_text = "使用说明：将文件夹拖拽到输入框即可生成路径列表（自动忽略重复路径）"
help_label = tk.Label(frame, text=help_text, fg="gray")
help_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')

# 输入框（可以拖拽文件夹）
entry = tk.Entry(frame, width=200)
entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

# 输出框（显示文件夹路径）
output_text = tk.Text(frame, width=200, height=10)
output_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

def export_to_clipboard():
    """导出内容到剪贴板，使用消息框提供操作反馈"""
    try:
        content = output_text.get(1.0, tk.END).strip()
        if content:
            pyperclip.copy(content)
            messagebox.showinfo("成功", "内容已复制到剪贴板")
        else:
            messagebox.showwarning("提示", "输出框为空，无法导出")
    except Exception as e:
        messagebox.showerror("错误", f"复制到剪贴板时出错：{str(e)}")

def clear_all():
    """清空所有输入和输出内容"""
    entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)

def scan_string(input_string):
    """
    解析拖拽数据中的路径
    处理带空格的路径（使用{}包围）和不带空格的路径
    """
    result = []
    i = 0
    while i < len(input_string):
        if input_string[i] == '{':
            i += 1
            start = i
            while i < len(input_string) and input_string[i] != '}':
                i += 1
            result.append(input_string[start:i])
            i += 1
        else:
            start = i
            while i < len(input_string) and input_string[i] != ' ':
                i += 1
            result.append(input_string[start:i])
        
        if i < len(input_string) and input_string[i] == ' ':
            i += 1
    
    return [path for path in result if path.strip()]

def get_existing_paths():
    """获取输出框中已存在的路径列表"""
    content = output_text.get(1.0, tk.END).strip()
    if content:
        return set(content.split('\n'))
    return set()

def on_drop(event):
    """
    处理文件夹拖拽事件
    包含错误处理和用户反馈
    自动检测并忽略重复的路径
    """
    """
    event.data 字符串格式如下:
    规律： 如果文件路径中有空格，就用{}包起来，否则直接用空格区分
    '{C:/Users/wiz/Documents/华为电脑管家13.0.6.360 雷蛇已验证AI字幕} C:/Users/wiz/Documents/HonorSuite {C:/Users/wiz/Documents/Virtual Machines} C:/Users/wiz/Documents/华为电脑管家'
    'C:/Users/wiz/Documents/华为电脑管家 C:/Users/wiz/Documents/HonorSuite {C:/Users/wiz/Documents/Virtual Machines}'
    """

    try:
        # 获取已存在的路径
        existing_paths = get_existing_paths()
        
        # 解析拖拽的路径
        folder_paths = scan_string(event.data)
        
        # 过滤掉重复的路径
        new_paths = [path for path in folder_paths if path not in existing_paths]
        
        if not new_paths:
            messagebox.showinfo("提示", "所有拖入的路径都已存在，已自动忽略")
            return
            
        # 获取新路径的文件夹名称
        folder_names = [os.path.basename(folder) for folder in new_paths]
        
        # 更新输入框
        current_text = entry.get()
        if current_text:
            current_text += "; "
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_text + '; '.join(folder_names))
        
        # 更新输出框，只添加新的路径
        current_output = output_text.get(1.0, tk.END).strip()
        if current_output:
            output_text.insert(tk.END, '\n' + '\n'.join(new_paths) + '\n')
        else:
            output_text.insert(tk.END, '\n'.join(new_paths) + '\n')
        
    except Exception as e:
        messagebox.showerror("错误", f"处理拖拽数据时出错：{str(e)}")

# 创建按钮框架
button_frame = tk.Frame(frame)
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

# 添加按钮
export_button = tk.Button(button_frame, text="复制到剪贴板", command=export_to_clipboard)
export_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="清空内容", command=clear_all)
clear_button.pack(side=tk.LEFT, padx=5)

# 配置网格权重
frame.grid_columnconfigure(0, weight=1)

# 绑定拖拽事件
entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', on_drop)

# 运行主循环
root.mainloop()

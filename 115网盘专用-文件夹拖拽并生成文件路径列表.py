import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import pyperclip
from tkinter import messagebox, ttk, filedialog
import configparser

def validate_inputs():
    """验证所有输入是否为空"""
    validations = [
        (source_entry.get().strip(), "链接文件夹不能为空"),
        (target_entry.get().strip(), "目标文件夹不能为空"),
        (thread_spinbox.get().strip(), "同步线程数不能为空"),
        (soft_link_entry.get().strip(), "软链接后缀不能为空"),
        (meta_entry.get().strip(), "元数据后缀不能为空")
    ]
    
    for value, message in validations:
        if not value:
            messagebox.showwarning("验证失败", message)
            return False
    return True

def save_config():
    """保存配置到config.ini文件"""
    if not validate_inputs():
        return False
        
    config = configparser.ConfigParser()
    config['Settings'] = {
        'source_folder': source_entry.get().strip(),
        'target_folder': target_entry.get().strip(),
        'thread_count': thread_spinbox.get().strip(),
        'soft_link_extensions': soft_link_entry.get().strip(),
        'metadata_extensions': meta_entry.get().strip(),
        'path_list': output_text.get(1.0, tk.END).strip()  # 保存文本区域内容
    }
    
    try:
        with open('config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        messagebox.showinfo("成功", "配置已保存到config.ini")
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存配置文件时出错：{str(e)}")
        return False

def load_config():
    """从config.ini文件加载配置"""
    if not os.path.exists('config.ini'):
        return
        
    config = configparser.ConfigParser()
    try:
        config.read('config.ini', encoding='utf-8')
        if 'Settings' in config:
            source_entry.delete(0, tk.END)
            source_entry.insert(0, config['Settings'].get('source_folder', ''))
            
            target_entry.delete(0, tk.END)
            target_entry.insert(0, config['Settings'].get('target_folder', ''))
            
            thread_spinbox.delete(0, tk.END)
            thread_spinbox.insert(0, config['Settings'].get('thread_count', '5'))
            
            soft_link_entry.delete(0, tk.END)
            soft_link_entry.insert(0, config['Settings'].get('soft_link_extensions', 
                '.mkv;.iso;.ts;.mp4;.avi;.rmvb;.wmv;.m2ts;.mpg;.flv;.rm'))
            
            meta_entry.delete(0, tk.END)
            meta_entry.insert(0, config['Settings'].get('metadata_extensions',
                '.nfo;.jpg;.png;.svg;.ass;.srt;.sup'))
                
            # 加载文本区域内容
            output_text.delete(1.0, tk.END)
            path_list = config['Settings'].get('path_list', '')
            if path_list:
                output_text.insert(tk.END, path_list)
    except Exception as e:
        messagebox.showerror("错误", f"加载配置文件时出错：{str(e)}")

def on_sync_all():
    """一键全同步按钮点击事件"""
    if save_config():
        # 这里可以添加其他同步相关的代码
        pass

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
    source_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)

def browse_folder(entry):
    """浏览文件夹"""
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0, tk.END)
        entry.insert(0, folder)

def scan_string(input_string):
    """解析拖拽数据中的路径"""
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

def on_source_drop(event):
    """处理源文件夹拖拽事件"""
    try:
        existing_paths = get_existing_paths()
        folder_paths = scan_string(event.data)
        new_paths = [path for path in folder_paths if path not in existing_paths]
        
        if not new_paths:
            messagebox.showinfo("提示", "所有拖入的路径都已存在，已自动忽略")
            return
            
        folder_names = [os.path.basename(folder) for folder in new_paths]
        
        current_text = source_entry.get()
        if current_text:
            current_text += "; "
        source_entry.delete(0, tk.END)
        source_entry.insert(tk.END, current_text + '; '.join(folder_names))
        
        current_output = output_text.get(1.0, tk.END).strip()
        if current_output:
            output_text.insert(tk.END, '\n' + '\n'.join(new_paths))
        else:
            output_text.insert(tk.END, '\n'.join(new_paths))
        
    except Exception as e:
        messagebox.showerror("错误", f"处理拖拽数据时出错：{str(e)}")

def on_target_drop(event):
    """处理目标文件夹拖拽事件"""
    try:
        folder_paths = scan_string(event.data)
        if len(folder_paths) > 1:
            messagebox.showwarning("提示", "目标文件夹只能拖入单个文件夹")
            return
        
        if folder_paths:
            folder_path = folder_paths[0]
            if os.path.isdir(folder_path):
                target_entry.delete(0, tk.END)
                target_entry.insert(0, os.path.abspath(folder_path))
            else:
                messagebox.showwarning("提示", "请拖入文件夹而不是文件")
        
    except Exception as e:
        messagebox.showerror("错误", f"处理拖拽数据时出错：{str(e)}")

# 创建主窗口
root = TkinterDnD.Tk()
root.title("115网盘文件共路径生成器")
root.geometry("800x600")

# 创建主框架
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# 使用说明
help_text = "使用说明: 将文件夹拖拽到输入框即可生成路径列表 (自动忽略重复路径)"
help_label = ttk.Label(frame, text=help_text, foreground="gray")
help_label.pack(fill=tk.X, pady=(0, 10))

# 主文本区域（显示路径）
text_frame = ttk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)
output_text = tk.Text(text_frame, height=15)
output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# 链接文件夹区域
source_frame = ttk.Frame(frame)
source_frame.pack(fill=tk.X, pady=2)
ttk.Label(source_frame, text="链接文件夹").pack(side=tk.LEFT)
source_entry = ttk.Entry(source_frame)
source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Button(source_frame, text="浏览", command=lambda: browse_folder(source_entry)).pack(side=tk.RIGHT)

# 目标文件夹区域
target_frame = ttk.Frame(frame)
target_frame.pack(fill=tk.X, pady=2)
ttk.Label(target_frame, text="目标文件夹").pack(side=tk.LEFT)
target_entry = ttk.Entry(target_frame)
target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Button(target_frame, text="浏览", command=lambda: browse_folder(target_entry)).pack(side=tk.RIGHT)

# 同步线程数
thread_frame = ttk.Frame(frame)
thread_frame.pack(fill=tk.X, pady=2)
ttk.Label(thread_frame, text="同步线程数:").pack(side=tk.LEFT)
thread_spinbox = ttk.Spinbox(thread_frame, from_=1, to=32, width=10)
thread_spinbox.set(5)
thread_spinbox.pack(side=tk.LEFT, padx=5)

# 软链接后缀
soft_link_frame = ttk.Frame(frame)
soft_link_frame.pack(fill=tk.X, pady=2)
ttk.Label(soft_link_frame, text="软链接后缀:").pack(side=tk.LEFT)
soft_link_entry = ttk.Entry(soft_link_frame)
soft_link_entry.insert(0, ".mkv;.iso;.ts;.mp4;.avi;.rmvb;.wmv;.m2ts;.mpg;.flv;.rm")
soft_link_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Label(soft_link_frame, text="以;隔开").pack(side=tk.RIGHT)

# 元数据后缀
meta_frame = ttk.Frame(frame)
meta_frame.pack(fill=tk.X, pady=2)
ttk.Label(meta_frame, text="元数据后缀:").pack(side=tk.LEFT)
meta_entry = ttk.Entry(meta_frame)
meta_entry.insert(0, ".nfo;.jpg;.png;.svg;.ass;.srt;.sup")
meta_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Label(meta_frame, text="以;隔开").pack(side=tk.RIGHT)

# 开始同步区域
sync_frame = ttk.LabelFrame(frame, text="开始同步", padding=5)
sync_frame.pack(fill=tk.X)

# 按钮组
button_frame = ttk.Frame(sync_frame)
button_frame.pack(fill=tk.X, pady=5)

buttons = [
    ("一键全同步", on_sync_all),
    ("创建软链接", None),
    ("下载元数据", None),
    ("复制到剪贴板", export_to_clipboard),
    ("清空文件夹列表", clear_all)
]

for btn_text, cmd in buttons:
    btn = ttk.Button(button_frame, text=btn_text, command=cmd)
    btn.pack(side=tk.LEFT, padx=2)

# 绑定拖拽事件
source_entry.drop_target_register(DND_FILES)
source_entry.dnd_bind('<<Drop>>', on_source_drop)

target_entry.drop_target_register(DND_FILES)
target_entry.dnd_bind('<<Drop>>', on_target_drop)

# 加载配置
load_config()

# 运行主循环
root.mainloop()

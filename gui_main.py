#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于ddddocr的图形界面验证码识别程序
支持图片上传、预览和识别结果展示
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import ddddocr
import os
from pathlib import Path

class CaptchaRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("验证码识别工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 当前图片路径
        self.current_image_path = None
        self.current_image = None
        self.photo = None
        
        # 初始化识别器
        try:
            self.ocr = ddddocr.DdddOcr(show_ad=False)
        except Exception as e:
            messagebox.showerror("错误", f"初始化识别器失败：{str(e)}")
            self.ocr = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="验证码识别工具", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="图片选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="图片路径:").grid(row=0, column=0, sticky=tk.W)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(file_frame, textvariable=self.path_var, state="readonly")
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        
        self.browse_btn = ttk.Button(file_frame, text="选择图片", command=self.browse_image)
        self.browse_btn.grid(row=0, column=2, padx=(5, 0))
        
        # 图片预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="图片预览", padding="10")
        preview_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = ttk.Label(preview_frame, text="请选择图片进行预览", 
                                     background="white", anchor=tk.CENTER)
        self.preview_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 识别按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        self.recognize_btn = ttk.Button(button_frame, text="识别验证码", 
                                       command=self.recognize_captcha, state="disabled")
        self.recognize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="清空", command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT)
        
        # 结果输出区域
        result_frame = ttk.LabelFrame(main_frame, text="识别结果", padding="10")
        result_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def browse_image(self):
        """选择图片文件"""
        file_types = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择验证码图片",
            filetypes=file_types
        )
        
        if filename:
            self.load_image(filename)
    
    def load_image(self, image_path):
        """加载并预览图片"""
        try:
            # 验证文件格式
            valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
            file_ext = Path(image_path).suffix.lower()
            if file_ext not in valid_extensions:
                messagebox.showerror("错误", f"不支持的文件格式：{file_ext}")
                return
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                messagebox.showerror("错误", "文件不存在")
                return
            
            self.current_image_path = image_path
            self.path_var.set(image_path)
            
            # 加载图片
            self.current_image = Image.open(image_path)
            
            # 获取预览区域尺寸
            preview_width = 400
            preview_height = 300
            
            # 计算缩放比例，保持宽高比
            img_width, img_height = self.current_image.size
            
            # 计算缩放比例，让图片在预览区域内尽可能大且保持比例
            width_ratio = preview_width / img_width
            height_ratio = preview_height / img_height
            scale_ratio = min(width_ratio, height_ratio, 2.0)  # 限制最大放大倍数为2倍
            
            # 计算新尺寸
            new_width = int(img_width * scale_ratio)
            new_height = int(img_height * scale_ratio)
            
            # 调整图片大小
            preview_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 创建居中显示的图片
            self.photo = ImageTk.PhotoImage(preview_image)
            
            # 配置标签以居中显示图片
            self.preview_label.configure(
                image=self.photo, 
                text="",
                compound=tk.CENTER,  # 图片居中
                anchor=tk.CENTER    # 内容居中
            )
            
            # 启用识别按钮
            self.recognize_btn.configure(state="normal")
            self.status_var.set(f"已加载图片: {os.path.basename(image_path)} (尺寸: {img_width}x{img_height}, 预览: {new_width}x{new_height})")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败：{str(e)}")
            self.status_var.set("加载图片失败")
    
    def recognize_captcha(self):
        """识别验证码"""
        if not self.current_image_path or not self.ocr:
            return
        
        try:
            self.status_var.set("正在识别验证码...")
            self.recognize_btn.configure(state="disabled")
            self.root.update()
            
            # 读取图片文件
            with open(self.current_image_path, 'rb') as f:
                image_bytes = f.read()
            
            # 识别验证码
            result = self.ocr.classification(image_bytes)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"图片路径: {self.current_image_path}\n")
            self.result_text.insert(tk.END, f"识别结果: {result}\n")
            self.result_text.insert(tk.END, f"识别时间: {self.get_current_time()}\n")
            
            self.status_var.set("识别完成")
            
        except Exception as e:
            error_msg = f"识别过程中出现错误：{str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_msg)
            self.status_var.set("识别失败")
            messagebox.showerror("错误", error_msg)
        finally:
            self.recognize_btn.configure(state="normal")
    
    def clear_all(self):
        """清空所有内容"""
        self.current_image_path = None
        self.current_image = None
        self.photo = None
        
        self.path_var.set("")
        self.preview_label.configure(image=None, text="请选择图片进行预览")
        self.result_text.delete(1.0, tk.END)
        self.recognize_btn.configure(state="disabled")
        self.status_var.set("已清空")
    
    def get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """主函数"""
    root = tk.Tk()
    app = CaptchaRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包配置文件 - 用于将Python程序打包为exe文件
支持64位和32位版本
"""

import os
import sys
from cx_Freeze import setup, Executable

# 基础配置
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 使用GUI界面，不显示控制台窗口

# 包含的文件
include_files = []

# 排除的模块（减少打包体积）
excludes = ["tkinter.test", "unittest", "email", "http", "xml", 
           "pydoc", "doctest", "multiprocessing", "bz2", 
           "lzma", "ssl", "sqlite3"]

# 包含的模块
includes = ["tkinter", "PIL", "ddddocr", "urllib", "urllib.parse", "pathlib"]

# 构建选项 - cx_Freeze的正确配置格式
build_exe_options = {
    "includes": includes,
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 0,  # 完全关闭优化以避免导入问题
    "silent": True,  # 静默模式
}

# 程序描述
setup(
    name="CaptchaRecognizer",
    version="1.0.0",
    description="基于ddddocr的验证码识别工具",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "gui_main.py",
            base=base,
            target_name="CaptchaRecognizer.exe",
            icon=None,  # 可以添加图标文件路径
        )
    ]
)
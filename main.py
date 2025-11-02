#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于ddddocr的图片验证码识别程序
用户输入图片地址，调用识别输出结果
"""

import ddddocr
import os
import sys
from pathlib import Path

def identify_captcha(image_path):
    """
    识别验证码图片
    
    Args:
        image_path (str): 图片文件路径
        
    Returns:
        str: 识别结果
    """
    try:
        # 清理路径中的引号
        image_path = image_path.strip('"\'')
        
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return f"错误：文件不存在 - {image_path}"
        
        # 检查文件是否为图片
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        file_ext = Path(image_path).suffix.lower()
        if file_ext not in valid_extensions:
            return f"错误：不支持的文件格式 - {file_ext}，支持的格式：{', '.join(valid_extensions)}"
        
        # 初始化ddddocr识别器，禁用详细日志
        ocr = ddddocr.DdddOcr(show_ad=False)
        
        # 读取并识别图片
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        result = ocr.classification(image_bytes)
        return result
        
    except Exception as e:
        return f"识别过程中出现错误：{str(e)}"

def main():
    """主程序"""
    print("=== 验证码识别程序 ===")
    print("基于ddddocr开发")
    print("支持格式：JPG, JPEG, PNG, BMP, GIF")
    print("=" * 30)
    
    while True:
        try:
            # 获取用户输入的图片路径
            image_path = input("\n请输入验证码图片路径（输入'quit'退出程序）: ").strip()
            
            if image_path.lower() == 'quit':
                print("程序已退出，感谢使用！")
                break
            
            if not image_path:
                print("请输入有效的图片路径")
                continue
            
            # 识别验证码
            print(f"正在识别图片：{image_path}")
            result = identify_captcha(image_path)
            
            print(f"识别结果：{result}")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，感谢使用！")
            break
        except Exception as e:
            print(f"程序运行出错：{str(e)}")

if __name__ == "__main__":
    main()
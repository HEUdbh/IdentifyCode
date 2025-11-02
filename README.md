# 验证码识别程序

基于ddddocr开发的验证码识别程序，支持命令行和图形界面两种使用方式。

## 安装依赖

```bash
pip install ddddocr pillow
```

## 使用方法

### 1. 命令行版本 (main.py)

```bash
python main.py
```

- 按照提示输入验证码图片的完整路径
- 程序将显示识别结果
- 输入 `quit` 退出程序

### 2. 图形界面版本 (gui_main.py)

```bash
python gui_main.py
```

- 打开程序后会显示图形界面
- 点击上传按钮选择验证码图片
- 程序会自动预览图片并显示识别结果
- 通过界面按钮操作，直观便捷

### 3. 可执行文件版本 (exe)

在 `build/exe.win-amd64-3.12/` 目录下找到 `CaptchaRecognizer.exe` 文件：

- 直接双击 `CaptchaRecognizer.exe` 运行程序
- 使用图形界面进行操作
- 无需安装Python环境即可运行

## 打包程序

如需重新打包程序，可使用以下命令：

```bash
python setup.py build_exe
```

打包后的可执行文件将生成在 `build/exe.win-amd64-3.12/` 目录下。

## 4. 效果预览

下面是程序运行效果的截图：

![验证码识别程序效果截图1](images/屏幕截图%202025-11-02%20181016.png)

![验证码识别程序效果截图2](images/屏幕截图%202025-11-02%20192112.png)

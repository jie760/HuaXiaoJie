import webview
import threading
import uvicorn
import sys
import os

# 导入我们在 app.py 里写好的 FastAPI app
from backend.app import app

# 1. 获取打包后资源的绝对路径
def resource_path(relative_path):
    """ 获取打包后资源的绝对路径 """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后，文件会被解压到 sys._MEIPASS 临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("../frontend"), relative_path)

# 2. 定义启动后端的函数（供后台线程调用）
def start_backend():
    # 运行 Uvicorn，关闭日志的重复输出
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

if __name__ == '__main__':
    print("正在启动后台服务...")
    # 3. 创建一个守护线程来运行 FastAPI 后端
    # daemon=True 意味着当主窗口关闭时，这个线程会自动被杀掉
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    print("正在打开桌面窗口...")
    # 4. 加载前端的 index.html（使用 resource_path 解决路径问题）
    window = webview.create_window(
        title="洁的本地AI助手",
        url=resource_path("../frontend/index.html"),
        width=800,
        height=600
    )

    # 5. 启动窗口
    webview.start()
    print("应用已退出。")
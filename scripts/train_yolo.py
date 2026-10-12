import os
import ctypes
from importlib.util import find_spec

if os.name == 'nt':  # Windows 系统
    try:
        spec = find_spec("torch")
        if spec and spec.origin:
            dll_path = os.path.join(os.path.dirname(spec.origin), "lib", "c10.dll")
            if os.path.exists(dll_path):
                ctypes.CDLL(os.path.normpath(dll_path))
    except Exception:
        pass
from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 加载预训练模型（会自动下载一个几MB的 yolo11n_one.pt 文件）
    model = YOLO(r"D:\tools\task one\yolo11n.pt")

    # 2. 开始训练
    # data="coco8.yaml" 是官方自带的微小型数据集
    # epochs=10 代表训练10轮，参数可以自己决定
    # imgsz=640 代表图片输入尺寸
    print("开始训练...")
    results = model.train(data="coco8.yaml", epochs=10, imgsz=640)
    print("训练完成！")
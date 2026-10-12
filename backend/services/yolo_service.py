# 视觉服务层
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import os


class YOLOService:
    def __init__(self, model_path="backend/models/yolo11n_one.pt"):
        # 如果路径不对，尝试相对路径修正
        if not os.path.exists(model_path):
            model_path = "../backend/models/yolo11n_one.pt"
        self.model = YOLO(model_path)
        print(f"✅ YOLO 模型加载成功: {model_path}")

    def detect(self, image_bytes: bytes):
        """核心计算逻辑：处理图片并返回标注图Base64与识别标签"""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = self.model(img)
        annotated_img = results[0].plot()

        labels = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = self.model.names[cls_id]
            labels.append(f"{class_name} ({conf:.2f})")

        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return {"image": img_base64, "labels": labels}
# 华小洁 (HuaXiaoNiu) 系统架构设计

## 📖 设计思想
本项目严格遵循 **“前后端高度解耦”** 与 **“模块化封装”** 原则。前端只负责 UI 展示与用户交互；后端主程序（`app.py`）只负责组装模块；所有的计算、推理、业务逻辑均下沉至独立的 `Service` 层。

## 🏗️ 系统整体架构图

```text
【前端 Frontend (HTML/CSS/JS)】
       ↓ 用户上传图片/输入问题
[API 网关 (FastAPI) - backend/app.py]
       ↓ 路由分发
[API 路由层 - backend/api/routes.py]
       ↓         ↓
[YOLO 服务]      [LLM 服务]
yolo_service.py   llm_service.py
       ↓         ↓
[YOLO 模型]       [Ollama 本地引擎]
yolo11n.pt        (qwen2.5:14b / minicpm-v)
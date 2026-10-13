# 华小洁 (HuaXiaoJie) 系统架构设计

---

## 📖 设计思想
本项目严格遵循 **“前后端高度解耦”** 与 **“模块化封装”** 原则。前端只负责 UI 展示与用户交互；后端主程序（`app.py`）只负责组装模块；所有的计算、推理、业务逻辑均下沉至独立的 `Service` 层。

## 💻 技术栈清单
- 前端：HTML5, CSS3, ES6 JavaScript, Electron (桌面端集成)
- 后端：Python 3.11, FastAPI, Uvicorn, OpenCV
- AI 推理：YOLOv11 (目标检测), Ollama (qwen2.5:14b 文本推理, minicpm-v 多模态推理)
- 版本控制：Git, Gitee


---

## 🔄 核心数据流
### 图像识别请求 (POST /api/detect)
前端上传图片 -> routes.py 接收 -> 调用 YOLOService -> 运行推理，绘制 bounding box -> 返回 JSON (含 Base64 图片和识别标签)。

### AI 对话/诊断请求 (POST /api/chat)
前端发送 JSON (query, image_base64) -> routes.py -> 调用 LLMService。

### LLMService 判断是否带图：
- 有图：调用多模态模型 minicpm-v，结合视觉上下文输出诊断结果。
- 无图：调用逻辑模型 qwen2.5:14b，结合系统级 RPG 提示词输出对话反馈。

### 前端渲染
接收后端 JSON 返回，利用 JavaScript 动态更新 DOM，渲染诊断结果或游戏剧情。

---

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
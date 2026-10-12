# 华小牛 (HuaXiaoNiu) - 基于多模态大模型的农业智能诊断终端



## 📖 项目简介



“华小牛”是一个结合了 YOLO 目标检测与本地多模态大模型（Minicpm-v / Qwen2.5）的农场 AI 助手。它支持图像识别、兽医诊断以及基于大模型的 RPG 闯关玩法，旨在辅助农业科普与农场管理。



---



## 🏗️ 架构设计



- \*\*前端\*\*：HTML/CSS/JS (原生)

- \*\*后端\*\*：Python FastAPI (负责模块组装、API计算与服务推送)

- \*\*视觉引擎\*\*：YOLO (Ultralytics) 负责目标检测

- \*\*推理引擎\*\*：Ollama (本地部署) 负责多模态理解与逻辑推理

- \*\*桌面端\*\*：Electron (内嵌 Web 应用)



---



## 📂 目录结构



```text

task_one/

├── backend/            # FastAPI 后端与 AI 服务

│   ├── services/       # 业务逻辑层（YOLO 服务、LLM 服务）

│   ├── api/            # 路由层

│   └── app.py          # 主程序入口

├── frontend/           # 前端 UI 页面

├── electron\_app/       # Electron 桌面壳

├── scripts/            # 训练与测试独立脚本

├── docs/               # 工程日志与说明文档

└── README.md           # 项目说明文档
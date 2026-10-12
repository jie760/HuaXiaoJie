# 华小洁 (HuaXiaoNiu) 项目工程日志

> 记录人：jie (华南农业大学)
> 日期：2026年10月

## 📌 阶段一：本地大模型环境搭建与踩坑
*   **初期尝试（失败）**：尝试从 ModelScope 下载 `DeepSeek-V4.1-Flash` 原生权重（约600GB），下载半小时未果，且发现 Ollama 仅支持 `.gguf` 格式。
    *   **解决方案**：果断放弃原生大模型，改用轻量级 `qwen2.5:7b`（后升级至 `14b`），通过 `ollama run` 直接拉取（约4.7GB），成功在本地运行。
*   **Ollama 连接报错**：遇到 `id_ed25519` 缺失和 Docker 容器无法访问宿主机。
    *   **解决方案**：清理 `.ollama` 目录，并通过命令行 `setx OLLAMA_HOST "0.0.0.0"` 暴露监听地址，解决了容器互访问题。

## 📌 阶段二：Docker 与 Dify 编排
*   **WSL 缺失与镜像下载超时**：Docker Desktop 依赖 WSL 2，且国内无法拉取官方镜像。
    *   **解决方案**：管理员运行 `wsl --install`，并在 Docker Engine 配置国内加速器（daocloud、1panel）。
*   **Weaviate 组件连接超时**：Dify 启动过程中，向量库拉取失败。
    *   **解决方案**：修改 `docker-compose.yaml` 中的镜像地址前缀，重新拉起容器。
*   **Dify 接入 Ollama 报错 `Failed to parse`**：容器内 `localhost` 无法访问宿主机。
    *   **解决方案**：将 Base URL 修正为 `http://host.docker.internal:11434`，成功在 Dify 内实现可视化工作流编排。

## 📌 阶段三：全栈开发（Web/Electron）
*   **路径与依赖冲突**：Node.js 被错误安装在 `D:\tools\node_modules`，导致系统环境变量混乱。
    *   **解决方案**：重新安装 Node.js 至默认路径 `C:\Program Files\nodejs`，并在 PyCharm 中手动配置 Node 解释器。
*   **前端与后端脱节**：初期 API Key 硬编码在前端，且纯文本大模型无法看图。
    *   **解决方案**：使用 FastAPI 搭建中间层，隐藏密钥。引入多模态模型 `minicpm-v`，结合 YOLO 识别结果，通过 `api/chat` 将图片 Base64 和文本提示词一同送入模型。

## 📌 阶段四：YOLO 训练与多模态融合
*   **WinError 4551 报错**：PyTorch 的 `c10.dll` 被 Windows 智能应用控制拦截。
    *   **解决方案**：关闭系统“智能应用控制”并将 PyTorch 目录加入安全排除项。
*   **小模型工具调用失败**：本地 7B/14B 模型在进行复杂的 Agent 工具调用时（如自动写文件建预设）经常报错。
    *   **解决方案**：放弃让模型自动生成配置文件，改为手动编写 `huaxiaoniu.json` 并在前端简化交互逻辑。

## 📌 阶段五：工程化重构与版本控制
*   **大文件推送到 Gitee 失败**：历史提交中存在 102MB 的模型权重文件。
    *   **解决方案**：关闭 PyCharm，手动删除隐藏的 `.git` 目录。重新 `git init`，确保 `.gitignore` 位于根目录且生效（忽略 `*.pt`、`runs/` 等），最后使用 `git push -f` 成功推送干净代码。
*   **代码架构混乱**：初期所有逻辑堆在 `server.py` 中，不符合面试官“模块化封装”的要求。
    *   **解决方案**：进行架构重构，将业务逻辑拆分为 `services`（YOLO、LLM）和 `api`（路由），主程序 `app.py` 仅负责组装和启动。

## 🎯 下一步计划
1. 完善 `docs/` 下的架构文档。
2. 进一步优化前端 UI，提升“华小洁”农场闯关游戏的交互体验。
3. 尝试通过 Dify 接入本地知识库（RAG），为“华小洁”提供更专业的农业兽医知识。
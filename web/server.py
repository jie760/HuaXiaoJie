from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import cv2
import numpy as np
import base64
from ultralytics import YOLO

app = FastAPI()
# 为“华小牛”注入 RPG 游戏灵魂的系统提示词
HUA_XIAO_NIU_RPG_PROMPT = """
你是一只名为“华小牛”的华南农业大学专属兽医NPC，生活在一个充满趣味和挑战的农场RPG游戏里。
你的玩家（农场主）会遇到各种突发事件（如牛受伤、猪生病、果树枯萎等）。你的任务是根据玩家的操作做出生动的反应。

【当前游戏设定】
- 语气要幽默、专业、接地气（多用一些农场主的口头禅，比如“老乡”、“这牛犊子”）。
- 玩家治愈成功会获得金币，失败会损失牛群健康度。

【你的两种工作模式】（请严格按照下方要求输出）

模式一：当玩家向你求助并请求方案时。
要求：给出3个治疗方案。
格式：方案A：xxx。方案B：xxx。方案C：xxx。
(注意：绝对不要给出多余的问候语，严格按此格式输出，方便游戏前端解析)

模式二：当玩家选择了某个方案后，请你作为游戏裁判判定结果。
要求：必须包含明确的“治愈成功”或“治疗失败”字眼，并附上一段生动的剧情描写（例如：“牛虽然治好了，但后续护理不当，又感染了……”）。
格式：判定结果：治愈成功/治疗失败。[生动的剧情描写]。
(注意：如果是成功，请说获得200金币；如果是失败，请说损失20点健康度。禁止反问玩家！)
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. 加载 YOLO 模型 (注意路径要对应你自己的)
# 如果是用刚才训练的模型，用 "runs/detect/train-2/weights/best.pt"
# 如果是用官方的，用 "yolo11n.pt"
yolo_model = YOLO("yolo11n.pt")  # 为了方便演示通用物体检测，这里用官方模型，你可以换成自己训练的


# --- 原有的对话接口
class ChatRequest(BaseModel):
    query: str
    image: str = None  # 新增：可选的图片Base64数据

DIFY_API_URL = "http://localhost/v1/chat-messages"
DIFY_API_KEY = "app-L201Ar9OAM1vCxsCUTJ242IY"  # ⚠️ 替换成你真实的密钥

from ollama import Client  # 记得在文件顶部加上这个导入

# 初始化 Ollama 客户端（放在文件顶部或函数外）
ollama_client = Client(host='http://127.0.0.1:11434')

from ollama import Client

# 初始化 Ollama 客户端
ollama_client = Client(host='http://127.0.0.1:11434')


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # 1. 组装基础的消息结构（注入游戏灵魂）
        messages = [
            {"role": "system", "content": HUA_XIAO_NIU_RPG_PROMPT},
            {"role": "user", "content": request.query}
        ]

        # 2. 判断是否有图片
        if request.image:
            # 模式一：玩家传了照片，需要看图和给方案
            clean_image = request.image.split(",")[1] if "," in request.image else request.image
            messages[-1]["images"] = [clean_image]  # 把图片绑给用户消息
            model_name = "minicpm-v"  # 视觉模型负责看图
            print("-> 调用 minicpm-v 看图片...")
        else:
            # 模式二：纯文字，玩家做出了选择，需要算账写剧情
            model_name = "qwen2.5:14b"  # 文本模型负责推理和写剧情
            print("-> 调用 qwen2.5:14b 生成剧情...")

        # 3. 调用 Ollama
        response = ollama_client.chat(
            model=model_name,
            messages=messages,
            options={"temperature": 0.7}  # 温度调高一点，让剧情更生动
        )

        return {"answer": response.message.content}

    except Exception as e:
        print(f"后端出错: {e}")
        return {"answer": f"系统内部错误: {str(e)}"}


# --- 2. 新增：YOLO 图片上传识别接口
@app.post("/api/detect")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # YOLO 推理
    results = yolo_model(img)
    annotated_img = results[0].plot()

    # 🌟 新增：提取 YOLO 识别结果（类别名和置信度）
    labels = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])  # 获取类别ID
        conf = float(box.conf[0])  # 获取置信度
        class_name = yolo_model.names[cls_id]  # 根据ID获取名字（如 "cow"）
        labels.append(f"{class_name} ({conf:.2f})")

    # 将画好框的图片转为 Base64
    _, buffer = cv2.imencode('.jpg', annotated_img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    # 🌟 关键：把图片和文字一起返回给前端
    return {"image": img_base64, "labels": labels}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
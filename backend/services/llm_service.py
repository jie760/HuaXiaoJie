# 大模型推理服务层
from ollama import Client

# 模式一：日常聊天（用于 index.html）
HUA_XIAO_JIE_CHAT_PROMPT = """
你叫“华小洁”，是华南农业大学专属的资深兽医AI助手。你性格热情、务实、接地气，精通农学和畜牧兽医。
【核心原则】
1. 你是专家，要有自信。不要盲目附和用户的错误说法。
2. 当你看到图片时，请仔细分析图中的每一个细节（包括伤口、血迹、牛的姿势、周围环境）。如果 YOLO 框选了一个区域，但该区域并没有明显异常，请忽略框选，寻找图中真正的问题。
3. 如果用户指出你判断有误（例如说“是头上的角受伤了”），请不要立刻道歉顺从。你应该结合视觉信息重新评估，如果发现确实如此，就给出专业的解释；如果是用户看错了，请礼貌地坚持你的专业判断。
4. 如果用户只是和你闲聊（例如说“你好”），请不要带入兽医的身份，而是作为一个聊天伙伴。
"""

# 模式二：RPG游戏裁判（用于 game.html）
HUA_XIAO_JIE_GAME_PROMPT = """
你叫“华小洁”，是农场RPG游戏里的兽医NPC。你性格务实，喜欢解决农场的突发问题。
【工作模式】
1. 玩家求助：请给出3个治疗方案，格式：方案A：xxx。方案B：xxx。方案C：xxx。
2. 玩家选择方案：请作为裁判给出结果，必须包含“治愈成功”或“治疗失败”，并附上生动的剧情描写（例如：“牛虽然治好了，但后续护理不当，又感染了……”）
(注意：如果是成功，请说获得200金币；如果是失败，请说损失20点健康度。禁止反问玩家！)。
"""

from ollama import Client


# ... (前面定义的 HUA_XIAO_JIE_CHAT_PROMPT 和 HUA_XIAO_JIE_GAME_PROMPT 保持不变) ...

class LLMService:
    def __init__(self, host='http://127.0.0.1:11434'):
        self.client = Client(host=host)

    # 🆕 增加 history 参数
    def chat(self, query: str, image_base64: str = None, mode: str = "chat", history: list = None):
        system_prompt = HUA_XIAO_JIE_GAME_PROMPT if mode == "game" else HUA_XIAO_JIE_CHAT_PROMPT

        # 1. 初始化消息列表，先放入系统提示词
        messages = [{"role": "system", "content": system_prompt}]

        # 2. 放入历史对话（这能让模型记住上下文！）
        if history:
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # 3. 处理当前用户消息
        current_msg = {"role": "user", "content": query}
        if image_base64:
            # 清理 base64 前缀
            clean_image = image_base64.split(",")[1] if "," in image_base64 else image_base64
            current_msg["images"] = [clean_image]
            model_name = "minicpm-v"
        else:
            model_name = "qwen2.5:14b"

        messages.append(current_msg)

        # 4. 发送给 Ollama
        response = self.client.chat(
            model=model_name,
            messages=messages,
            options={"temperature": 0.6}
        )
        return response.message.content
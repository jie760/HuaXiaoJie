# 大模型推理服务层
from ollama import Client

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


class LLMService:
    def __init__(self, host='http://127.0.0.1:11434'):
        self.client = Client(host=host)

    def chat(self, query: str, image_base64: str = None):
        """核心推理逻辑：纯文本走 qwen，带图走 minicpm-v"""
        messages = [
            {"role": "system", "content": HUA_XIAO_NIU_RPG_PROMPT},
            {"role": "user", "content": query}
        ]

        if image_base64:
            # 清理 base64 前缀
            clean_image = image_base64.split(",")[1] if "," in image_base64 else image_base64
            messages[-1]["images"] = [clean_image]
            model_name = "minicpm-v"
        else:
            model_name = "qwen2.5:14b"

        response = self.client.chat(
            model=model_name,
            messages=messages,
            options={"temperature": 0.7}
        )
        return response.message.content
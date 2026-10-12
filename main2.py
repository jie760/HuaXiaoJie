import requests
import json

# ⚠️ 1. 填写你在 Dify 生成的 API 密钥（在 Dify 应用 -> 访问 API -> API 密钥里复制）
API_KEY = "app-zUt5xLzYO1IgYFqjM6fROXzg"

# ⚠️ 2. Dify 的本地 API 地址（通常默认是这个）
API_URL = "http://localhost/v1/chat-messages"

# 准备发送给大模型的数据
payload = {
    "inputs": {},
    "query": "你好，请用一句话介绍一下你自己。",  # 你在这里输入想问的问题
    "response_mode": "blocking",  # 阻塞模式，等模型完整回答完再一次性返回（最简单）
    "user": "user_001"
}

# 设置请求头
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("正在向 Dify 发送请求，请稍等...\n")

try:
    # 发送 POST 请求
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    # 检查是否请求成功 (HTTP状态码 200)
    if response.status_code == 200:
        result = response.json()
        print("🎉 大模型回答：")
        print(result.get("answer", "未找到回答内容"))
    else:
        print(f"❌ 请求失败，状态码：{response.status_code}")
        print(f"错误信息：{response.text}")

except Exception as e:
    print(f"❌ 连接出错：{e}")
    print("请检查：1. Docker Desktop 是否运行；2. Dify 容器是否已启动。")
# ... (前面的代码不变)
payload = {
    "inputs": {},
    "query": "请写一首关于春天的短诗。",
    "response_mode": "streaming",  # ⚠️ 改成流式
    "user": "user_001"
}
# ... (headers不变)

response = requests.post(API_URL, headers=headers, json=payload, stream=True)
print("🎉 大模型回答：")
for line in response.iter_lines():
    if line:
        decoded_line = line.decode('utf-8')
        if decoded_line.startswith('data: '):
            data_json = json.loads(decoded_line[6:])
            # Dify 的流式事件类型中，message 是正在生成的文本片段
            if data_json.get("event") == "message":
                print(data_json.get("answer"), end="", flush=True)
print("\n")
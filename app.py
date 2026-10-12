import streamlit as st
import requests
import json

st.title("我的本地 AI 助手")

# ⚠️ 这里必须替换成你的 Dify 密钥和 API 地址
API_KEY = "app-zUt5xLzYO1IgYFqjM6fROXzg"  # 换成你自己的密钥
API_URL = "http://localhost/v1/chat-messages"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("你想问什么？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 准备发送给 Dify 的数据
    payload = {
        "inputs": {},
        "query": prompt,
        "response_mode": "blocking",
        "user": "web_user_001"
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 显示 AI 正在思考
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            try:
                response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                if response.status_code == 200:
                    answer = response.json().get("answer", "未找到回答")
                else:
                    answer = f"请求失败，状态码：{response.status_code}"
            except Exception as e:
                answer = f"连接出错：{e}"

            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generate_summary(old_summary, new_messages):
    prompt = f"""
你是一个对话摘要助手。

请将旧摘要与新增聊天记录合并，生成新的摘要。

要求：
1. 保留用户的重要信息和仍然有效的目标。
2. 保留对后续对话有帮助的上下文。
3. 删除重复内容和无关寒暄。
4. 不要编造信息。
5. 尽量控制在200字以内。

旧摘要：
{old_summary}

新增聊天记录：
{json.dumps(new_messages, ensure_ascii=False)}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一个负责整理历史对话的摘要助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
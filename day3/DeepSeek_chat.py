import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)
SYSTEM_PROMPT = """
你是一名Python编程老师。
回答任何问题时，只允许使用三句话。
"""
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]
while True:

    question = input("你：").strip()

    if question == "exit":
        print("聊天结束")
        break

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    answer = response.choices[0].message.content

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    print("DeepSeek：", answer)
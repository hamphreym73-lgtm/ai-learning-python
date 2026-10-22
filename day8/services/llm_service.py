import json

from openai import OpenAI

from day8.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    MODEL_NAME
)

from day8.tools.tool_registry import TOOL_REGISTRY


client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_school_notices",
            "description": "搜索学校通知，根据关键词查找相关通知",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词，例如奖学金、助学金、比赛"
                    }
                },
                "required": ["keyword"]
            }
        }
    }
]


def chat(messages):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    if response.usage:
        print("输入 Token：", response.usage.prompt_tokens)
        print("输出 Token：", response.usage.completion_tokens)
        print("总 Token：", response.usage.total_tokens)

    return response.choices[0].message.content

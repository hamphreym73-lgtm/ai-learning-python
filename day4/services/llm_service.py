import json

from openai import OpenAI

from day4.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    MODEL_NAME
)

from day4.tools.tool_registry import TOOL_REGISTRY


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

    while True:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS
        )

        message = response.choices[0].message

        # DeepSeek不需要调用工具，直接返回回答
        if not message.tool_calls:
            return message.content

        # 保存DeepSeek的工具调用请求
        messages.append(message)

        # 执行DeepSeek选择的工具
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print("模型决定调用工具：", tool_name)
            print("工具参数：", arguments)

            tool_function = TOOL_REGISTRY.get(tool_name)

            if tool_function:
                result = tool_function(**arguments)
            else:
                result = {
                    "error": "没有找到这个工具"
                }

            print("工具执行结果：", result)

            # 把工具结果重新交给DeepSeek
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
            )
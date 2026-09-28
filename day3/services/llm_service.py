from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL_NAME
from tools.timetool import get_current_time
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def chat(messages):
    # 第一次请求：让模型判断是否需要工具
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    # 不需要工具，直接返回模型回答
    if not message.tool_calls:
        return message.content

    # 模型要求调用工具
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name

    print("模型决定调用工具：", tool_name)

    # 执行对应的 Python 工具
    if tool_name == "get_current_time":
        result = get_current_time()
    else:
        result = "未知工具"

    print("工具执行结果：", result)

    # 保存模型发出的工具调用请求
    messages.append(message)

    # 保存工具执行结果
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    # 第二次请求：让模型根据工具结果生成最终答案
    final_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools
    )

    final_answer = final_response.choices[0].message.content

    return final_answer
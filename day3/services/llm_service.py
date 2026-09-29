from openai import OpenAI

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    MODEL_NAME
)

import json
from tools.tool_registry import TOOL_REGISTRY
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

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "search_school_notices",

            "description":
            "搜索学校通知，根据关键词查找相关通知",

            "parameters": {

                "type": "object",

                "properties": {

                    "keyword": {

                        "type": "string",

                        "description":
                        "搜索关键词，例如奖学金、助学金、比赛、教务"

                    }

                },

                "required": [
                    "keyword"
                ]
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


        # 情况1：模型直接回答
        if not message.tool_calls:

            return message.content



        # 情况2：模型要求调用工具

        messages.append(
            message
        )


        for tool_call in message.tool_calls:


            tool_name = tool_call.function.name


            arguments = json.loads(
                tool_call.function.arguments
            )


            print("调用工具：", tool_name)

            print("参数：", arguments)



            # 找对应Python函数

            tool_function = TOOL_REGISTRY.get(
                tool_name
            )


            if tool_function:

                result = tool_function(
                    **arguments
                )

            else:

                result = "工具不存在"



            print("工具返回：", result)



            # 把工具结果交回给模型

            messages.append(
                {
                    "role": "tool",

                    "tool_call_id":
                    tool_call.id,

                    "content":
                    json.dumps(
                        result,
                        ensure_ascii=False
                    )
                }
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
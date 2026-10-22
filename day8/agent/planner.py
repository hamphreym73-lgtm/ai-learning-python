from day8.services.llm_service import chat

def create_plan(task):

    messages = [
        {
            "role": "system",
            "content": """
你是一个任务规划助手。


你是一个任务规划助手。

如果用户需要查询学校通知，请输出：

ACTION: search_school_notices
KEYWORD: 核心搜索关键词

规则：
1. KEYWORD 只填写通知主题，例如奖学金、助学金、比赛、教务。
2. 不要把“申请截止时间”“什么时候截止”“详细内容”等问题描述放进 KEYWORD。
3. 用户既要查通知又要核实截止时间时，先搜索通知主题，再根据真实通知正文核实截止时间。
4. 如果不需要工具，输出：

ACTION: none

只输出计划，不要回答用户问题。


如果不需要工具，
输出：

ACTION: none
"""
        },
        {
            "role": "user",
            "content": task
        }
    ]

    return chat(messages)


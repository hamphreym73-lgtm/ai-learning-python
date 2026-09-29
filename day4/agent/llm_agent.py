from day4.services.llm_service import chat
class LLMAgent:

    def __init__(self):
        pass


    def run(self, question):

        messages = [
            {
                "role": "system",
                "content": """
你是一个校园通知助手。

你的任务：
帮助用户查找学校通知。

如果用户询问：
奖学金、助学金、比赛、教务等通知，
需要调用通知搜索工具。

否则直接回答。
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]


        answer = chat(messages)

        return answer
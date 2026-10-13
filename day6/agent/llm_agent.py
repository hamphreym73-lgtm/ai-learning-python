from day6.services.llm_service import chat
from day6.agent.memory import ConversationMemory


class LLMAgent:

    def __init__(self):
        self.memory = ConversationMemory()

        self.memory.add_system_message("""
你是一个校园通知助手。

你的任务：
帮助用户查找学校通知。

如果用户询问：
奖学金、助学金、比赛、教务等通知，
需要调用通知搜索工具。

否则直接回答。
""")

    def run(self, question):

        # 1. 保存用户问题
        self.memory.add_user_message(question)

        # 2. 获取最近的对话历史
        messages = self.memory.get_recent_messages()

        # 3. 调用 DeepSeek
        answer = chat(messages)

        # 4. 保存 AI 的回答
        self.memory.add_assistant_message(answer)

        # 5. 返回结果
        return answer
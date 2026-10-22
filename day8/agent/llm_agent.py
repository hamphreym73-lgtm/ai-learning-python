from day8.services.llm_service import chat
from day8.agent.memory import ConversationMemory
from day8.agent.summary_memory import SummaryMemory
from day8.services.summary_service import generate_summary

class LLMAgent:

    def __init__(self):

        self.memory = ConversationMemory()

        self.summary_memory = SummaryMemory()

        self.memory.add_system_message("""
你是一个校园通知助手。

你的任务：
帮助用户查找学校通知。

如果用户询问：
奖学金、助学金、比赛、教务等通知，
需要调用通知搜索工具。

否则直接回答。
""")

    def check_and_update_summary(self):

        messages = self.memory.get_messages()

        if len(messages) > 12 and len(messages) % 6 == 0:
            print("触发摘要更新")

            old_summary = self.summary_memory.get_summary()

            new_summary = generate_summary(
                old_summary,
                messages
            )

            self.summary_memory.update_summary(
                new_summary
            )
        self.memory.compress_memory()
    def run(self, question):

        # 1. 保存用户问题
        self.memory.add_user_message(question)


        # 2. 获取最近聊天
        messages = self.memory.get_recent_messages()


        # 3. 获取历史摘要
        summary = self.summary_memory.get_summary()


        # 4. 如果存在摘要，加入上下文
        if summary:

            messages.insert(
                1,
                {
                    "role": "system",
                    "content": f"""
以下是用户历史信息摘要：

{summary}

回答问题时请结合这些信息。
"""
                }
            )


        # 5. 调用 DeepSeek
        answer = chat(messages)


        # 6. 保存回答
        self.memory.add_assistant_message(answer)
        self.check_and_update_summary()

        return answer
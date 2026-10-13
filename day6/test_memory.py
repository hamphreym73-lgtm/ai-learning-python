from agent.memory import ConversationMemory


memory = ConversationMemory()

memory.add_user_message(
    "最近有什么奖学金通知"
)

memory.add_assistant_message(
    "有三条通知"
)

print(memory.get_messages())
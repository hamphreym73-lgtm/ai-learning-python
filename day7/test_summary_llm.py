from day7.agent.summary_memory import SummaryMemory
from day7.services.summary_service import generate_summary

memory = SummaryMemory()

old_summary = "用户正在学习Python"

new_messages = [
    {
        "role": "user",
        "content": "我现在开始学习AI Agent"
    },
    {
        "role": "assistant",
        "content": "我们可以从Tool Calling开始"
    }
]

new_summary = generate_summary(old_summary, new_messages)

print("DeepSeek生成的摘要：")
print(new_summary)

if new_summary:
    memory.update_summary(new_summary)
    print("摘要已保存到JSON")
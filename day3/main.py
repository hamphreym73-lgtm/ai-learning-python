from prompts import SYSTEM_PROMPT
from services.llm_service import chat


messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


while True:
    question = input("你：").strip()

    if question == "exit":
        print("聊天结束")
        break

    messages.append({
        "role": "user",
        "content": question
    })

    answer = chat(messages)

    messages.append({
        "role": "assistant",
        "content": answer
    })

    print("DeepSeek：", answer)
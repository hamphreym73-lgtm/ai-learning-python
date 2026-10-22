from day8.agent.llm_agent import LLMAgent

# 创建 Agent 对象，只创建一次
agent = LLMAgent()

while True:
    question = input("你：")

    # 输入 exit 就退出
    if question == "exit":
        break

    # 调用 Agent，获取回答
    answer = agent.run(question)

    print("Agent：", answer)
from agent.llm_agent import LLMAgent

agent = LLMAgent()


while True:

    question = input("你：")

    result = agent.run(question)

    print("Agent:", result)
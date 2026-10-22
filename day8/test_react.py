from day8.agent.react_agent import ReactAgent
from day8.agent.planner import create_plan


agent = ReactAgent(create_plan)

task = "帮我查奖学金通知，并核实申请截止时间"

answer = agent.run(task)

print(answer)
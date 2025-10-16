import asyncio
from agents import Agent, Runner

# 이 한 줄이 핵심!
asyncio.set_event_loop(asyncio.new_event_loop())

hello_agent = Agent(
    name="HelloAgent",
    instructions="당신은 HelloAgent입니다. 당신의 임무는 '안녕하세요'라고 인사하는 것입니다.",
)

result = Runner.run_sync(hello_agent, "프랑스어로만 인사해주세요.")
print(result.final_output)
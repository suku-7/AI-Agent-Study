import asyncio
from agents import Agent, Runner

async def main():
    hello_agent = Agent(
        name="HelloAgent",
        instructions="당신은 HelloAgent입니다. 당신의 임무는 '안녕하세요'라고 인사하는 것입니다."
    )
    result = await Runner.run(hello_agent, "일본어로 인사해주세요.")

    print(result.final_output)

    return result

if __name__ == "__main__":
    asyncio.run(main())
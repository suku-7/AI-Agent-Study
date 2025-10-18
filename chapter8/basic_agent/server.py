import sys
from pathlib import Path
import uvicorn
sys.path.append(str(Path(__file__).parent.parent))
from a2a.server.apps import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from basic_agent.agent_executor import HelloAgentExecutor

def create_agent_card() -> AgentCard:
    """에이전트 카드를 만드는 함수"""
    greeting_skill = AgentSkill(
        id="basic_greeting",
        name="Basic Greeting",
        description="간단한 인사와 기본적인 대화를 제공합니다",
        tags=["greeting", "hello", "basic"],
        examples=["안녕하세요", "hello", "hi", "고마워요"],
        input_modes=["text"],
        output_modes=["text"],
    )

    agent_card = AgentCard(
        name="Basic Hello World Agent",
        description="A2A 프로토콜을 학습하기 위한 기본적인 Hello World 에이전트입니다.",
        url="http://localhost:9999/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[greeting_skill],
        supports_authenticated_extended_card=False,
    )
    return agent_card

def main():
    agent_card = create_agent_card()

    port = 9999
    host = "0.0.0.0"  # 서버는 0.0.0.0으로 바인딩

    print("Hello World 에이전트 서버 시작 중...")
    print(f"서버 구동: http://localhost:{port}")  # 사용자에게는 localhost 표시
    print(f"Agent Card: http://localhost:{port}/.well-known/agent-card.json")
    print("이것은 A2A 프로토콜 학습을 위한 기본 예제입니다\n")

    request_handler = DefaultRequestHandler(
        agent_executor=HelloAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AFastAPIApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    app = server.build()
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Message
from a2a.utils import new_agent_text_message

class HelloAgent:
    """랭체인과 OpenAI를 사용한 간단한 Hello World 에이전트."""

    def __init__(self):
        self.chat = ChatOpenAI(
            model="gpt-5-mini",
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """당신은 친절한 Hello World 에이전트입니다.
                    사용자와 간단한 대화를 나누고, 인사와 기본적인 질문에 답변합니다.
                    당신의 목표는 사용자에게 친근하고 도움이 되는 경험을 제공하는 겁니다.""",
                ),
                ("user", "{message}"),
            ]
        )
    async def invoke(self, user_message: str) -> str:
        """유저 메시지를 처리하고 응답을 생성합니다."""
        chain = self.prompt | self.chat
        response = await chain.ainvoke({"message": user_message})

        return response.content

class HelloAgentExecutor(AgentExecutor):
    """간단한 HelloWorld 에이전트의 Executor"""

    def __init__(self):
        self.agent = HelloAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ):
        """요청을 처리하고 응답을 생성합니다."""
        message = context.message
        for part in message.parts:
            if part.root.text:
                user_message = part.root.text

        result = await self.agent.invoke(user_message)

        await event_queue.enqueue_event(new_agent_text_message(result))
    
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,        
    ):
        """요청을 취소"""
        error_msg = "취소 기능은 지원되지 않습니다. Hello 에이전트는 즉시 응답합니다."
        error_message = Message(
            role="agent",
            parts={"type": "text", "text": error_msg},
            messageId="cancel_error",
        )
        event_queue.enqueue_event(error_message)
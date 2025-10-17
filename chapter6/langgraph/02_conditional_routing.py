from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import random

class EmotionBotState(BaseModel):
    user_message: str = Field(default="", description="사용자 입력 메시지")
    emotion: str = Field(default="", description="분석된 감정")
    response: str = Field(default="", description="최종 응답 메시지")

# Structured output을 위한 스키마
class EmotionClassification(BaseModel):
    emotion: Literal["positive", "negative", "neutral"]

llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

def analyze_emotion(state: EmotionBotState) -> Dict[str, Any]:
    message = state.user_message
    print(f"LLM 감정 분석 중: '{message}'")

    # Structured output 사용
    structured_llm = llm.with_structured_output(EmotionClassification)
    
    messages = [
        SystemMessage(
            content="당신은 감정 분석 전문가입니다. 사용자의 메시지를 분석하여 감정을 분류해주세요."
        ),
        HumanMessage(content=f"다음 메시지의 감정을 분석해주세요: '{message}'"),
    ]
    
    result = structured_llm.invoke(messages)
    emotion = result.emotion
    
    print(f"LLM 감정 분석 결과 : {emotion}")
    return {"emotion": emotion}

def generate_positive_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["정말 좋은 소식이네요!", "기분이 좋으시군요", "멋지네요!"]
    return {"response": random.choice(responses)}

def generate_negative_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["힘든 시간이시군요. 괜찮아요", "마음이 아프시겠어요.", "더 좋은 날이 올거에요."]
    return {"response": random.choice(responses)}

def generate_neutral_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["감사해요! 더 자세히 말씀해주세요", "이해했어요. 다른 도움이 필요하면 말씀하세요!", "흥미로운 주제네요!"]
    return {"response": random.choice(responses)}

def route_by_emotion(state: EmotionBotState,) -> Literal["positive_response", "negative_response", "neutral_response"]:
    emotion = state.emotion
    print(f"라우팅 : {emotion}")

    if emotion == "positive":
        return "positive_response"
    elif emotion == "negative":
        return "negative_response"
    else:
        return "neutral_response"

def create_emotion_bot_graph():
    workflow = StateGraph(state_schema=EmotionBotState)

    workflow.add_node("analyze_emotion", analyze_emotion)
    workflow.add_node("positive_response", generate_positive_response)
    workflow.add_node("negative_response", generate_negative_response)
    workflow.add_node("neutral_response", generate_neutral_response)

    workflow.add_edge(START, "analyze_emotion")
    workflow.add_conditional_edges(
        "analyze_emotion", 
        route_by_emotion,
        {
            "positive_response": "positive_response",
            "negative_response": "negative_response",
            "neutral_response": "neutral_response",
        },
    )

    workflow.add_edge("positive_response", END)
    workflow.add_edge("negative_response", END)
    workflow.add_edge("neutral_response", END)

    return workflow.compile()

def main():
    print("=== 감정 분석 챗봇 테스트 === \n")
    app = create_emotion_bot_graph()

    test_cases = [
        "오늘 정말 기분이 좋아요!",
        "너무 슬프고 힘들어요...",
        "날씨가 어떤가요?",
    ]
    for i, message in enumerate(test_cases, 1):
        print(f"테스트 {i}: '{message}'")
        # 딕셔너리로 전달
        result = app.invoke({"user_message": message})
        print(f"응답: {result['response']}\n")

    # 그래프 시각화
    mermaid_png = app.get_graph().draw_mermaid_png()
    with open("./02_conditional_routing.png", "wb") as f:
        f.write(mermaid_png)
            
if __name__ == "__main__":
    main()
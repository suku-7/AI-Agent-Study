from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import random
import re

class EmotionBotState(BaseModel):
    user_message: str = Field(default="", description="사용자 입력 메시지")
    emotion: str = Field(default="", description="분석된 감정")
    response: str = Field(default="", description="최종 응답 메시지")

llm = ChatOpenAI(model="gpt-5-mini", max_tokens=100)

def analyze_emotion(state: EmotionBotState) -> Dict[str, Any]:
    message = state.user_message
    print(f"LLM 감정 분석 중: '{message}'")
    
    # Few-shot 프롬프팅을 사용하여 모델의 출력 형식을 더 명확하게 지정
    prompt = """당신은 감정 분석 전문가입니다. 사용자의 메시지를 분석하여 'positive', 'negative', 'neutral' 셋 중 하나로 감정을 분류하세요. 당신의 답변은 반드시 'positive', 'negative', 'neutral' 중 하나의 단어여야 합니다.

사용자 메시지: "오늘 정말 기분이 좋아요!"
분석 결과: positive

사용자 메시지: "너무 슬프고 힘들어요.."
분석 결과: negative

사용자 메시지: "날씨가 어떤가요?"
분석 결과: neutral

사용자 메시지: "{user_message}"
분석 결과:"""

    messages = [
        HumanMessage(content=prompt.format(user_message=message))
    ]
    
    response = llm.invoke(messages)
    
    response_text = response.content.strip().lower()

    if re.search(r'\bpositive\b', response_text):
        emotion = 'positive'
    elif re.search(r'\bnegative\b', response_text):
        emotion = 'negative'
    else:
        emotion = 'neutral'

    print(f"LLM 감정 분석 결과 : {emotion}")
    return {"emotion": emotion}

def generate_positive_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["정말 좋은 소식이네요!", "기분이 좋으시군요!", "멋지네요!"]
    return {"response": random.choice(responses)}

def generate_negative_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["힘든 시간이시군요. 괜찮아요.", "마음이 아프시겠어요.", "더 좋은 날이 올거에요."]
    return {"response": random.choice(responses)}

def generate_neutral_response(state: EmotionBotState) -> Dict[str, Any]:
    responses = ["감사해요! 더 자세히 말씀해주세요.", "이해했어요. 다른 도움이 필요하면 말씀하세요!", "흥미로운 주제네요!"]
    return {"response": random.choice(responses)}

def route_by_emotion(state: EmotionBotState) -> Literal["positive_response", "negative_response", "neutral_response"]:
    emotion = state.emotion
    
    if emotion == "positive":
        return "positive_response"
    elif emotion == "negative":
        return "negative_response"
    else:
        return "neutral_response"
    
def create_emotion_bot_graph():
    workflow = StateGraph(EmotionBotState)

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
        }
    )
    workflow.add_edge("positive_response", END)
    workflow.add_edge("negative_response", END)
    workflow.add_edge("neutral_response", END)

    return workflow.compile()

def main():
    print("===감정 분석 챗봇 테스트===\n")
    app = create_emotion_bot_graph()

    test_cases = [
        "오늘 정말 기분이 좋아요!",
        "너무 슬프고 힘들어요..",
        "날씨가 어떤가요?",
    ]

    for i, message in enumerate(test_cases, 1):
        print(f"테스트 {i}: '{message}'")
        state = EmotionBotState(user_message=message)
        result = app.invoke(state)
        print(f"응답: {result['response']}\n")

        mermaid_png = app.get_graph().draw_mermaid_png()
        with open("./02_conditional_routing.png", "wb") as f:
            f.write(mermaid_png)

if __name__ == "__main__":
    main()
import random
from langchain.tools import tool
from langchain_openai import ChatOpenAI

@tool
def rps() -> str:
    """가위바위보 중 하나를 랜덤하게 선택"""
    return random.choice(["가위", "바위", "보"])

llm = ChatOpenAI(temperature=0.0).bind_tools([rps])
llm_for_chat = ChatOpenAI(temperature=0.7)
print(type(llm))

def judge(user_choice, computer_choice):
    """가위바위보 승패를 판정합니다."""
    user_choice = user_choice.strip()
    computer_choice = computer_choice.strip()
    if user_choice == computer_choice:
        return "무승부"
    elif (user_choice, computer_choice) in [
        ("가위", "보"),
        ("바위", "가위"),
        ("보", "바위"),
    ]:
        return "승리"
    else:
        return "패배"
print("가위바위보! (종료: q)")
while (user_input := input("\n가위/바위/보: ")) != "q":
    ai_msg = llm.invoke(
        f"가위바위보 게임: 사용자가 {user_input}를 냈습니다. rps tool을 사용하세요."
    )

    if ai_msg.tool_calls:
        print(type(rps))
        llm_choice = rps.invoke("")
        print(f" LLM이 선택한 도구: {llm_choice}")
        result = judge(user_input, llm_choice)

        print(f"승부: {result}")
        
        final = llm_for_chat.invoke(
            f"가위바위보 게임 결과를 재미있게 해설해주세요."
            f"사용자: {user_input}, AI: {llm_choice}, 결과 : 사용자의 {result}"
        )
        print(final)
        print(f" LLM 해설: {final.content}")
        print(f"게임 요약: 당신({user_input}) vs AI({llm_choice}) => {result}")
    else:
        print("Tool 호출 실패")
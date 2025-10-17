from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
import random

class GuessGameState(BaseModel):
    target_number: int = Field(default=0, description="맞춰야 할 숫자")
    user_guess: int = Field(default=0, description="사용자 추측")
    attempts: int = Field(default=0, description="시도 횟수")
    max_attempts: int = Field(default=5, description="최대 시도 횟수")
    game_status: str = Field(default="playing", description="게임 상태")
    response: str = Field(default="", description="응답 메시지")

def game_setup(state: GuessGameState) -> Dict[str, Any]:
    target = random.randint(1, 50)
    print("게임 시작!")

    return {
        "target_number": target,
        "game_status": "playing",
        "response": f"1~50 사이의 숫자를 맞춰보세요! (최대 {state.max_attempts}회)",
        "attempts": 0,
    }

def user_guess(state: GuessGameState) -> Dict[str, Any]:
    guess = input(f"\n입력 [{state.attempts + 1}/{state.max_attempts}회]: ")
    print(f"[{state.attempts + 1}번째 시도] 추측: {guess}")
    return {"user_guess": int(guess), "attempts": state.attempts + 1}

def check_guess(state: GuessGameState) -> Dict[str, Any]:
    target = state.target_number
    guess = state.user_guess
    attempts = state.attempts

    print(f"[check_guess] {guess} (시도: {attempts}회)")

    if guess == target:
        print("정답!")
        return {
            "game_status": "won",
            "response": f"정답! {guess}를 {attempts}번 만에 맞췄습니다!",
        }
    elif attempts >= state.max_attempts:
        print("시도 횟수 초과")
        return {
            "game_status": "lost",
            "response": f"게임 종료! 정답은 {target}이었습니다.",
        }
    else:
        hint = "더 큰 수" if guess < target else "더 작은 수"
        remaining = state.max_attempts - attempts
        print(f"계속 진행: {hint}")
        return {
            "game_status": "playing",
            "response": f"{guess}는 틀렸습니다. {hint}를 시도해보세요! 남은 기회: {remaining}회",
        }

def route_game(state: GuessGameState) -> Literal["continue", "end"]:
    print(f"라우팅 체크: 상태={state.game_status}, 시도={state.attempts}")
    if state.game_status == "playing":
        return "continue"
    else:
        return "end"

def create_guess_game_graph():
    workflow = StateGraph(GuessGameState)
    workflow.add_node("setup", game_setup)
    workflow.add_node("guess", user_guess)
    workflow.add_node("check", check_guess)
    
    workflow.add_edge(START, "setup")
    workflow.add_edge("setup", "guess")
    workflow.add_edge("guess", "check")

    workflow.add_conditional_edges(
        "check",
        route_game,
        {
            "continue": "guess",
            "end": END,
        }
    )
    return workflow.compile()

def main():
    print("=== 루프 워크플로 예제 ===\n")
    app = create_guess_game_graph()

    # dict로 전달
    result = app.invoke({"max_attempts": 5})

    print(f"\n최종 결과: {result['response']}")
    print(f"게임 상태: {result['game_status']}")
    print(f"총 시도: {result['attempts']}회")
    
    # 그래프 구조 출력
    try:
        # 그래프 시각화
        mermaid_png = app.get_graph().draw_mermaid_png()
        with open("./04.png", "wb") as f:
            f.write(mermaid_png)
    except Exception as e:
        print(f"그래프 출력 실패: {e}")
if __name__ == "__main__":
    main()
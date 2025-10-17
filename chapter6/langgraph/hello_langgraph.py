from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

class WorkflowStep:
    GREETING = "GREETING"
    PROCESSING = "PROCESSING"

class GraphState(BaseModel):
    name: str = Field(default="", description="사용자 이름")
    greeting: str = Field(default="", description="생성된 인사말")
    processed_message: str = Field(default="", description="처리된 최종 메시지")

def generate_greeting(state: GraphState) -> Dict[str, Any]:
    name = state.name or "아무개"
    greeting = f"안녕하세요, {name}님!"
    print(f"[generate_greeting] 인사말 생성: {greeting}")
    return {"greeting": greeting}

def process_message(state: GraphState) -> Dict[str, Any]:
    greeting = state.greeting
    processed_message = f"{greeting} LangGraph에 오신 것을 환영합니다!"
    print(f"[process_message] 최종 메시지: {processed_message}")

    return {"processed_message": processed_message}

def create_hello_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node(WorkflowStep.GREETING, generate_greeting)
    workflow.add_node(WorkflowStep.PROCESSING, process_message)

    workflow.add_edge(START, WorkflowStep.GREETING)

    workflow.add_edge(WorkflowStep.GREETING, WorkflowStep.PROCESSING)
    workflow.add_edge(WorkflowStep.PROCESSING, END)

    app = workflow.compile()
    return app

def main():
    print("=== Hello 랭그래프 === \n")
    app = create_hello_graph()

    # invoke에는 초기 입력값을 딕셔너리로 전달합니다.
    initial_input = {"name": "수쿠"}
    print("초기 입력:", initial_input)
    print("\n--- 그래프 실행 시작 ---")

    # invoke의 최종 결과는 딕셔너리입니다.
    final_state = app.invoke(initial_input)

    print("--- 그래프 실행 종료 --- \n")
    # final_state가 딕셔너리이므로 바로 출력합니다.
    print("최종 상태:", final_state)
    # 딕셔너리 키로 결과에 접근합니다.
    print(f"\n결과 메시지: {final_state['processed_message']}")

    print("\n--- 그래프 구조 (ASCII) ---")
    app.get_graph().draw_ascii()

    print("\n--- 그래프 이미지 생성 (hello_langgraph.png) ---")
    try:
        png_bytes = app.get_graph().draw_mermaid_png()
        with open("./hello_langgraph.png", "wb") as f:
            f.write(png_bytes)
        print("hello_langgraph.png 파일이 생성되었습니다.")
    except Exception as e:
        print(f"그래프 이미지 생성 중 오류 발생: {e}")
        print("이미지 생성을 위해 'pip install playwright' 와 'playwright install' 명령어를 실행했는지 확인하세요.")

if __name__ == "__main__":
    main()
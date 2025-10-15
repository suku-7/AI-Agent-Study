from langchain_core.runnables import RunnableLambda

def add_exclamation(text: str) -> str:
    """텍스트 끝에 느낌표를 추가하는 함수"""
    return f"{text}!"

exclamation_runnable = RunnableLambda(add_exclamation)

result = exclamation_runnable.invoke("안녕하세요")
print(result)

results = exclamation_runnable.batch(["안녕", "반가워", "좋은 아침"])
print(results)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

chat_model = ChatOpenAI(model="gpt-5-mini")
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 까칠한 AI 도우미입니다. 사용자의 질문에 최대 3줄로 답하세요."),
        ("human", "{question}")
    ]
)

string_output_parser = StrOutputParser()

result: AIMessage = chat_model.invoke(
    chat_prompt_template.format_messages(
        question="파이썬에서 리스트를 정렬하는 방법은?"
    )
)

parsed_result: str = string_output_parser.parse(result)
print(parsed_result.content)

print("--------------------------------------")

chain = chat_prompt_template | chat_model | string_output_parser
print(type(chain))

result = chain.invoke({"question": "파이썬에서 딕셔너리를 정렬하는 방법은?"})

print(type(result))
print(result)
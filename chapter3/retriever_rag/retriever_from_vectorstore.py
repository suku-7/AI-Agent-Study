# 1. 필요한 라이브러리 임포트
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 2. 임베딩 모델 및 텍스트 분할기 초기화
# OpenAIEmbeddings: 텍스트를 벡터로 변환하는 모델
embeddings = OpenAIEmbeddings()
# CharacterTextSplitter: 문서를 지정된 크기로 분할하는 도구
text_splitter = CharacterTextSplitter(separator=".", chunk_size=50, chunk_overlap=20)

# 3. 문서 데이터 생성
# 벡터 저장소에 저장할 문서들을 Document 객체로 생성
documents = [
    Document(
        page_content="파이썬은 읽기 쉽고 배우기 쉬운 프로그래밍 언어입니다."
        "다양한 분야에서 활용되며, 특히 데이터 과학과 AI 개발에 인기가 높습니다.",
        metadata={"source": "python_intro.txt", "topic": "programming"}
    ),
    Document(
        page_content="자바스크립트는 웹브라우저에서 실행되는 프로그래밍 언어로 시작했지만, " 
        "현재는 서버 사이드 개발에도 널리 사용됩니다. Node.js가 대표적입니다.",
        metadata={"source": "js_guide.txt", "topic": "programming"}
    ),
    Document(
        page_content="머신러닝은 데이터에서 패턴을 학습하는 AI의 한 분야입니다."
        "지도 학습, 비지도 학습, 강화 학습 등 다양한 방법론이 있습니다.",
        metadata={"source": "ml_basics.txt", "topic": "ai"}
    )
]

# 4. 문서 분할
# 생성한 문서들을 텍스트 분할기를 이용해 작은 조각으로 나눔
split_docs = text_splitter.split_documents(documents)

# 5. 벡터 저장소 기반의 리트리버 생성
# 분할된 문서와 임베딩 모델을 사용해 FAISS 벡터 저장소를 만들고, 이를 리트리버로 변환
# 리트리버는 질문과 가장 유사한 문서를 찾아주는 역할을 함
retriever = FAISS.from_documents(split_docs, embeddings).as_retriever(
    search_type="similarity",  # 유사도 기반으로 검색
    search_kwargs={"k":1},      # 가장 유사한 문서 1개를 반환
)

# 6. 리트리버 동작 테스트
# "초보자가 배우기 좋은 프로그래밍 언어는?"라는 질문으로 관련 문서를 검색
print("--- 리트리버 검색 결과 ---")
results = retriever.get_relevant_documents("초보자가 배우기 좋은 프로그래밍 언어는?")
for i, doc in enumerate(results, 1):
    print(
        f"{i}. {doc.page_content[:30]}... | 출처: {doc.metadata['source']} | 주제 : {doc.metadata['topic']}"
    )
print("-" * 25)

# 7. 언어 모델(LLM) 및 프롬프트 템플릿 설정
# gpt-5-mini 모델을 사용하는 ChatOpenAI 객체 생성
llm = ChatOpenAI(model_name="gpt-5-mini")
# LLM에게 전달할 프롬프트 템플릿 정의
message = """
질문에 대한 답변을 작성할 때, 리트리버에게 가져온 문서를 참고하여 답변을 작성하세요.

질문:
{question}

참고:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

# 8. RAG 체인 구성 (LCEL 사용)
# LCEL(LangChain Expression Language)을 사용해 RAG 체인을 간결하게 정의
# 체인 실행 순서:
# 1. retriever가 질문에 맞는 문맥(context)을 가져옴
# 2. RunnablePassthrough가 질문(question)을 그대로 전달
# 3. prompt가 context와 question을 받아 LLM에 입력할 프롬프트를 완성
# 4. llm이 완성된 프롬프트를 바탕으로 답변을 생성
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# 9. RAG 체인 실행
# "초보자가 배우기 좋은 프로그래밍 언어는?"라는 질문으로 체인을 실행
response = chain.invoke("초보자가 배우기 좋은 프로그래밍 언어는?")

# 10. 최종 결과 출력
print("\n--- LLM 응답 ---")
print(response.content)

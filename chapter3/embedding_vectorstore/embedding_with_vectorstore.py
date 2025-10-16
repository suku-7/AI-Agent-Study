from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

texts = [
    "파이썬은 배우기 쉬운 프로그래밍 언어입니다.",
    "자바스크립트는 웹 개발에 널리 사용됩니다",
    "꽁꽁 얼어붙은 한강 위로 고양이가 걸어갑니다.",
    "어리석은 자는 멀리서 행복을 찾고, 현명한 자는 자신의 발치에서 행복을 키워간다.",
    "계단을 밟아야 계단 위에 올라설 수 있다",
    "인생은 10%의 사건과 90%의 반응으로 이루어져 있습니다.",
    "성공은 실패를 거듭하는 것이 아니라, 실패를 거듭하면서도 열정을 잃지 않는 겁니다.",
    "하루에 3시간을 걸으면 7년 후에 지구를 한바퀴 돌 수 있습니다.",
    "인공지능은 머신러닝과 딥러닝을 통해 발전하고 있습니다.",
]

vectorstore = FAISS.from_texts(texts, embeddings)

query = "힘이 나는 명언 알려주세요."
docs = vectorstore.similarity_search(query, k=2)
print("검색 결과 : ")
for i, doc in enumerate(docs):
    print(f"{i+1}. {doc.page_content}")

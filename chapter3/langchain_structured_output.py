# Pydantic은 데이터 유효성 검사 및 구조 정의를 위한 라이브러리입니다.
# BaseModel을 상속받아 데이터 구조를 정의하며, Field는 각 필드에 대한 추가 정보를 제공합니다.
from pydantic import BaseModel, Field
# (가상) init_chat_model 함수는 사전 정의된 설정을 사용하여 언어 모델을 초기화합니다.
from langchain.chat_models import init_chat_model

# 언어 모델(LLM)을 초기화합니다. 'gpt-5-mini'는 예시 모델명입니다.
llm = init_chat_model("gpt-5-mini", model_provider="openai")


# 1. Pydantic을 사용하여 원하는 출력 데이터 구조(스키마)를 정의합니다.
# 이 클래스는 LLM이 반환할 결과물의 '설계도' 역할을 합니다.
class MovieReview(BaseModel):
    """ 영화 리뷰 스키마 정의 """
    # Field의 description은 LLM에게 각 필드가 무엇을 의미하는지 알려주는 힌트가 됩니다.
    title: str = Field(description="영화 제목")
    rating: float = Field(description="10점 만점 평점 (예 : 7.5)")
    review: str = Field(description="한글 리뷰 (3~4문장)")


# 2. '.with_structured_output()'을 사용하여 LLM에 출력 스키마(MovieReview)를 연결합니다.
# 이제 이 LLM은 MovieReview 클래스 구조에 맞춰서 결과를 반환하도록 설정됩니다.
structured_llm = llm.with_structured_output(MovieReview)

# 3. 구조화된 출력을 지원하는 LLM을 호출(invoke)합니다.
# LangChain은 내부적으로 '기생충' 리뷰 요청과 MovieReview 스키마 정보를 조합하여 LLM에 전달합니다.
result: MovieReview = structured_llm.invoke(
    "영화 '기생충'에 대한 리뷰를 작성해주세요."
)

# 4. 결과 확인
# 반환된 'result'는 단순 텍스트가 아닌 MovieReview 객체입니다.
# 따라서 '.' 연산자를 통해 각 필드에 직접 접근할 수 있어 매우 편리합니다.
print("영화 제목:", result.title)
print("평점:", result.rating)
print("리뷰:", result.review)
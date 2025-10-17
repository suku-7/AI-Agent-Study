from google.adk.agents import Agent
from pydantic import BaseModel, Field

class BookRecommendation(BaseModel):
    title: str = Field(description="책 제목")
    author: str = Field(description="저자")
    genre: str = Field(description="장르")
    reason: str = Field(description="추천 이유")
    ration: float = Field(description="평점 (1-5)")

class BookList(BaseModel):
    BookRecommendation: list[BookRecommendation]
    total_count: int

root_agent = Agent(
    name="book_recommender",
    model="gemini-2.5-flash",
    description="책을 추천하고 구조화된 형식으로 반환",
    instruction="""사용자의 관심사에 맞는 책을 추천해주세요.
    반드시 지정된 JSON 스키마 형식으로 답변하세요.""",
    output_schema=BookList,
)

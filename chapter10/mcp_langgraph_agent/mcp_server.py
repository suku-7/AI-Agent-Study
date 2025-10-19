import json
import feedparser
import httpx
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from mcp.server.fastmcp import FastMCP
from geopy.geocoders import Nominatim

mcp = FastMCP("Yozm-ai-agent")

@mcp.tool()
def scrape_page_text(url: str) -> str:
    """웹페이지의 텍스트 콘텐츠를 스크랩합니다."""
    resp = httpx.get(url)

    if resp.status_code != 200:
        return f"Failed to fetch {url}"
    soup = BeautifulSoup(resp.text, "html.parser")

    if soup.body:
        text = soup.body.get_text(separator=" ", strip=True)
        return " ".join(text.split())
    return ""

def get_coordinated(city_name: str) -> tuple[float, float]:
    """도시 이름을 받아 위도와 경도를 반환합니다."""
    geolocator = Nominatim(user_agent="weather_app_langgraph")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    raise ValueError(f"좌표를 찾을 수 없습니다: {city_name}")

@mcp.tool()
def get_weather(city_name: str) -> str:
    """도시 이름을 받아 해당 도시의 현재 날씨 정보를 반환합니다."""
    print(f"날씨 조회: {city_name}")
    latitude, longitude = get_coordinated(city_name)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = httpx.get(url)
    result = response.json()
    print(result)
    return json.dumps(result)

@mcp.tool()
def get_news_headlines() -> str:
    """구글 RSS 피드에서 최신 뉴스와 URL을 반환합니다."""
    rss_url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        return "뉴스를 가져올 수 없습니다."
    
    news_list = []
    for i, entry in enumerate(feed.entries, 1):
        title = getattr(entry, "title", "제목 없음")
        link = getattr(entry, "link", "#")

        print(f"뉴스 {i}: {title} - {link}")

        if not title or title == "None":
            title = "제목 없음"
        if not link or link == "None":
            link = "#"
        
        news_item = f"{i}. [{title}]({link})"
        news_list.append(news_item)

    return "\n".join(news_list)

@mcp.tool()
def get_kbo_rank() -> str:
    """한국 프로야구 구단의 랭킹을 가져옵니다"""
    result = httpx.get("https://sports.daum.net/prx/hermes/api/team/rank.json?leagueCode=kbo&seasonKey=2025")
    return result.text

@mcp.tool()
def today_schedule() -> str:
    """임의의 스케줄을 반환합니다."""
    events = ["10:00 팀 미팅", "13:00 점심 약속", "15:00 프로젝트 회의", "19:00 헬스장"]
    return " | ".join(events)

@mcp.tool()
def daily_quote() -> str:
    """사용자에게 영감을 주는 명언을 출력합니다."""
    chat_model = ChatOpenAI(model="gpt-5-mini")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 오늘 하루의 명언을 알려주는 도우미입니다. 사용자의 명언 요청이 있을시 명언만 출력합니다.",
            ),
            ("human", "오늘의 명언을 출력해주세요.")
        ]
    )
    chain = prompt | chat_model
    response = chain.invoke({})
    return response.content

@mcp.tool()
def brief_today() -> str:
    """사용자의 하루 시작을 돕기 위해 날씨, 뉴스, 일정 등을 종합하여 전달합니다."""
    return """
다음을 순서대로 실행하고, 실행한 결과를 사용자에게 알려주세요.
첫째로 사용자가 위치한 도시를 파악하세요. 위치를 모른다면, 사용자에게 질문하세요.
둘째로 사용자의 위치를 기반으로 get_weather 도구를 호출하여 날씨 정보를 찾아서 제공합니다.
셋째로 get_news_headlines 도구를 사용하여 오늘의 주요 뉴스를 출력합니다.
넷째로 get_kbo_rank 도구를 사용하여 현재 시간 프로야구 랭킹 및 전적을 리스트 형태로 출력합니다.
다섯째로 today_schedule 도구를 사용하여 오늘 사용자의 일정을 알려줍니다.
마지막으로 daily_quote을 사용하여 명언을 출력하고, 따뜻한 말 한마디를 덧붙입니다.
출력은 다음과 같이 해주세요.
# 사용자님을 위한 맞춤 요약

### 오늘의 날씨
[get_weather의 결과]

### 오늘자 주요 뉴스
[get_news_haedlines의 결과] (링크를 함께 제공합니다)

### 야구단 랭킹
[get_kbo_rank의 결과]

### 오늘의 업무 일정
[today_schedule의 결과]

### 영감을 주는 격언 한마디
[daily_quote의 결과]
"""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

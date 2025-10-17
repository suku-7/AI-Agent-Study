from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

weather_fetcher = Agent(
    name="weather",
    model="gemini-2.5-flash",
    output_key="weather_info",
    instruction="오늘의 날씨 정보를 제공하세요",
    tools=[google_search],
)

news_fetcher = Agent(
    name="news",
    model="gemini-2.5-flash",
    output_key="news_info",
    instruction="오늘의 주요 뉴스를 요약하세요.",
    tools=[google_search],
)

stock_fetcher = Agent(
    name="stocks",
    model="gemini-2.5-flash",
    output_key="stock_info",
    instruction="주요 주식 시장 동향을 제공하세요.",
    tools=[google_search],
)

parallel_fetcher = ParallelAgent(
    name="multi_info_fetcher",
    sub_agents=[weather_fetcher, news_fetcher, stock_fetcher],
    description="여러 정보를 동시에 수집",
)

summarizer = Agent(
    name="daily_briefing",
    model="gemini-2.5-flash",
    instruction="""
    수집된 정보를 종합하여 일일 브리핑을 작성하세요:
    - 날씨: {weather_info}
    - 뉴스: {news_info}
    - 주식: {stock_info}

    간결하고 읽기 쉬운 형식으로 정리하세요.
    """,
)

daily_briefing_pipeline = SequentialAgent(
    name="daily_briefing_system",
    sub_agents=[parallel_fetcher, summarizer],
    description="정보를 병렬로 수집한 후 종합 브리핑 생성",
)

root_agent = daily_briefing_pipeline
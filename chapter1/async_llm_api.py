import asyncio
import os
import logging
import random

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
claude_client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

async def simulate_random_failure():
    if random.random() < 0.5:
        logger.warning("인위적으로 API 호출 실패 발생(테스트용)")
        raise ConnectionError("인위적으로 발생시킨 연결 오류(테스트용)")
    await asyncio.sleep(random.uniform(0.1, 0.5))

@retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(),
        before_sleep=lambda retry_state: logger.warning(
            f"API 호출 실패: {retry_state.outcome.exception()}, {retry_state.attempt_number}번째 재시도 중..."
        )
)
async def call_async_openai(prompt: str, model: str = "gpt-5-mini") -> str:
    logger.info(f"OpenAI API 호출 시작: {model}")

    await simulate_random_failure()

    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    logger.info("OpenAI API 호출 성공")
    return response.choices[0].message.content

async def call_async_claude(prompt: str, model: str = "claude-3-5-haiku-latest") -> str:
    logger.info(f"Claude API 호출 시작: {model}")
    response = await claude_client.messages.create(
        model=model, max_tokens=1000, messages=[{"role": "user", "content": prompt}]
    )
    logger.info("Claude API 호출 성공")
    return response.content[0].text
async def main():
    print("동시에 API 호출하기 (재시도 로직 포함)")
    prompt = "비동기 프로그래밍에 대해 2-3 문장으로 설명해주세요."
    openai_task = call_async_openai(prompt)
    claude_task = call_async_claude(prompt)

    try:
        openai_response, claude_response = await asyncio.gather(openai_task, claude_task, return_exceptions=False)
        print(f"OpenAI 응답: {openai_response}")
        print(f"Claude 응답: {claude_response}")
    except Exception as e:
        logger.error(f"API 호출 중 처리되지 않은 오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
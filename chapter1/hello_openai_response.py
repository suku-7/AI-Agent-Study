from openai import OpenAI
client = OpenAI()

def get_responses(prompt, model="gpt-5-mini"):
    response = client.responses.create(
        model=model,
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )
    return response.output_text

if __name__ == '__main__':
    prompt = """
https://platform.openai.com/docs/api-reference/responses/create를 읽어서 리스폰스 API에 대해 요약 정리해주세요.
"""
    output = get_responses(prompt)
    print(output)
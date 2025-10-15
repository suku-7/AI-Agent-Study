from openai import OpenAI
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
client = OpenAI()

LITTLE_PRINCE_PERSONA = """
당신은 생텍쥐페리의 '어린 왕자'입니다. 다음 특성을 따라주세요:
1. 순수한 관점으로 세상을 바라봅니다.
2. "어째서?"라는 질문을 자주 하며 호기심이 많습니다.
3. 철학적 통찰을 단순하게 표현합니다.
4. "어른들은 참 이상해요"라는 표현을 씁니다.
5. B-612 소행성에서 왔으며 장미와의 관계를 언급합니다.
6. 여우의 "길들임"과 "책임"에 대한 교훈을 중요시합니다.
7. "중요한 것은 눈에 보이지 않아"라는 문장을 사용합니다.
8. 공손하고 친절한 말투를 사용합니다.
9. 비유와 은유로 복잡한 개념을 설명합니다.
항상 간결하게 답변하세요. 길어야 두세 문장으로 응답하고, 어린 왕자의 순수함과 지혜를 담아내세요.
복잡한 주제도 본질적으로 단순화하여 설명하세요.
"""

messages = []
previous_response_id = None

def chatbot_response(user_message: str, previous_response_id=None):
    result = client.responses.create(
        model="gpt-5-mini",
        reasoning={"effort": "low"},
        instructions=LITTLE_PRINCE_PERSONA,
        input=user_message,
        previous_response_id=previous_response_id,
    )
    return result

@app.get("/", response_class=HTMLResponse)
async def read_root():
    chat_history = ""
    for msg in messages:
        if msg["role"] == "user":
            chat_history += f"<p><b>당신:</b> {msg['content']}</p>"
        else:
            chat_history += f"<p><b>어린 왕자:</b> {msg['content']}</p>"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>어린 왕자 챗봇</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>어린 왕자 챗봇</h1>
        <div>
            {chat_history}
        </div>
        <form action="/chat" method="post">
            <input type="text" name="message" placeholder="메세지를 입력하세요..." required>
            <button type="submit">전송</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    global previous_response_id, messages

    messages.append({"role": "user", "content": message})
    result = chatbot_response(message, previous_response_id)
    previous_response_id = result.id
    messages.append({"role": "little_prince", "content": result.output_text})

    return await read_root()

if __name__ == "__main__":
    uvicorn.run(
        "chatbot4_little_prince_web_ui:app", host="127.0.0.1", port=8000, reload=True
    )

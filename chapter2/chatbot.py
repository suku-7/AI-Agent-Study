from openai import OpenAI

client = OpenAI()

def chatbot_response(user_message:str):
    result = client.responses.create(model="gpt-5-mini", input=user_message)
    return result

if __name__ == "__main__":
    while True:
        user_message = input("메세지:")
        if user_message.lower() == "exit":
            print("대화를 종료합니다.")
            break
        
        result = chatbot_response(user_message)
        print("챗봇 :" + result.output_text)
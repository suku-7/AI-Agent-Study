from openai import OpenAI

client = OpenAI()

def chatbot_response(user_message:str, previous_response_id=None):
    result = client.responses.create(model="gpt-5-mini", input=user_message, previous_response_id=previous_response_id)
    return result

if __name__ == "__main__":
    previous_response_id = None

    while True:
        user_message = input("메세지:")
        if user_message.lower() == "exit":
            print("대화를 종료합니다.")
            break
        
        result = chatbot_response(user_message, previous_response_id)
        previous_response_id = result.id
        print("챗봇 :" + result.output_text)
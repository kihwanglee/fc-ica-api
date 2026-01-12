import os                                                                               
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def start_chat():
    chat = client.chats.create(model="gemini-2.5-flash")
    
    # 첫 번째 질문
    response1 = chat.send_message("안녕! 나는 파이썬 개발자야.")
    print(f"AI: {response1.text}")
    
    # 두 번째 질문 (이전 맥락 유지)
    response2 = chat.send_message("내가 방금 나를 누구라고 소개했었지?")
    print(f"AI: {response2.text}")

start_chat()

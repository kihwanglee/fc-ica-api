import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_text():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="인공지능의 미래에 대해 짧게 설명해줘."
    )
    print("--- 텍스트 생성 결과 ---")
    print(response.text)

if __name__ == "__main__":
    generate_text()
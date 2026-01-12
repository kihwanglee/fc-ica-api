import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- 사용 가능한 모델 목록 ---")
try:
    # 내 키로 권한이 있는 모델들을 출력합니다.
    for model in client.models.list():
        print(f"Model Name: {model.name}")
except Exception as e:
    print(f"오류 발생: {e}")
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="인공지능의 미래에 대해 짧게 설명해줘.",
    )
    print("--- 텍스트 생성 결과 ---")
    print(response.output_text)


if __name__ == "__main__":
    generate_text()

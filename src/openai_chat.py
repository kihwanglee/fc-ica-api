import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def start_chat():
    messages = [{"role": "user", "content": "안녕! 나는 파이썬 개발자야."}]

    response1 = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
    )
    print(f"AI: {response1.output_text}")

    messages.append({"role": "assistant", "content": response1.output_text})
    messages.append({"role": "user", "content": "내가 방금 나를 누구라고 소개했었지?"})

    response2 = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
    )
    print(f"AI: {response2.output_text}")


if __name__ == "__main__":
    start_chat()

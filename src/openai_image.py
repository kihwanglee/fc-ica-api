import base64
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image_to_data_url(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def analyze_image():
    image_path = Path(__file__).resolve().parent / "sample_image.jpg"
    image_url = encode_image_to_data_url(str(image_path))

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "이 사진의 분위기와 주요 사물을 설명해줘."},
                    {"type": "input_image", "image_url": image_url},
                ],
            }
        ],
    )

    print("--- 이미지 분석 결과 ---")
    print(response.output_text)


if __name__ == "__main__":
    analyze_image()

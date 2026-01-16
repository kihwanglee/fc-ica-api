import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

def analyze_image():
    # 이미지 파일 로드
    image_path = Path(__file__).resolve().parent / "sample_image.jpg"
    img = Image.open(image_path)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=["이 사진의 분위기와 주요 사물을 설명해줘.", img]
    )
    print("--- 이미지 분석 결과 ---")
    print(response.text)

analyze_image()

# 🚀 Google AI API (Gemini 2.5) 사용 가이드

이 문서는 최신 `google-genai` 라이브러리를 사용하여 텍스트 생성, 멀티모달(이미지) 분석, 그리고 대화형 세션을 구현하는 방법을 다룹니다.

---

## 1. 환경 준비

### 1.1 API 키 발급

1. [Google AI Studio](https://aistudio.google.com/)에서 API 키를 발급받습니다.
2. 프로젝트 루트 폴더에 `.env` 파일을 생성하고 키를 저장합니다.
```text
GOOGLE_API_KEY=your_actual_api_key_here
```



### 1.2 라이브러리 설치

```bash
pip install -U google-genai python-dotenv pillow
```

---

## 2. 기본 텍스트 생성 (Basic Text Generation)

가장 기본적인 텍스트 질문-답변 예제입니다.

```python
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
```

---

## 3. 멀티모달 입력 (Multimodal: Text & Image)

텍스트와 이미지를 동시에 입력하여 이미지를 분석하는 예제입니다.

```python
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
```

---

## 4. 대화형 세션 (Chat Session)

이전 대화 맥락을 유지하면서 상호작용하는 채팅 예제입니다.

```python
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
```

---

## 5. 핵심 기능 요약

| 기능 | 사용 메서드 | 특징 |
| --- | --- | --- |
| **텍스트 생성** | `client.models.generate_content()` | 단발성 질문 및 요청 처리 |
| **멀티모달** | `contents=[text, image]` | 이미지, 문서 등 복합 데이터 분석 |
| **채팅 세션** | `client.chats.create()` | 대화 히스토리를 자동으로 관리 |


# 🚀 OpenAI API 사용 가이드

이 문서는 최신 `openai` 라이브러리를 사용하여 텍스트 생성, 멀티모달(이미지) 분석, 그리고 대화형 세션을 구현하는 방법을 다룹니다.

---

## 1. 환경 준비

### 1.1 API 키 발급

1. [OpenAI Platform](https://platform.openai.com/)에서 API 키를 발급받습니다.
2. 프로젝트 루트 폴더에 `.env` 파일을 생성하고 키를 저장합니다.
```text
OPENAI_API_KEY=your_actual_api_key_here
```



### 1.2 라이브러리 설치

```bash
pip install -U openai python-dotenv pillow
```

---

## 2. 기본 텍스트 생성 (Basic Text Generation)

가장 기본적인 텍스트 질문-답변 예제입니다.

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="인공지능의 미래에 대해 짧게 설명해줘."
    )
    print("--- 텍스트 생성 결과 ---")
    print(response.output_text)

if __name__ == "__main__":
    generate_text()
```

---

## 3. 멀티모달 입력 (Multimodal: Text & Image)

텍스트와 이미지를 동시에 입력하여 이미지를 분석하는 예제입니다.

```python
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

analyze_image()
```

---

## 4. 대화형 세션 (Chat Session)

이전 대화 맥락을 유지하면서 상호작용하는 채팅 예제입니다.

```python
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

start_chat()
```

---

## 5. 핵심 기능 요약

| 기능 | 사용 메서드 | 특징 |
| --- | --- | --- |
| **텍스트 생성** | `client.responses.create()` | 단발성 질문 및 요청 처리 |
| **멀티모달** | `input=[text, image]` | 이미지, 문서 등 복합 데이터 분석 |
| **채팅 세션** | `input=messages` | 대화 히스토리를 직접 관리 |

# fc-ica-api

## 개요

- FC ICA 6 기획-개발 라이브 세션
- API의 이해와 활용

## 문서 안내

- `doc/api_guide.md` : 전체 API 개요 및 사용 흐름
- `doc/openai_guide.md` : OpenAI API 사용 가이드 및 예제
- `doc/gemini_guide.md` : Google Gemini API 사용 가이드 및 예제
- `doc/google_oauth_guide.md` : Google OAuth 설정 가이드

## 프로젝트 설정 가이드

### 1. 가상환경 생성 (venv)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

1. 프로젝트 루트에 `.env` 파일을 생성합니다.
2. `.env` 파일을 열고 실제 API 키 입력:
   - OpenAI API 키: https://platform.openai.com/api-keys
   - Google AI 키: https://aistudio.google.com/
   - GitHub Token: https://github.com/settings/tokens
   - Kakao API 키: https://developers.kakao.com

### 4. 보안 주의사항

- ⚠️ `.env` 파일은 절대 Git에 커밋하지 마세요!
- ⚠️ API 키를 코드에 직접 작성하지 마세요!
- ⚠️ API 키가 노출되면 즉시 재발급하세요!

### 5. 실행 방법 (.env 적용)

- `python-dotenv`를 사용하므로, **프로젝트 루트에서 실행**해야 `.env`가 정상 로드됩니다.
- 필요한 키를 `.env`에 입력한 뒤 아래처럼 실행하세요.

```bash
# 예시: OpenAI 텍스트
python src/openai_text.py

# 예시: OpenAI 이미지
python src/openai_image.py

# 예시: Gemini 이미지
python src/gemini_image.py

# 예시: 날씨 API 실행
python src/openweathermap.py

# 예시: 깃허브 API 실행
python src/github.py
```

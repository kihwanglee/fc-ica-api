# fc-ica-api

## 개요

- FC ICA 6 기획-개발 특강 (3)
- API의 이해와 활용

## 프로젝트 설정 가이드

### 1. 환경 변수 설정

1. `.env.example` 파일을 복사하여 `.env` 파일 생성:
```bash
   cp .env.example .env
```

2. `.env` 파일을 열고 실제 API 키 입력:
   - OpenAI API 키: https://platform.openai.com/api-keys
   - GitHub Token: https://github.com/settings/tokens
   - Kakao API 키: https://developers.kakao.com

3. 필수 라이브러리 설치:
```bash
   pip install python-dotenv requests
```

### 2. 보안 주의사항

- ⚠️ `.env` 파일은 절대 Git에 커밋하지 마세요!
- ⚠️ API 키를 코드에 직접 작성하지 마세요!
- ⚠️ API 키가 노출되면 즉시 재발급하세요!

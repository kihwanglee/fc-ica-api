"""
Google OAuth 2.0 로그인 예제 (FastAPI)

이 예제는 Google OAuth 2.0을 사용하여 사용자 인증을 구현합니다.

사용 방법:
1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID 및 시크릿을 발급받습니다.
2. .env 파일에 다음 환경 변수를 설정합니다:
   - GOOGLE_CLIENT_ID
   - GOOGLE_CLIENT_SECRET
   - GOOGLE_REDIRECT_URI (예: http://localhost:8000/callback)
3. 다음 명령어로 서버를 실행합니다:
   python src/google_oauth.py
4. 브라우저에서 http://localhost:8000/login 으로 접속합니다.
"""

import requests
import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import urllib.parse
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = FastAPI(title="Google OAuth 2.0 예제", description="FastAPI를 사용한 Google 로그인 예제")

# 환경 변수에서 설정 로드
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/callback')


@app.get("/")
def read_root():
    """홈 페이지"""
    return {
        "message": "Google OAuth 2.0 예제 API",
        "endpoints": {
            "/login": "Google 로그인 페이지로 리다이렉트",
            "/callback": "Google OAuth 콜백 처리"
        }
    }


@app.get('/login')
def login_with_google():
    """
    Google 로그인 페이지로 리다이렉트
    
    사용자를 Google OAuth 인증 페이지로 보냅니다.
    """
    if not GOOGLE_CLIENT_ID:
        return JSONResponse(
            content={"error": "환경 변수 GOOGLE_CLIENT_ID가 설정되지 않았습니다."},
            status_code=500
        )
    
    scope = 'profile email'
    
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': scope
    }
    
    auth_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params)
    return RedirectResponse(url=auth_url)


@app.get('/callback')
def handle_callback(request: Request):
    """
    OAuth 콜백 처리
    
    Google에서 리다이렉트된 인증 코드를 받아 액세스 토큰으로 교환하고,
    사용자 정보를 가져옵니다.
    """
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET]):
        return JSONResponse(
            content={"error": "환경 변수가 설정되지 않았습니다."},
            status_code=500
        )
    
    code = request.query_params.get('code')
    
    if not code:
        return JSONResponse(
            content={"error": "인증 코드가 제공되지 않았습니다."},
            status_code=400
        )
    
    # 액세스 토큰 교환
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    try:
        token_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data=token_data
        )
        
        if token_response.status_code != 200:
            return JSONResponse(
                content={
                    "error": "토큰 교환 실패",
                    "details": token_response.text
                },
                status_code=token_response.status_code
            )
        
        access_token = token_response.json()['access_token']
        
        # 액세스 토큰으로 사용자 정보 조회
        user_info_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if user_info_response.status_code != 200:
            return JSONResponse(
                content={
                    "error": "사용자 정보 조회 실패",
                    "details": user_info_response.text
                },
                status_code=user_info_response.status_code
            )
        
        user = user_info_response.json()
        print(f"로그인 성공: {user.get('email', 'N/A')}")
        
        return JSONResponse(content=user)
    
    except requests.exceptions.RequestException as e:
        return JSONResponse(
            content={"error": "API 요청 중 오류 발생", "details": str(e)},
            status_code=500
        )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

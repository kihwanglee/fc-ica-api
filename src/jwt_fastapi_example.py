"""
JWT 인증 예제 (FastAPI)

이 예제는 JWT 토큰을 발급하고 보호된 API를 호출하는 기본 흐름을 보여줍니다.

사용 방법:
1. .env 파일에 다음 환경 변수를 설정합니다:
   - JWT_SECRET_KEY
2. JWT_SECRET_KEY 생성 방법 (택1):
   - python -c "import secrets; print(secrets.token_urlsafe(32))"
   - openssl rand -hex 32
3. 다음 명령어로 서버를 실행합니다:
   python src/jwt_fastapi_example.py
"""

import os
from datetime import datetime, timedelta

import jwt
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("환경 변수 JWT_SECRET_KEY가 설정되지 않았습니다.")

security = HTTPBearer()


def generate_token(user):
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(
    credentials=Depends(security),
):
    token = credentials.credentials
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다.",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
        ) from exc


@app.post("/login")
def login(payload):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="이메일과 비밀번호가 필요합니다.")

    user = {"id": 1, "email": email, "role": "user"}
    token = generate_token(user)
    return {"token": token}


@app.get("/protected-data")
def protected_data(user=Depends(verify_token)):
    return {"message": "인증 성공!", "user": user}


def login_and_use_api(email, password):
    login_response = requests.post(
        "https://api.example.com/login",
        json={"email": email, "password": password},
    )
    token = login_response.json()["token"]

    data_response = requests.get(
        "https://api.example.com/protected-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    return data_response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
JWT 로그인 클라이언트 예제

사용 방법:
1) 서버 실행: python src/jwt_fastapi_example.py
2) 클라이언트 실행: python src/jwt_login_client.py
"""

import json

import requests

BASE_URL = "http://localhost:8000"


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["token"]


def fetch_protected_data(token):
    response = requests.get(
        f"{BASE_URL}/protected-data",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    token = login("test@example.com", "pass1234")
    data = fetch_protected_data(token)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

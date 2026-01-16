import os

import requests
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_REST_API_KEY")


def search_address(query):
    """카카오 로컬 주소 검색 API 호출"""
    if not KAKAO_API_KEY:
        print("환경 변수 KAKAO_REST_API_KEY가 설정되지 않았습니다.")
        return None

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": query}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"API 요청 실패: {exc}")
        return None

    data = response.json()
    return data.get("documents", [])


if __name__ == "__main__":
    results = search_address("서울시 강남구 테헤란로")
    if results:
        print(results)

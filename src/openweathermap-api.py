import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
city = 'Seoul'

def get_weather():
    if not API_KEY:
        print("환경 변수 OPENWEATHER_API_KEY가 설정되지 않았습니다.")
        return
    
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'kr'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"{city} 날씨: {data['weather'][0]['description']}")
    print(f"온도: {data['main']['temp']}°C")

get_weather()
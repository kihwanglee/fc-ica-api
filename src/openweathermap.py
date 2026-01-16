import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    def get_weather(self, city):
        """특정 도시의 날씨 정보 조회"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'kr'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'날씨 정보 조회 실패: {e}')
            return None
    
    def display_weather(self, city):
        """날씨 정보를 보기 좋게 출력"""
        data = self.get_weather(city)
        
        if not data:
            return
        
        print(f"\n{'='*40}")
        print(f"📍 {city} 날씨 정보")
        print(f"{'='*40}")
        print(f"🌡️  온도: {data['main']['temp']}°C")
        print(f"🌡️  체감 온도: {data['main']['feels_like']}°C")
        print(f"☁️  날씨: {data['weather'][0]['description']}")
        print(f"💧 습도: {data['main']['humidity']}%")
        print(f"💨 풍속: {data['wind']['speed']}m/s")
        print(f"{'='*40}\n")
    
    def compare_cities(self, cities):
        """여러 도시의 날씨 비교"""
        print("\n🌍 도시별 날씨 비교\n")
        
        for city in cities:
            self.display_weather(city)

# 사용 예시
if __name__ == '__main__':
    dashboard = WeatherDashboard()
    
    # 한 도시 조회
    dashboard.display_weather('Seoul')
    
    # 여러 도시 비교
    cities = ['Seoul', 'Busan', 'Jeju', 'Tokyo', 'New York']
    dashboard.compare_cities(cities)
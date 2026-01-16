import requests
import os
from collections import Counter
import re
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

class NewsAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        
        if not self.api_key:
            raise ValueError("환경 변수 NEWS_API_KEY가 설정되지 않았습니다.")
    
    def search_news(self, query, language='ko', page_size=100):
        """뉴스 검색"""
        url = f'{self.base_url}/everything'
        params = {
            'q': query,
            'language': language,
            'pageSize': page_size,
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'뉴스 검색 실패: {e}')
            return None
    
    def extract_keywords(self, text, top_n=10):
        """텍스트에서 키워드 추출"""
        # 한글, 영문만 추출 (최소 2글자)
        words = re.findall(r'[가-힣]{2,}|[a-zA-Z]{3,}', text)
        
        # 불용어 제거 (간단한 예시)
        stopwords = {'그리고', '하지만', '그래서', '있다', '되다', '하다'}
        words = [w for w in words if w not in stopwords]
        
        # 빈도 계산
        word_counts = Counter(words)
        return word_counts.most_common(top_n)
    
    def analyze_news_trends(self, query):
        """뉴스 트렌드 분석"""
        data = self.search_news(query)
        
        if not data or data['totalResults'] == 0:
            print('뉴스를 찾을 수 없습니다.')
            return
        
        articles = data['articles']
        
        # 모든 기사 제목과 설명 합치기
        all_text = ' '.join([
            (article.get('title', '') + ' ' + article.get('description', ''))
            for article in articles
        ])
        
        # 키워드 추출
        keywords = self.extract_keywords(all_text, top_n=15)
        
        print(f"\n📰 '{query}' 관련 뉴스 분석")
        print(f"{'='*40}")
        print(f"총 기사 수: {data['totalResults']}")
        print(f"\n주요 키워드:")
        
        for word, count in keywords:
            print(f"  {word}: {count}회")
        
        print(f"\n최신 뉴스 3건:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   출처: {article['source']['name']}")
            print(f"   링크: {article['url']}")

# 사용 예시
if __name__ == '__main__':
    try:
        analyzer = NewsAnalyzer()
        analyzer.analyze_news_trends('인공지능')
    except ValueError as e:
        print(f"오류: {e}")
        print("News API 키를 발급받으세요: https://newsapi.org")
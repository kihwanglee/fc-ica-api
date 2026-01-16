import requests
import os
from dotenv import load_dotenv
from collections import Counter

# .env 파일에서 환경 변수 로드
load_dotenv()

class GitHubAnalyzer:
    def __init__(self):
        self.token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # 토큰이 있을 때만 Authorization 헤더 추가
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
            print("✅ GitHub 토큰 로드됨")
        else:
            print("⚠️  환경 변수 GITHUB_PERSONAL_ACCESS_TOKEN이 설정되지 않았습니다.")
            print("   토큰 없이도 사용 가능하지만 시간당 60회로 제한됩니다.")
    
    def get_user_repos(self, username):
        """사용자의 모든 레포지토리 조회"""
        repos = []
        page = 1
        
        while True:
            url = f'{self.base_url}/users/{username}/repos'
            params = {
                'page': page,
                'per_page': 100,
                'sort': 'updated'
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                
                # 에러 처리
                if response.status_code != 200:
                    print(f"❌ API 요청 실패: HTTP {response.status_code}")
                    if response.status_code == 401:
                        print("   토큰이 유효하지 않습니다. .env 파일의 토큰을 확인하세요.")
                    elif response.status_code == 403:
                        print("   API 사용량 제한 초과")
                        print(f"   남은 요청: {response.headers.get('X-RateLimit-Remaining')}")
                    elif response.status_code == 404:
                        print(f"   사용자 '{username}'를 찾을 수 없습니다.")
                    return []
                
                data = response.json()
                
                if not data:
                    break
                
                repos.extend(data)
                page += 1
                
                # 100개 미만이면 마지막 페이지
                if len(data) < 100:
                    break
                
            except requests.exceptions.RequestException as e:
                print(f"❌ 요청 오류: {e}")
                return []
        
        return repos
    
    def analyze_languages(self, username):
        """사용 언어 통계 분석"""
        repos = self.get_user_repos(username)
        
        if not repos:
            print(f"\n❌ '{username}'의 레포지토리를 가져올 수 없습니다.")
            return
        
        # 언어별 레포지토리 수 집계
        languages = [repo['language'] for repo in repos if repo['language']]
        language_counts = Counter(languages)
        
        print(f"\n👤 {username}의 언어 사용 통계")
        print(f"{'='*40}")
        print(f"총 레포지토리 수: {len(repos)}")
        print(f"언어 정보 있는 레포지토리: {len(languages)}")
        
        if language_counts:
            print(f"\n사용 언어 순위:")
            for lang, count in language_counts.most_common(10):
                percentage = (count / len(repos)) * 100
                print(f"  {lang:15s}: {count:3d}개 ({percentage:5.1f}%)")
        else:
            print("\n⚠️  언어 정보가 없습니다.")
    
    def get_popular_repos(self, username, top_n=5):
        """인기 레포지토리 조회 (스타 수 기준)"""
        repos = self.get_user_repos(username)
        
        if not repos:
            print(f"\n❌ '{username}'의 레포지토리를 가져올 수 없습니다.")
            return
        
        # 스타 수로 정렬
        sorted_repos = sorted(
            repos,
            key=lambda x: x['stargazers_count'],
            reverse=True
        )[:top_n]
        
        print(f"\n⭐ 인기 레포지토리 Top {top_n}")
        print(f"{'='*40}")
        
        for i, repo in enumerate(sorted_repos, 1):
            print(f"\n{i}. {repo['name']}")
            print(f"   ⭐ Stars: {repo['stargazers_count']:,}")
            print(f"   🍴 Forks: {repo['forks_count']:,}")
            print(f"   📝 언어: {repo['language'] or 'N/A'}")
            
            if repo['description']:
                desc = repo['description'][:80]
                print(f"   📄 {desc}{'...' if len(repo['description']) > 80 else ''}")
    
    def get_contribution_stats(self, username):
        """기여 통계"""
        repos = self.get_user_repos(username)
        
        if not repos:
            print(f"\n❌ '{username}'의 레포지토리를 가져올 수 없습니다.")
            return
        
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        
        print(f"\n📊 기여 통계")
        print(f"{'='*40}")
        print(f"총 레포지토리: {len(repos):,}")
        print(f"총 스타 수: {total_stars:,}")
        print(f"총 포크 수: {total_forks:,}")
        print(f"평균 스타/레포: {total_stars/len(repos):.1f}")

# 사용 예시
if __name__ == '__main__':
    analyzer = GitHubAnalyzer()
    
    username = 'torvalds'  # 분석할 GitHub 사용자명
    
    analyzer.analyze_languages(username)
    analyzer.get_popular_repos(username, top_n=5)
    analyzer.get_contribution_stats(username)
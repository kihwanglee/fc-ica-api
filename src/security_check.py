# security_check.py
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_security():
    """보안 설정 확인"""
    issues = []
    
    # 1. .env 파일이 .gitignore에 있는지 확인
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' not in gitignore_content:
                issues.append("⚠️  .gitignore에 .env가 추가되지 않았습니다!")
    else:
        issues.append("⚠️  .gitignore 파일이 없습니다!")
    
    # 2. 필수 환경 변수 확인
    required_vars = [
        'OPENAI_API_KEY',
        'JWT_SECRET_KEY',
    ]
    
    for var in required_vars:
        if not os.getenv(var):
            issues.append(f"⚠️  필수 환경 변수 {var}가 설정되지 않았습니다!")
    
    # 3. JWT 비밀키 강도 확인
    jwt_secret = os.getenv('JWT_SECRET_KEY', '')
    if len(jwt_secret) < 32:
        issues.append("⚠️  JWT_SECRET_KEY가 너무 짧습니다! (최소 32자 권장)")
    
    # 결과 출력
    if issues:
        print("🔒 보안 문제 발견:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print("✅ 모든 보안 체크 통과!")
        return True

if __name__ == '__main__':
    if not check_security():
        sys.exit(1)
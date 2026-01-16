import requests
from datetime import datetime

class CurrencyConverter:
    def __init__(self):
        # 무료 API: exchangerate-api.com
        self.base_url = 'https://api.exchangerate-api.com/v4/latest'
        self.cache = {}
    
    def get_rates(self, base='USD'):
        """환율 정보 조회 (캐싱 포함)"""
        # 캐시 확인
        if base in self.cache:
            return self.cache[base]
        
        try:
            response = requests.get(f'{self.base_url}/{base}')
            response.raise_for_status()
            data = response.json()
            
            # 캐시 저장
            self.cache[base] = data
            return data
        except requests.RequestException as e:
            print(f'환율 정보 조회 실패: {e}')
            return None
    
    def convert(self, amount, from_currency, to_currency):
        """통화 변환"""
        rates_data = self.get_rates(from_currency)
        
        if not rates_data:
            return None
        
        rate = rates_data['rates'].get(to_currency)
        
        if not rate:
            print(f'{to_currency} 환율 정보 없음')
            return None
        
        converted = amount * rate
        
        print(f"\n💱 환율 변환 결과")
        print(f"{'='*40}")
        print(f"{amount:,.2f} {from_currency} = {converted:,.2f} {to_currency}")
        print(f"환율: 1 {from_currency} = {rate:.4f} {to_currency}")
        print(f"업데이트 시간: {rates_data['date']}")
        print(f"{'='*40}\n")
        
        return converted
    
    def compare_currencies(self, amount, base, targets):
        """여러 통화로 동시 변환"""
        print(f"\n💰 {amount} {base} →")
        print(f"{'='*40}")
        
        for target in targets:
            result = self.convert(amount, base, target)

# 사용 예시
if __name__ == '__main__':
    converter = CurrencyConverter()
    
    # 단일 변환
    converter.convert(10000, 'KRW', 'USD')
    
    # 여러 통화로 변환
    converter.compare_currencies(
        amount=1000000,
        base='KRW',
        targets=['USD', 'EUR', 'JPY', 'CNY']
    )
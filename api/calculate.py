# api/calculate.py (지역별 차등 적용 강화 버전)
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import sys
import os

# 중요: engine 폴더의 파일을 찾을 수 있도록 경로를 설정합니다.
current_dir = os.path.dirname(__file__)
engine_path = os.path.join(current_dir, '..', 'engine')
if engine_path not in sys.path:
    sys.path.append(engine_path)

# 우리가 만든 도구들을 불러옵니다.
try:
    from download_metsis_solar_data import fetch_solar_data
    from parse_kepco_grid_report import get_grid_efficiency
except ImportError:
    # 파일을 못 찾을 경우를 대비한 기본 함수 정의
    def fetch_solar_data(region): return 1.1 if "서울" in region else 1.4
    def get_grid_efficiency(region): return 1.2 if "서울" in region else 1.1

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        kwh_str = query_components.get("kwh", ["0"])[0]
        addr = query_components.get("addr", [""])[0]
        
        kwh = float(kwh_str)

        # 1. 지역별로 다른 계수를 가져옵니다.
        # 서울이면 L=1.2, R=1.1 / 제주면 L=1.1, R=1.4 정도로 작동할 거예요.
        L = get_grid_efficiency(addr)  # 송전 효율 [cite: 106]
        R = fetch_solar_data(addr)      # 재생에너지 신뢰도/일사량 [cite: 106]
        
        # 2. 고정 계수
        T = 1.5  # 시간대 가중치 [cite: 106]
        C = 1.1  # 탄소 저감 가치 [cite: 106]

        # 3. 최종 VT 계산 (VT = E * L * T * C * R) [cite: 105]
        result_vt = kwh * L * T * C * R
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "vt": round(result_vt, 2),
            "address": addr,
            "details": {
                "location_factor": L,
                "solar_factor": R,
                "formula": "E * L * T * C * R"
                # ... 기존 계산 로직 아래에 추가 ...
        
        # 1 VT당 예상 가격 (예: 250원) [cite: 123]
        vix_price = 250 
        estimated_revenue = round(result_vt * vix_price, 0)

        response_data = {
            "vt": round(result_vt, 2),
            "address": addr,
            "revenue": format(int(estimated_revenue), ','), # 천 단위 콤마
            "details": {
                "location_factor": L,
                "solar_factor": R,
                "vix_price": vix_price
            }
        }
            }
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
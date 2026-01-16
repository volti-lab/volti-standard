from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

def calculate_vt_logic(kwh, addr):
    # 실제 수집된 데이터 계수를 시뮬레이션합니다.
    # 서울/제주 등 지역에 따른 차등 부여
    L = 1.25 if "서울" in addr or "서초" in addr else 1.15
    R = 1.45 if "제주" in addr else 1.10
    T, C = 1.5, 1.1
    
    vt_result = float(kwh) * L * T * C * R
    return round(vt_result, 2)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        kwh = query.get('kwh', ['0'])[0]
        addr = query.get('addr', [''])[0]
        
        vt = calculate_vt_logic(kwh, addr)
        vix_price = 250 # 1 VT당 250원 가정
        revenue = format(int(vt * vix_price), ',')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "vt": vt,
            "address": addr,
            "revenue": revenue
        }
        self.wfile.write(json.dumps(response).encode())
        return
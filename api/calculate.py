from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# Volti 핵심 공식 (기획서 Step 1 반영)
def calculate_vt_logic(kwh, addr):
    # 기본 계수: Location(1.2), Time(1.5), Carbon(1.1), Renewable(1.0) [cite: 105, 106]
    L, T, C, R = 1.2, 1.5, 1.1, 1.0
    vt_result = float(kwh) * L * T * C * R
    return round(vt_result, 2)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. 사용자가 보낸 주소와 발전량 데이터를 읽습니다.
        query_components = parse_qs(urlparse(self.path).query)
        kwh = query_components.get("kwh", ["0"])[0]
        addr = query_components.get("addr", [""])[0]

        # 2. 파이썬 로직으로 계산합니다.
        result_vt = calculate_vt_logic(kwh, addr)

        # 3. 결과를 다시 브라우저로 보냅니다.
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            "vt": result_vt,
            "address": addr
        }
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
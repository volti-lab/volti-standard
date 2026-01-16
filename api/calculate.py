from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

def calculate_vt_logic(kwh, addr, months):
    # 변동 계수 설정 (분석 로그용)
    L = 1.25 if "서울" in addr or "서초" in addr else 1.15
    R = 1.45 if "제주" in addr else 1.10
    T, C = 1.5, 1.1
    # 노후도 감가상각 (준공 후 기간에 따른 차등)
    age_factor = 1.0 if int(months) <= 1 else 0.95
    
    vt_result = float(kwh) * L * T * C * R * age_factor
    return {
        "vt": round(vt_result, 2),
        "factors": {"L": L, "T": T, "C": C, "R": R, "Age": age_factor}
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        kwh = query.get('kwh', ['0'])[0]
        addr = query.get('addr', [''])[0]
        months = query.get('months', ['1'])[0]
        
        result = calculate_vt_logic(kwh, addr, months)
        vix_price = 250 
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "vt": result["vt"],
            "revenue": format(int(result["vt"] * vix_price), ','),
            "log": result["factors"]
        }
        self.wfile.write(json.dumps(response).encode())
        return
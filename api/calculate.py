from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

def calculate_vt_logic(kwh, addr, months, method):
    # 변동 계수 설정
    L = 1.25 if "서울" in addr or "서초" in addr else 1.15
    R = 1.45 if "제주" in addr else 1.10
    T, C = 1.5, 1.1
    
    # 노후도 감가상각 (준공 후 기간에 따른 차등)
    age_factor = 1.0 
    if int(months) == 12: age_factor = 0.98 # 1년 미만 소폭 감가
    elif int(months) == 36: age_factor = 0.95 # 3년 이상 감가

    # 생산 방법에 따른 추가 가중치 (희소성, 안정성, 환경성)
    method_factor = 1.0
    if method == "solar": method_factor = 1.05 # 보편적, 탄소 저감 우수
    elif method == "wind": method_factor = 1.10 # 지역 특성, 고효율 가능
    elif method == "hydro": method_factor = 1.15 # 안정적, 환경 영향 최소
    elif method == "geothermal": method_factor = 1.20 # 가장 안정적, 희소성 높음
    elif method == "etc": method_factor = 1.0 # 기타 재생에너지

    vt_result = float(kwh) * L * T * C * R * age_factor * method_factor
    return {
        "vt": round(vt_result, 2),
        "factors": {"L": L, "T": T, "C": C, "R": R, "Age": age_factor, "Method": method_factor}
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        kwh = query.get('kwh', ['0'])[0]
        addr = query.get('addr', [''])[0]
        months = query.get('months', ['1'])[0]
        method = query.get('method', ['solar'])[0] # 생산 방법 기본값 추가
        
        result = calculate_vt_logic(kwh, addr, months, method) # method 인자 전달
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
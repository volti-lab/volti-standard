import datetime
import uuid

def create_vt_certificate(addr, kwh, vt_value):
    """
    Volti 인증서 정보를 생성합니다.
    (나중에 PDF 생성 라이브러리와 연결될 부분입니다.)
    """
    cert_id = str(uuid.uuid4())[:8].upper() # 고유 ID 생성
    issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    certificate_content = f"""
    ======= [Volti Verified Certificate] =======
    인증서 번호: VT-{cert_id}
    발행 일자: {issue_date}
    발전 지역: {addr}
    발전량: {kwh} kWh
    최종 Volti 가치: {vt_value} VT
    -------------------------------------------
    "이 VT는 지역 상생과 탄소 저감을 위해 기여한 
    가치 있는 에너지임을 Volti Standard가 보증합니다."
    ============================================
    """
    return certificate_content

if __name__ == "__main__":
    # 테스트 실행
    sample_cert = create_vt_certificate("제주도 서귀포시", 100, 184.8)
    print(sample_cert)
    
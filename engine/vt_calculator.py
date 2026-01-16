def calculate_volti(energy_kwh, location_l, time_t, carbon_c, renewable_r):
    """
    Volti(VT) 산정 공식[cite: 105]:
    VT = E * L * T * C * R
    """
    vt_value = energy_kwh * location_l * time_t * carbon_c * renewable_r
    return round(vt_value, 4)

# 예시 계산
print(f"1kWh 발전 시 Volti 가치: {calculate_volti(1, 1.2, 1.5, 1.1, 1.0)} VT")


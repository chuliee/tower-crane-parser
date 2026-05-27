import numpy as np
from scipy import stats

label1 = '4월 상부제어'
label2 = '5월 원격제어'
trimming_ratio = 20 ## %단위

def main():
    result_text = ''
    data1 = load_dat('data1.dat')
    data2 = load_dat('data2.dat')


    for label, data in [(label1, data1), (label2, data2)]:
        print_section(label)
        dat_info = analysis_dat(data)
        print(f'  표본     : {dat_info[0]}')
        print(f'  평균     : {dat_info[1]:.2f}')
        print(f'  중앙값   : {dat_info[2]:.2f}')
        print(f'  표준편차 : {dat_info[3]:.2f}')
        print(f'  왜도(Skewness)  : {dat_info[4]:+.2f}  → {interpret_skew(dat_info[4])}')
        print(f'  첨도(Kurtosis)  : {dat_info[5]:+.2f}  → {interpret_kurt(dat_info[5])}')
        result_text = result_text + f'표본: {dat_info[0]:.2f}, 평균: {dat_info[1]:.2f}, 중앙값: {dat_info[2]:.2f}, 표준편차: {dat_info[3]:.2f}, 왜도: {dat_info[4]:.2f}, 첨도: {dat_info[5]:.2f}\n'
    
    print_section(f"Yuen's t-test 결과 (trimming = {trimming_ratio}%)")
    try:
        yuen_info = yuen_ttest(data1, data2, trimming_ratio/100)
        print(f'  Trimmed mean (집단1) : {yuen_info[0]:.2f}')
        print(f'  Trimmed mean (집단2) : {yuen_info[1]:.2f}')
        print(f'  t 통계량             : {yuen_info[2]:.2f}')
        print(f'  자유도 (df)          : {yuen_info[3]:.2f}')
        print(f'  p-value              : {yuen_info[4]:.2f}')
        print(f'\n  → {interpret_p(yuen_info[4])}')
        result_text = result_text + f'"{label1}" 평균: {yuen_info[0]}(100%), "{label2}" 평균: {yuen_info[1]}({((yuen_info[1]/yuen_info[0])*100):.2f}%)\n'
        result_text = result_text + f't-통계량: {yuen_info[2]:.2f}, 자유도: {yuen_info[3]:.2f}, p-value: {yuen_info[4]:.2f}, {interpret_p(yuen_info[4])}' + '\n'
    except ValueError as e:
        print(f'  오류: {e}')
    
    print(f"\n{'='*45}\n")
    with open('result.dat', 'w', encoding='utf-8') as f:
        f.write(result_text)

def load_dat(filename):
    values = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            try:
                values.append(float(line.replace(',', ''))) ## 천단위 쉼표 허용
            except ValueError:
                pass ## 헤더나 문자열 행 무시
    return np.array(values)

 
def analysis_dat(data):
    # 표본 수, 평균, 중앙 값, 표준편차, 왜도, 첨도 계산
    return len(data), np.mean(data), np.median(data), np.std(data, ddof=1), stats.skew(data, bias=False), stats.kurtosis(data, bias=False)


def yuen_ttest(x, y, tr):
    x = np.sort(x)
    y = np.sort(y)
 
    n1, n2 = len(x), len(y)
    g1 = int(np.floor(n1 * tr))
    g2 = int(np.floor(n2 * tr))
    h1 = n1 - 2 * g1
    h2 = n2 - 2 * g2
 
    if h1 < 2 or h2 < 2:
        raise ValueError('Trimming 후 유효 표본이 너무 적습니다. tr 값을 줄이거나 데이터를 확인하세요.')
 
    # Trimmed mean
    tm1 = np.mean(x[g1:n1 - g1])
    tm2 = np.mean(y[g2:n2 - g2])
 
    # Winsorized variance
    xw = np.clip(x, x[g1], x[n1 - g1 - 1])
    yw = np.clip(y, y[g2], y[n2 - g2 - 1])
 
    sw1 = np.var(xw, ddof=1) * (n1 - 1) / (h1 * (h1 - 1))
    sw2 = np.var(yw, ddof=1) * (n2 - 1) / (h2 * (h2 - 1))
 
    # t 통계량
    se = np.sqrt(sw1 + sw2)
    t_stat = (tm1 - tm2) / se
 
    # 자유도 (Welch 방식)
    df = (sw1 + sw2) ** 2 / ((sw1 ** 2 / (h1 - 1)) + (sw2 ** 2 / (h2 - 1)))
 
    # p-value (양측)
    p_value = 2 * stats.t.sf(abs(t_stat), df)
 
    return tm1, tm2, t_stat, df, p_value
 

def print_section(title):
    print(f"\n{'='*45}")
    print(f'  {title}')
    print(f"{'='*45}")


def interpret_skew(v):
    a = abs(v)
    if a <= 0.5:   return '정규분포에 가까움'
    elif a <= 1.0: return '약간 치우침'
    elif a <= 2.0: return '중간 정도 치우침 ⚠'
    else:          return '심하게 치우침 ❌'


def interpret_kurt(v):
    a = abs(v)
    if a <= 1.0:   return '정규분포에 가까움'
    elif a <= 3.0: return '약간 벗어남 ⚠'
    else:          return '많이 벗어남 ❌'

 
def interpret_p(p, alpha=0.05):
    if p < alpha:
        return f'유의함 (p < {alpha}) → 두 집단 간 차이 있음'
    else:
        return f'유의하지 않음 (p ≥ {alpha}) → 두 집단 간 차이 없음'
 
main()
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

file_path = './bbox/BBox20260303072945.td'
start_time = '2026-02-28 07:00:00'
end_time = '2026-02-28 16:30:00'

with open(file_path, 'r') as f:
    df = pd.read_csv(f) # object
    df['Time'] = pd.to_datetime(df['Time']) # convert 'Time' from TEXT to DATETIME


    df_mod = df.copy()
    
    time_mask = (df_mod['Time'] >= start_time) & (df_mod['Time'] <= end_time)
    df_mod = df_mod.loc[time_mask]

    # np luffing
    np_luffing_rad = np.arccos(df_mod['Radius'] / 50)
    df_mod['Luffing'] = np.degrees(np_luffing_rad)
    df_mod['Height_gr'] = (np.sin(np_luffing_rad) * 50) - df['Height'] 

    print(len(df))
    print(len(df_mod))
    print(df_mod.head)
    
plt.rcParams['figure.figsize'] = (12, 10)  # 전체 그래프 크기
plt.rcParams['lines.linewidth'] = 1.5

# 2. 4개의 서브플롯 생성 (4행 1열)
fig, axes = plt.subplots(4, 1, sharex=True) # X축(시간) 공유

# 대상 컬럼 리스트
columns_to_plot = ['Load', 'Luffing', 'Angle', 'Height_gr']
colors = ['blue', 'green', 'orange', 'red']
labels = ['Load (t)', 'Luffing (°)', 'Angle (°)', 'Height (m)']

for i, col in enumerate(columns_to_plot):
    axes[i].plot(df_mod['Time'], df_mod[col], color=colors[i], label=col)
    axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axes[i].xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    axes[i].set_ylabel(labels[i])
    axes[i].grid(True, linestyle='--', alpha=0.5)
    axes[i].legend(loc='upper right')

# 3. 레이아웃 및 X축 설정
plt.xlabel('Time')
# plt.xticks(rotation=45) # 시간 라벨이 겹치지 않게 회전
plt.suptitle(f'Crane Data Analysis ({start_time} ~ {end_time})', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # 제목 공간 확보

# 4. 그래프 저장 및 출력
# plt.savefig('worktime_analysis.png') # 파일로 저장
plt.show() # 화면에 출력



    # for d in raw_data:
    #     # t = t + 1
    #     print(d[1])
    #     df = pd.to_datetime(d[1])

    #     print(df)
    #     print(type(df))

# print(t)
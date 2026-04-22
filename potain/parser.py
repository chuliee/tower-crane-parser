import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import shutil

from datetime import time
from pathlib import Path

start_time = time(6, 0, 0)
end_time = time(18, 0, 0)

init_path = [Path('./images'), Path('./bbox/parsed'), Path('./bbox_by_date/parsed')]
for p in init_path: p.mkdir(parents=True, exist_ok=True)

def bbox_by_date():
    bbox_files = list(Path('./bbox').glob('*.csv'))
    for bf in bbox_files:
        shutil.move(str(bf), str(bf.with_suffix('.td')))
    bbox_files = list(Path('./bbox').glob('*.td'))
    for bf in bbox_files:
        with open(bf, 'r') as f:
            df = pd.read_csv(f) # object
            df['Time'] = pd.to_datetime(df['Time']) # convert 'Time' from TEXT to DATETIME

            for date, group in df.groupby(df['Time'].dt.date):
                file_name = f'{date}_{bf.stem}_len({len(group)}).td'
                # if len(group) > 40000:
                file_name = f'{date}_{group["Time"].iloc[0].strftime("%H%M%S")}_{group["Time"].iloc[-1].strftime("%H%M%S")}_len({len(group)}).td'
                group.to_csv(f'./bbox_by_date/{file_name}', index=False, encoding='utf-8-sig')
                print(f'Saved bbox_by_date: {file_name}')
                # else:
                    # print(f'Dropped {file_name}')
        shutil.move(str(bf), './bbox/parsed')

def parse_bbox_to_image():
    bbox_files = list(Path('./bbox_by_date').glob('*.td'))
    # print(bbox_files)
    for bf in bbox_files:
        with open(bf, 'r') as f:
            df = pd.read_csv(f) # object
            df['Time'] = pd.to_datetime(df['Time']) # convert 'Time' from TEXT to DATETIME
            df_mod = df.copy()
            
            time_mask = (df_mod['Time'].dt.time >= start_time) & (df_mod['Time'].dt.time <= end_time)
            df_mod = df_mod.loc[time_mask]

            # np_luffing_rad = np.arccos(df_mod['Radius'] / 50)
            # df_mod['Luffing'] = np.degrees(np_luffing_rad)
            # df_mod['Height_gr'] = df['Height'] - (np.sin(np.radians(df_mod['Elevation'])) * 50)
    
            plt.rcParams['figure.figsize'] = (12, 15)  # 전체 그래프 크기
            plt.rcParams['lines.linewidth'] = 1.5

            # 2. 4개의 서브플롯 생성 (4행 1열)
            fig, axes = plt.subplots(4, 1, sharex=True) # X축(시간) 공유

            # 대상 컬럼 리스트
            columns_to_plot = ['Load', 'Elevation', 'Angle', 'Height']
            colors = ['blue', 'green', 'orange', 'red']
            labels = ['Load (t)', 'Luffing (°)', 'Swing (°)', 'Height (m)']

            for i, col in enumerate(columns_to_plot):
                axes[i].plot(df_mod['Time'], df_mod[col], color=colors[i], label=col)
                axes[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                axes[i].xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
                axes[i].set_ylabel(labels[i])
                axes[i].grid(True, linestyle='--', alpha=0.5)
                axes[i].legend(loc='upper right')

                if col == 'Load':       axes[i].set_ylim(-1, 20)
                if col == 'Elevation':    axes[i].set_ylim(0, 90)
                if col == 'Angle':      axes[i].set_ylim(0, 360)
                if col == 'Height':  axes[i].set_ylim(0, 100)

            # 3. 레이아웃 및 X축 설정
            plt.xlabel('Time')
            # plt.xticks(rotation=45) # 시간 라벨이 겹치지 않게 회전
            plt.suptitle(f'Crane Data Analysis ({bf.stem[0:10]} {start_time} ~ {end_time})', fontsize=15)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # 제목 공간 확보

            # 4. 그래프 저장 및 출력
            plt.savefig(f'./images/{bf.stem}.png') # 파일로 저장
            plt.close()
            # plt.show() # 화면에 출력
            print(bf, len(df_mod))
        shutil.move(str(bf), './bbox_by_date/parsed')

def main():
    dummy = input('Proceed raw data parsing? (Y/N) ')
    if dummy == 'y' or dummy == 'Y': bbox_by_date()
    dummy = input('Proceed visualization? (Y/N) ')
    if dummy == 'y' or dummy == 'Y': parse_bbox_to_image()

main()
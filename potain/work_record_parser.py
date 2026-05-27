import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import shutil

from datetime import time
from pathlib import Path

start_time = time(6, 0, 0)
end_time = time(18, 0, 0)
load_interval = 3
load_len_min = 20
load_min = 0.1

# 초기 폴더 생성
init_path = ['./result/work_record', './result/images', './data/bbox', './data/bbox_by_date']
for p in init_path:
    Path(p).mkdir(parents=True, exist_ok=True)

# def bbox_by_date():
#     bbox_files = list(Path('./bbox').glob('*.csv'))
#     for bf in bbox_files:
#         shutil.move(str(bf), str(bf.with_suffix('.td')))
#     bbox_files = list(Path('./bbox').glob('*.td'))
#     for bf in bbox_files:
#         with open(bf, 'r') as f:
#             df = pd.read_csv(f) # object
#             df['Time'] = pd.to_datetime(df['Time']) # convert 'Time' from TEXT to DATETIME

#             for date, group in df.groupby(df['Time'].dt.date):
#                 file_name = f'{date}_{bf.stem}_len({len(group)}).td'
#                 # if len(group) > 40000:
#                 file_name = f'{date}_{group["Time"].iloc[0].strftime("%H%M%S")}_{group["Time"].iloc[-1].strftime("%H%M%S")}_len({len(group)}).td'
#                 group.to_csv(f'./bbox_by_date/{file_name}', index=False, encoding='utf-8-sig')
#                 print(f'Saved bbox_by_date: {file_name}')
#                 # else:
#                     # print(f'Dropped {file_name}')
#         shutil.move(str(bf), './bbox/parsed')

def read_bbox_files():
    # 기존에 처리된 파일명 불러오기
    with open(Path(f'{init_path[3]}/work_record_parser.tdl'), 'r') as f:
        parsed_files = set(line.strip() for line in f if line.strip())

    # 데이터 불러오기
    bbox_dict = dict()
    bbox_files = list(Path(init_path[3]).glob('*.td'))
    # print(bbox_files)
    for bf in bbox_files:
        if bf.name not in parsed_files:
            with open(bf, 'r') as f:
                df = pd.read_csv(f, dtype={19: str}) # object
                df['Time'] = pd.to_datetime(df['Time']) # convert 'Time' from TEXT to DATETIME
                df_mod = df.copy()
                
                time_mask = (df_mod['Time'].dt.time >= start_time) & (df_mod['Time'].dt.time <= end_time)
                df_mod = df_mod.loc[time_mask]
                bbox_dict[bf.name] = df_mod
        else:
            pass
    return bbox_dict

def process_bbox_files(bbox_dict):
    with open(Path(f'{init_path[0]}/total.tdr'), 'w') as f1: 
        for k, v in bbox_dict.items(): # *.td 파일 선택
            work_list = []
            current_work = []
            interval_buffer = []
            work_flag = False
            
            for _, row in v.iterrows():
                value_load = float(row['Load'])
                if value_load > 0.0:
                    if len(interval_buffer) > 0:
                        current_work.extend(interval_buffer)
                        interval_buffer = []
                    current_work.append(row)
                    work_flag = True
                else:
                    if work_flag:
                        interval_buffer.append(row)
                        if len(interval_buffer) >= load_interval:
                            if len(current_work) >= load_len_min:
                                print(len(current_work))
                                df_mod = pd.DataFrame(current_work)
                                print(df_mod['Time'].iloc[0])
                                if df_mod['Load'].max() >= load_min:
                                    if df_mod['Angle'].iloc[0] != 0 and df_mod['Angle'].iloc[0] != 360 and df_mod['Angle'].iloc[-1] != 0 and df_mod['Angle'].iloc[-1] != 360:
                                        work_list.append(pd.DataFrame(current_work))
                            else:
                                pass
                            # load_interval보다 클 경우 작업을 끊고 변수를 초기화
                            work_flag = False
                            current_work = []
                            interval_buffer = []
                        else:
                            pass

            # Work별로 시작 시간, 종료 시간, 시작 위치, 종료 위치, 하중값 추출
            with open(Path(f'{init_path[0]}/{k}.tdr'), 'w') as f2:                
                for i, df in enumerate(work_list, 1):
                    f1.write(f"{df['Time'].iloc[0].date()},{i},{df['Time'].iloc[0].time()},{df['Time'].iloc[-1].time()},{df['Load'].max()},{df['Angle'].iloc[0]},{df['Angle'].iloc[-1]},{df['Elevation'].iloc[0]},{df['Elevation'].iloc[-1]}")
                    f1.write('\n')
                    f2.write(f"{df['Time'].iloc[0].date()},{i},{df['Time'].iloc[0].time()},{df['Time'].iloc[-1].time()},{df['Load'].max()},{df['Angle'].iloc[0]},{df['Angle'].iloc[-1]},{df['Elevation'].iloc[0]},{df['Elevation'].iloc[-1]}")
                    f2.write('\n')
                                    # summary = {
                        #     'work_no': f'work{i}',
                        #     'start_time': df['Time'].iloc[0],
                        #     'end_time': df['Time'].iloc[-1],
                        #     'max_load': df['Load'].max(),
                        #     'start_angle': df['Angle'].iloc[0],
                        #     'end_angle': df['Angle'].iloc[-1],
                        #     'start_elevation': df['Elevation'].iloc[0],
                        #     'start_elevation': df['Elevation'].iloc[-1]
                        # }
            print(k)    
                        

    return None


def main():
    bbox_dict = read_bbox_files()
    result = process_bbox_files(bbox_dict)

main()
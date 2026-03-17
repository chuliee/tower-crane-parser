import glob
import json
import os
import requests
import time

start_date = 20260301
end_date = 20260316
dates = []
folder_path = './wind_data'

def request_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f'Failed: {url}')
        data = False
    return data

def manage_json(date, type):
    file = f'{folder_path}/{type}_data/{date}_{type}.json'
    if not os.path.isfile(file):
        url = f'http://15.165.129.45:5007/api/wind/{type}/14335C57D38F/{date}'
        data = request_json(url)
        if data:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f'{date}_{type}.json: Saved')
        else:
            pass
    else:
        print(f'{date}_{type}.json: Already exist')

for d in range(start_date, end_date + 1):
    manage_json(d, 'daily')
    manage_json(d, '10min')

json_files = glob.glob(os.path.join(f'{folder_path}/10min_data/', '*.json'))
with open(f'wind_data_{time.time()}.csv', 'w') as r:
    r.write('date_time,avg,max,min\n')
    for j in json_files:
        with open(j, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            data = raw_data['data']
            for d in data:
                datetime = d['datetime']
                davg = d['status']['wind']
                dmax = d['status']['max']
                dmin = d['status']['min']
                r.write(f'{datetime},{davg},{dmax},{dmin}\n')


    # file_daily = f'{folder_path}/1hr_data/{d}_daily.json'
    # if not os.path.isfile(file_daily):
    #     url_daily = f'http://15.165.129.45:5007/api/wind/daily/14335C57D38F/{d}'
    #     data = request_json(url_daily)
    #     if data:
    #         with open(file_daily, 'w', encoding='utf-8') as f:
    #             json.dump(data, f, indent=4)
    #         print(f'{d}_daily.json: Saved')
    #     else:
    #         pass
    # else:
    #     print(f'{d}_daily.json: Already exist')
    
    # file_10min = f'{folder_path}/10min_data/{d}_daily.json'
    # if not os.path.isfile(file_daily):
    # url_10min = f'http://15.165.129.45:5007/api/wind/10min/14335C57D38F/{d}'

    # if response.status_code == 200:
    #     data = response.json()
    


# folder_path = './wind_data/10min_data/'
# 


# with open(f'wind_data_{time.time()}.csv', 'w') as r:
#     r.write('date_time,avg,max,min\n')
#     for j in json_files:
#         with open(j, 'r', encoding='utf-8') as f:
#             raw_data = json.load(f)
#             data = raw_data['data']
#             for d in data:
#                 datetime = d['datetime']
#                 davg = d['status']['wind']
#                 dmax = d['status']['max']
#                 dmin = d['status']['min']
#                 r.write(f'{datetime},{davg},{dmax},{dmin}\n')

# print(temp)
# print(len(temp))
# # print(data)
# # print(f"데이터 타입: {type(data)}")

# # 1. JSON 파일이 있는 폴더 경로 (예: 'data_folder')
# folder_path = 'your_folder_path' 

# # 2. 해당 폴더 내의 모든 .json 파일 경로 가져오기
# json_files = glob.glob(os.path.join(folder_path, '*.json'))

# all_data = []

# for file_path in json_files:
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#             all_data.append(data) # 리스트에 각 파일의 dict 저장
#             print(f"성공적으로 불러옴: {os.path.basename(file_path)}")
            
#     except Exception as e:
#         print(f"파일 읽기 실패 ({file_path}): {e}")

# # 3. 결과 확인
# print(f"총 {len(all_data)}개의 파일을 불러왔습니다.")
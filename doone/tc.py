import json

file_path = './tc_data/log097.json'
# file_path = './wind_data/20260212_10min.json'

with open(file_path, 'r', encoding='utf-8') as file:
    raw_data = json.load(file)
    data = raw_data['2026/02/13 15:21:11']
    temp = []
    for d in data:
        if d['topic'] not in temp:
            temp.append(d['topic'])

print(temp)
print(len(temp))
# print(data)
# print(f"데이터 타입: {type(data)}")

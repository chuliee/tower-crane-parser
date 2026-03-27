import pulp
import itertools
import random

# 1. 문제 설정: 7개의 도시 좌표 생성 (임의 설정)
num_cities = 7
cities = range(num_cities)
locations = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in cities}

# 도시 간 거리 계산 (유클리드 거리)
def get_distance(c1, c2):
    loc1, loc2 = locations[c1], locations[c2]
    return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)**0.5

dist = {(i, j): get_distance(i, j) for i in cities for j in cities if i != j}

# 2. 모델 정의
prob = pulp.LpProblem("TSP_7_Cities", pulp.LpMinimize)

# 3. 의사결정 변수
# x[i, j] = 1 이면 도시 i에서 j로 이동함
x = pulp.LpVariable.dicts("x", dist.keys(), cat=pulp.LpBinary)

# u[i] = MTZ 제약 조건을 위한 보조 변수 (방문 순서)
u = pulp.LpVariable.dicts("u", cities, lowBound=0, upBound=num_cities-1, cat=pulp.LpContinuous)

# 4. 목적 함수: 전체 이동 거리 최소화
prob += pulp.lpSum([dist[i, j] * x[i, j] for (i, j) in dist.keys()])

# 5. 제약 조건
# (1) 각 도시에서 나가는 길은 오직 하나
for i in cities:
    prob += pulp.lpSum([x[i, j] for j in cities if i != j]) == 1

# (2) 각 도시로 들어오는 길은 오직 하나
for j in cities:
    prob += pulp.lpSum([x[i, j] for i in cities if i != j]) == 1

# (3) MTZ Subtour Elimination (부분 경로 제거 제약식)
# 도시 0을 시작점으로 잡고 나머지 도시들에 대해 순서 부여
for i in cities:
    for j in cities:
        if i != j and i != 0 and j != 0:
            prob += u[i] - u[j] + num_cities * x[i, j] <= num_cities - 1

# 6. 솔버 실행
prob.solve(pulp.PULP_CBC_CMD(msg=0))

# 7. 결과 출력
print(f"최적화 상태: {pulp.LpStatus[prob.status]}")
print(f"최단 경로 총 거리: {pulp.value(prob.objective):.2f}")

# 경로 추적
curr_city = 0
path = [0]
while len(path) < num_cities:
    for j in cities:
        if (curr_city, j) in x and pulp.value(x[curr_city, j]) == 1:
            path.append(j)
            curr_city = j
            break
path.append(0)  # 다시 시작점으로 복귀
print(f"최적 경로: {' -> '.join(map(str, path))}")
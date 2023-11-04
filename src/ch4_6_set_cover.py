from vis import SetCoverVisualizer as Visualizer
from copy import deepcopy

# Set Cover 시작
u={1,2,3,4,5,6,7,8,9,10}
f=[
  {1,2,3,8},
  {1,2,3,4,8},
  {1,2,3,4},
  {2,3,4,5,7,8},
  {4,5,6,7},
  {5,6,7,9,10},
  {4,5,6,7},
  {1,2,4,8},
  {6,9},
  {6,10},
]
U = deepcopy(u) # 원본에서 제거하면서 진행할 것이므로
F = deepcopy(f) # 복사를 해 둔다

vis = Visualizer('Set Cover - Simple Set')
vis.setup(vis.get_main_module())
vis.reset()

# 나중에 Loop 로 변경하기 위해 강제 들여쓰기 목적으로 if True 를 쓴다
if True:    
    max_i, max_c = -1, 0
    for i in range(len(F)):        # subset 들을 대상으로 Loop 를 돈다
      cnt = 0
      vis.comp(i)
      subset = sorted(list(F[i]))  # 정렬할 필요는 없지만 vis 를 위해 정렬한다
      for v in subset:             # 그냥 for v in F[i] 로 해도 좋다
        if v in U: cnt += 1        # U 에 원소가 있으면 cnt 를 증가한다
        vis.comp(i, v, cnt)
      if max_c < cnt:              # 겹치는 갯수 중 max 를 max_c,
        max_i, max_c = i, cnt      # 그 위치를 max_i 에 저장한다 
    print(f'{max_i=}')
    vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다

print(u)              # u 의 원소를 모두 출력
print(f[1], f[5])     # f[1] 과 f[5] 를 각각 출력
print(f[1] | f[5])    # f[1] 과 f[5] 의 합집합을 출력해 보면 u 와 같다
# 따라서 위 두 집합을 선택하면 최소 선택으로 u 를 모두 cover 할 수 있다

vis.end()


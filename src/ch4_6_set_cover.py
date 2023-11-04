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
    for i in range(len(F)):        # subset 들을 대상으로 Loop 를 돈다
      cnt = 0
      vis.comp(i)
      subset = sorted(list(F[i]))  # 정렬할 필요는 없지만 vis 를 위해 정렬한다
      for v in subset:             # 그냥 for v in F[i] 로 해도 좋다
        if v in U: cnt += 1        # U 에 원소가 있으면 cnt 를 증가한다
        vis.comp(i, v, cnt)
    vis.fix(3)                     # 임시로 3 번이 가장 많은 원소가 겹침을 보인다

print(u)              # u 의 원소를 모두 출력
print(f[1], f[5])     # f[1] 과 f[5] 를 각각 출력
print(f[1] | f[5])    # f[1] 과 f[5] 의 합집합을 출력해 보면 u 와 같다
# 따라서 위 두 집합을 선택하면 최소 선택으로 u 를 모두 cover 할 수 있다

vis.end()


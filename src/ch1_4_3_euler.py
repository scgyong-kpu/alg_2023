from vis import EulerVisualizer as Visualizer
# from vis import Dummy as Visualizer
from data_city import City

def start():
  euler_circuit = [start_vertex] # 첫 점을 넣은 배열로 초기화한다

  cv = start_vertex # cv: current vertex

  while True:
    if len(adj_list[start_vertex]) == 0: break
    # 시작점에 연결된 간선이 없을때까지 반복한다

    vis.mark_vertex(cv)

    adjs = len(adj_list[cv]) 
    # 현재 점에서 연결된 점이 몇 개인가?
    # 한개뿐이라면 그리로 가면 되고 여러개라면 선택해야 한다
    if adjs == 1:
      nv = adj_list[cv][0] # 다음 점은 하나밖에 없는 그곳으로 결정하자
      print(f'{nv} 는 유일한 길이다. 이쪽으로 갈 수밖에 없다')
      # nv = next vertex
    else:
      # 여러 개 중에서 후보를 고를 예정이다
      # 이번 간선을 삭제하고도 돌아올 수 있다면 가도 좋은 것으로 판단하자

      candidates = adj_list[cv][:]
      for cand in candidates:
        # cand = 이번 점 으로 가도 좋은지 판단해 보는 후보선수

        vis.remove_edge(cv, cand)
        # 간선을 임시로 제거해 본다. 
        # 간선을 양방향으로 저장하고 있으므로 둘 다 삭제해야 한다
        adj_list[cv].remove(cand)
        adj_list[cand].remove(cv)

        # cv 에서 cand 까지 연결 되는지 확인한다
        # cv 로부터 연결 가능한 모든 점을 받아서 그 안에 있는지 확인한다
        vis.dfs_push()
        is_connected = is_point_connnected_to(cv, cand)
        vis.dfs_pop()

        vis.revive_edge(cv, cand)
        # 연결되는지만 확인하려고 간선을 제거한 것이므로
        # 다시 복원시킨다
        adj_list[cv].append(cand)
        adj_list[cand].append(cv)

        print(f'{cv}~{cand} 간선을 삭제했을 때: {cand=} {is_connected=}')
        # 원래는 연결되니 그만 해야 하지만 모든 점들을 확인해 보기로 한다

        # 연결된다면 이번 점으로 진행하기로 한다.
        if is_connected:
          nv = cand      # nv = next vertex
          break

        # 아니라면 다음 후보로 넘어간다

    # nv 쪽으로 가는 것이 확정되었으므로 cv~nv 사이의 간선은 제거한다.
    print(f'{cv=} {nv=} {adj_list[cv]=}')
    adj_list[cv].remove(nv)
    adj_list[nv].remove(cv)

    vis.settle_edge(cv, nv)

    # nv 를 오일러 서킷에 추가한다
    euler_circuit.append(nv)
    print(f'{nv} 이(가) 추가되었다. {euler_circuit=}')

    cv = nv # 이제 nv 가 cv 가 되어 다음 루프를 계속한다

  vis.finish_euler(euler_circuit)

def is_point_connnected_to(v, to, pts=None):
  # 특정 점에 연결 가능한지만 확인하면 되므로 모든 점을 알 필요는 없다
  # 이미 방문한 점은 pts 라는 집합에 넣도록 하며
  # 첫 호출시에는 빈 set 이 되도록 default argument 로 넣어 둔다 ( pts=None )
  if pts == None: pts = set()

  pts.add(v) # 이번 점을 넣고
  vis.dfs_push(v)
  for w in adj_list[v]: # v 에 연결되는 모든 점들에 대해
    if not w in pts:    # 아직 방문한적이 없었으면
      if w == to:
        vis.dfs_push(w)
        vis.dfs_pop()
        return True # 이번에 연결하는 점이 목표점이면 바로 리턴
      connected = is_point_connnected_to(w, to, pts) # 재귀 호출한다
      if connected: 
        vis.dfs_pop()
        return True

  vis.dfs_pop()
  return False # 내 이후로 연결되는 것이 없다

def list_all_edges():
  vertex_count = len(adj_list)
  print(f'{vertex_count=}')
  for u in range(vertex_count):
    ends = adj_list[u]
    # print(f'{u=} : {ends=}')
    for v in ends:
      print(f'{u=}, {v=}')

if __name__ == '__main__':
  vis = Visualizer('Euler Cuicit')
  cities = [
      City("Clean", 103, 116, 0),
      City("Prosy", 271, 123, 1),
      City("Rabbi", 295, 183, 2),
      City("Addle", 523, 206, 3),
      City("Smell", 430, 282, 4),
      City("Quite", 387, 404, 5),
      City("Lives", 277, 401, 6),
      City("Cross", 207, 521, 7),
      City("Synth", 198, 330, 8),
      City("Tweak", 108, 293, 9),
      City("Medic", 230, 206, 10),
      City("Glade", 297, 312, 11),
      City("Breve", 492, 480, 12),
  ]
  while True:
    adj_list = [
      [1, 9], [0, 2], [1, 3, 10, 11], [2, 12], [5, 11], [4, 6], [5, 11], 
      [8, 12], [7, 9, 10, 11], [8, 0], [2, 8], [2, 8, 4, 6], [3, 7]
    ]
    # 인접점 표기 방식으로 그래프를 표현한다
    # adj_list[a] 가 list 이고 그 안에 b 가 있으면 a-b 간선이 있는 것으로 본다

    # list_all_edges()
    start_vertex = 0
    vis.setup(vis.get_main_module())
    start()
    again = vis.end()
    if not again: break

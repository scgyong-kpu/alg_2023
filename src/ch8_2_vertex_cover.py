from vis import VertexCoverVisualizer as Visualizer
from copy import deepcopy
from random import randrange
import data_sample_cities as dsc


class VertexCover:
  def __init__(self, cities, edges, usingSetCover=True):
    self.cities = cities
    self.edges = edges
    self.usingSetCover = usingSetCover
    self.main = self.setCoverMain if usingSetCover else self.maxMatchMain
    self.build_graph() # for visualizer

  def build_graph(self):
    n_cities = len(self.cities)
    self.graph = {u: dict() for u in range(n_cities)}
    for u,v,w in self.edges:
      self.graph[u][v] = w
      self.graph[v][u] = w

  def setCoverMain(self):
    print('Using Set Cover')
    n_cities = len(self.cities)
    n_edges = len(self.edges)
    self.u = { i for i in range(n_edges) }      # self.u 는 전체 간선번호 집합
    self.f = [ set() for _ in range(n_cities) ] # self.f 는 각 vertex 가 선택되었을 때 cover 되는 간선번호 집합
    for i in range(n_edges):                    # 모든 edge 들에 대해 간선번호 추가
      u,v,w = self.edges[i]
      self.f[u].add(i)                          # u 로 cover 되는 간선번호 i 추가
      self.f[v].add(i)                          # v 로 cover 되는 간선번호 i 추가
    print(self.u, self.f)
    self.U = deepcopy(self.u)                   # U, F 는 원소를 없애가면서 작업할 것이므로
    self.F = deepcopy(self.f)                   # u, f 로부터 deepcopy 하여 준비한다

    self.C = []
    while self.U:
      max_i = self.F.index(max(self.F, key=lambda s: len(s & self.U))) # ch46sc commit 들을 참고한다
      vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다
      print(f'fixing {max_i}')
      S = self.F[max_i]              # F 에서 U 와의 교집합이 가장 큰 부분집합
      self.U -= S                    # U 에서 해당 부분집합의 원소를 제거한다
      print(S, self.U, self.F)
      self.F[max_i] = set()
      self.C.append(S)

    vis.draw()

  def maxMatchMain(self):
    print('Using Maximul Matching')
    n_cities = len(self.cities)
    n_edges = len(self.edges)
    self.adjs = [ set() for _ in range(n_cities) ]
    print(self.adjs)
    for i in range(n_edges):
      u,v,w = self.edges[i]
      self.adjs[u].add(v)
      self.adjs[v].add(u)
    print(self.adjs)        # 각 점에서 연결되는 점들을 저장하는 Adj Set 을 만들어 둔다
    self.vc = set()         # 결과가 저장될 Vertex Cover
    edge_count = 0          # 지운 edge 수. n_edges 까지 지워지면 (cover 되면) 프로그램 종료

    vertices = list(range(n_cities))
    while edge_count < n_edges:
      print(f'{self.adjs=}, {vertices=}')
      vi = randrange(len(vertices))         # 살아있는 정점 중 하나를 랜덤하게 골라서
      u = vertices.pop(vi)                  # 뽑아낸다
      print(f'{vi=} {u=} {self.adjs[u]=}')
      if not self.adjs[u]: continue         # 이 점 주위에 연결된것이 없다면 (모두 지워졌다면) 넘어간다
      v = self.adjs[u].pop()                # 있으니까 그 중 하나를 뽑아낸다
      print(f'{u=} {v=}')
      vis.matching(u,v)                     # u~v 를 매칭으로 삼는다

      for n in (u, v):                      # u 와 v 에 대해서 동일한 작업을 할 예정이므로 loop 를 돈다
        self.vc.add(n)                      # 매칭의 양쪽끝점인 u 와 v 를 VC 에 추가한다
        print(f'{self.vc=}')

        for k in range(n_cities):           # 모든 점 k 에 대하여
          if k in self.adjs[n]:             # n 에서 k 로 가는 선이 살아있다면 (안 지워졌다면)
            print(f'<{n=} {k=} {self.adjs[n]=} {self.adjs[k]=}')
            self.adjs[n].remove(k)          # 그 선은 지운다
            if n in self.adjs[k]:           # k 에서 n 으로 가는 선도 살아있다면 삭제한다.
              self.adjs[k].remove(n)        # u~v 선은 중복하여 삭제될 수 있기 때문에 살아있는지 확인 후 삭제한다
            print(f'>{n=} {k=} {self.adjs[n]=} {self.adjs[k]=}')
            edge_count += 1                 # 삭제한 edge 의 수를 증가시킨다

      print(f'vc={self.vc} {edge_count=} {n_edges=}')

      break # 일단 한바퀴만

    vis.draw()

vis = Visualizer('Vertex Cover')
usingSetCover = False
while True:
  vc = VertexCover(dsc.cities, dsc.edges, usingSetCover)
  vis.setup(vc)
  vc.main()
  again = vis.end()
  if not again: break
  if vis.restart_lshift:
    dsc.next()
  elif vis.restart_rshift:
    dsc.random()
  else:
    usingSetCover = not usingSetCover

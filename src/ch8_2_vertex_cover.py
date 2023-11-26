from vis import VertexCoverVisualizer as Visualizer
from copy import deepcopy
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

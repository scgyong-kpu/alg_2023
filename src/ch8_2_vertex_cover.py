from vis import VertexCoverVisualizer as Visualizer
from copy import deepcopy
import data_sample_cities as dsc


class VertexCover:
  def __init__(self, cities, edges, usingSetCover=True):
    self.cities = cities
    self.edges = edges
    self.usingSetCover = usingSetCover
    self.main = self.setCoverMain if usingSetCover else self.maxMatchMain

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
    vis.draw()

  def maxMatchMain(self):
    print('Using Maximul Matching')
    vis.draw()

vis = Visualizer('Vertex Cover')
usingSetCover, gen = True, True
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

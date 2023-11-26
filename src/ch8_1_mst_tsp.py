from vis import MstTspVisualizer as Visualizer
from random import randint, seed, shuffle
from heapdict import heapdict
import data_sample_cities as dsc

class TspMst:
  def __init__(self, cities, edges):
    self.cities = cities
    self.n_cities = len(cities)
    self.edges = edges

  def build_graph(self, edges):
    g = {u: dict() for u in range(self.n_cities)}
    for u,v,w in edges:
      g[u][v] = w
      g[v][u] = w
    return g

  def main(self):
    self.start_index = randint(0, self.n_cities-1)
    vis.set_start(self.start_index)
    self.g = self.build_graph(self.edges)
    self.mst()

  def mst(self):
    self.completed = set()
    self.completed.add(self.start_index) # 시작점을 완성집합에 넣어둔다
    self.weights = heapdict()
    self.weights[self.start_index] = 0   # 시작점까지의 거리 0 을 넣고 최초꺼낼때 나오도록 한다
    self.origins = dict()
    self.origins[self.start_index] = self.start_index # 거쳐 가는 점 정보에 같은 수를 넣어서 출발지로 삼는다
    vis.append(0, self.start_index)
    self.mst_edges = []                  # 결과를 저장할 Edge List

    while self.weights:
      v, w = self.weights.popitem()      # 알려진 거리가 가장 가까운 점(v)과 거리(w) 를 얻는다
      u = self.origins[v]                # v 에 가려면 u 를 들러서 가야 한다는 것을 알아낸다
      if u != v:                         # v 가 출발점이 아니라면
        self.mst_edges.append((u, v, w))   # (u,v,w) 를 MST 에 추가한다
        self.completed.add(v)
      vis.fix(v, u)

      for adj, weight in self.g[v].items():  # 지금 확정되는 점 v 주위의 점들 adj 들에 대하여
        if adj in self.completed: continue   # 이미 완성집합에 들어있으면 무시한다
        vis.compare(adj, v, weight, True)
        if adj in self.weights and self.weights[adj] < weight: continue # 거리정보가 있는데 이미 가까우면 무시한다
        self.weights[adj] = weight           # adj 까지 가는 가까운 거리는 weight 이며
        self.origins[adj] = v                # adj 까지 가려면 v 를 통해서 가야 한다

      if len(self.completed) == 1: break

    vis.finish()

vis = Visualizer('TSP using MST')
while True:
  alg = TspMst(dsc.cities, dsc.edges)
  vis.setup(alg)
  alg.main()
  again = vis.end()
  if not again: break
  if vis.restart_lshift:
    dsc.next()
  elif vis.restart_rshift:
    dsc.random()


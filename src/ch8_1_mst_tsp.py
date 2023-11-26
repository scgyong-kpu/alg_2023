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
    vis.draw()

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


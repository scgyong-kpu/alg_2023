from vis import PrimVisualizer as Visualizer
from random import randrange
import data_sample_cities as dsc
import heapdict
# heapdict 를 사용하기 위해서는 설치가 필요하다
# pip install heapdict

# adjacency matrix - array of array
def build_graph():
  global graph
  graph = {u: dict() for u in range(n_cities)}
  for u,v,w in edges:
    graph[u][v] = w
    graph[v][u] = w
  print(graph)
  print_adj_matrix()

def print_adj_matrix():
  for u in range(n_cities):
    for v in range(n_cities):
      w = f'{graph[u][v]:5d}' if v in graph[u] else ' ....'
      print(w, end='')
    print()
  print()

def main():
  global n_cities
  n_cities = len(cities)

  build_graph()

  start_city_index = randrange(n_cities)
  print(f'{n_cities} cities, starts from {cities[start_city_index]}')

  global weights, completed
  weights = heapdict.heapdict()
  weights[start_city_index] = 0, start_city_index # weight, from
  #저장 순서는 (weight, index, from) 이다

  completed = set()

  global mst
  mst = []
  while weights:
    ci, (w, fr) = weights.popitem() # key=cityToIndex, value=(weight,cityFromIndex)
    completed.add(ci)
    if (fr != ci):
      mst.append((fr, ci, w))
      vis.fix(ci, fr)

    adjacents = graph[ci]
    for adj in adjacents:
      if adj in completed: continue
      weight = adjacents[adj]
      if adj in weights:    # adj 에 대해 가중치가 저장되어 있다면
        w = weights[adj][0] # 가중치를 가져온다
        if weight < w:      # 가져온 것보다 비용이 적다면
          weights[adj] = weight, ci    # 교체한다
          vis.update(weight, adj, ci)
        else:
          vis.compare(adj, ci, weight)
      else:                        # 저장되어 있지 않다면
        weights[adj] = weight, ci   # 추가한다
        vis.append(weight, adj, ci)

    if len(mst) >= n_cities - 1: break

if __name__ == '__main__':
  vis = Visualizer('Minimum Spanning Tree - Prim')
  idx = 0
  while True:
    cities, edges = dsc.cities, dsc.edges
    vis.setup(vis.get_main_module())
    vis.draw()
    main()
    again = vis.end()
    if not again: break
    if vis.restart_lshift:
      dsc.next()
    elif vis.restart_rshift:
      dsc.random()

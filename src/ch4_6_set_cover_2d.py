from vis import CitySetCoverVisualizer as Visualizer
import data_sample_cities as dsc
from copy import deepcopy

def build_graph():
  global graph
  graph = {u: dict() for u in range(n_cities)}
  for u,v,w in edges:
    graph[u][v] = w
    graph[v][u] = w

def main():
  global n_cities
  n_cities = len(cities)

  build_graph()

  global u, f, U, F
  f = [
    set(list(d.keys()) + [u]) for u,d in graph.items()
  ]
  print(f)
  U = deepcopy(u)
  F = deepcopy(f)
  vis.draw()

  return
  vis.wait(1000)

  global C
  C = []
  while U:
    max_i = F.index(max(F, key=lambda s: len(s & U)))
    vis.fix(max_i)                 # max_i 번째에 가장 원소가 많이 겹친다
    S = F[max_i] # F 에서 U 와의 교집합이 가장 큰 부분집합
    U -= S       # U 에서 해당 부분집합의 원소를 제거한다
    F[max_i] = set()
    C.append(S)
    print(f'{U=}, {C=}')
  vis.draw()


if __name__ == '__main__':
  vis = Visualizer('Set Cover - Cities')
  while True:
    cities, edges = dsc.cities, dsc.edges
    u = set(range(0, len(cities)))
    vis.setup(vis.get_main_module())
    vis.draw()
    main()
    again = vis.end()
    if not again: break
    if vis.restart_lshift:
      dsc.next()
    elif vis.restart_rshift:
      dsc.random()

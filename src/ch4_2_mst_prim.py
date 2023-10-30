from vis import PrimVisualizer as Visualizer
import data_sample_cities as dsc

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

  start_city_index = 0
  print(f'{n_cities} cities, starts from {cities[start_city_index]}')

  global weights, completed
  weights = []
  weights.append((0, start_city_index, 0))
  #저장 순서는 (weight, index, from) 이다

  completed = set()

  global mst
  mst = []
  while weights:
    print('<', weights)
    w, ci, fr = pop_smallest_weight()
    completed.add(ci)
    print('>', weights)
    if (fr != ci):
      mst.append((fr, ci, w))
      vis.fix(ci, fr)
      print(f'{mst=}')

    adjacents = graph[ci]
    for adj in adjacents:
      if adj in completed: continue
      weight = adjacents[adj]
      prev_weight = find_weight(adj)
      print(f'find_weight({adj}, {prev_weight})')
      if prev_weight == None:    # 기존에 저장된 적이 없다. 추가하자
        weights.append((weight, adj, ci))
        vis.append(weight, adj, ci)
      elif prev_weight > weight: # 저장된 비용보다 적다. 갱신하다
        update_weight(adj, weight, ci)
        vis.update(weight, adj, ci)
      else:                      # 기존의 비용이 적다. 내버려두자
        vis.compare(adj, ci)
      print(' - ', weights)

    if len(mst) >= n_cities - 1: break

def find_weight(ci):
  for e in weights:
    if e[1] == ci:
      return e[0]
  return None

def update_weight(ci_to, weight, ci_from):
  for wi in range(0, len(weights)):
    if ci_to == weights[wi][1]:
      weights[wi] = (weight, ci_to, ci_from)
      return
  return

def pop_smallest_weight():
  min_wi = 0
  min_w = weights[min_wi][0]
  for wi in range(1, len(weights)):
    w = weights[wi][0]
    if w < min_w:
      min_w = w
      min_wi = wi
  return weights.pop(min_wi)

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

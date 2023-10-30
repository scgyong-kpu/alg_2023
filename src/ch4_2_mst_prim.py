from vis import PrimVisualizer as Visualizer
import data_sample_cities as dsc
import heapq

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
    w, ci, fr = heapq.heappop(weights)
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
      for wi in range(0, len(weights)): # 가중치들을 저장해놓은 곳에서
        w, c1, c2 = weights[wi]
        if c1 == adj:    # 연결되는 점에 대한 기록이 있다면
          if weight < w: # 그리고 이번에 연결되는 점의 가중치가 더 작다면
            weights.pop(wi)
            heapq.heappush(weights, (weight, adj, ci)) # 가중치 정보를 교체한다
            vis.update(weight, adj, ci)
          else:
            vis.compare(adj, ci)
          break
      else: # for 에서 break 로 종료하지 않았다면
        heapq.heappush(weights, (weight, adj, ci)) # 기록이 없었으므로 추가한다
        vis.append(weight, adj, ci)

      print(' - ', weights)

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

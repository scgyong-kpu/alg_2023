from vis import KruskalVisualizer as Visualizer
import data_sample_cities as dsc

def union(u, v):
  global roots
  uroot = find_root(u)
  vroot = find_root(v)
  if uroot > vroot:
    uroot,vroot = vroot,uroot
  roots[vroot] = uroot

def find_root(u):
  if u != roots[u]:
    roots[u] = find_root(roots[u]) # 경로압축
  return roots[u]

def main():
  # sorted_edges = sorted(edges, key=lambda e: e[2])
  # print(sorted_edges)
  n_cities = len(cities)

  global roots
  roots = [x for x in range(n_cities)] 
  
  edges.sort(key=lambda e: e[2])
  copy = edges[:]
  vis.sort_edges()

  mst = []
  total_cost = 0

  while len(mst) < n_cities - 1 and copy:
    u,v,w = copy.pop(0)
    if find_root(u) == find_root(v): 
      vis.ignore(u, v, w)
      continue
    c1, c2 = cities[u], cities[v]
    total_cost += w
    mst.append((u, v))
    union(u, v)
    vis.append(u, v, w)
    
    # if (len(mst) == 6): break
  vis.finish()

if __name__ == '__main__':
  vis = Visualizer('MST - Kruskal')
  while True:
    cities, edges = dsc.cities, dsc.edges
    vis.setup(vis.get_main_module())
    main()
    again = vis.end()
    if not again: break
    if vis.restart_lshift:
      dsc.next()
    elif vis.restart_rshift:
      dsc.random()


from vis import PrimVisualizer as Visualizer
import data_sample_cities as dsc

# adjacency matrix - array of array
def build_graph():
  n_cities = len(cities)
  global graph
  graph = [[0 for _ in range(n_cities) ] for _ in range(n_cities)]
  print(graph)

def main():
  n_cities = len(cities)
  build_graph()


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

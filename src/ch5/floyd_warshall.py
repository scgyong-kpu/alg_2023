# Shortest Path - Floyd Warshall
from city import City, five_letter_cities
# from edge import edges
import two_d_visualizer as vis
import random
from math import sqrt

class Floyd:
  def __init__(self):
    self.cities = [
      City("Quiff", 525, 248, 0),
      City("Wrote", 1, 260, 1),
      City("Thong", 190, 385, 2),
      City("Melon", 527, 416, 3),
      City("React", 296, 659, 4),
      City("Rabbi", 6, 758, 5),
      City("Auger", 442, 866, 6),
    ]
    self.n_cities = len(self.cities)
    self.input = {
      0: { 1:662, 2:613, 3:162, },
      1: { 0:272, 2:240, 5:278, },
      2: { 1:174, 0:413, 4:167, },
      3: { 0:172, 2:300, 6:649, },
      4: { 5:219, 6:272, },
      5: { 1:374, 2:311, 4:223, 6:539, },
      6: { 5:436, 4:314, 3:586, },
    }
    self.INF = float('inf')
    self.dgraph = {}
    self.dirs = {}
    for u in range(self.n_cities):
      self.dgraph[u] = {}
      self.dirs[u] = {}
      for v in range(self.n_cities):
        if u in self.input and v in self.input[u]:
          self.dgraph[u][v] = self.input[u][v]
          self.dirs[u][v] = v
        else:
          self.dgraph[u][v] = self.INF
          self.dirs[u][v] = -1
      self.dgraph[u][u] = 0


    # self.gen_graph()

  def gen_graph(self):
    for u, dests in self.input.items():
      c1 = self.cities[u]
      ss = '%d: { ' % (u)
      for v, w in dests.items():
        c2 = self.cities[v]
        d = distance(c1, c2)
        dd = int(d * random.uniform(0.5, 1.5))
        ss += '%d:%3d, ' % (v, dd)
        # print(u,v,w, dd)
      ss += '},'
      print(ss)

  # def dist(self, u, v):
  #   if u in self.dgraph:
  #     dests = self.dgraph[u]
  #     if v in dests:
  #       return dests[v]
  #   return self.INF

  # def set_dist(self, u, v, d):
  #   if not u in self.dgraph: self.dgraph[u] = {}
  #   self.dgraph[u][v] = d

  def start(self):
    N = self.n_cities
    for k in range(N):
      for i in range(N):
        for j in range(N):
          vis.floyd_compare(i, j, k)
          dist = self.dgraph[i][j]
          via = self.dgraph[i][k] + self.dgraph[k][j]
          if via < dist:
            self.dgraph[i][j] = via
            self.dirs[i][j] = k
            vis.floyd_update(i, j, k)


    vis.floyd_update()



def distance(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return sqrt(dx ** 2 + dy ** 2)

floyd = Floyd()

if __name__ == '__main__':
  random.seed('hello')
  vis.init('Shortest Path - Floyd Warshall')
  # vis.speed = 200
  vis.floyd_init(floyd)
  floyd.start()
  vis.end()

from vis import MstTspVisualizer as Visualizer
from random import randint, seed, shuffle
from heapdict import heapdict
import data_sample_cities as dsc

class TspMst:
  def __init__(self, cities, edges):
    self.cities = cities
    self.n_cities = len(cities)
    self.edges = edges

  def main(self):
    self.start_index = randint(0, self.n_cities-1)
    vis.set_start(self.start_index)
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


from vis import VertexCoverVisualizer as Visualizer
import data_sample_cities as dsc


class VertexCover:
  def __init__(self, cities, edges, usingSetCover=True):
    self.cities = cities
    self.edges = edges
    self.usingSetCover = usingSetCover
    self.main = self.setCoverMain if usingSetCover else self.maxMatchMain

  def setCoverMain(self):
    print('Using Set Cover')
    vis.draw()

  def maxMatchMain(self):
    print('Using Maximul Matching')
    vis.draw()

vis = Visualizer('Vertex Cover')
usingSetCover, gen = True, True
while True:
  vc = VertexCover(dsc.cities, dsc.edges, usingSetCover)
  vis.setup(vc)
  vc.main()
  again = vis.end()
  if not again: break
  if vis.restart_lshift:
    dsc.next()
  elif vis.restart_rshift:
    dsc.random()
  else:
    usingSetCover = not usingSetCover

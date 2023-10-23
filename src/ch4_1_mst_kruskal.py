from vis import PlanarVisualizer as Visualizer
import data_sample_cities as dsc

if __name__ == '__main__':
  vis = Visualizer('Cities')
  while True:
    cities, edges = dsc.cities, dsc.edges
    vis.setup(vis.get_main_module())
    vis.draw()
    again = vis.end()
    if not again: break
    dsc.next()


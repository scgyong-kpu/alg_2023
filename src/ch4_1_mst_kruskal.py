from data_city import City, five_letter_cities
# from vis import KruskalVisualizer as Visualizer
from vis import PlanarVisualizer as Visualizer
import random

if __name__ == '__main__':
  vis = Visualizer('Cities')
  beg = 340
  end = 348
  cities = five_letter_cities[beg:end]
  vis.setup(vis.get_main_module())
  vis.draw()
  vis.end()

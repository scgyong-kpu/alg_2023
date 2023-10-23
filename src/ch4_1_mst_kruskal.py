from data_city import City, five_letter_cities
# from vis import KruskalVisualizer as Visualizer
from vis import PlanarVisualizer as Visualizer
import random

if __name__ == '__main__':
  vis = Visualizer('Cities')
  beg = 340
  end = 348
  cities = five_letter_cities[beg:end]
  edges = [
    (0, 1, 668), (0, 2, 312), (0, 4, 128), (1, 2, 652), (1, 3, 1206), 
    (1, 5, 958), (2, 4, 902), (2, 6, 476), (2, 7, 175), (3, 5, 540), 
    (3, 6, 449), (3, 7, 601), (4, 6, 430), (6, 7, 925)
  ]
  vis.setup(vis.get_main_module())
  vis.draw()
  vis.end()

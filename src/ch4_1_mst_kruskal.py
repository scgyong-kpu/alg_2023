from data_city import City, five_letter_cities
# from vis import KruskalVisualizer as Visualizer
from vis import PlanarVisualizer as Visualizer
import random

if __name__ == '__main__':
  vis = Visualizer('Cities')
  beg = 154
  end = 165
  cities = five_letter_cities[beg:end]
  edges = [
    (0, 2, 524), (0, 4, 133), (0, 7, 422), (0, 9, 786), (1, 2, 127), 
    (1, 8, 139), (2, 5, 491), (2, 8, 248), (3, 6, 460), (3, 7, 431), 
    (3, 9, 715), (3, 10, 528), (4, 5, 440), (4, 7, 325), (4, 9, 709), 
    (5, 7, 250), (5, 8, 329), (5, 9, 204), (5, 10, 497), (6, 7, 682), 
    (6, 10, 114), (7, 9, 377), (7, 10, 345), (9, 10, 298)
  ]
  vis.setup(vis.get_main_module())
  vis.draw()
  vis.end()

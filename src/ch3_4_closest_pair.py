from vis import ClosestPairVisualizer as Visualizer
# from vis import Dummy as Visualizer
from data_city import City, five_letter_cities
from random import randint, seed, shuffle
from math import sqrt

def main():
  print(cities)
  # s,e,d = brute_all()
  # s,e,d = devide_and_conquer()
  # print(s,e,d)
  # print(cities[s],cities[e],d)

if __name__ == '__main__':
  seed('Closest')
  vis = Visualizer('Closest Pair')
  while True:
    beg = randint(0, 100)
    end = beg + 2 #randint(beg+10, beg+30)
    cities = five_letter_cities[beg:end]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break


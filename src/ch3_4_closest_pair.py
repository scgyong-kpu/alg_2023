from vis import ClosestPairVisualizer as Visualizer
# from vis import Dummy as Visualizer
from data_city import City, five_letter_cities
from random import randint, seed, shuffle
from math import sqrt

def distance_sq(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return dx ** 2 + dy ** 2

def distance(c1, c2):
  dx, dy = c1.x - c2.x, c1.y - c2.y
  return sqrt(dx ** 2 + dy ** 2)

def brute_force(arr, left, right):
  n_cities = len(cities)
  closest = [-1, -1, float('inf')]
  for i1 in range(left, right+1):
    c1 = cities[i1]
    for i2 in range(i1+1, right+1):
      c2 = cities[i2]
      dist = distance(c1, c2)
      vis.compare(i1,i2,dist)
      if dist < closest[2]:
        closest = [i1, i2, dist]
  return closest

def brute_all():
  n_cities = len(cities)
  vis.push()
  s,e,d = brute_force(cities, 0, n_cities - 1)
  # vis.pop()
  return s,e,d

def main():
  print(cities)
  s,e,d = brute_all()
  # s,e,d = devide_and_conquer()
  # print(s,e,d)
  print(cities[s],cities[e],d)

if __name__ == '__main__':
  seed('Closest')
  vis = Visualizer('Closest Pair')
  while True:
    beg = randint(0, 100)
    end = randint(beg+10, beg+20)
    cities = five_letter_cities[beg:end]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break


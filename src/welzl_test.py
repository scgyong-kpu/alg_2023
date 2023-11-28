from data_city import five_letter_cities, City
from math import sqrt
from heapdict import heapdict
from vis import ClusterVisualizer as Visualizer
from random import seed, randint

def distance_between(i1, i2):
  if i1 >= len(cities) or i2 >= len(cities):
    print(f'{i1=} {i2=} {len(cities)=}')
  c1, c2 = cities[i1], cities[i2]
  return sqrt((c1.x-c2.x)**2+(c1.y-c2.y)**2)

cities = five_letter_cities[:100]
centers = [0]
dists = heapdict()

x1, x2 = (1000, 1010)
y1, y2 = (1000, 1010)

for i in range(len(cities)):
  cities[i].x, cities[i].x = randint(x1, x2), randint(y1, y2)
  x1 -= 10; x2 += 10
  y1 -= 10; y2 += 10

dists[0] = 0,0
vis = Visualizer('Welzl Test')
vis.setup(vis.get_main_module(), True)
for i in range(len(cities)):
  d = distance_between(0, i)
  dists[i] = (-d, 0)

  vis.compare(i, 0, d)

vis.draw()
vis.end()



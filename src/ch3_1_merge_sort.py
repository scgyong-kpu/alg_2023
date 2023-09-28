from vis import MergeSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)
  mid = count // 2
  array[0:mid] = sorted(array[0:mid])
  array[mid:] = sorted(array[mid:])

  vis.push(0, mid-1, count-1)
  print('after :', array)

if __name__ == '__main__':
  seed('Hello')
  vis = Visualizer('Merge Sort')
  while True:
    count = randint(20, 40)
    array = [ randint(1, 99) for _ in range(count) ]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break

    